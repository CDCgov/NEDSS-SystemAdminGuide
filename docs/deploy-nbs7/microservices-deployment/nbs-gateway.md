---
title: NBS Gateway
layout: page
parent: 4. Deploy NBS 7 microservices
nav_order: 5
redirect_from:
  - /docs/6_microservices_deployment/4_nbs_gateway.html
  - /docs/6_microservices_deployment/4_nbs_gateway/
  - /docs/3_base_application/nbs-gateway.html
  - /docs/3_base_application/nbs-gateway/
---

# Deploy NBS Gateway for NBS 7

This page walks through deploying the NBS Gateway using the `nbs-gateway` Helm chart from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}. Complete [Validate Elasticsearch, Modernization API, and NiFi](./validate-es-mapi-nifi.html) before starting this page. After you finish, proceed to [Data processing](./data-processing.html).

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy NBS Gateway using Helm

Use the ['nbs-gateway' Helm chart][nedss-helm-nbs-gateway-chart] to deploy NBS Gateway into your Kubernetes cluster. NBS Gateway routes requests between NBS 7 microservices and the legacy NBS 6 application. Before you begin, have your domain values and Keycloak client secret available. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) and [Retrieve the nbs-modernization client secret](../full-deploy/kubernetes-setup/deploy-keycloak.html#retrieve-the-nbs-modernization-client-secret) if you need help determining any values.

1. Use Git to clone your own local copy of the public [NEDSS-Helm repository][nedss-helm]. The following steps use the files in `charts/nbs-gateway/` from that repository.
1. In `values.yaml`, replace `app.EXAMPLE_DOMAIN` with the URL of your NBS 7 application and `app-classic.EXAMPLE_DOMAIN` with the URL of your existing NBS 6 application. Use the values from the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records).
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nbs-gateway"
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Verify that Page Builder is disabled:

   ```yaml
   pageBuilder:
     enabled: "false"
   ```

1. Enable OIDC and set the client secret for Keycloak login authentication. See [Retrieve the nbs-modernization client secret](../full-deploy/kubernetes-setup/deploy-keycloak.html#retrieve-the-nbs-modernization-client-secret) for instructions on retrieving the client secret.

   ```yaml
   oidc:
     enabled: "true"
     client:
       id: "nbs-modernization"
       secret: "EXAMPLE_OIDC_SECRET"
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
