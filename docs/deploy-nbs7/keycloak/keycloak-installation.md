---
title: Install Keycloak
layout: page
parent: Deploy cluster infrastructure
nav_order: 2
has_children: false
nav_enabled: true
redirect_from:
  - /docs/5_keycloak/1_keycloak_installation.html
  - /docs/5_keycloak/1_keycloak_installation/
  - /docs/5_keycloak/2_enable_keycloak_auth.html
  - /docs/5_keycloak/2_enable_keycloak_auth/
  - /docs/deploy-nbs7/keycloak/enable-keycloak-auth.html
  - /docs/deploy-nbs7/keycloak/enable-keycloak-auth/
description: Install Keycloak, create the NBS service and user realms, configure service clients, and retrieve client secrets for NBS 7 microservices deployment.
---

# Install Keycloak and configure authentication setup

This page walks through installing Keycloak and configuring the authentication setup that NBS 7 microservices require. Complete these steps before you deploy NBS 7 microservices.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Overview

Keycloak provides authentication for `modernization-api`, `nbs-gateway`, `dataingestion-service`, and `nnd-service`. It uses two separate realms:

- `NBS` - contains service clients for data ingestion, NND, and SRTE data access.
- `nbs-users` - contains the user-facing authentication client used by the NBS gateway and the NBS application.

