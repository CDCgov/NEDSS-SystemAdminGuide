---
title: Update the Kubernetes control plane
layout: page
parent: Maintain NBS 7
nav_order: 2
redirect_from:
  - /docs/maintain-nbs7/eks-upgrade.html
  - /docs/maintain-nbs7/eks-upgrade/
---

# Update the Amazon EKS control plane

This page describes how to use Terraform to upgrade the Amazon Elastic Kubernetes Service (Amazon EKS) control plane and node groups for your NBS 7 deployment. You should perform a control plane upgrade when Amazon Web Services (AWS) releases a new Kubernetes version or when your current version approaches end-of-support.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Kubernetes version compatibility

While NBS {{ site.version_latest }} was tested against Kubernetes 1.35, later Kubernetes versions are expected to be compatible. To minimize cost, we suggest running the latest version in AWS standard support at the time of your deployment. For current version end dates, see [Understand the Kubernetes version lifecycle on EKS](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html) in the AWS documentation.

Before you begin the upgrade, review the following:

- **Cost impact:** Amazon EKS clusters on extended support versions incur additional cost. For more information, see [Amazon EKS extended support for Kubernetes version pricing](https://aws.amazon.com/blogs/containers/amazon-eks-extended-support-for-kubernetes-versions-pricing) on the AWS blog and the Amazon EKS [pricing page](https://aws.amazon.com/eks/pricing/).
- **Forced upgrades:** When a version exits extended support, [AWS automatically upgrades the control plane to the oldest supported version](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#extended-support-faqs). Automatic upgrades do not account for workload compatibility, add-on versions, or your deployment schedule. To maintain control over your upgrade timing, complete upgrades before the extended support window closes.
- **One minor version at a time:** You must upgrade the control plane one minor version at a time. You cannot skip versions. If you are multiple versions behind, you must repeat this procedure for each version. For more information, see [Update existing cluster to new Kubernetes version](https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html#_step_2_review_upgrade_considerations) in the AWS documentation.
- **Control plane upgrades are irreversible:** You cannot downgrade a cluster to a previous Kubernetes version. If the upgrade causes unexpected issues, your recovery options are limited to debugging the upgraded cluster or restoring the cluster from a backup. Ensure you have a tested backup and a rollback plan for your workloads before you begin.
- **Plan for downtime:** The control plane upgrade does not typically cause service disruption. However, the node group upgrade is likely to cause a disruption, primarily due to the Linkerd/mTLS issue described in [Known issue: Linkerd and mTLS](#known-issue-linkerd-and-mtls). Schedule a maintenance window before you begin.

To receive advance notice of upcoming version deprecations and end-of-support dates, check the **Your account health** page in the [AWS Health Dashboard](https://health.aws.amazon.com/health/home) regularly. You can also subscribe to the [EKS Kubernetes release calendar](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar) to track upcoming release and retirement dates.
{: .note }

## Prerequisites

Before you begin, confirm the following:

### Access and tooling

- You have IAM permissions to modify Amazon EKS clusters and node groups. Required actions include `eks:UpdateClusterVersion`, `eks:UpdateNodegroupVersion`, and `eks:DescribeCluster`. For the full list, see [Amazon EKS identity-based policy examples](https://docs.aws.amazon.com/eks/latest/userguide/security_iam_id-based-policy-examples.html) in the AWS documentation.
- You have installed Terraform and configured it with access to your NBS 7 state backend. The Terraform configuration for this procedure is in the [eks-nbs][nedss-infra-terraform-eks] directory of the NEDSS-Infrastructure repository.
- You have installed the AWS CLI and `kubectl` and authenticated to your cluster.

### Pre-upgrade checks

- You have backed up your Terraform state backend.
- Your cluster is in a healthy state. All nodes are in `Ready` status and no pods are in a failed state.
- You have verified that your target Kubernetes version is compatible with all Amazon EKS managed add-ons currently installed on your cluster. Note that Amazon EKS automatically installs self-managed add-ons such as the Amazon VPC CNI plugin, kube-proxy, and CoreDNS. For more information, see [Amazon EKS add-ons](https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html) and [Update an Amazon EKS add-on](https://docs.aws.amazon.com/eks/latest/userguide/updating-an-add-on.html) in the AWS documentation.

You must upgrade one minor version at a time. You cannot skip versions. If you are multiple versions behind your target, plan to run this procedure once for each version.
{: .important }

## Steps to complete

To minimize risk and ensure a clean state at each version, this procedure uses targeted Terraform **applies**.

### Step 1: Identify target resources in Terraform state

Before you run any targeted **applies**, identify the Amazon EKS resource addresses in your Terraform state.

Bash:

```bash
terraform state list | grep -E "aws_eks_cluster|aws_eks_node_group"
```

PowerShell:

```powershell
terraform state list | Select-String "aws_eks_cluster|aws_eks_node_group"
```

For a standard NBS 7 deployment using the NEDSS-Infrastructure Terraform repository, the output should include (see [main.tf][nedss-infra-terraform-eks-main]):

```text
module.eks_nbs.module.eks.aws_eks_cluster.this[0]
module.eks_nbs.module.eks.module.eks_managed_node_group["main"].aws_eks_node_group.this[0]
```

These are the target addresses to use in Steps 2 and 3. If your deployment uses a customized module structure and returns different addresses, substitute those addresses in the `-target` flags in Steps 2 and 3.

### Step 2: Upgrade the control plane

The AWS CLI and Terraform commands in Steps 2–6 work in both Bash and PowerShell. Repeat these steps for each minor version between your current version and your target version. Do not proceed to the next version until the cluster reaches `ACTIVE` status at the current version.

1. In [variables.tf][nedss-infra-terraform-eks-variables], update the `cluster_version` default value to the next minor version:

   ```terraform
   variable "cluster_version" {
     description = "Version of the AWS EKS cluster to provision"
     default     = "<next_version>"
   }
   ```

1. Run a targeted apply against the cluster resource:

   ```bash
   terraform apply -target="module.eks_nbs.module.eks.aws_eks_cluster.this[0]"
   ```

1. Confirm the cluster has reached `ACTIVE` status at the new version before you continue:

   ```bash
   aws eks describe-cluster --name <cluster_name> \
      --query "cluster.{Version:version,Status:status}"
   ```

   The output should show the new version and `ACTIVE` status. Do not proceed until you have confirmed both values.

1. Repeat steps 1–3 in this section for each remaining minor version until the cluster reaches the target version.

### Step 3: Upgrade node groups

After the control plane reaches the target version, upgrade your node groups.

1. Run a targeted apply against the node group resource:

   ```bash
   terraform apply -target="module.eks_nbs.module.eks.module.eks_managed_node_group[\"main\"].aws_eks_node_group.this[0]"
   ```

1. Confirm new nodes have joined the cluster and reached `Ready` status:

   ```bash
   kubectl get nodes
   ```

All nodes should show `Ready` in the `STATUS` column.

### Step 4: Upgrade Amazon EKS managed add-ons

> If your deployment uses NBS 7.12 or later, managed add-ons (CoreDNS, kube-proxy, Amazon VPC CNI) are included in the `eks_nbs` module and are updated when Step 2 runs. In that case, you can skip this step.
{: .note }

If you are running a version earlier than NBS 7.12, complete this step to upgrade your managed add-ons to versions compatible with the new Kubernetes version. Skipping this step on an older version risks leaving add-ons running on incompatible versions, which might cause networking or DNS failures.

1. List the add-ons installed on your cluster and their current versions:

   ```bash
   aws eks list-addons --cluster-name <cluster_name>
   ```

1. For each add-on, check which versions are compatible with your target Kubernetes version:

   ```bash
   aws eks describe-addon-versions \
      --addon-name <addon_name> \
      --kubernetes-version <target_version> \
      --query "addons[].addonVersions[].addonVersion"
   ```

1. Update each add-on to the latest compatible version:

   ```bash
   aws eks update-addon \
      --cluster-name <cluster_name> \
      --addon-name <addon_name> \
      --addon-version <target_addon_version> \
      --resolve-conflicts OVERWRITE
   ```

   The `--resolve-conflicts OVERWRITE` flag allows the update to proceed even if you have customized your add-on configuration from the AWS default. If your deployment includes custom add-on configurations you need to preserve, use `--resolve-conflicts PRESERVE` instead. With `PRESERVE`, the update fails rather than overwrite local changes, and you must resolve conflicts manually. If you are unsure which flag to use, check with your infrastructure team.
   {: .important }

1. Repeat the previous step for each add-on in your cluster.

1. Confirm each add-on reaches `ACTIVE` status before you move on:

   ```bash
   aws eks describe-addon \
      --cluster-name <cluster_name> \
      --addon-name <addon_name> \
      --query "addon.{Version:addonVersion,Status:status}"
   ```

### Step 5: Reconcile configuration

After all targeted **applies** are complete, run a full **plan** and **apply** to resolve any remaining configuration drift. Targeted **applies** do not update all dependent resources. This step ensures your infrastructure state is fully reconciled.

```bash
terraform plan
terraform apply
```

Review the plan output before applying. Confirm that no unexpected changes are included.

If Linkerd unexpectedly stops during the upgrade, see [Known issue: Linkerd and mTLS](#known-issue-linkerd-and-mtls) for troubleshooting guidance.
{: .note }

### Step 6: Verify the upgrade

After completing steps 1–5, confirm the upgrade was successful.

1. Verify the control plane version:

   ```bash
   aws eks describe-cluster --name <cluster_name> \
      --query "cluster.version"
   ```

1. Verify all nodes are running the target version and are in `Ready` status:

   ```bash
   kubectl get nodes -o wide
   ```

1. Verify all pods are running:

   ```bash
   kubectl get pods --all-namespaces
   ```

   No pods should be in `Error`, `CrashLoopBackOff`, or `Pending` status.

1. Verify NBS is functioning correctly by logging into the system and confirming that advanced search works.

## Known issue: Linkerd and mTLS {#known-issue-linkerd-and-mtls}

During node group upgrades, Linkerd might unexpectedly stop. When this occurs, mTLS connections between NBS services are interrupted.

**Required action:** After the node upgrade completes, restart all NBS services to reset mTLS state and restore full connectivity.

1. Confirm the deployments in the `default` namespace before restarting:

   ```bash
   kubectl get deployments -n default
   ```

1. Restart all deployments in the namespace:

   ```bash
   kubectl rollout restart deployment -n default
   ```

[nedss-infra-terraform-eks]: <https://github.com/CDCgov/NEDSS-Infrastructure/tree/{{ site.version_latest_tag }}/terraform/aws/app-infrastructure/eks-nbs>
[nedss-infra-terraform-eks-main]: <https://github.com/CDCgov/NEDSS-Infrastructure/blob/{{ site.version_latest_tag }}/terraform/aws/app-infrastructure/eks-nbs/main.tf>
[nedss-infra-terraform-eks-variables]: <https://github.com/CDCgov/NEDSS-Infrastructure/blob/{{ site.version_latest_tag }}/terraform/aws/app-infrastructure/eks-nbs/variables.tf>
