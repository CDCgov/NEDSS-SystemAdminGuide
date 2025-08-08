---
title: NBS Gateway
layout: page
parent: Microservices Deployment
nav_order: 4
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy nbs-gateway via helm chart

1. The helm chart for nbs-gateway should be available under charts/nbs-gateway.
2. In the values.yaml, replace all occurrences of app.EXAMPLE_DOMAIN with the URL of your modern app and app-classic.EXAMPLE_DOMAIN with the URL of your existing NBS 6 as shown in the [Table](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/2_nginx_ingress_deployment.html#deploy-nginx-ingress-controller-on-the-kubernetes-cluster). 
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
5. Make sure OIDC is enabled for keycloak login authentication and update the client secret (need the value from keycloak - refer [Enable Keycloak Auth step h](/NEDSS-SystemAdminGuide/docs/5_keycloak/2_enable_keycloak_auth.html#enable-keycloak-auth))
   ```yaml
   Oidc:
     enabled: "true"
     client:
      id: "nbs-modernization"
      secret:"EXAMPLE_OIDC_SECRET"
   ```
6. After updating the values file, Run the following command from the charts directory to install nbs-gateway.
   ```bash
   helm install nbs-gateway -f ./nbs-gateway/values.yaml nbs-gateway
   ```
7. IMPORTANT: Check to see if the pod is running before proceeding with the next deployment using the below command. If the pod is still creating (or in any other state other than running), wait and/or troubleshoot.
   ```bash
   kubectl get pods
   ```