Both realms are created in [Create the NBS and nbs-users realms](#create-the-nbs-and-nbs-users-realms).

Locate the Keycloak Helm chart in the [NEDSS-Helm repository][nedss-helm-keycloak-chart] before you begin.

## Create the Keycloak database

Create the Keycloak database and database user before you deploy the Helm chart.

> Any compatible SQL client works for this step, including SQL Server Management Studio (SSMS).
{: .note }

1. Using your SQL client, authenticate into your database server:

   | Field | Value |
   |---|---|
   | DB Endpoint | Your database endpoint |
   | Username | `admin` |
   | Password | Your database admin password |

1. Run the following script (also available as [nbs_keycloak.sql][nedss-helm-keycloak-sql] in the NEDSS-Helm repository) to create the Keycloak database and database user. Replace `'EXAMPLE_KCDB_PASS8675309'` with a complex password that meets your organization's standards. Store this password - you will need it in `values.yml` in the next section.

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

   ![SQL Server Management Studio Databases tree showing the keycloak database created with its Tables, Views, and Security nodes expanded](images/keycloak-database-creation.png)

## Configure the Helm chart

1. In [values.yml][nedss-helm-keycloak-values], update the following parameters:

   | Parameter | Template value | Description |
   |---|---|---|
   | `adminUser` | `admin` | Keycloak admin account for the web UI. Keep the template value or change it to match your organization's naming conventions. |
   | `adminPassword` | `EXAMPLE_KC_PASS8675309` | Password for the Keycloak admin user. Use a complex password that meets your organization's standards. |
   | `KC_DB` | `mssql` | Database type. Keep the template value. |
   | `KC_DB_URL` | `jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=keycloak;encrypt=true;trustServerCertificate=true;` | Replace `EXAMPLE_DB_ENDPOINT` with your database endpoint. |
   | `KC_DB_USERNAME` | `NBS_keycloak` | Keycloak database account. Keep the template value or change it to match your organization's naming conventions. |
   | `KC_DB_PASSWORD` | `EXAMPLE_KCDB_PASS8675309` | Must match the password you set in the previous section. |
   | `efsFileSystemId` | `EXAMPLE_EFS_ID` | **In AWS deployments:** The Amazon EFS file system ID from the AWS console or CLI. Provides persistent storage for themes. **In Azure deployments:** Azure Files requires different configuration. See [Deploy on Azure](../deploy-on-azure.html) for Azure file storage configuration. |

## Deploy Keycloak

Install the Keycloak Helm chart and verify the pod is running before you continue.

1. Authenticate to your Kubernetes cluster:

   <div class="code-example" markdown="1">

   **Amazon Elastic Kubernetes Service (Amazon EKS):**

   ```bash
   aws eks --region us-east-1 update-kubeconfig --name <clustername>
   ```

   **Azure Kubernetes Service (AKS):**

   ```bash
   az aks get-credentials --resource-group <resource-group> --name <clustername>
   ```

   </div>

1. From the `charts` directory, install the Keycloak Helm chart. This step takes at least 5 minutes while the init container becomes available. See the [README in `charts/keycloak`][nedss-helm-keycloak-chart] for details.

   ```bash
   helm install keycloak --namespace default -f keycloak/values.yml keycloak
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

> Port forwarding is not supported by CloudShell by default. Run these commands from a system that has both network access to your Kubernetes cluster endpoint and a browser. If you completed the installation from CloudShell, switch to a jumpbox or desktop with network connectivity to your cluster endpoint.
{: .important }

1. Set up port forwarding:

   ```bash
   export POD_NAME=$(kubectl get pods --namespace default -o name);
   echo "Visit http://127.0.0.1:8080/auth to use your application";
   kubectl --namespace default port-forward "$POD_NAME" 8080;
   ```

1. In a browser, go to `http://127.0.0.1:8080/auth` and select **Administrative console**.

   ![Keycloak welcome page at the /auth path with the Administration Console, Documentation, Keycloak Project, Mailing List, and Report an issue links](images/kyecloak-login.png)

1. Sign in using the `adminUser` and `adminPassword` values you configured in the Helm chart.

   ![Keycloak sign-in form with username and password fields and a Sign in button](images/keycloak-ui.png)

   After you sign in, the admin console opens to the **master** realm welcome page, as shown below.

   ![Keycloak admin console welcome page for the master realm, with the side navigation showing Clients, Client scopes, Realm roles, Users, Groups, Sessions, and Events](images/keycloak-ui-2.png)

## Create the NBS and nbs-users realms

Keycloak uses two realms for NBS 7: the **NBS realm** for service clients, and the **nbs-users realm** for user-facing authentication. Create both using the same procedure, with a different import file for each.

| Realm | Import file | Purpose |
|---|---|---|
| NBS | [`01-NBS-realm-with-DI-client.json`][nedss-helm-keycloak-di-client] | Contains service clients for data ingestion, NND, and SRTE data access. Seeds the `di-keycloak-client` service client in the same step. |
| nbs-users | [`02-nbs-users-realm.json`][nedss-helm-keycloak-nbs-users-realm] | Provides user-facing authentication for the NBS application and NBS gateway. Contains the client used by `modernization-api` and `nbs-gateway` for OIDC login. |

> OIDC must be enabled when you deploy `modernization-api` and `nbs-gateway`. You configure OIDC during microservices deployment, not on this page. See [Deploy NBS 7 microservices](../microservices-deployment/deploy-nbs7-microservices.html) for OIDC configuration steps.
{: .note }

1. From the side navigation, select **Create realm**.
1. Upload the import file for the realm you're creating, then select **Create**. The realm name field auto-populates after upload.
1. Verify the realm and its clients are created successfully.

The following screenshots show this procedure for the NBS realm.

![Keycloak side navigation with the realm selector open, showing the master realm and a Create realm button](images/create-new-realm.png)

![Keycloak Create realm form with 01-NBS-realm-with-DI-client.json uploaded, JSON content visible in the resource file area, and realm name field populated with NBS](images/nbs-realm-di-client-2.png)

![Keycloak admin console showing a Realm created successfully confirmation message and the NBS realm welcome page](images/nbs-realm-di-client.png)

The procedure is the same for the nbs-users realm, shown below with `02-nbs-users-realm.json` uploaded.

![Keycloak side navigation with the realm selector open, showing the Keycloak master realm, the NBS realm, and a Create realm button](images/nbs-users-realm.png)

![Keycloak Create realm form with 02-nbs-users-realm.json uploaded, JSON content visible in the resource file area, and realm name field populated with nbs-users](images/nbs-users-realm-2.png)

![Keycloak realm selector dropdown listing the Keycloak master realm, NBS realm, and nbs-users realm](images/nbs-users-realm-3.png)

## Configure service clients

The imported configuration seeds a random client secret for each service client. You can regenerate these secrets or use them as generated. Retrieve and store each secret before you proceed to microservices deployment.

The NBS realm contains three service clients:

| Client | Import file | Notes |
|---|---|---|
| `di-keycloak-client` | Imported with the NBS realm - no separate import needed | Used by the data ingestion service |
| `nnd-keycloak-client` | [`05-nbs-users-nnd-client.json`][nedss-helm-keycloak-nnd-client] | Used by the NND service |
| `srte-data-keycloak-client` | [`06-nbs-users-srte-data-client.json`][nedss-helm-keycloak-srte-client] | Used for SRTE data access |

### Retrieve a client secret

Use the following steps to retrieve the secret for any of the three service clients listed above.

1. In the **NBS** realm, go to **Clients** and select the client.
1. Open the **Credentials** tab.
1. Select the eye icon to reveal the secret and copy it.
1. Store the secret securely in your organization's secrets manager.

The following screenshots show this procedure for `di-keycloak-client`. The Credentials tab looks the same for the other two clients, with the client-specific secret shown in the same field.

![Keycloak Clients list in the NBS realm with di-keycloak-client highlighted in the Client ID column](images/di-client-id.png)

![Keycloak Credentials tab for di-keycloak-client showing the masked client secret field with eye and copy icons and a Regenerate button](images/di-client-secret.png)

### Import the NND client

The `nnd-keycloak-client` is not included in the initial NBS realm import. Import it separately before you retrieve its secret.

1. In the **NBS** realm, go to **Realm settings**, select the **Action** dropdown, and select **Partial Import**.

   ![Keycloak NBS realm welcome page, shown before navigating to Realm settings](images/nnd-realm.png)

   Selecting **Partial Import** opens the dialog shown below, overlaying the Realm settings page, where you upload the client JSON file.

   ![Keycloak Partial import dialog open over the NBS realm settings page, with an empty resource file upload area and an Import button](images/nnd-realm-partial-import.png)

1. Upload [`05-nbs-users-nnd-client.json`][nedss-helm-keycloak-nnd-client] and select **Import**.

After the import completes, follow [Retrieve a client secret](#retrieve-a-client-secret) to get the secret for `nnd-keycloak-client`.

### Import the SRTE client

The `srte-data-keycloak-client` is not included in the initial NBS realm import. Import it separately before you retrieve its secret.

1. In the **NBS** realm, go to **Realm settings**, select the **Action** dropdown, and select **Partial Import**.
1. Upload [`06-nbs-users-srte-data-client.json`][nedss-helm-keycloak-srte-client] and select **Import**.

After the import completes, follow [Retrieve a client secret](#retrieve-a-client-secret) to get the secret for `srte-data-keycloak-client`.

## Import base users and clients

Import the base NBS users and development clients into the nbs-users realm.

1. Select the **nbs-users** realm, then go to **Realm settings** > **Action** > **Partial Import**.

   ![Keycloak Realm settings page for the nbs-users realm, showing the General tab with realm configuration options](images/nbs-users-base-users.png)

1. Upload [`03-nbs-users-base-users.json`][nedss-helm-keycloak-extra], select the three users, and select **Import**.

   The Partial import dialog shows the file uploaded with the three users selected for import.

   ![Keycloak Partial import dialog with 03-nbs-users-base-users.json uploaded and a 3 Users checkbox selected for import](images/nbs-users-base-users-2.png)

   After the import completes, Keycloak confirms that all three users were added.

   ![Keycloak Partial import confirmation listing three added users: msa, nbs-users-admin, and superuser](images/nbs-users-base-users-3.png)

1. Upload [`04-nbs-users-development-clients.json`][nedss-helm-keycloak-extra], select the one client, and select **Import**.

   The Partial import dialog shows the development client file uploaded and selected for import.

   ![Keycloak Partial import dialog with 04-nbs-users-development-clients.json uploaded and a 1 Clients checkbox selected for import](images/nbs-users-development.png)

   After the import completes, Keycloak confirms that the client was added.

   ![Keycloak Partial import confirmation showing one added client named nbs-development](images/nbs-users-development-2.png)

## Retrieve the nbs-modernization client secret
 
The `nbs-modernization` client in the **nbs-users** realm is used for OIDC login authentication across NBS 7 microservices, including `modernization-api` and `nbs-gateway`. Retrieve its secret to set the `oidc.client.secret` value when you deploy these microservices.
 
1. In the **nbs-users** realm, go to **Clients** and select `nbs-modernization`.
1. Open the **Credentials** tab and copy the **Client Secret**.
   ![Keycloak Credentials tab for the nbs-modernization client showing the masked client secret field with eye and copy icons and a Regenerate button](images/nbs-modernization.png)
1. Store this value securely. You will use it when setting `oidc.client.secret` in the values files for `modernization-api`, `nbs-gateway`, and other NBS 7 microservices that use OIDC login during microservices deployment.

## Set the login theme (optional)

You can use the pre-populated NBS login theme, keep the default Keycloak theme, or create a custom theme. The Keycloak Helm chart loads a sample NBS theme in a persistent volume mounted at `/opt/keycloak/themes/nbs`.

1. Select the **nbs-users** realm.
1. Go to **Realm settings** > **Themes** > **Login** and select your preferred theme.

   ![Keycloak Themes tab in Realm settings for the nbs-users realm, with the Login theme drop-down open showing base and keycloak options](images/nbs-login-theme.png)

[nedss-helm-keycloak-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/keycloak>
[nedss-helm-keycloak-sql]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/nbs_keycloak.sql>
[nedss-helm-keycloak-values]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/values.yml>
[nedss-helm-keycloak-di-client]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/extra/01-NBS-realm-with-DI-client.json>
[nedss-helm-keycloak-nnd-client]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/extra/05-nbs-users-nnd-client.json>
[nedss-helm-keycloak-srte-client]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/extra/06-nbs-users-srte-data-client.json>
[nedss-helm-keycloak-nbs-users-realm]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/keycloak/extra/02-nbs-users-realm.json>
[nedss-helm-keycloak-extra]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/keycloak/extra/>
