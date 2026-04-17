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

This page walks through deploying NiFi using the `nifi-efs` Helm chart.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy NiFi using Helm

> The NiFi ingress is disabled by default. To access the NiFi admin UI, set `ingress.enabled: true` in `values.yaml` before running the install command. Use a private domain name rather than a public one — NiFi has known security vulnerabilities.
{: .important }

1. Locate the Helm chart at `charts/nifi-efs`.
1. In `values.yaml`, replace all occurrences of `nifi.EXAMPLE_DOMAIN` with your domain name. See the [ingress controller domain table](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-nginx-ingress-controller-on-your-cluster) for reference.
1. Set the image repository and tag:

   ```yaml
   image:
     repository: quay.io/us-cdcgov/cdc-nbs-modernization/nifi
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Set `efsFileSystemId` to your [EFS file system ID](https://us-east-1.console.aws.amazon.com/efs/home?region=us-east-1#/file-systems).
1. Set the JDBC connection string using the same database endpoint and credentials from [Deploy NBS 7 microservices](../../deploy-nbs7/deploy-nbs7-microservices.html):

   ```yaml
   jdbcConnectionString: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=EXAMPLE_DB_NAME;user=EXAMPLE_ODSE_DB_USER;password=EXAMPLE_ODSE_DB_USER_PASSWORD;encrypt=true;trustServerCertificate=true;"
   ```

1. Set `singleUserCredentialsUsername` to replace the default `admin` username.
1. Set `singleUserCredentialsPassword` to your chosen password for the NiFi admin UI.
1. Install NiFi:

   ```bash
   helm install nifi -f ./nifi-efs/values.yaml nifi-efs
   ```

1. Confirm the pod is running before proceeding to the next deployment:

   ```bash
   kubectl get pods
   ```

   If the pod is still creating or in any other state, wait and troubleshoot before continuing.
