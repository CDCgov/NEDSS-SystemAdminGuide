---
title: Deploy NBS 7 microservices
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

This phase deploys the [[nbs-7]] application services into your [[kubernetes]] cluster using [[helm]]. Deploy services in the order listed. Each service has dependencies on the ones before it.

> The pages in this section apply to NBS {{ site.version_latest }}. GitHub links for the [NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm) repo are pinned to `{{ site.version_latest_tag }}`.
{: .note }

## Overview

Use the Helm CLI to deploy NBS 7 microservices into your Kubernetes cluster. Verify that each microservice starts successfully before you move to the next service.

## Before you begin

These steps require a Unix-compatible shell. On Microsoft Windows, use Git Bash, Windows Subsystem for Linux ([[wsl]]), or an equivalent terminal emulator.

Complete the following steps before you deploy the first microservice:

1. Verify that you are authenticated to your cloud provider and that your session targets the account for your NBS environment.
   - **AWS:** Run `aws sts get-caller-identity` and confirm the output shows your NBS account ID.
   - **Azure:** Run `az account show` and confirm the output shows your NBS subscription.
1. Verify that `kubectl` targets the correct Kubernetes cluster. Run `kubectl config current-context` and confirm that the output names your NBS cluster.
1. Use Git to clone your own local copy of the public [NEDSS-Helm][nedss-helm] repository.
1. Navigate to the `charts` directory of your cloned NEDSS-Helm repository. Run all Helm install commands from this directory.

