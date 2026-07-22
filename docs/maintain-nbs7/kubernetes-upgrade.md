---
title: Update the Kubernetes control plane
layout: page
parent: Maintain NBS 7
nav_order: 2
redirect_from:
  - /docs/maintain-nbs7/eks-upgrade.html
  - /docs/maintain-nbs7/eks-upgrade/
description: Use Terraform to upgrade the Kubernetes version for the control plane and nodes of your NBS 7 cluster.
---

# Update the Kubernetes version for your NBS 7 cluster

This page describes how to use Terraform to upgrade the Kubernetes version of your NBS 7 cluster.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Overview

This page applies to Amazon Elastic Kubernetes Service (Amazon EKS) on Amazon Web Services (AWS). It also applies to Azure Kubernetes Service (AKS) on Microsoft Azure (Azure).

> NBS added support for Azure deployments in NBS 7.13.
{: .important }

- The [Provision the cloud environment with Terraform](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html) page describes the NBS 7 Terraform layers. The Kubernetes cluster is part of layer 2, the `1-nbs7` folder.
- Amazon EKS groups worker nodes into {% include term-tooltip.html key="managed-node-group" term="**managed node groups**" id="k8s-upgrade-node-group" %}. AKS groups them into {% include term-tooltip.html key="node-pool" term="**node pools**" id="k8s-upgrade-node-pool" %}. This page uses the respective term for each cloud.

## Kubernetes version compatibility

Perform a Kubernetes version upgrade whenever Amazon EKS or AKS begins supporting a new Kubernetes version. At minimum, upgrade before your current Kubernetes version reaches end of support.

The Kubernetes community releases a new minor version roughly every four months. It typically stops providing Common Vulnerabilities and Exposures (CVE) patches for a version about a year after release. Staying current keeps your NBS 7 environment secure.

**NBS {{ site.version_latest }} was tested against Kubernetes version {{ site.version_k8s }}**, but later Kubernetes versions are expected to be compatible. To minimize cost, run the latest version available in **EKS Standard Support** or **AKS Standard Tier** at the time of your upgrade.

Test a Kubernetes version upgrade in a non-production environment first. Jurisdictions that do this tend to catch compatibility issues before they affect a production NBS 7 deployment. A successful non-production upgrade also increases confidence that the same steps will succeed in production.

For more information on version compatibility, see [Understand the Kubernetes version lifecycle on Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html). For AKS, see [Supported Kubernetes versions in Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions).

## Considerations before upgrading

Review the following before you begin the upgrade:

