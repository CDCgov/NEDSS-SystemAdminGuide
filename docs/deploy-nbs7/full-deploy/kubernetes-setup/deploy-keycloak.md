---
title: Deploy and configure Keycloak
layout: page
parent: Deploy cluster services
nav_order: 2
nav_enabled: true
description: Install Keycloak, create the NBS service and user realms, configure service clients, retrieve client secrets, and complete the final validation of Traefik and Keycloak.
redirect_from:
- /docs/5_keycloak/1_keycloak_installation.html
- /docs/5_keycloak/1_keycloak_installation/
- /docs/5_keycloak/2_enable_keycloak_auth.html
- /docs/5_keycloak/2_enable_keycloak_auth/
- /docs/deploy-nbs7/keycloak/enable-keycloak-auth.html
- /docs/deploy-nbs7/keycloak/enable-keycloak-auth/
- /docs/deploy-nbs7/keycloak/keycloak-installation.html
- /docs/deploy-nbs7/keycloak/keycloak-installation/
---

# Deploy and configure Keycloak for NBS 7

[[keycloak]] is the authentication service that lets users sign in to the [[nbs-7]] web UI. It provides authentication for `modernization-api`, `nbs-gateway`, `dataingestion-service`, and `nnd-service`, and, like the services in [Deploy core Kubernetes services](deploy-core-services.html), it is a core service. This page covers how to install Keycloak, configure the authentication setup that the NBS 7 microservices require, and validate [[traefik]] and Keycloak together. Complete these steps before you deploy the NBS 7 microservices.

**Already running Keycloak?** If your jurisdiction operates its own Keycloak and you want NBS 7 to authenticate against an existing realm, follow [Integrate NBS 7 with an existing Keycloak](existing-keycloak.html) instead of this page. This page installs the NBS-provided Keycloak and imports the NBS realms.
{: .note }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

Before you begin the procedures on this page, locate the `keycloak` [[helm-chart]] in the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}.

## Create the Keycloak database

Create the Keycloak database and database user before you deploy the Helm chart.

> Any compatible SQL client works for this step, including SQL Server Management Studio ([[ssms]]).
{: .note }

1. Using your SQL client, authenticate into your database server:

   | Field | Value |
   |----|----|
   | DB Endpoint | Your database endpoint |
   | Username | `admin` |
   | Password | Your database admin password |

1. Run the following script to create the Keycloak database and database user. Replace `'EXAMPLE_KCDB_PASS8675309'` with a complex password that meets your organization's standards. Store this password securely. You will need it in `values.yaml` in [Configure the Helm chart](#configure-the-helm-chart).

   ```sql
   use master
     IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'keycloak')
     BEGIN
       CREATE DATABASE keycloak
    END
   GO
     USE keycloak
   GO

   BEGIN
   CREATE LOGIN NBS_keycloak WITH PASSWORD = 'EXAMPLE_KCDB_PASS8675309';
   CREATE USER NBS_keycloak FOR LOGIN NBS_keycloak;
   EXEC sp_addrolemember N'db_owner', N'NBS_keycloak'
   END
   ```

The following screenshot shows the keycloak database created under **Databases** in SQL Server Management Studio, confirming the script ran successfully.

![SQL Server Management Studio Databases tree showing the keycloak database expanded under Databases, with its child nodes including Tables, Views, and Security](images/keycloak-database-creation.png)

## Configure the Helm chart

In [values.yaml][keycloak-values], update the following parameters:

<!-- markdownlint-disable MD055 MD056 -->

