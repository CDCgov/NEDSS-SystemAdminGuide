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

The NBS Gateway service routes requests between NBS 7 microservices and the legacy NBS 6 application. This page walks you through deploying NBS Gateway using Helm.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy NBS Gateway using Helm

1. Locate the NBS Gateway Helm chart in the [NEDSS-Helm repository][nedss-helm-nbs-gateway-chart].
1. In the `values.yaml`, replace all occurrences of `app.EXAMPLE_DOMAIN` with the URL of your modern app and `app-classic.EXAMPLE_DOMAIN` with the URL of your existing NBS 6 as shown in the [Deploy Traefik ingress controller](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-traefik-ingress-controller).
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nbs-gateway"
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Verify page-builder is disabled:

   ```yaml
   pageBuilder:
     enabled: "false"
   ```

1. Enable OIDC for Keycloak login authentication and set the client secret (see [Enable Keycloak Auth step h](../../deploy-nbs7/keycloak/enable-keycloak-auth.html#enable-keycloak-auth)):

   ```yaml
   Oidc:
     enabled: "true"
     client:
      id: "nbs-modernization"
      secret: "EXAMPLE_OIDC_SECRET"
   ```

1. Install NBS Gateway:

   ```bash
   helm install nbs-gateway -f ./nbs-gateway/values.yaml nbs-gateway
   ```

1. Verify the pod is running before proceeding to the next deployment:

   ```bash
   kubectl get pods
   ```

   If the pod is still creating or in any other non-running state, wait before continuing.

[nedss-helm-nbs-gateway-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/nbs-gateway>
