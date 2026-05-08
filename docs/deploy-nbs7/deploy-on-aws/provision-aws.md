---
title: Provision the AWS environment
layout: page
parent: Deploy on AWS
nav_order: 2
has_children: true
redirect_from:
   - /docs/3_base_application/1_terraform-deployment.html
   - /docs/3_base_application/1_terraform-deployment/
---

# Provision the AWS cloud environment
{: .no_toc }

This page covers the first deployment phase: provisioning the AWS cloud environment using Terraform. These steps prepare your Amazon Web Services (AWS) infrastructure and validate that the foundational resources are ready for Kubernetes deployment. Complete this section before proceeding to [Initial Kubernetes Deployment](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html).

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

Before you begin, complete the general [Prerequisites](../../deploy-nbs7/prerequisites.html) and the AWS-specific [Prerequisites for deploying on AWS](../../deploy-nbs7/deploy-on-aws/prerequisites.html).
{: .important }

## Prepare deployment files and configuration

Complete these steps to download the infrastructure package and prepare your environment-specific Terraform files.

1. Go to the [NEDSS-Infrastructure {{ site.version_latest_tag }} release page][nedss-infra-release-page]. Under **Assets**, download the `nbs-infrastructure-{{ site.version_latest_tag }}.zip` file.
1. Open a terminal (bash, macOS Terminal, CloudShell, or PowerShell) and unzip the downloaded file.
1. To hold your environment-specific configuration files, create a new directory in `/terraform/aws/`. Give the new directory an easily identifiable name such as `nbs7-mySTLT-config`.
1. Copy `terraform/aws/samples/archive/NBS7_standard` to the new directory and change into the new directory.

   ```bash
   cp -pr terraform/aws/samples/archive/NBS7_standard/* terraform/aws/nbs7-mySTLT-config
   cd terraform/aws/nbs7-mySTLT-config
   ```

   > Before you edit the `terraform.tfvars` and `terraform.tf` files, review the README files for each Terraform module under `terraform/aws/app-infrastructure` in each module's directory. Do not edit files in the individual modules.
   {: .note }

1. Update the `terraform.tfvars` and `terraform.tf` with your environment-specific values.

   If you plan to deploy the Data Compare tool, also add the following variables to your `terraform.tfvars` before running `terraform apply`. If you deployed to a non-default namespace, you should adjust the `datacompare_namespace_and_service` value accordingly.

   ```hcl
   create_datacompare_irsa              = true
   datacompare_s3_bucket_name           = "<your-s3-bucket-name>"
   datacompare_s3_bucket_keyname_prefix = "<your-key-prefix>"
   datacompare_namespace_and_service = ["default:data-compare-api-service", "default:data-compare-processor-service"]
   ```

   This creates the IAM role (`<eks-cluster-name>-datacompare-role`) and S3 access policy required by the Data Compare pods. The role ARN is referenced during [Data Compare deployment](../../deploy-nbs7/real-time-reporting/data-compare-tool.html).

## Validate AWS access and network prerequisites

Before running Terraform, validate database network access and confirm that your AWS authentication is active.

1. Review the inbound rules on the security groups attached to your database instance and ensure that the CIDR you intend to use with your NBS 7 VPC (`modern-cidr`) is allowed to access the database. For example, if the `modern-cidr` is `10.20.0.0/16`, there should be at least one rule in a security group associated with your database that allows MSSQL inbound access from your `modern-cidr` block.
   ![mssql-inbound-from-modern-cidr](../images/myssql-inbound-from-modern-cidr.png)
1. Verify that you are authenticated to AWS. Use the following command to verify access to the intended account. For more information, see the [AWS CLI credential configuration guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

   ```text
   $ aws sts get-caller-identity
   {
       "UserId": "AIDBZMOZ03E7R88J3DBTZ",
       "Account": "123456789012",
       "Arn": "arn:aws:iam::123456789012:user/lincolna"
   }
   ```

## Run Terraform provisioning

Run the Terraform commands in order to initialize state and apply your infrastructure changes. Terraform stores its state in an Amazon S3 bucket. The following commands assume that you are running Terraform authenticated to the same AWS account that contains your existing NBS 6 application. Adjust the commands accordingly if this does not match your setup.

1. Change to the account configuration directory created in [Prepare deployment files and configuration](#prepare-deployment-files-and-configuration) that contains `terraform.tfvars`, and `terraform.tf`. For this example, those files are in the `nbs7-mySTLT-config` directory.

   ```text
   cd terraform/aws/nbs7-mySTLT-config
   ```

1. Initialize Terraform by running:

   ```text
   terraform init
   ```

1. Run `terraform plan` to calculate the set of changes that need to be applied:

   ```text
   terraform plan
   ```

   ![terraform-plan](../images/terraform-plan-latest.png)
1. Review the changes carefully to verify that they match your intention and do not unintentionally affect other configurations that you depend on. Then run `terraform apply`:

   ```text
   terraform apply
   ```

1. If `terraform apply` generates errors, review and resolve the errors, then rerun `terraform apply`.

## Validate provisioned AWS resources

After applying Terraform, verify that the expected AWS infrastructure resources were created correctly.

1. Review the `terraform apply` output in your terminal to verify that the infrastructure was created without errors.
1. In the Amazon VPC console, verify that the newly created VPC and subnets were created as expected. Then review the associated Route Tables to verify that the CIDR blocks you defined are present.
1. In the Amazon EKS console, select the cluster and inspect **Resources > Pods** and **Compute**. Verify that the cluster was created successfully and that at least 30 pods and 3 to 5 compute nodes are present, based on the minimum and maximum node values defined in `terraform/aws/app-infrastructure/eks-nbs/variables.tf`.

## Connect to EKS and validate cluster readiness

Use these steps to connect to the cluster and verify that core Kubernetes resources are available before continuing.

1. While authenticated with AWS, open a terminal or command line. Use the following command to authenticate into the Amazon EKS cluster and the [cluster name that you deployed in the environment](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html).

   ```bash
   aws eks --region us-east-1 update-kubeconfig --name <clustername> # e.g. cdc-nbs-sandbox
   ```

   If the command errors out, verify that:
   - There are no issues with the AWS CLI installation.
   - You have set the correct AWS environment variables.
   - You are using the correct cluster name, as shown in the Amazon EKS console.
1. Run the following command to verify that you can run commands to interact with the Kubernetes objects and the cluster:

   ```bash
   kubectl get pods --namespace=cert-manager
   ```

   This command should return 3 pods. If it does not, refresh your AWS credentials and repeat the verification steps.
1. Verify that worker nodes are registered and ready to run workloads:

   ```bash
   kubectl get nodes
   ```

   Verify that multiple nodes are listed and each node shows a status of `Ready`. If nodes are missing or show `NotReady`, check node group health in Amazon EKS and verify your AWS authentication before continuing.

## Next steps

You have now installed your core infrastructure and Kubernetes cluster. Continue to [Initial Kubernetes Deployment](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html) to configure your cluster.

[nedss-infra-release-page]: <https://github.com/CDCgov/NEDSS-Infrastructure/releases/tag/{{ site.version_latest_tag }}>
