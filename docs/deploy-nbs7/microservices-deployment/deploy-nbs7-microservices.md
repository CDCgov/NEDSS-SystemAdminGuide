---
title: Deploy NBS 7 microservices
layout: page
parent: Deploy NBS 7
nav_order: 6
has_children: true
redirect_from:
  - /docs/6_microservices_deployment/0_microservices_deployment.html
  - /docs/6_microservices_deployment/0_microservices_deployment/
  - /docs/deploy-nbs7/deploy-nbs7-microservices.html
  - /docs/deploy-nbs7/deploy-nbs7-microservices/
description: Install and configure NBS 7 application services using Helm, including Elasticsearch, NiFi, and the Modernization API.
---

# Deploy NBS 7 microservices
{: .no_toc }

This phase deploys the NBS 7 application services into your Kubernetes cluster using Helm. Deploy services in the order listed. Each service has dependencies on the ones before it.

> The pages in this section apply to NBS {{ site.version_latest }}. Github links for the [NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm) repo are pinned to `{{ site.version_latest_tag }}`.
{: .note }

## Overview

Use the Helm CLI to deploy NBS 7 microservices into your Kubernetes cluster. Deploy the Helm charts in order. Verify that each microservice starts successfully before moving to the next service.

## Helm values reference for NBS 7 microservices

The following table lists common Helm values used across NBS 7 microservices. Have these values available before you begin deployment.

| Name of value | Placeholder in values.yaml | Description |
|---|---|---|
| `efsFileSystemId` | `EXAMPLE_EFS_ID` | **In AWS deployments:** The Amazon EFS file system ID for the shared network file system used by Elasticsearch and NiFi for persistent storage. Find this in the AWS EFS console under **File systems**, or in the Terraform outputs from infrastructure provisioning. **In Azure deployments:** Azure Files requires different values.yaml configuration. See [Deploy on Azure](../deploy-on-azure.html) for Azure file storage configuration. |
| `nbsExternalName` | `app-classic.EXAMPLE_DOMAIN` | The domain name for your existing NBS 6 application. Use the value that you configured for the classic app in the DNS records table during Traefik ingress controller setup. |
| `ingress*` | `app.EXAMPLE_DOMAIN` or `nifi.EXAMPLE_DOMAIN` | The domain name for your NBS 7 application or NiFi admin UI. Use the value that you configured in the DNS records table during Traefik ingress controller setup. |
| Example value: `ingressHost` | `data.EXAMPLE_DOMAIN` | The domain name for the data ingestion endpoint. Use the value that you configured in the DNS records table during Traefik ingress controller setup. |
| Example value: `jdbc*` | `EXAMPLE_DB_ENDPOINT` | The hostname or endpoint of your NBS database server. Find this in the console for your database hosting service or in the Terraform outputs from infrastructure provisioning. |
| | `EXAMPLE_DB_NAME` | The name of the NBS ODSE database on your database server. The default is `NBS_ODSE`. |
| | `EXAMPLE_ODSE_DB_USER` / `EXAMPLE_DB_USER` | The database login used by NBS microservices. The default is `nbs_ods`. |
| | `EXAMPLE_ODSE_DB_USER_PASSWORD` / `EXAMPLE_DB_USER_PASSWORD` | The password for the database user. Retrieve this from your secrets manager or your infrastructure team. |
| `security.tokenSecret` | `EXAMPLE_TOKEN_SECRET` | The token secret used to encrypt JWT tokens. Use the token secret generated during the pagebuilder-api deployment. `[SME REVIEW: confirm accuracy]` |
| `security.parameterSecret` | `EXAMPLE_PARAMETER_SECRET` | A randomly generated 32-character string used to encrypt parameter values. Generate one with: `openssl rand -base64 32 \| cut -c1-32` |
| `singleUserCredentialsUsername` | `EXAMPLE_NIFI_ADMIN_USER` | A username for the NiFi admin UI. Choose any username except `admin`. |
| `singleUserCredentialsPassword` | `EXAMPLE_NIFI_ADMIN_USER_PASSWORD` | A password for the NiFi admin UI account. |
| `nifiSensitivePropsKey` | `EXAMPLE_NIFI_SENSITIVE_PROPS` | A randomly generated string of at least 12 characters. NiFi uses this key to encrypt sensitive values it stores internally. |
| `oidc.client.secret` | `EXAMPLE_OIDC_SECRET` | The client secret for Keycloak login authentication. Retrieve this from the Keycloak admin UI: select the **NBS** realm, go to **Clients**, select the relevant client, and copy the value from the **Credentials** tab. See [Retrieve the nbs-modernization client secret](../../deploy-nbs7/keycloak/keycloak-installation.html#retrieve-the-nbs-modernization-client-secret). |
| Example value: `kafka.cluster` | `EXAMPLE_KAFKA_ENDPOINT(S)` / `EXAMPLE_KAFKA_MULTI_CLUSTER_ENDPOINTS` | A comma-delimited list of the private plaintext endpoints for your Kafka brokers. In AWS deployments, find these in the Amazon MSK console under your cluster > **View client information** > **Bootstrap servers (plaintext)**. `[SME REVIEW: Azure path TBD]` |
| `sftp.*` | `EXAMPLE_SFTP_HOST` `EXAMPLE_SFTP_USER` `EXAMPLE_SFTP_PASS` `EXAMPLE_SFTP_FILE_EXTNS` `EXAMPLE_SFTP_FILE_PATHS` | Connection details for the SFTP server used by the data ingestion service, including host, username, password, file extensions, and file paths. `[SME REVIEW: confirm whether these are STLT-managed or provisioned as part of NBS infrastructure]` |
| `nbs.authuser` | `EXAMPLE_NBS_AUTHUSER` | `[SME REVIEW: Is this a Keycloak user, a database user, or something else?]` |
<!-- markdownlint-disable MD058 -->
<div class="three-column-values-table" markdown="1">

| `keycloak.srte.clientId` | `EXAMPLE_SRTE_CLIENT_ID` | The Keycloak client ID for SRTE data access. The default is `srte-data-keycloak-client`. Confirm in the Keycloak admin UI under the **NBS** realm > **Clients**. |
| `keycloak.srte.clientSecret` | `EXAMPLE_SRTE_CLIENT_SECRET` | The client secret for SRTE data access. Retrieve from the Keycloak admin UI: **NBS** realm > **Clients** > `srte-data-keycloak-client` > **Credentials** tab. |

</div>
<!-- markdownlint-enable MD058 -->

> Run Helm install commands from the `charts` directory for all microservices. Before you run Helm install commands, verify you are authenticated to AWS by running `aws sts get-caller-identity`.
{: .note }