- **One minor version at a time:** Upgrade the control plane and nodes one minor version at a time, for example from 1.35 to 1.36. You cannot skip versions. If you are multiple versions behind, repeat [Step 2: Upgrade the control plane](#step-2-upgrade-the-control-plane) once for each intervening version.
- **Plan for downtime:** The control plane upgrade does not typically cause service disruption, but the node upgrade might. This is due to a known Linkerd and mutual TLS (mTLS) issue described in [Validate Linkerd and mTLS](#validate-linkerd-and-mtls). Schedule a maintenance window before you begin.
- **Cost impact:** Running certain cluster configurations increases cost on either cloud.
  - **AWS:** Amazon EKS clusters on Extended Support versions incur additional cost. For more information, see [Amazon EKS pricing](https://aws.amazon.com/eks/pricing/).
  - **Azure:** AKS Premium Tier clusters incur additional cost. For more information, see [AKS pricing](https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/).
- **Forced upgrades:** Automatic upgrades performed by either cloud provider do not check whether your workload is compatible with the target Kubernetes version. To keep control over timing, complete your own upgrade before the support window for your current version closes.
  - **AWS:** Once the Kubernetes version of a cluster reaches the end of Standard Support, Amazon EKS automatically enrolls the cluster in Extended Support. The control plane is auto-upgraded once Extended Support for that version ends. For current support windows, see [Understand the Kubernetes version lifecycle on Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html).
  - **Azure:** Once the Kubernetes version of a cluster is no longer supported, AKS reserves the right to automatically upgrade the cluster. For more information, see the [AKS version FAQs: Can you stay on a Kubernetes version forever?](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions?tabs=azure-cli#can-you-stay-on-a-kubernetes-version-forever)
- **Downgrading the control plane version:** Rollback support after an upgrade differs by cloud.
  - **AWS:** You can revert an Amazon EKS control plane to the previous minor version within seven days of an in-place upgrade. See [Rollback cluster to previous Kubernetes version](https://docs.aws.amazon.com/eks/latest/userguide/rollback-cluster.html).
  - **Azure:** You cannot revert an AKS control plane to the previous version. See [AKS upgrade FAQs](https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-faq#is-rollback-supported-if-the-aks-upgrade-fails-or-causes-issues-).
- **Backing up your cluster (optional):** On either cloud, you can debug issues on the upgraded cluster directly. You can also back up your cluster before the upgrade to create a restore point.
  - **AWS:** See [Back up your EKS Clusters with AWS Backup](https://docs.aws.amazon.com/eks/latest/userguide/integration-backup.html).
  - **Azure:** See [Back up Azure Kubernetes Service by using Azure Backup](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-cluster-backup).

> Each cloud provider offers ways to receive advance notice of upcoming Kubernetes version deprecations and end-of-support dates.
>
> - **AWS:** Check the **Your account health** page in the [AWS Health Dashboard](https://health.aws.amazon.com/health/home) regularly. You can also subscribe to the [Amazon EKS Kubernetes release calendar](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar).
> - **Azure:** See the [AKS release tracker](https://learn.microsoft.com/en-us/azure/aks/release-tracker). You can also [subscribe to AKS events](https://learn.microsoft.com/en-us/azure/aks/quickstart-event-grid) such as `NewKubernetesVersionAvailable`.
{: .note }

## Prerequisites

This page provides guidance specific to NBS 7. AWS and Azure change their own upgrade mechanics independently of this guide, so this page assumes familiarity with the following:

- **AWS:** [Update existing cluster to new Kubernetes version](https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html#_step_2_review_upgrade_considerations) in the Amazon EKS User Guide.
- **Azure:** [Upgrade the Azure Kubernetes Service (AKS) cluster control plane](https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-control-plane) in the AKS documentation. Also review the other pages within the **Perform upgrades and rollbacks** section.

### Access and tooling prerequisites

Confirm you have completed the following prerequisites. You can find more information on these items in the [Provision the cloud environment with Terraform](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html) section of the deployment guide.

- You have completed [Authenticate to your cloud provider](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html#authenticate-to-your-cloud-provider) for the NBS 7 environment you are upgrading.
- You have completed [Connect to Kubernetes cluster](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html#connect-to-kubernetes-cluster) for that environment.
- You have retrieved your `nbs7-<your_STLT_name>-<your_environment_name>` folder and confirmed it contains a `1-nbs7` folder with a `terraform.tfvars` file and the rest of the layer 1 `.tf` files. You likely saved this file as part of the deployment process in the [Save your Terraform code](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html#save-your-terraform-code) step. For more information on finding and configuring the original folder, see  [Prepare Terraform files and configuration](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html#prepare-terraform-files-and-configuration).

### Pre-upgrade checks

Perform the following checks before you begin the update.

- **Verify that your cluster is in a healthy state.** All nodes are in `Ready` status and all pods are in `Running` status. Running `kubectl get pods --all-namespaces` shows the same left and right number in the `READY` column for every pod. This is expected, since each NBS 7 microservice runs in the `default` namespace with a `linkerd-proxy` sidecar container.
- **Determine your order of operations.** You might need to complete [Step 3](#step-3-upgrade-nodes) and [Step 4](#step-4-upgrade-amazon-eks-managed-add-ons) after each control plane upgrade in [Step 2](#step-2-upgrade-the-control-plane), instead of waiting until all control planes are upgraded. This applies when either of the following is true:
  1. There are more than two versions between your current version and your target version. Both Amazon EKS and AKS allow nodes to run up to three minor versions behind the control plane, so waiting introduces the risk of exceeding that limit mid-upgrade.
  1. Any Amazon EKS cluster add-on currently installed is a version that is not compatible with your target Kubernetes version. This check does not apply to AKS.
     - **AWS:** Check compatibility by running `aws eks list-addons --cluster-name <CLUSTER_NAME>`. Then, for each add-on returned, run `aws eks describe-addon-versions --kubernetes-version <TARGET_VERSION> --addon-name <ADDON_NAME> --query 'addons[].addonVersions[].addonVersion'`. For more information, see [Amazon EKS add-ons](https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html) and [Update an Amazon EKS add-on](https://docs.aws.amazon.com/eks/latest/userguide/updating-an-add-on.html).

## Step 1: Identify target resources in Terraform state

Run all Terraform commands on this page from your `1-nbs7` folder, inside your `nbs7-<your_STLT_name>-<your_environment_name>` folder. You might need to run `terraform init` in that folder first. If any command does not complete successfully, resolve the issue before you continue.

Open a terminal in your `1-nbs7` folder and run the following command to list the relevant resources in your Terraform state:

```bash
terraform state list | grep -E "aws_eks_cluster|aws_eks_node_group|azurerm_kubernetes_cluster"
```

If you are using PowerShell, use `Select-String` instead:

```powershell
terraform state list | Select-String "aws_eks_cluster|aws_eks_node_group|azurerm_kubernetes_cluster"
```

For a standard NBS 7 environment using the [NEDSS-Infrastructure](https://github.com/CDCgov/NEDSS-Infrastructure) repository, the output includes the target resources as shown in the following examples:

- **AWS:**

   ```text
   module.eks_nbs.module.eks.aws_eks_cluster.this[0]
   module.eks_nbs.module.eks.module.eks_managed_node_group["main"].aws_eks_node_group.this[0]
   ```

   Use the `aws_eks_cluster` address as the target for [Step 2](#step-2-upgrade-the-control-plane) and the `aws_eks_node_group` address as the target for [Step 3](#step-3-upgrade-nodes).

- **Azure:**

   ```text
   module.aks_nbs7.module.aks.azurerm_kubernetes_cluster.main
   ```

   Use the `azurerm_kubernetes_cluster` address as the target for both [Step 2](#step-2-upgrade-the-control-plane) and [Step 3](#step-3-upgrade-nodes).

> If your environment uses a customized module structure, this command might return different addresses. In that case, substitute those addresses in the `-target` flags in Steps 2 and 3.
{: .important }

## Step 2: Upgrade the control plane

To minimize risk, this procedure uses targeted Terraform **applies**, which limit each `terraform apply` to a specific resource and its dependencies without changing other resources. Each `terraform apply` on this page runs a plan first and shows you the output. It then prompts you to type `yes` before applying the plan. Review each plan carefully before you confirm. For more on why this matters, see [Run Terraform provisioning](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html#run-terraform-provisioning).

Repeat this step for each minor version between your current version and your target version, until the cluster reaches the target version.

1. In the `terraform.tfvars` file in your `1-nbs7` folder, set `kubernetes_version_control_plane` to the next version.

   ```hcl
   kubernetes_version_control_plane = "<next_version>"
   ```

1. Run a targeted apply against the cluster resource:

   ```bash
   terraform apply -target='<TARGET_ADDRESS_FOR_STEP_2>'
   ```

1. Confirm the control plane reached the new version and the cluster is up:

   - **AWS:**

     ```bash
     aws eks describe-cluster --name <CLUSTER_NAME> --query "cluster.[version, status]"
     ```

     The output should show your new version and `ACTIVE` status.

   - **Azure:**

     ```bash
     az aks show --resource-group <RESOURCE_GROUP_NAME> --name <CLUSTER_NAME> --query "[kubernetesVersion, powerState.code]" -o tsv
     ```

     The output should show your new version and `Running` status.

1. Repeat this step for each remaining minor version until the cluster reaches your target version.

## Step 3: Upgrade nodes

After the control plane reaches your target version, upgrade the {% include term-tooltip.html key="managed-node-group" term="node group" id="k8s-upgrade-step3-node-group" %} or {% include term-tooltip.html key="node-pool" term="node pool" id="k8s-upgrade-step3-node-pool" %}:

1. Update `terraform.tfvars` in your `1-nbs7` folder:

   - **AWS:** Set `kubernetes_version_node_group` to your target Kubernetes version, and set `kubernetes_ami_release_version` to the latest recommended Amazon Machine Image (AMI) release for that version.
   - **Azure:** Set `kubernetes_default_node_pool_orchestrator_version` to your target Kubernetes version.

1. Run a targeted apply against the node resource:

   ```bash
   terraform apply -target='<TARGET_ADDRESS_FOR_STEP_3>'
   ```

1. Confirm new nodes joined the cluster, are on the expected version, and reached `Ready` status:

   ```bash
   kubectl get nodes -o wide
   ```

1. Confirm all pods are in `Running` status, with the same left and right number in the `READY` column for each pod:

   ```bash
   kubectl get pods --all-namespaces
   ```

### Validate Linkerd and mTLS

After a node version upgrade, Linkerd might stop working if mTLS connections between NBS 7 microservices are interrupted. There is no reliable way to tell in advance whether this has happened. Complete the following steps after every node upgrade, regardless of whether you observe a problem:

1. Review the deployments and pods in the `default` namespace:

   ```bash
   kubectl get deployments -n default
   kubectl get pods -n default
   ```

1. Restart all deployments in that namespace:

   ```bash
   kubectl rollout restart deployment -n default
   ```

1. For one of the restarted deployments, confirm the rollout completed:

   ```bash
   kubectl rollout status deployment/<deployment-name> -n default
   ```

   The command should report that the deployment was successfully rolled out. Repeat this check for the other deployments.

1. Confirm all pods are in `Running` status, with the same left and right number in the `READY` column. Pods in the `default` namespace should specifically show `2/2`:

   ```bash
   kubectl get pods --all-namespaces
   ```

## Step 4: Upgrade Amazon EKS managed add-ons

> This step does not apply to AKS. Add-ons and cluster extensions in AKS are pinned to specific versions that align with each Kubernetes minor version. Azure upgrades them automatically when the control plane upgrades.
{: .note }

1. List the Amazon EKS add-ons installed on your cluster and their current versions:

   ```bash
   aws eks list-addons --cluster-name <CLUSTER_NAME>
   ```

1. For each add-on the previous command returns, check which versions are compatible with your target Kubernetes version:

   ```bash
   aws eks describe-addon-versions \
      --kubernetes-version <TARGET_VERSION> \
      --addon-name <ADDON_NAME> \
      --query "addons[].addonVersions[].addonVersion"
   ```

1. For each add-on, update it to the latest compatible version returned by the previous command:

   ```bash
   aws eks update-addon \
      --cluster-name <CLUSTER_NAME> \
      --addon-name <ADDON_NAME> \
      --addon-version <TARGET_ADDON_VERSION> \
      --resolve-conflicts OVERWRITE
   ```

   The `--resolve-conflicts OVERWRITE` flag allows the update to proceed even if you customized the add-on configuration away from the AWS default. If your environment includes custom add-on configuration that you need to preserve, use `--resolve-conflicts PRESERVE` instead. With `PRESERVE`, the update fails rather than overwrite your changes, and you resolve conflicts manually. Check with your infrastructure team if you are not sure which flag applies to your environment.
   {: .important }

   <!-- SME REVIEW: confirm whether the kubernetes_addons variable from PR #319 changes how add-on versions are managed on apply, and whether the terraform.tfvars update in the next bullet is still the correct way to prevent Terraform drift after this manual update. -->

   In the `kubernetes_addons` variable in `terraform.tfvars` in your `1-nbs7` folder, update `addon_version` for this add-on to the version you just applied. This keeps the add-on version you just set from being reverted by [Step 5](#step-5-address-remaining-terraform-changes).

1. Repeat the previous three items for each add-on in your cluster.

1. Confirm each add-on reached `ACTIVE` status on the target version:

   ```bash
   aws eks describe-addon \
      --cluster-name <CLUSTER_NAME> \
      --addon-name <ADDON_NAME> \
      --query "addon.[addonVersion,status]"
   ```

## Step 5: Address remaining Terraform changes

Targeted applies do not update every dependent resource, so run a full plan and apply to resolve any remaining configuration drift:

```bash
terraform plan
terraform apply
```

Review the plan output before you confirm. Apply only if the changes it lists are ones you intend to make.

## Step 6: Further verification

After completing Steps 1 through 5, confirm the upgrade succeeded:

1. Confirm all pods are still in `Running` status, with the same left and right number in the `READY` column:

   ```bash
   kubectl get pods --all-namespaces
   ```

1. To verify that NBS is functioning correctly, log in to the system and confirm that Advanced Patient Search works.

## Step 7: Save your tfvars changes

To save the changes you made to `1-nbs7/terraform.tfvars` during this procedure, complete the steps in [Save your Terraform code](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html#save-your-terraform-code).
