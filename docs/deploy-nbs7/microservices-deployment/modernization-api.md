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

This page walks through deploying the Modernization API using the `modernization-api` Helm chart.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> This page applies to NBS {{ site.version_latest }}. Helm chart links are pinned to `{{ site.version_latest_tag }}`.
{: .note }

## Deploy Modernization API using Helm

1. Locate the Modernization API Helm chart in the [NEDSS-Helm repository][nedss-helm-modernization-api-chart].
1. In `values.yaml`, replace all occurrences of `app.EXAMPLE_DOMAIN` with the URL of your modern app and `app-classic.EXAMPLE_DOMAIN` with the URL of your existing NBS 6. See the [DNS records table](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#create-dns-records) for reference.
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/modernization-api"
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Set the JDBC connection string using the same database endpoint and credentials from [Deploy NBS 7 microservices](../../deploy-nbs7/deploy-nbs7-microservices.html):

   ```yaml
   jdbc:
     connectionString: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=EXAMPLE_DB_NAME;user=EXAMPLE_ODSE_DB_USER;password=EXAMPLE_ODSE_DB_USER_PASSWORD;encrypt=true;trustServerCertificate=true;"
     user: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
   ```

1. Verify that page-builder is disabled:

   ```yaml
   pageBuilder:
     enabled: "false"
   ```

1. Set the token secret and parameter secret to encrypt JWT tokens. Use the token secret generated for `pagebuilder-api`, and generate the parameter secret with `openssl rand -base64 32 | cut -c1-32`:

   ```yaml
   security:
     tokenSecret: "EXAMPLE_TOKEN_SECRET"
     parameterSecret: "EXAMPLE_PARAMETER_SECRET"
   ```

1. Verify that OIDC is enabled for Keycloak login authentication:

   ```yaml
   Oidc:
     enabled: "true"
   ```

1. Install the Modernization API:

   ```bash
   helm install modernization-api -f ./modernization-api/values.yaml modernization-api
   ```

1. Check the ingress for RTR services:

   ```bash
   kubectl describe ingress main-ingress-resource
   ```

1. Confirm the pod is running before proceeding to the next deployment:

   ```bash
   kubectl get pods
   ```

   If the pod is still creating or in any other state, wait and troubleshoot before continuing.

[nedss-helm-modernization-api-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/modernization-api>
