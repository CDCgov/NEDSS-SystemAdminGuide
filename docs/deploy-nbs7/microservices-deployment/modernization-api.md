---
title: Modernization API
layout: page
parent: 4. Deploy NBS 7 microservices
nav_order: 2
redirect_from:
  - /docs/6_microservices_deployment/2_modernization_api.html
  - /docs/6_microservices_deployment/2_modernization_api/
  - /docs/3_base_application/modernization-api.html
  - /docs/3_base_application/modernization-api/
---

# Deploy the Modernization API for NBS 7

This page walks through deploying the Modernization API using the `modernization-api` Helm chart from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}. Complete [Elasticsearch](./elasticsearch.html) before starting this page. After you finish, proceed to [NiFi](./nifi.html) deployment.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy Modernization API using Helm

Use the ['modernization-api' Helm chart][nedss-helm-modernization-api-chart] to deploy the Modernization API into your Kubernetes cluster. Before you begin, have your database credentials and domain values available. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) if you need help determining any values.

1. Use Git to clone your own local copy of the public [NEDSS-Helm repository][nedss-helm]. The following steps use the files in `charts/modernization-api/` from that repository.
1. In `values.yaml`, replace `app.EXAMPLE_DOMAIN` with the URL of your NBS 7 application and `app-classic.EXAMPLE_DOMAIN` with the URL of your existing NBS 6 application. Use the values from the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records).
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/modernization-api"
     tag: <release-version-tag> # for example, v1.4.0
   ```

1. Set the JDBC connection string using the database endpoint and credentials from the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices):

   ```yaml
   jdbc:
     connectionString: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=EXAMPLE_DB_NAME;user=EXAMPLE_ODSE_DB_USER;password=EXAMPLE_ODSE_DB_USER_PASSWORD;encrypt=true;trustServerCertificate=true;"
     user: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
   ```

1. Verify that Page Builder is disabled:

   ```yaml
   pageBuilder:
     enabled: "false"
   ```

1. Set the token secret and parameter secret. For values and instructions, see the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices):

   ```yaml
   security:
     tokenSecret: "EXAMPLE_TOKEN_SECRET"
     parameterSecret: "EXAMPLE_PARAMETER_SECRET"
   ```

1. Enable OIDC and set the client secret for Keycloak login authentication. See [Retrieve the nbs-modernization client secret](../full-deploy/kubernetes-setup/deploy-keycloak.html#retrieve-the-nbs-modernization-client-secret) for instructions on retrieving the client secret.

   ```yaml
   oidc:
     enabled: "true"
     client:
       id: "nbs-modernization"
       secret: "EXAMPLE_OIDC_SECRET"
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