| Template value | Parameter | Description |
|----|----|----|
| `<<EXAMPLE_KEYCLOAK_ADMIN_PASSWORD>>` | `deployment.keycloak.env.keycloakAdminPassword` | Password for the Keycloak admin user. Use a complex password that meets your organization's standards. The admin username, `keycloakAdmin`, defaults to `admin`. |
| `<<EXAMPLE_KC_DB_USER_PASSWORD>>` | `deployment.keycloak.env.kcDbPassword` | Password for the Keycloak database account. Must match the password you set in [Create the Keycloak database](#create-the-keycloak-database). |
| `jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=keycloak;encrypt=true;trustServerCertificate=true;` | `deployment.keycloak.env.kcDbUrl` | Connection string for the Keycloak database. Replace `EXAMPLE_DB_ENDPOINT` with your database endpoint. |
| `EXAMPLE_EFS_ID` | `efsFileSystemId` | **AWS only.** The [[amazon-efs]] file system ID from the AWS console or CLI. Provides persistent storage for Keycloak themes. |
| `EXAMPLE_STORAGE_ACCOUNT_NAME` | `azure.files.storageAccountName` | **Azure only.** The name of the Azure storage account that provides persistent storage for Keycloak themes. |
| `EXAMPLE_RESOURCE_GROUP_NAME` | `azure.files.resourceGroupName` | **Azure only.** The resource group that contains the Azure storage account. |
{: .three-column-values-table }

## Deploy Keycloak

Use the following steps to install the Keycloak Helm chart and verify the pod is running. The `kubectl` commands on this page require the cluster connection you configured in [Connect to Kubernetes cluster](../provision-cloud-infrastructure/provision-cloud-environment.html#connect-to-kubernetes-cluster).

1. From the `charts` directory, install the Keycloak Helm chart. This step takes at least 5 minutes while the init container becomes available. See the [README in `charts/keycloak`][keycloak-chart-readme] for details.

   ```bash
   helm install keycloak --namespace default -f keycloak/values.yaml keycloak
   ```

   After installation completes, the Keycloak database populates with its application tables, as shown in the following screenshot.

   ![SQL Server Management Studio Tables node expanded under the keycloak database, showing Keycloak application tables such as CLIENT, CLIENT_SCOPE, and CLIENT_SESSION](images/keycloak-database-tables.png)

1. Verify the pod is running before you continue:

   ```bash
   kubectl get pods -n default
   ```

## Access the Keycloak admin interface
{: #access-the-keycloak-admin-interface }

Use port forwarding to access the Keycloak web UI from your local machine.

> Port forwarding is not supported by AWS CloudShell or Azure Cloud Shell by default. Run these commands from a system that has both network access to your Kubernetes cluster endpoint and a browser. If you completed the installation from AWS CloudShell or Azure Cloud Shell, switch to a jumpbox or desktop with network connectivity to your cluster endpoint.
{: .important }

1. Set up port forwarding:

   ```bash
   kubectl port-forward deploy/keycloak-deployment 8080
   ```

1. In a browser, navigate to `http://127.0.0.1:8080/auth` and select **Administration Console**.

   <!-- The filename kyecloak-login.png contains a typo. Do not rename this file without also updating this reference. -->
   ![Keycloak welcome page at the /auth path with the Administration Console, Documentation, Keycloak Project, Mailing List, and Report an issue links](images/kyecloak-login.png)

1. Sign in using the `adminUser` and `adminPassword` values you configured in the Helm chart.

   ![Keycloak sign-in form with username and password fields and a Sign in button](images/keycloak-ui.png)

After you sign in, the admin console opens to the **master** realm welcome page.

![Keycloak admin console welcome page for the master realm, with the side navigation showing Clients, Client scopes, Realm roles, Users, Groups, Sessions, and Events](images/keycloak-ui-2.png)

## Create the NBS and nbs-users realms

Keycloak uses two realms for NBS 7: the **NBS** realm for service clients, and the **nbs-users** realm for user-facing authentication. Create both using the same procedure, with a different import file for each.

| Realm | Import file | Purpose |
|----|----|----|
| NBS | `01-NBS-realm-with-DI-client.json` | Contains service clients for data ingestion, NND, and SRTE data access. Seeds the `di-keycloak-client` service client in the same step. |
| nbs-users | `02-nbs-users-realm.json` | Provides user-facing authentication for the NBS application and NBS gateway. Contains the client used by `modernization-api` and `nbs-gateway` for OpenID Connect ([[oidc]]) login. |

> OIDC must be enabled when you deploy `modernization-api` and `nbs-gateway`. You configure OIDC during microservices deployment, not on this page. See [Deploy NBS 7 microservices](../../microservices-deployment/deploy-nbs7-microservices.html) for OIDC configuration steps.
{: .note }

1. From the side navigation, select **Create realm**. The following screenshot shows the realm selector open in the **master** realm, where the **Create realm** button appears:

   ![Keycloak side navigation with the realm selector open, showing the master realm and a Create realm button](images/create-new-realm.png)

1. Upload the import file for the realm you're creating, then select **Create**. The **Realm name** field auto-populates after upload. The following screenshot shows the **NBS** realm import with `01-NBS-realm-with-DI-client.json` uploaded:

   ![Keycloak Create realm form with 01-NBS-realm-with-DI-client.json uploaded, JSON content visible in the resource file area, and realm name field populated with NBS](images/nbs-realm-di-client-2.png)

1. Verify the realm and its clients are created successfully. After you create both realms, the realm selector lists all three realms. The following screenshot shows the selector after the **nbs-users** realm import:

   ![Keycloak realm selector dropdown listing the Keycloak master realm, NBS realm, and nbs-users realm](images/nbs-users-realm-3.png)

## Import base users and clients

Import the base NBS users and development clients into the **nbs-users** realm:

1. Select the **nbs-users** realm, then navigate to **Realm settings** > **Action** > **Partial Import**.

   ![Keycloak Realm settings page for the nbs-users realm, showing the General tab with realm configuration options](images/nbs-users-base-users.png)

1. Upload `03-nbs-users-base-users.json`, select the three users, and select **Import**.

   The **Partial import** dialog shows the file uploaded with the three users selected for import.

   ![Keycloak Partial import dialog with 03-nbs-users-base-users.json uploaded and a 3 Users checkbox selected for import](images/nbs-users-base-users-2.png)

   After the import completes, Keycloak confirms that all three users were added.

   ![Keycloak Partial import confirmation listing three added users: msa, nbs-users-admin, and superuser](images/nbs-users-base-users-3.png)

1. Upload `04-nbs-users-development-clients.json`, select the one client, and select **Import**.

   The **Partial import** dialog shows the development client file uploaded and selected for import.

   ![Keycloak Partial import dialog with 04-nbs-users-development-clients.json uploaded and a 1 Clients checkbox selected for import](images/nbs-users-development.png)

   After the import completes, Keycloak confirms that the client was added.

   ![Keycloak Partial import confirmation showing one added client named nbs-development](images/nbs-users-development-2.png)

## Set the login theme (optional)

You can use the pre-populated NBS login theme, keep the default Keycloak theme, or create a custom theme. The Keycloak Helm chart loads a sample NBS theme in a persistent volume mounted at `/opt/keycloak/themes/nbs`.

1. Select the **nbs-users** realm.
1. Navigate to **Realm settings** > **Themes** > **Login** and select your preferred theme.

   ![Keycloak Themes tab in Realm settings for the nbs-users realm, with the Login theme drop-down open showing base and keycloak options](images/nbs-login-theme.png)

## NBS 6 user requirement

NBS 7 authenticates each user in Keycloak and then hands the username off to [[classic-nbs|NBS 6]]. Every user who signs in to NBS 7 must exist as an active `user_id` in the NBS 6 `Auth_user` table. If the user is missing or not `ACTIVE`, Keycloak login succeeds but NBS 6 page access fails.

To confirm that a user's NBS 6 account exists and is active, run the following query. The `user_id` must match the Keycloak username, and `record_status_cd` must be `ACTIVE`:

```sql
SELECT user_id, record_status_cd, nedss_entry_id
FROM NBS_ODSE.dbo.Auth_user
WHERE user_id = 'superuser';
```

## Final validation of Traefik and Keycloak

This validation depends on the DNS records from [Deploy core Kubernetes services](deploy-core-services.html#create-dns-records) and the Keycloak configuration on this page. Use a browser to verify the following:

1. Navigate to `https://app.<DOMAIN_NAME.TLD>` and verify that the NBS 7 Welcome page is shown. The following screenshot shows the Welcome page from the NBS demo environment. Your Welcome page will differ.

   ![NBS 7 demo site Welcome page with a Login panel and a Login to NBS demo site button](images/nbs7-welcome-page.png)

1. Select **Login** and verify that the Keycloak login page is shown.

   ![Keycloak login page for the NBS application with username and password fields and a Sign In button](images/keycloak-user-login.png)

1. Open your browser's developer tools. For example, in Chrome, select **View** > **Developer** > **Developer Tools**.

1. Sign in and verify that authentication works and that the NBS 7 Home page is shown.

1. In developer tools, select **Network** and select a `.js` file. Under **Headers** > **Response headers**, verify the following values:

   ```text
   Cache-Control: max-age=1209600, immutable
   Cross-Origin-Opener-Policy: same-origin
   X-Frame-Options: Allow
   ```

   ![NBS 7 home page with browser console expanded to show the Network tab with verifiable values highlighted](images/nbs7-home-page.png)

## Import service clients and retrieve secrets

The imported configuration seeds a random client secret for most service clients. You can regenerate these secrets or use them as generated. Retrieve and store each secret before you proceed to microservices deployment.

<!-- markdownlint-disable MD055 MD056 -->

| Client | Realm | Import needed | Import file | Used by |
|----|----|----|----|----|
| `case-notification-service` | NBS | ✓ Yes | [08-nbs-users-case-notification-service.json][keycloak-case-notification-client] | [Case notification service](../../microservices-deployment/case-notification/case-notification-service.html) |
| `di-keycloak-client` | NBS | No | Not needed | [Data ingestion service](../../microservices-deployment/data-ingestion/data-ingestion.html) |
| `nbs-modernization` | nbs-users | No | Not needed | OIDC login for [Modernization API](../../microservices-deployment/modernization-api.html) and [NBS Gateway](../../microservices-deployment/nbs-gateway.html) |
| `nnd-keycloak-client` | NBS | ✓ Yes | [05-nbs-users-nnd-client.json][keycloak-nnd-client] | [NND service](../../microservices-deployment/nnd-service/deploy-data-sync-service-api-cloud.html) |
| `srte-data-keycloak-client` | NBS | ✓ Yes | [06-nbs-users-srte-data.json][keycloak-srte-client] | SRTE data access |

### Import the additional clients

For each service client that has **Yes** in the **Import needed** column of the [clients table](#import-service-clients-and-retrieve-secrets), complete the following steps:

1. In the realm listed for that client, navigate to **Realm settings**, select the **Action** dropdown, and select **Partial Import**.
1. Upload the import file listed for that client and select **Import**.

After each import completes, follow [Retrieve a client secret](#retrieve-a-client-secret) to get the secret for that client.

### Retrieve a client secret

Use the following steps to retrieve the secret for any service client in the [clients table](#import-service-clients-and-retrieve-secrets):

1. In the realm listed for that client, navigate to **Clients** and select the client.
1. Open the **Credentials** tab.
1. Select the eye icon to reveal the secret and copy it.
1. Store the secret securely in your organization's secrets manager, such as [[aws-secrets-manager]] or [[azure-key-vault]].

The following screenshots show this procedure for `di-keycloak-client`.

![Keycloak Clients list in the NBS realm with di-keycloak-client highlighted in the Client ID column](images/di-client-id.png)

The **Credentials** tab looks the same for the other clients, with the client-specific secret shown in the same field.

![Keycloak Credentials tab for di-keycloak-client showing the masked client secret field with eye and copy icons and a Regenerate button](images/di-client-secret.png)

## Next steps

Continue to [Deploy NBS 7 microservices](../../microservices-deployment/deploy-nbs7-microservices.html).

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[keycloak-values]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/values.yaml>
[keycloak-chart-readme]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/keycloak>
[keycloak-case-notification-client]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/extra/08-nbs-users-case-notification-service.json>
[keycloak-nnd-client]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/extra/05-nbs-users-nnd-client.json>
[keycloak-srte-client]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/extra/06-nbs-users-srte-data.json>
