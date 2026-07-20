---
title: NiFi
layout: page
parent: Deploy NBS 7 microservices
nav_order: 3
redirect_from:
  - /docs/6_microservices_deployment/3_nifi.html
  - /docs/6_microservices_deployment/3_nifi/
  - /docs/3_base_application/nifi.html
  - /docs/3_base_application/nifi/
---

# Deploy NiFi for NBS 7

This page walks through deploying NiFi using the `nifi` Helm chart from the [NEDSS-Helm][nedss-helm-nifi-chart] repository for NBS version {{ site.version_latest }}.

## Prerequisites

This page assumes you've completed [Before you begin](./deploy-nbs7-microservices.html#before-you-begin) for the microservices phase and each microservice deployment page before this one, in order. The page immediately before this one is the [Modernization API](./modernization-api.html) deployment.

Have your database credentials and domain values available. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) if you need help determining any values.

## Deploy NiFi using Helm

Complete the following steps to deploy the ['nifi' Helm chart][nedss-helm-nifi-chart] from the `charts/nifi/` directory of your cloned NEDSS-Helm repository:

> `nifi.EXAMPLE_DOMAIN` only needs to be set if you enable the NiFi ingress. The NiFi ingress is disabled by default due to known security vulnerabilities. If you need access to the NiFi admin UI, use a private domain name.
{: .important }

1. Search `values.yaml` for `EXAMPLE` and fill in the EFS file system ID, JDBC connection string, and NiFi sensitive properties key. The [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) lists the values to use.
1. If you enable the NiFi ingress, replace `nifi.EXAMPLE_DOMAIN` in `values.yaml` with your domain name from the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records), then enable the ingress:

   ```yaml
   ingress:
     enabled: true
   ```

1. Install NiFi:

   ```bash
   helm install "nifi" ./nifi -f ./nifi/values.yaml
   ```

1. Confirm the pod is running before proceeding to the next deployment:

   ```bash
   kubectl get pods
   ```

If the pod is not in a running state, wait and troubleshoot before continuing to [validate Elasticsearch, Modernization API, and NiFi](./validate-es-mapi-nifi.html).

[nedss-helm-nifi-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/nifi>
