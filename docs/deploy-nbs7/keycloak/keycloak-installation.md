---
title: Install Keycloak
layout: page
parent: Deploy cluster infrastructure
nav_order: 2
has_children: true
nav_enabled: true
redirect_from:
  - /docs/5_keycloak/1_keycloak_installation.html
  - /docs/5_keycloak/1_keycloak_installation/
---

# Keycloak Installation
{: .no_toc }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

The Keycloak Helm chart provides authentication for `modernization-api`, `nbs-gateway`, `data-ingestion-api`, and `nnd`.

## Create the Keycloak database

> Any compatible SQL client can be used, including SQL Server Management Studio (SSMS).
{: .note }

1. Using your SQL client, authenticate into the RDS instance where NBS is running:
   - **DB Endpoint** – DB Endpoint
   - **Username** – `admin`
   - **Password** – `database_admin_password`

1. Run the script below (from `<Helm extract directory>/charts/keycloak/nbs_keycloak.sql`) to create the Keycloak database and database user. Replace `'EXAMPLE_KCDB_PASS8675309'` with a complex password that meets your organization's standards. Store this password securely — you will need it in the `values.yaml` file in the next section.

   ```bash
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

   **Validation: Keycloak database is created**

   ![keycloak-database-creation](images/keycloak-database-creation.png)

## Configure the Helm chart

1. In `{Helm extract directory}/charts/keycloak/values.yml`, update the following parameters:

   | **Parameter** | **Template Value** | **Example / Description** |
   |---|---|---|
   | adminUser | admin | Keycloak admin account for the Web UI. Keep the template value or change to match organizational naming conventions. |
   | adminPassword | EXAMPLE_KC_PASS8675309 | Password for the Keycloak admin user. Use a complex password matching organizational standards. |
   | KC_DB | mssql | mssql |
   | KC_DB_URL | jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=keycloak;encrypt=true;trustServerCertificate=true; | jdbc:sqlserver://mydbendpoint:1433;databaseName=keycloak;encrypt=true;trustServerCertificate=true; |
   | KC_DB_USERNAME | NBS_keycloak | Keycloak database account. Keep the template value or change to match organizational naming conventions. |
   | KC_DB_PASSWORD | EXAMPLE_KCDB_PASS8675309 | Must match the password set in step 2 of the previous section. |
   | efsFileSystemId | EXAMPLE_EFS_ID | EFS file system ID from the AWS console or CLI. Provides persistent storage for themes. |

## Deploy Keycloak

1. Authenticate to the Amazon EKS cluster:

   ```bash
   aws eks --region us-east-1 update-kubeconfig --name <clustername> # e.g. cdc-nbs-sandbox
   ```

1. From the charts directory, install the Keycloak Helm chart. This step takes at least 5 minutes while the init container becomes available. See the README in `Helm/charts/keycloak` for details.

   ```bash
   Helm install keycloak --namespace default -f keycloak/values.yaml keycloak
   ```

   ![keycloak-database-tables](images/keycloak-database-tables.png)

1. Verify the pod is running before proceeding:

   ```bash
   kubectl get pods -n default
   ```

## Access the Keycloak admin interface

> Port forwarding is not supported by CloudShell by default. Run these commands from a system that has both network access to the Amazon EKS endpoint and a browser. If you completed the installation from CloudShell, switch to a jumpbox or desktop with network connectivity to the Amazon EKS endpoint.
{: .note }

1. Set up port forwarding:

   ```bash
   export POD_NAME=$(kubectl get pods --namespace default -o name);
   echo "Visit http://127.0.0.1:8080/auth to use your application";
   kubectl --namespace default port-forward "$POD_NAME" 8080;
   ```

1. In a browser, navigate to <http://127.0.0.1:8080/auth> and select **Administrative console**.

   ![keycloak-ui-interface](images/kyecloak-login.png)

1. Sign in using the `adminUser` and `adminPassword` values configured in the Helm chart.

   ![keycloak-ui-login](images/keycloak-ui.png)
   ![keycloak-ui-2-login](images/keycloak-admin-ui-first-time-login.png)

## Create the NBS realm

1. Create a new realm to contain the NBS-specific client and user/group configurations.

   ![nbs-create-new-realm](images/create-new-nbs-realm-with-di-client.png)

1. Upload `{Helm extract directory}/charts/keycloak/extra/01-NBS-realm-with-DI-client.json` and click **Create**. This imports the NBS realm and clients.

   ![nbs-create-new-realm-2](images/create-new-nbs-realm-with-di-client-2.png)
   ![nbs-create-new-realm-3](images/create-new-nbs-realm-with-di-client-3.png)

1. Verify the realm and clients are created successfully.

   ![nbs-realm-di-client-creation](images/nbs-realm-di-client-3.png)

## Configure service clients

The imported configuration seeds a random client secret for each service client. You may regenerate or use a secure local client secret. Repeat the import and retrieval steps below for each client.

### DI client

1. Navigate to the **NBS Realm** in the left menu and click **Clients**.
1. Select `di-keycloak-client` and open the **Credentials** tab.
1. Click the eye icon to reveal the secret and copy it.
1. Store the secret for use by the applications (for example, in AWS Secrets Manager at `keycloak/client/secret/di`).

   ![di-client-id](images/di-client-id.png)
   ![di-client-secret](images/di-client-secret.png)

### NND client

1. In the **NBS Realm**, open **Realm settings**, click the **Action** dropdown, and select **Partial Import**.

   ![nnd-realm](images/nnd-realm.png)
   ![nnd-realm-partial-import](images/nnd-realm-partial-import.png)

1. Upload `<Helm extract directory>/charts/keycloak/extra/05-nbs-users-nnd-client.json` and click **Create**.
1. Navigate to the **NBS Realm** in the left menu and click **Clients**.
1. Select `nnd-keycloak-client` and open the **Credentials** tab.
1. Click the eye icon to reveal the secret and copy it.
1. Store the secret (for example, in AWS Secrets Manager at `keycloak/client/secret/nnd`).

   ![nnd-client-id](images/nnd-client-id.png)
   ![nnd-client-secret](images/nnd-client-secret.png)

### SRTE client

1. In the **NBS Realm**, open **Realm settings**, click the **Action** dropdown, and select **Partial Import**.
1. Upload `<Helm extract directory>/charts/keycloak/extra/06-nbs-users-srte-data-client.json` and click **Create**.
1. Navigate to the **NBS Realm** in the left menu and click **Clients**.
1. Select `srte-data-keycloak-client` and open the **Credentials** tab.
1. Click the eye icon to reveal the secret and copy it.
1. Store the secret (for example, in AWS Secrets Manager at `keycloak/client/secret/srte`).
