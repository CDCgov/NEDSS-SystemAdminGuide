---
title: Elasticsearch
layout: page
parent: Deploy NBS 7 microservices
nav_order: 1
redirect_from:
  - /docs/6_microservices_deployment/1_elasticsearch.html
  - /docs/6_microservices_deployment/1_elasticsearch/
  - /docs/3_base_application/elasticsearch.html
  - /docs/3_base_application/elasticsearch/
---

# Deploy Elasticsearch for NBS 7

This page walks through deploying Elasticsearch using the `elasticsearch` Helm chart from the [NEDSS-Helm][nedss-helm-elasticsearch-chart] repository for NBS version {{ site.version_latest }}. This is the first microservice to deploy. After you finish, proceed to [Modernization API](./modernization-api.html) deployment.

## Prerequisites

Complete the following before you begin this page:

- Complete the steps in [Before you begin](./deploy-nbs7-microservices.html#before-you-begin) for the microservices phase.
- Have your persistent storage configuration values available. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) if you need help determining any values.

## Deploy Elasticsearch using Helm

Complete the following steps to deploy the ['elasticsearch' Helm chart][nedss-helm-elasticsearch-chart] from the `charts/elasticsearch/` directory of your cloned NEDSS-Helm repository:

1. <!-- [SME REVIEW] The Azure azure.files.storageAccountName and azure.files.resourceGroupName values aren't in the Helm values reference table yet. We need to add them there. -->
   In the `elasticsearch/values.yaml` file, search for `EXAMPLE` and fill in your environment-specific values for AWS or Azure as appropriate. The [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) lists the values to use.
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
