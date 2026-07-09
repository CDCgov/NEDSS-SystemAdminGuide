---
title: 4. Deploy NBS 7 microservices
layout: page
parent: NBS 7 full deployment
nav_order: 4
has_children: true
redirect_from:
  - /docs/6_microservices_deployment/0_microservices_deployment.html
  - /docs/6_microservices_deployment/0_microservices_deployment/
  - /docs/deploy-nbs7/deploy-nbs7-microservices.html
  - /docs/deploy-nbs7/deploy-nbs7-microservices/
description: Install and configure NBS 7 application services using Helm, including Elasticsearch, NiFi, and the Modernization API.
---

# Deploy NBS 7 microservices

This phase deploys the NBS 7 application services into your Kubernetes cluster using Helm. Deploy services in the order listed. Each service has dependencies on the ones before it.

> The pages in this section apply to NBS {{ site.version_latest }}. GitHub links for the [NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm) repo are pinned to `{{ site.version_latest_tag }}`.
{: .note }

## Overview

Use the Helm CLI to deploy NBS 7 microservices into your Kubernetes cluster. Verify that each microservice starts successfully before you move to the next service.

## Before you begin

Complete the following steps before you deploy the first microservice:

1. Verify that you are authenticated to your cloud provider and that your session targets the account for your NBS environment.
   - **AWS:** Run `aws sts get-caller-identity` and confirm the output shows your NBS account ID.
   - **Azure:** Run `az account show` and confirm the output shows your NBS subscription.
1. Navigate to the `charts` directory of your cloned NEDSS-Helm repository. Run all Helm install commands from this directory.

## Helm values reference for NBS 7 microservices

The following table lists common Helm values used across NBS 7 microservices. Have these values available before you begin deployment.

<!-- markdownlint-disable MD055 MD056 -->

| Name of value | Placeholder in values.yaml | Description |
|---|---|---|
| `efsFileSystemId` | `EXAMPLE_EFS_ID` | **For AWS deployments only:** The Amazon EFS file system ID for the shared network file system used by Elasticsearch and NiFi for persistent storage. Find this in the AWS EFS console under **File systems**, or in the Terraform outputs from infrastructure provisioning.|
| `nbsExternalName` | `app-classic.EXAMPLE_DOMAIN` <!-- [SME REVIEW] The DNS records table has no classic-app entry; confirm where app-classic DNS setup is documented. --> | The domain name for your existing NBS 6 application. Use the value that you configured for the classic app in the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records). |
| `ingress*` | `app.EXAMPLE_DOMAIN` or `nifi.EXAMPLE_DOMAIN` | The domain name for your NBS 7 application or NiFi admin UI. Use the value that you configured in the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records). |
| Varies by chart, for example: `ingressHost` | `data.EXAMPLE_DOMAIN` | The domain name for the data ingestion endpoint. Use the value that you configured in the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records). |
| Varies by chart, for example: `jdbc*` | `EXAMPLE_DB_ENDPOINT` | The hostname or endpoint of your NBS database server. Find this in the console for your database hosting service or in the Terraform outputs from infrastructure provisioning. |
| Varies by chart | `EXAMPLE_DB_NAME` | The name of the NBS ODSE database on your database server. The default is `NBS_ODSE`. |
| Varies by chart | `EXAMPLE_ODSE_DB_USER` / `EXAMPLE_DB_USER` | The database login used by NBS microservices. The default is `nbs_ods`. |
| Varies by chart | `EXAMPLE_ODSE_DB_USER_PASSWORD` / `EXAMPLE_DB_USER_PASSWORD` | The password for the database user. Retrieve this from your secrets manager or your infrastructure team. |
| `security.tokenSecret` | `EXAMPLE_TOKEN_SECRET` | The secret that the Modernization API uses to encrypt authentication tokens. Generate a random value with: `openssl rand -base64 64 \| tr -d '\n'` |
| `security.parameterSecret` | `EXAMPLE_PARAMETER_SECRET` | The secret that the Modernization API uses to encrypt search parameters. Generate a random value with: `openssl rand -base64 32 \| cut -c1-32` |
| `singleUserCredentialsUsername` | `EXAMPLE_NIFI_ADMIN_USER` | The username for the NiFi admin UI. Choose any username except `admin`. |
| `singleUserCredentialsPassword` | `EXAMPLE_NIFI_ADMIN_USER_PASSWORD` | The password for the NiFi admin UI account. |
| `nifiSensitivePropsKey` | `EXAMPLE_NIFI_SENSITIVE_PROPS` | The password that NiFi uses to derive an encryption key for sensitive values that it stores internally. Generate a random value of at least 12 characters with: `openssl rand -base64 32 \| cut -c1-32` |
| `oidc.client.secret` | `EXAMPLE_OIDC_SECRET` | The client secret for Keycloak login authentication. Retrieve this from the Keycloak admin UI: select the **NBS** realm, go to **Clients**, select the relevant client, and copy the value from the **Credentials** tab. See [Retrieve the nbs-modernization client secret](../full-deploy/kubernetes-setup/deploy-keycloak.html#retrieve-the-nbs-modernization-client-secret). |
| Varies by chart, for example: `kafka.cluster` | `EXAMPLE_KAFKA_ENDPOINT(S)` / `EXAMPLE_KAFKA_MULTI_CLUSTER_ENDPOINTS` | A comma-separated list of the private plaintext endpoints for your Kafka brokers. In AWS deployments, find these in the Amazon MSK console under your cluster > **View client information** > **Bootstrap servers (plaintext)**. |
| `sftp.*` | `EXAMPLE_SFTP_HOST` `EXAMPLE_SFTP_USER` `EXAMPLE_SFTP_PASS` `EXAMPLE_SFTP_FILE_EXTNS` `EXAMPLE_SFTP_FILE_PATHS` | Connection details for the external SFTP server used by the data ingestion service, including host, username, password, file extensions, and file paths. The SFTP server is managed by your jurisdiction and is not provisioned as part of NBS infrastructure. These values are required only if you configure SFTP polling for manual ELR file drop-off. |
| `nbs.authuser` | `EXAMPLE_NBS_AUTHUSER` | The username of the NBS account that the data processing service uses to import and export data. Use a service account, typically the `ELRImporter` type user that your jurisdiction already has set up. |
| `keycloak.srte.clientId` | `EXAMPLE_SRTE_CLIENT_ID` | The Keycloak client ID for SRTE data access. The default is `srte-data-keycloak-client`. This client is not included in the initial **NBS** realm import and requires a separate import step. See [Import additional service clients](../full-deploy/kubernetes-setup/deploy-keycloak.html#import-additional-service-clients). |
| `keycloak.srte.clientSecret` | `EXAMPLE_SRTE_CLIENT_SECRET` | The client secret for SRTE data access. After you import the client, retrieve the secret from the **Credentials** tab. See [Retrieve a client secret](../full-deploy/kubernetes-setup/deploy-keycloak.html#retrieve-a-client-secret). |
{: .three-column-values-table }

After you gather these values, continue to the deployment pages. The table of contents on this page lists the deployment pages in order, starting with the first service to deploy. Complete each page in sequence.
