---
title: NBS Gateway
layout: page
parent: Deploy NBS 7 microservices
nav_order: 5
redirect_from:
  - /docs/6_microservices_deployment/4_nbs_gateway.html
  - /docs/6_microservices_deployment/4_nbs_gateway/
  - /docs/3_base_application/nbs-gateway.html
  - /docs/3_base_application/nbs-gateway/
---

# Deploy NBS Gateway for NBS 7

This page walks through deploying the NBS Gateway using the `nbs-gateway` Helm chart from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}. NBS Gateway routes requests between NBS 7 microservices and the legacy NBS 6 application. After you finish this page, proceed to [Data processing](./data-processing.html).

## Prerequisites

This page assumes you've completed [Before you begin](./deploy-nbs7-microservices.html#before-you-begin) for the microservices phase and each microservice deployment page before this one, in order. The page immediately before this one is [Validate Elasticsearch, Modernization API, and NiFi](./validate-es-mapi-nifi.html).

Have your domain values and Keycloak client secret available. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) and [Import service clients and retrieve secrets](../full-deploy/kubernetes-setup/deploy-keycloak.html#import-service-clients-and-retrieve-secrets) if you need help determining any values.

## Deploy NBS Gateway using Helm

Complete the following steps to deploy the ['nbs-gateway' Helm chart][nedss-helm-nbs-gateway-chart] from the `charts/nbs-gateway/` directory of your cloned NEDSS-Helm repository:

1. Search `values.yaml` for `EXAMPLE` and fill in your environment-specific values:
   - For the NBS 7 and NBS 6 application domain values, use the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records).
   - For the OIDC client secret used for Keycloak login authentication, see [Import service clients and retrieve secrets](../full-deploy/kubernetes-setup/deploy-keycloak.html#import-service-clients-and-retrieve-secrets).
1. Confirm the following feature flags in `values.yaml`:
   - Page Builder is disabled:

     ```yaml
     pageBuilder:
       enabled: "false"
     ```

   - OIDC is enabled:

     ```yaml
     oidc:
       enabled: "true"
       client:
         id: "nbs-modernization"
     ```

1. Install NBS Gateway:

   ```bash
   helm install "nbs-gateway" ./nbs-gateway -f ./nbs-gateway/values.yaml
   ```

1. Confirm the pod is running before proceeding to the next deployment:

   ```bash
   kubectl get pods
   ```

If the pod is not in a running state, wait and troubleshoot before continuing to deploy [Data processing](./data-processing.html).

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-nbs-gateway-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/nbs-gateway>
