---
title: Provision cloud environment
layout: page
parent: Provision cloud infrastructure
nav_order: 2
description: Use Terraform to provision the network, Kubernetes cluster, and supporting services for NBS 7 in AWS or Azure.
redirect_from:
  - /docs/3_base_application/1_terraform-deployment.html
  - /docs/3_base_application/1_terraform-deployment/
  - /docs/deploy-nbs7/deploy-on-aws/provision-aws.html
  - /docs/deploy-nbs7/deploy-on-aws/provision-aws/
---

# Provision the cloud environment with Terraform

This page covers how to use Terraform to provision the NBS 7 cloud environment in AWS or Azure. The Terraform code creates the network, the Kubernetes cluster, and the supporting services that the rest of this guide builds on. When you complete the steps on this page, substitute `<cloud-provider>` with `aws` or `azure`. The person who provisions this infrastructure should have operational knowledge of [Terraform](https://developer.hashicorp.com/terraform/docs).

> Before you begin, complete the general [Prerequisites](../prerequisites.html) and the [Cloud prerequisites](cloud-prerequisites.html).
{: .important }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Validate database access

Your NBS 7 environment requires access to your NBS 6 SQL Server database. Confirm this access before you run Terraform provisioning.

### AWS

If your database is in Amazon RDS, review the inbound rules on the security groups attached to your database instance. Confirm that the Classless Inter-Domain Routing (CIDR) block you intend to use for your NBS 7 VPC (`modern-cidr`) is allowed to access the database. For example, if the `modern-cidr` is `10.20.0.0/16`, at least one rule in a security group associated with your database must allow MSSQL inbound access from that block:

![AWS security group inbound rules table with a rule of type MSSQL that allows TCP port 1433 access from the modern-cidr source block 10.20.0.0/16](images/myssql-inbound-from-modern-cidr.png)

### Azure

If your database is in Azure, in the same VNet as your NBS 7 environment, Azure allows all internal traffic within a VNet by default. To confirm, in the Azure Portal, go to the network security group attached to your database and confirm that the default inbound rules are present:

![Azure Portal inbound security rules for a network security group, showing the default rules AllowVnetInBound and AllowAzureLoadBalancerInBound with the Allow action and DenyAllInBound with the Deny action, listed with their priorities, ports, protocols, sources, and destinations](images/azure-nsg-default-inbound-rules.png)

Alternatively, an inbound security rule on that network security group is sufficient if it allows port 1433, with the destination set to the VNet of your database and the source set to the IP addresses of your AKS cluster.

<!-- [SME REVIEW] Josh comment 30 open question: add guidance for databases that are not in Amazon RDS and not in Azure (for example, self-managed SQL Server on EC2 or on premises). Confirm the validation path with Josh or Mike Ward. -->

## Authenticate to your cloud provider

Terraform, kubectl, and Helm commands require an authenticated session with your cloud provider. This section requires the tools from [Management workstation setup](cloud-prerequisites.html#management-workstation-setup).

### AWS

1. Run the [`aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) command to authenticate to your AWS account.
1. Confirm that you are authenticated by running the following command and verifying that it prints your account details. For more information, see the [AWS CLI credential configuration guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

   ```text
   $ aws sts get-caller-identity
   {
       "UserId": "AIDBZMOZ03E7R88J3DBTZ",
       "Account": "123456789012",
       "Arn": "arn:aws:iam::123456789012:user/lincolna"
   }
   ```

### Azure

1. Run the [`az login`](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli) command to authenticate to your Azure subscription.
1. Confirm that you are authenticated by running the following command and verifying that it prints details of your subscription:

   ```text
   az account show
   ```

## Prepare Terraform files and configuration

Complete these steps to download the infrastructure code and prepare your environment-specific Terraform files:

1. Go to the [NEDSS-Infrastructure {{ site.version_latest_tag }} release page][nedss-infra-release-page]. Under **Assets**, download the `nbs-infrastructure-{{ site.version_latest_tag }}.zip` file.
1. Unzip the downloaded file.
1. Open a terminal and change into the top-level directory from the unzipped file:

   ```bash
   cd nbs-infrastructure-{{ site.version_latest_tag }}
   ```

1. To hold your environment-specific configuration files, create a new directory in `terraform/<cloud-provider>/`. Give the directory an easily identifiable name in the format `nbs7-<STLT>-<environment>`:

   ```bash
   cd terraform/<cloud-provider>
   mkdir nbs7-mySTLT-test
   ```

1. Copy the sample code from `terraform/<cloud-provider>/samples/` into your new environment directory, and change into that directory:

   ```bash
   cp -pr samples/* ./nbs7-mySTLT-test
   cd nbs7-mySTLT-test
   ```

   The samples contain a directory for each NBS 7 Terraform layer. Each directory name starts with a number that sets the order in which you apply the layers:

   ```text
   $ ls -F | sort
   0-landing-zone/
   1-nbs6/
   2-nbs7/
   3-applications/
   ```

   The [README in the NEDSS-Infrastructure repository][nedss-infra-readme] explains the layered Terraform design.

   > Skip the `1-nbs6` layer. The [Cloud prerequisites](cloud-prerequisites.html) require an existing NBS 6 instance, so you do not provision one here.
   {: .note }

1. In each Terraform layer directory, update the `terraform.tfvars` and `terraform.tf` files with your environment-specific values. The commentary in those files provides detailed instructions. Do not edit files in the individual Terraform modules.

   If you plan to deploy the Data Compare tool on AWS, also add the following variables to your `terraform.tfvars` before you apply. If you deploy to a non-default namespace, adjust the `datacompare_namespace_and_service` value accordingly. <!-- [SME REVIEW] Confirm which Terraform layer's tfvars file receives the Data Compare variables in the layered structure (2-nbs7 or 3-applications). This block predates the layered design. -->

   ```hcl
   create_datacompare_irsa              = true
   datacompare_s3_bucket_name           = "<your-s3-bucket-name>"
   datacompare_s3_bucket_keyname_prefix = "<your-key-prefix>"
   datacompare_namespace_and_service = ["default:data-compare-api-service", "default:data-compare-processor-service"]
   ```

   This creates the AWS Identity and Access Management (IAM) role (`<eks-cluster-name>-datacompare-role`) and S3 access policy that the Data Compare pods require. The role ARN is referenced during [Data Compare deployment](../../real-time-reporting/data-compare-tool.html).

## Run Terraform provisioning

For each Terraform layer directory, this section initializes the directory, generates an execution plan, and applies the changes. Repeat the following steps for each layer in your environment directory, in the numeric order of the directory names.

> The following commands assume that you run Terraform authenticated to the same AWS account or Azure subscription that contains your existing NBS 6 application.
{: .note }

1. In a terminal, change to the Terraform layer directory that contains the `terraform.tfvars` and `terraform.tf` files you updated in [Prepare Terraform files and configuration](#prepare-terraform-files-and-configuration):

   ```bash
   cd nbs-infrastructure-{{ site.version_latest_tag }}/terraform/<cloud-provider>/nbs7-<STLT>-<environment>/<number>-<layer-description>
   ```

1. Initialize Terraform:

   ```text
   terraform init
   ```

1. Generate an execution plan. The plan shows the changes that a corresponding `terraform apply` command would make to the resources in your cloud provider:

   ```text
   terraform plan -out=tfplan
   ```

   The command prints a summary line such as the following:

   ```text
   Plan: 142 to add, 0 to change, 0 to destroy.
   ```

   > Carefully review the full plan output and verify that the changes exactly match your intention before you continue. If you change your Terraform code, if resources in your account or subscription change by other means, or if significant time passes during your review, rerun `terraform plan -out=tfplan` and review it again. Never run `terraform apply -auto-approve`, because it applies changes without review and can be highly destructive.
   {: .important }

1. Apply the changes from the plan:

   ```text
   terraform apply tfplan
   ```

   The command prints a summary line, and its numbers should match the numbers from the plan summary:

   ```text
   Apply complete! Resources: 142 added, 0 changed, 0 destroyed.
   ```

1. If the apply command prints errors, review and resolve the errors, then rerun the plan and apply steps.

## Connect to Kubernetes cluster

> This section requires an authenticated session from [Authenticate to your cloud provider](#authenticate-to-your-cloud-provider).
{: .note }

Run the command for your cloud provider to configure `kubectl` to connect to the Kubernetes cluster that Terraform provisioned:

- **AWS:**

  ```bash
  aws --region <REGION> eks update-kubeconfig --name <MANAGED_CLUSTER_NAME>
  ```

- **Azure:**

  ```bash
  az aks get-credentials --resource-group <RESOURCE_GROUP_NAME> --name <MANAGED_CLUSTER_NAME>
  ```

If the command returns an error, verify that:

- Your cloud provider CLI installation works.
- Your authenticated session is still active.
- You used the correct cluster name, as shown in the Amazon EKS console or the Azure Portal.

## Validate Kubernetes cluster readiness

1. **Confirm core pods are running:** Print the Kubernetes core infrastructure pods and verify that each pod has a `STATUS` of `Running`:

   ```bash
   kubectl get pods --namespace=kube-system
   ```

1. **Confirm nodes are ready:** Verify that the Kubernetes worker nodes are registered and ready to run workloads. Each node should have a `STATUS` of `Ready`:

   ```bash
   kubectl get nodes
   ```

Both commands must work as expected before you continue. [Amazon EKS][eks-troubleshooting] and [AKS][aks-troubleshooting] provide troubleshooting guidance.

## Save your Terraform code

Your `nbs7-<STLT>-<environment>` directory contains the `terraform.tfvars` and `terraform.tf` files that define your environment. You need this directory again for any future maintenance of the infrastructure you provisioned with Terraform. Save the directory somewhere you can retrieve it later.

## Next steps

Continue to [Set up Kubernetes](../kubernetes-setup.html) to deploy the core services and Keycloak.

[nedss-infra-release-page]: <https://github.com/CDCgov/NEDSS-Infrastructure/releases/tag/{{ site.version_latest_tag }}>
[nedss-infra-readme]: <https://github.com/CDCgov/NEDSS-Infrastructure/blob/{{ site.version_latest_tag }}/README.md>
[eks-troubleshooting]: <https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html>
[aks-troubleshooting]: <https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/welcome-azure-kubernetes>
