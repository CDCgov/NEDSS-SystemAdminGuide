---
title: Update EKS control plane
layout: page
parent: Maintain NBS 7
nav_order: 3
---

# Update the EKS control plane
{: .no_toc }

You can use Terraform to upgrade the Amazon Elastic Kubernetes Service (EKS) control plane and node groups for your NBS 7 deployment. Perform a control plane upgrade when AWS releases a new Kubernetes version or when your current version approaches end-of-support.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Considerations

AWS retires Kubernetes versions on a scheduled basis. Clusters that run end-of-support versions do not receive security patches or technical support, so plan your upgrades before your current version reaches end-of-support.

You must perform EKS control plane upgrades **one minor version at a time**. You cannot skip minor versions. To minimize risk and ensure a clean state at each version hop, this procedure uses targeted Terraform ***applies***.

## Prerequisites

Before you begin, confirm the following:

* You have IAM permissions to modify Amazon EKS clusters and node groups.
* You have installed Terraform and configured it with access to your NBS 7 state backend.
* You have backed up your Terraform state backend.
* You have installed the AWS CLI and `kubectl` and authenticated to your cluster.
* Your cluster is in a healthy state. All nodes are in `Ready` status and no pods are in a failed state.

You must perform upgrades one minor version at a time. You cannot skip versions.
{: .important }

## Steps to complete

### Step 1: Identify target resources in Terraform state

Before you run any targeted **applies**, identify the EKS resource addresses in your Terraform state.

**Bash:**

   ```bash
   terraform state list | grep -E "aws_eks_cluster|aws_eks_node_group"
   ```

**PowerShell:**

   ```text
   terraform state list | Select-String "aws_eks_cluster|aws_eks_node_group"
   ```

Take note of the full resource addresses that are returned. You will use these as targets in Steps 2 and 3\.

### Step 2: Upgrade the control plane

Repeat the following steps for each minor version between your current version and your target version. Do not proceed to the next version until the cluster reaches `ACTIVE` status at the current version.

1. In your Terraform configuration, update the `cluster_version` variable to the next minor version:

   ```text
   cluster_version = "<next_version>"
   ```

2. Run a targeted apply against the cluster resource:

   ```bash
   terraform apply -target="module.eks.aws_eks_cluster.this"
   ```

3. Confirm the cluster has reached `ACTIVE` status at the new version before you continue:

   ```bash
   aws eks describe-cluster --name <cluster_name> \
      --query "cluster.{Version:version,Status:status}"
   ```

   The output should show the new version and `ACTIVE` status. Do not proceed until you have confirmed both values.

4. Repeat steps 1–3 for each remaining minor version until the cluster reaches the target version.

### Step 3: Upgrade node groups

After the control plane reaches the target version, upgrade your node groups.

1. Run a targeted apply against the node group resource:

   ```bash
   terraform apply -target="module.eks.aws_eks_node_group.workers"
   ```

1. Confirm new nodes have joined the cluster and reached `Ready` status:

   ```bash
   kubectl get nodes
   ```

All nodes should show `Ready` in the `STATUS` column.

### Step 4: Reconcile configuration

After all targeted applies are complete, run a full **plan** and **apply** to resolve any remaining configuration drift. Targeted applies do not update all dependent resources. This step ensures your infrastructure state is fully reconciled.

   ```bash
   terraform plan
   terraform apply
   ```

Review the plan output before applying. Confirm that no unexpected changes are included.

If Linkerd unexpectedly stops during the upgrade, see [Known issue: Linkerd and mTLS](#known-issue-linkerd-and-mtls) for troubleshooting guidance.
{: .note }

### Step 5: Verify the upgrade

After completing steps 1 - 4, confirm the upgrade was successful.

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

## Known issue: Linkerd and mTLS {#known-issue-linkerd-and-mtls}

During node group upgrades, Linkerd might unexpectedly stop. When this occurs, mTLS connections between NBS services are interrupted.

**Required action:** After the node upgrade completes, restart all NBS services to reset mTLS state and restore full connectivity.

```bash
kubectl rollout restart deployment -n <namespace>
```

Confirm the correct namespace for the rollout restart command.