Each user who signs in to NBS 7 must exist as an ACTIVE `user_id` in the [[classic-nbs|NBS 6]] `Auth_user` table. If that account is missing or not ACTIVE, [[keycloak]] login still succeeds, but a user who could use NBS 6 before can no longer open NBS 6 pages. For more information, see [NBS 6 user requirement](../full-deploy/kubernetes-setup/deploy-keycloak.html#nbs-6-user-requirement).
{: .important }

## Helm values reference for NBS 7 microservices

The following table lists common Helm values used across NBS 7 microservices. Have these values available before you begin deployment.

<!-- markdownlint-disable MD055 MD056 -->

| Placeholder in values.yaml | Name of value | Description |
|---|---|---|
| `app-classic.EXAMPLE_DOMAIN` | `nbsExternalName` | The domain name for your existing NBS 6 application. This is the [[dns]] name you already use for classic NBS today, not a new record you create as part of the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records). |
| `EXAMPLE_DB_ENDPOINT` | Varies by chart, for example: `jdbc*` | The hostname or endpoint of your NBS database server. Find this in the console for your database hosting service or in the Terraform outputs from infrastructure provisioning. |
| `EXAMPLE_DB_NAME` | Varies by chart | The name of the database that the chart's service connects to. For most services, such as [[apache-nifi\|NiFi]] and the Modernization API, this is the NBS [[ods-odse\|ODSE]] database, `NBS_ODSE` by default. For the `reporting-pipeline-service` chart, use the reporting database that you chose in [RTR database setup](real-time-reporting/real-time-reporting.html): `RDB`, or `RDB_MODERN`. |
| `EXAMPLE_ODSE_DB_USER` / `EXAMPLE_DB_USER` / `EXAMPLE_DB_USERNAME` | Varies by chart | The database login used by NBS microservices. The default is `nbs_ods`. |
| `EXAMPLE_ODSE_DB_USER_PASSWORD` / `EXAMPLE_DB_USER_PASSWORD` / `EXAMPLE_DB_PASSWORD` | Varies by chart | The password for the database user. Retrieve this from your secrets manager or your infrastructure team. |
| `EXAMPLE_KAFKA_ENDPOINT(S)` / `EXAMPLE_KAFKA_ENDPOINT_AND_PORT` / `EXAMPLE_KAFKA_MULTI_CLUSTER_ENDPOINTS` | `kafka.cluster` (varies by chart) | A comma-separated list of the private plaintext broker endpoints (port 9092) for your [[kafka]] cluster. **AWS:** find these in the [[amazon-msk\|Amazon MSK]] console under your cluster > **View client information** > **Bootstrap servers (plaintext)**. **Azure:** use the worker-node broker hostnames (`wn*...:9092`) of your [[hdinsight\|HDInsight]] Kafka cluster, available from the cluster in the Azure portal or from the Terraform outputs from infrastructure provisioning. |
| `app.EXAMPLE_DOMAIN`, `data.EXAMPLE_DOMAIN`, or `nifi.EXAMPLE_DOMAIN` | Varies by chart, for example: `ingressHost` | The public hostname for the service. Charts reference it under keys such as `ingressHost` or `dataingestion.uri`. Use `app.` for the NBS application tier (NBS Gateway and Modernization API), `data.` for the data services tier (data ingestion, data processing, and Data Sync), and `nifi.` for the NiFi admin UI. Use the values that you configured in the [DNS records table](../full-deploy/kubernetes-setup/deploy-core-services.html#create-dns-records). |
| `EXAMPLE_EFS_ID` | `efsFileSystemId` | **AWS deployments:** The [[amazon-efs\|Amazon EFS]] file system ID for the persistent network file storage used by services that need it. Find it in the EFS console under **File systems** or in the Terraform outputs. |
| `EXAMPLE_STORAGE_ACCOUNT_NAME` and `EXAMPLE_RESOURCE_GROUP_NAME` | `azure.files.storageAccountName` and `azure.files.resourceGroupName` | **Azure deployments:** The [[azure-files\|Azure Files]] storage account name and its resource group, which provide the persistent network file storage. The NEDSS-Infrastructure `terraform/azure/modules/1-nbs7/storage-account` module creates these. |
| `EXAMPLE_TOKEN_SECRET` | `security.tokenSecret` | The secret that the Modernization API uses to encrypt authentication tokens. Generate a random value with: <code>openssl rand -base64 64 &#124; tr -d '\n'</code> |
| `EXAMPLE_PARAMETER_SECRET` | `security.parameterSecret` | The secret that the Modernization API uses to encrypt search parameters. Generate a random value with: <code>openssl rand -base64 32 &#124; cut -c1-32</code> |
| `EXAMPLE_NIFI_ADMIN_USER` | `singleUserCredentialsUsername` | The username for the NiFi admin UI. Choose any username except `admin`. |
| `EXAMPLE_NIFI_ADMIN_USER_PASSWORD` | `singleUserCredentialsPassword` | The password for the NiFi admin UI account. |
| `EXAMPLE_NIFI_SENSITIVE_PROPS` | `nifiSensitivePropsKey` | The password that NiFi uses to derive an encryption key for sensitive values that it stores internally. Generate a random value of at least 12 characters with: <code>openssl rand -base64 32 &#124; cut -c1-32</code> |
| `EXAMPLE_OIDC_SECRET` | `oidc.client.secret` | The client secret for Keycloak login authentication. Retrieve this from the Keycloak admin UI: select the **NBS** realm, navigate to **Clients**, select the relevant client, and copy the value from the **Credentials** tab. See [Import service clients and retrieve secrets](../full-deploy/kubernetes-setup/deploy-keycloak.html#import-service-clients-and-retrieve-secrets). |
| `EXAMPLE_NBS_AUTHUSER` | `nbs.authuser` | The username of the NBS account that the data processing service uses to import and export data. Use a service account, typically the `ELRImporter` type user that your jurisdiction already has set up. |
| `EXAMPLE_SRTE_CLIENT_ID` | `keycloak.srte.clientId` | The Keycloak client ID for [[srt-srte\|SRTE]] data access. The default is `srte-data-keycloak-client`. This client is not included in the initial **NBS** realm import and requires a separate import step. See [Import service clients and retrieve secrets](../full-deploy/kubernetes-setup/deploy-keycloak.html#import-service-clients-and-retrieve-secrets). |
| `EXAMPLE_SRTE_CLIENT_SECRET` | `keycloak.srte.clientSecret` | The client secret for SRTE data access. After you import the client, retrieve the secret from the **Credentials** tab. See [Import service clients and retrieve secrets](../full-deploy/kubernetes-setup/deploy-keycloak.html#import-service-clients-and-retrieve-secrets). |
| `EXAMPLE_SFTP_HOST` `EXAMPLE_SFTP_USER` `EXAMPLE_SFTP_PASS` `EXAMPLE_SFTP_FILE_EXTNS` `EXAMPLE_SFTP_FILE_PATHS` | `sftp.*` | Connection details for the external [[sftp]] server used by the data ingestion service, including host, username, password, file extensions, and file paths. The SFTP server is managed by your jurisdiction and is not provisioned as part of NBS infrastructure. These values are required only if you configure SFTP polling for manual [[elr]] file drop-off. |
| `EXAMPLE_DB_PORT` | `jdbc.connection_url` (port) | The port of your NBS database server, set as a separate value within the [[jdbc]] connection string. The default for [[microsoft-sql-server\|SQL Server]] is `1433`. |
{: .three-column-values-table }

After you gather these values, continue to the deployment pages. The table of contents on this page lists the deployment pages in order, starting with the first service to deploy. Complete each page in sequence.

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
