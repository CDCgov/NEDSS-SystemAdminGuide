---
title: NBS Gateway
layout: page
parent: Deploy NBS 7 microservices
nav_order: 5
nav_enabled: true
redirect_from:
  - /docs/6_microservices_deployment/4_nbs_gateway.html
  - /docs/6_microservices_deployment/4_nbs_gateway/
  - /docs/3_base_application/nbs-gateway.html
  - /docs/3_base_application/nbs-gateway/
---

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy nbs-gateway via helm chart

1. The helm chart for nbs-gateway should be available under `charts/nbs-gateway`.
2. In the `values.yaml`, replace all occurrences of `app.EXAMPLE_DOMAIN` with the URL of your modern app and `app-classic.EXAMPLE_DOMAIN` with the URL of your existing NBS 6 as shown in the [Table](../../../docs/deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-nginx-ingress-controller-on-your-cluster).
3. Ensure the image repository and tags are populated with the following:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nbs-gateway"
     tag: <release-version-tag> e.g v1.0.1
   ```

4. Verify page-builder is disabled

   ```yaml
   pageBuilder:
     enabled: "false"
   ```

5. Make sure OIDC is enabled for keycloak login authentication and update the client secret (need the value from keycloak - refer [Enable Keycloak Auth step h](../../../docs/deploy-nbs7/keycloak/enable-keycloak-auth.html#enable-keycloak-auth))

   ```yaml
   Oidc:
     enabled: "true"
     client:
      id: "nbs-modernization"
      secret: "EXAMPLE_OIDC_SECRET"
   ```

6. After updating the values file, Run the following command from the charts directory to install nbs-gateway.

   ```bash
   helm install nbs-gateway -f ./nbs-gateway/values.yaml nbs-gateway
   ```

7. IMPORTANT: Check to see if the pod is running before proceeding with the next deployment using the below command. If the pod is still creating (or in any other state other than running), wait and/or troubleshoot.

   ```bash
   kubectl get pods
   ```
