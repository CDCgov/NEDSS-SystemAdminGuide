---
title: Configure Linkerd and Cluster Autoscaler
layout: page
parent: Initial Kubernetes Deployment
nav_order: 4
nav_enabled: true
---

# Configure Linkerd and Cluster Autoscaler
{: .no_toc }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Annotate the default namespace for Linkerd

Linkerd must be installed as part of the Terraform infrastructure deployment before completing these steps. Annotating the default namespace enables Linkerd mTLS on all microservices deployed in the following steps.

1. Annotate the default namespace:

   ```bash
   kubectl annotate namespace default "linkerd.io/inject=enabled"
   ```

   ![linkerd](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/images/3_linkerd.png)

1. Verify the annotation is in place:

   ```bash
   kubectl get namespace default -o=jsonpath='{.metadata.annotations}'
   ```

   The output should include `{"linkerd.io/inject":"enabled"}`.

1. If this is an update rather than a new install, restart the application pods in the default namespace so that Linkerd sidecars are injected. Restarted pods should show `2/2` in the ready column.

## Install the Cluster Autoscaler

The Cluster Autoscaler is a Helm chart that horizontally scales cluster nodes as needed. Update the following values in `charts/cluster-autoscaler/values.yaml` with values from the AWS console:

```yaml
clusterName: <EXAMPLE_EKS_CLUSTER_NAME>
autoscalingGroups:
  - name: <EXAMPLE_AWS_AUTOSCALING_GROUP_NAME>
    maxSize: 5
    minSize: 3
awsRegion: us-east-1
```

Install the chart:

```bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler
helm upgrade --install cluster-autoscaler autoscaler/cluster-autoscaler \
  -f ./cluster-autoscaler/values.yaml \
  --namespace kube-system
```

Verify the pod is running:

```bash
kubectl --namespace=kube-system get pods \
  -l "app.kubernetes.io/name=aws-cluster-autoscaler,app.kubernetes.io/instance=cluster-autoscaler"
```
