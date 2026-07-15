---
title: Modernization API
layout: page
parent: Deploy NBS 7 microservices
nav_order: 2
redirect_from:
  - /docs/6_microservices_deployment/2_modernization_api.html
  - /docs/6_microservices_deployment/2_modernization_api/
  - /docs/3_base_application/modernization-api.html
  - /docs/3_base_application/modernization-api/
---

# Deploy the Modernization API for NBS 7

This page walks through deploying the Modernization API using the `modernization-api` Helm chart from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}. After you finish this page, proceed to [NiFi](./nifi.html) deployment.

## Prerequisites

Complete the following before you begin this page:

- If you haven't already, complete [Before you begin](./deploy-nbs7-microservices.html#before-you-begin) for the microservices phase.
- Complete [Elasticsearch](./elasticsearch.html) deployment.
- Have your database credentials and domain values available. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) if you need help determining any values.

## Deploy Modernization API using Helm

Complete the following steps to deploy the ['modernization-api' Helm chart][nedss-helm-modernization-api-chart] from the `charts/modernization-api/` directory of your cloned NEDSS-Helm repository:

1. Search `values.yaml` for `EXAMPLE` and fill in your environment-specific values:
   - For the NBS 7 and NBS 6 application domain values, use the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records).
   - For the database connection, token secret, and parameter secret values, see the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices).
   - For the OIDC client secret used for Keycloak login authentication, see [Retrieve the nbs-modernization client secret](../full-deploy/kubernetes-setup/deploy-keycloak.html#retrieve-the-nbs-modernization-client-secret).
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

1. Install the Modernization API:

   ```bash
   helm install "modernization-api" ./modernization-api -f ./modernization-api/values.yaml
   ```

1. Confirm the pod is running before proceeding to the next deployment:

   ```bash
   kubectl get pods
   ```

If the pod is not in a running state, wait and troubleshoot before continuing to deploy the [NiFi](./nifi.html) microservice.

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-modernization-api-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/modernization-api>
