---
title: Modernization API
layout: page
parent: Microservices Deployment
nav_order: 2
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy Modernization API via helm chart

1. The helm chart for modernization should be available under charts/modernization-api.
2. In the values.yaml file, replace all occurrences of app.EXAMPLE_DOMAIN with the URL of your modern app and app-classic.EXAMPLE_DOMAIN with the URL of your existing NBS 6 as shown in the Table-3.
3. Ensure the image repository and tags are populated with the following:
   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/modernization-api"
     tag: <release-version-tag> e.g v1.0.1
   ```
4. Populate the jdbc section (refer Table - 5) in the values file in the following format
   ```yaml
   jdbc:
     connectionString: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=NBS_ODSE;user=DBUsername;password=DBPassword;encrypt=true;trustServerCertificate=true;"
     user: "EXAMPLE_DB_USER"
     password: "EXAMPLE_DB_USER_PASSWORD"
   ```
5. Verify page-builder is disabled
   ```yaml
   pageBuilder:
     enabled: "false"
   ```
6. Update token secret and parameter secret to encrypt JWT (use token secret generated for pagebuilder-api above, generate parameter secret with openssl rand -base64 32 | cut -c1-32 )
   ```yaml
   security:
     tokenSecret: "EXAMPLE_TOKEN_SECRET"
     parameterSecret: "EXAMPLE_PARAMETER_SECRET"
   ```
7. Verify OIDC is enabled for keycloak login authentication
   ```yaml
   Oidc:
     enabled: "true"
   ```
8. Verify search view and table view are enabled
   ```yaml
   search:
    view:
      enabled: true
      table:
        enabled: true
   ```
9. Verify extended patient data is enabled
   ```yaml
   patient:
    add:
      extended:
        enabled: true
   ```
10. After updating the values file, run the following command to install modernization API.
   ```bash
   helm install modernization-api -f ./modernization-api/values.yaml modernization-api
   ```
11. To check ingress for RTR services
   ```bash
   kubectl describe ingress main-ingress-resource
   ```
12. IMPORTANT: Confirm the pod is running before proceeding with the next deployment using the below command. If the pod is still creating (or in any other state other than running), wait and/or troubleshoot.
   ```bash
   kubectl get pods
   ```
