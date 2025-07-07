---
title: Linkerd and Cluster Autoscaler
layout: page
parent: Initial Kubernetes Deployment
nav_order: 3
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Linkerd - Annotate default namespace
- a. Verify that linkerd is installed as part of the terraform infrastructure deployment by checking the pods status under the “linkderd” namespace. This will enable linkerd/MTLS on all the microservices installed in the follow steps
  ```bash
  kubectl annotate namespace default "linkerd.io/inject=enabled"
  ```
  ![linkerd](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/images/3_linkerd.png)
- b. Verify annotation is in place:
  ```bash
  kubectl get namespace default -o=jsonpath='{.metadata.annotations}'
  ```
  Should show “{"linkerd.io/inject":"enabled"}”
- c. If this is an update of the environment rather than a new install, restart the application pods in the default namespace for the linkerd sidecars to be injected into each pods. Should show 2/2 on the restarted pod.

## Cluster Autoscaler Installation
Cluster Autoscaler is a helm chart deployment that horizontally autoscales cluster nodes when deployed on the cluster. The following parameter values need to be modified on the values.yaml file. These values should be fetched from the AWS console.
```bash
clusterName: <EKS_CLUSTER_NAME>
autoscalingGroups:
  - name: <AUTOSCALING_GROUP_NAME>
    maxSize: 5
    minSize: 3
awsRegion: us-east-1

helm repo add autoscaler https://kubernetes.github.io/autoscaler
helm upgrade --install cluster-autoscaler autoscaler/cluster-autoscaler -f ./cluster-autoscaler/values.yaml --namespace kube-system
```
