---
title: Keycloak Installation
layout: page
nav_order: 6
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## KeyCloak Installation
There is a Keycloak helm chart 
- a. This will be needed for `pagebuilder-api`, `modernization-api`, `nbs-gateway`, and `data-ingestion-api`.
- b. **NOTE:** SQL Server Management Studio (SSMS) or any other compatible SQL client can be used to connect to the database instance.
- c. Using SSMS, authenticate into the RDS instance where NBS is running with the following information:
   - **DB Endpoint** – [DB Endpoint](#)
   - **Username** – `admin`
   - **Password** – `database_admin_password`
- d. Use the below script (from: `<helm extract directory>/charts/keycloak/nbs_keycloak.sql`) to create a KeyCloak database in the SQL server and a database user for connection. Make sure to update the `‘EXAMPLE_KCDB_PASS8675309’` password. Use a complex password matching organizational standards and store this securely for administrative access to Keycloak. This value will also be used in `values.yaml` file in step 5 below (shown in the table).
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
    **Validation step: KeyCloak database is created**
  ![keycloak-database-creation](/just-the-doc/docs/5_keycloak/images/keycloak-database-creation.png)
  
- e. In {helm extract directory}/charts/keycloak/values.yml, update the following parameters

| **Parameter**        | **Template Value**            | **Example/Description**                        |
|----------------------|-------------------------------|------------------------------------------------|
| adminUser            | admin                         | This is the Keycloak Admin account for use in the Web UI, keep template value or change to match organizational naming conventions |
| adminPassword        | EXAMPLE_KC_PASS8675309        | password123 - This is the password for the Keycloak admin user, use a complex password matching organizational standards. |
| KC_DB                | mssql                         | mssql |
| KC_DB_URL            | jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=keycloak;encrypt=true;trustServerCertificate=true; | jdbc:sqlserver://mydbendpoint:1433;databaseName=keycloak;encrypt=true;trustServerCertificate=true; |
| KC_DB_USERNAME       | NBS_keycloak                  | This is the Keycloak database account that the applications use to access the database, keep template value or change to match organizational naming conventions |
| KC_DB_PASSWORD       | EXAMPLE_KCDB_PASS8675309      | Make sure it matches sql db from Step 4 |
| efsFileSystemId      | EXAMPLE_EFS_ID                | EFS ID - This filesystem provides persistent storage to the container for themes etc, EFS file system id is available from the AWS console or the aws cli | 

- f. Deploy KeyCloak helm chart
  - a. Make sure you are authenticated to the EKS Cluster, if not use the below command
    ```bash
    aws eks --region us-east-1 update-kubeconfig --name <clustername> # e.g. cdc-nbs-sandbox
    ```
  - b. From the charts directory, run the below command to install KeyCloak (this step will take at least 5 minutes while the init container is available for uploading or modifying themes, see the README in the helm/charts/keycloak directory for details)
    ```bash
    helm install keycloak --namespace default -f keycloak/values.yaml keycloak
    ```
    ![keycloak-database-tables](/just-the-doc/docs/5_keycloak/images/keycloak-database-tables.png)
  - c. Check to see if the pod is running before proceeding with the next deployment using
    ```bash
    kubectl get pods -n default
    ```
- g. Setup port forwarding to allow access  to the keycloak admin interface(this must be done from a system that has access to the EKS endpoint AND a browser interface, if you did the install from cloudshell up to this point you now need a jumpbox or desktop with network connectivity to the EKS endpoint)
    - **Note: Portforwarding is not supported by cloudshell by default.**
      ```bash
      export POD_NAME=$(kubectl get pods --namespace default -o name);
      echo "Visit http://127.0.0.1:8080/auth to use your application"; 
      kubectl --namespace default port-forward "$POD_NAME" 8080;
      ```
- h. Connect to KeyCloak interface http://127.0.0.1:8080/auth in the browser and select Administrative console
  ![keycloak-ui-interface](/just-the-doc/docs/5_keycloak/images/kyecloak-login.png)
- i. Sign In using adminUser and adminPassword (Table - 4)
  ![keycloak-ui-login](/just-the-doc/docs/5_keycloak/images/keycloak-ui.png)
  ![keycloak-ui-2-login](/just-the-doc/docs/5_keycloak/images/keycloak-ui-2.png)
- j. Create a new Realm (to contain the NBS specific client and user/group configurations)
  ![nbs-create-new-realm](/just-the-doc/docs/5_keycloak/images/create-new-realm.png)
- k. Upload {helm extract directory}/charts/keycloak/extra/01-NBS-realm-with-DI-client.json which is part of the helm zip file in the keycloak chart and click on Create (this will import the NBS Realm and Clients)
  ![nbs-realm-di-client](/just-the-doc/docs/5_keycloak/images/nbs-realm-di-client.png)
  ![nbs-realm-di-client-2](/just-the-doc/docs/5_keycloak/images/nbs-realm-di-client-2.png)
- l. Realm and Clients are created successfully
  ![nbs-realm-di-client-3](/just-the-doc/docs/5_keycloak/images/nbs-realm-di-client-3.png)
- m. Retrieving the Client’s secret ( the imported configuration will seed a random client secret, you may regenerate or use secure local client secret )
    - a. Navigate to NBS Realm on the left menu
    - b. Click on Clients
    - c. Select di-keycloak-client\
    - d. Select Credentials tab
    - e. Click on the “eye” and copy the random secret
    - f. Store the Client secret for use by the applications. (e.g. in AWS store in Secrets Manager keycloak/client/secret/di)
   ![di-client-id](/just-the-doc/docs/5_keycloak/images/di-client-id.png)
   ![di-client-secret](/just-the-doc/docs/5_keycloak/images/di-client-secret.png)
- n. Create a new client for nnd service. Make sure NBS realm is selected.
   ![nnd-realm](/just-the-doc/docs/5_keycloak/images/nnd-realm.png)
- o. Under Realm settings, click on “Action” drop down on top right and click on “Partial Import”.
   ![nnd-realm-partial-import](/just-the-doc/docs/5_keycloak/images/nnd-realm-partial-import.png)
- p. Upload <helm extract directory>/charts/keycloak/extra/05-nbs-users-nnd-client.json which is part of the helm zip file in the keycloak chart and click on Create (this will import the nnd service client, (note this file was named incorrectly it should be loaded into the NBS realm as shown in the steps)
- q. Retrieving the Client’s secret ( the imported configuration will seed a random client secret )
    - a. Navigate to NBS Realm on the left menu
    - b. Click on Clients
    - c. Select nnd-keycloak-client
    - d. Select Credentials tab
    - e. Click on the “eye” and copy the secret into buffer
    - f. Store the Client secret for use by the applications. (e.g. in AWS store in Secrets Manager keycloak/client/secret/nnd)
   ![nnd-client-id](/just-the-doc/docs/5_keycloak/images/nnd-client-id.png)
   ![nnd-client-secret](/just-the-doc/docs/5_keycloak/images/nnd-client-secret.png)  
- r. Create new client for SRTE. Repeat steps as shown above to import SRTE client.
    - a. Under Realm settings, click on “Action” drop down on top right and click on “Partial Import”.
    - b. Upload <helm extract directory>/charts/keycloak/extra/05-nbs-users-srte-data-client.json which is part of the helm zip file in the keycloak chart and click on Create.
    - c. Retrieving the Client’s secret (the imported configuration will seed a random client secret)
         - Navigate to NBS Realm on the left menu
         - Click on Clients
         - Select srte-data-keycloak-client
         - Select Credentials tab
         - Click on the “eye” and copy the secret
         - Store the Client secret for use by the applications. (e.g. in AWS store in Secrets Manager keycloak/client/secret/nnd) 
