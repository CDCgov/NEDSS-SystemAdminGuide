---
title: Elasticsearch
layout: page
parent: 4. Deploy NBS 7 microservices
nav_order: 1
redirect_from:
  - /docs/6_microservices_deployment/1_elasticsearch.html
  - /docs/6_microservices_deployment/1_elasticsearch/
  - /docs/3_base_application/elasticsearch.html
  - /docs/3_base_application/elasticsearch/
---

# Deploy Elasticsearch for NBS 7

This page walks through deploying Elasticsearch using the `elasticsearch` Helm chart from the [NEDSS-Helm][nedss-helm-elasticsearch-chart] repository for NBS version {{ site.version_latest }}. This is the first microservice to deploy. After you finish, proceed to [Modernization API](./modernization-api.html) deployment.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy Elasticsearch using Helm

Use the ['elasticsearch' Helm chart][nedss-helm-elasticsearch-chart] to deploy Elasticsearch into your Kubernetes cluster. Before you begin, have your persistent storage configuration values available. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) if you need help determining any values.

1. Use Git to clone your own local copy of the public [NEDSS-Helm repository][nedss-helm-elasticsearch-chart]. The following steps use the files in `charts/elasticsearch/` from that repository.
1. Set `efsFileSystemId` in `values.yaml` to the file system ID for your environment. In AWS deployments, this is the Amazon EFS file system ID from the AWS console. In Azure deployments, Azure Files requires different configuration. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) for details.
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/elasticsearch"
     tag: <release-version-tag> # for example, v1.0.2
   ```

1. Install Elasticsearch:

   ```bash
   helm install elasticsearch -f ./elasticsearch/values.yaml elasticsearch
   ```

1. Confirm pod status is running:

   ```bash
   kubectl get pods
   ```

If the pod is not in a running state, wait and troubleshoot before continuing to deploy the [Modernization API](./modernization-api.html) microservice.

[nedss-helm-elasticsearch-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/elasticsearch>
