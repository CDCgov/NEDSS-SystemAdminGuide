---
title: Real Time Reporting (Preview)
layout: page
nav_order: 8
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

# Deploy Real Time Reporting via helm chart

>  ℹ️ **Note:** ***This feature is optional and in beta and not production ready. Please follow the steps if you would like to install it in your environment.***

This guide details steps to install NBS 7 Real Time Reporting end to end. Real Time Reporting provides rapid transformation and delivery of data from transactional database NBS_ODSE to the reporting database RDB. Changes are captured by enabling Change Data Capture on select NBS_ODSE and NBS_SRTE tables (list under [Onboarding: Service Users and Setup Scripts](#Onboarding-Service-Users-and-Setup-Scripts)). Row-level changes from these tables are published into Kafka topics and consumed by domain-specific Java services that extract and load data into RDB.

---

## Database Setup for Onboarding

The database scripts referenced in the guide are maintained in the [DataReporting](https://github.com/CDCgov/NEDSS-DataReporting/tree/main/liquibase-service) repository. The required database objects can be configured either by database change management tool Liquibase or manually executed. Both references will be provided within the same sections.

If there are problems encountered during Database Setup, please reach out to our support team(email nbs@cdc.gov).

### Onboarding: Prerequisites

1. Classic ETL: Please ensure the following ETL batch jobs have run successfully before setting up the reporting database for Real Time Reporting.
   - a. ETL scheduled jobs:
     - MasterEtl.bat
     - PHCMartETL.bat
     - covid19ETL.bat
   - b. Database setup:
     - Option 1: Using RDB is the default database for Real Time Reporting. Please turn off the classic ETL batch jobs and proceed with the onboarding steps.
     - Option 2: Creating a separate database (rdb_modern) for Real Time Reporting. Steps are listed under [Onboarding: UAT Database Setup](#Onboarding-UAT-Database-Setup) section.

2. Database Release Version: Verify the underlying database release version returned is 6.0.16 or higher. Execute the following query to verify the baseline NBS Release version:
     ```sql
       USE NBS_ODSE; 
       SELECT max(Version) current_version
       FROM NBS_ODSE.dbo.NBS_Release;
       
       --or use the below query to check the config value
       
       use [NBS_ODSE];
       select * from NBS_configuration where config_key = 'CODE_BASE'
     ```

3. Environment Variable: Set the appropriate environment variable to define the reporting database context. This ensures that scripts execute against the correct reporting database.
   - a. Option 1: RDB as default database. Please insert the following to NBS_configuration to default to RDB.
       ```sql
       IF NOT EXISTS(SELECT 1 FROM NBS_ODSE.DBO.NBS_configuration WHERE config_key ='ENV' AND config_value ='PROD')
       INSERT INTO NBS_ODSE.dbo.NBS_configuration
       (config_key, config_value, short_name, desc_txt, default_value, valid_values, category, add_release, version_ctrl_nbr, add_user_id, add_time, last_chg_user_id, last_chg_time, status_cd, status_time, admin_comment, system_usage, config_value_large)
       VALUES(N'ENV', N'PROD', N'RTR reporting database', N'Indicates scripts should be run against RDB database', NULL, N'UAT, PROD', N'RTR', N'7.11.0', 1, 0, getdate(), 0, getdate(), N'A', getdate(), NULL, NULL, NULL);
       ```
   - b. Option 2: rdb_modern as default database. This setting overrides the default RDB during script execution, unless the script explicitly prompts specification of a database.
       ```sql
       IF NOT EXISTS(SELECT 1 FROM NBS_ODSE.DBO.NBS_configuration WHERE config_key ='ENV' AND config_value ='UAT')
       INSERT INTO NBS_ODSE.dbo.NBS_configuration
       (config_key, config_value, short_name, desc_txt, default_value, valid_values, category, add_release, version_ctrl_nbr, add_user_id, add_time, last_chg_user_id, last_chg_time, status_cd, status_time, admin_comment, system_usage, config_value_large)
       VALUES(N'ENV', N'UAT', N'RTR reporting database', N'Indicates scripts should be run against UAT rdb_modern database', NULL, N'UAT, PROD', N'RTR', N'7.11.0', 1, 0, getdate(), 0, getdate(), N'A', getdate(), NULL, NULL, NULL);
       ```
     
### Onboarding: UAT Database Setup

[Optional] Restore RDB as rdb_modern database: If a separate database is required as part of UAT, please create a restored backup of the RDB as rdb_modern. This ensures availability of classic ETL hydrated RDB and to host necessary components for Real Time Reporting. If you have AWS RDS, please run the following steps.
   - i. Backup RDB
       - a. Login into AWS Account.
       - b. Navigate to RDS.
       - c. Ensure the RDS SQL Server has the Option for Backup and Restore Enabled in Options group.
       - d. Open any SQL Client and connect to SQL Server RDS instance.
       - e. Backup database to AWS S3.
            - Run this procedure to back up the SQL Server database to S3.
              ```sql
              exec msdb.dbo.rds_backup_database
              @source_db_name='RDB',
              @s3_arn_to_backup_to='arn:aws:s3:::cdc-nbs-state-upload-shared/Classic-6.0.16/rdb_classic_2024_07_22_5pmet.bak',
              @type='FULL'
              ```
            - Run the procedure to check the status.
              ```sql
              exec msdb.dbo.rds_task_status;
              ```
   - ii. Restore rdb_modern:
       - a. Open any SQL Client and connect to SQL Server RDS instance.
       - b. Restore RDB as rdb_modern by executing the following procedure.
            ```sql
            exec msdb.dbo.rds_restore_database  
            @restore_db_name='rdb_modern',
            @s3_arn_to_restore_from='arn:aws:s3:::cdc-nbs-state-upload-shared/Classic-6.0.16/rdb_classic_gdit_07_10_5pmet.bak',
            @type='FULL';
            ```
            - Run the procedure to check the status.
              ```sql
              exec msdb.dbo.rds_task_status;
              ```
### Onboarding: Service Users and Setup Scripts
One time onboarding steps required for Real Time Reporting setup.
1. Create database users: Each user will be provided with permissions it needs to do its job and nothing more! **Please review the scripts and update the PASSWORD field for before executing.**
    - a. Create admin user: User provides Liquibase required permissions to maintain necessary database components for Real Time Reporting, and enable Change Data Capture for tables.
      - Script location: [NEDSS-DataReporting/create-rtr-admin-user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/001-master/01_onboarding_scripts_user_creation/000-create_rtr_admin_user-001.sql)
    - b. Create Real Time Reporting microservice user logins: Create dedicated user accounts for each Real Time Reporting microservice. These users are wired in ArgoCD for each Real Time Reporting services.
      - Script location: [NEDSS-DataReporting/service-user-login-script](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/001-master/01_onboarding_scripts_user_creation/001-service_users_login_creation-001.sql)
      - Script location: [NEDSS-DataReporting/service-database-user-creation](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/001-master/01_onboarding_scripts_user_creation/002-service_database_user_creation-001.sql)
2. Create required database objects: Scripts required for Real Time Reporting can be executed via Liquibase or manually. 
    - Option 1: If Liquibase is the preferred approach, please refer to steps in the [Liquibase/liquibase](1_liquibase.md) section to create all necessary objects before moving to step 3.
    - Option 2: The required database objects can also be manually created. Documentation on script execution sequence and supplemental `db_upgrade.bat` file is provided to support manual setup. 
      - Script location: [NEDSS-DataReporting/db-upgrade](https://github.com/CDCgov/NEDSS-DataReporting/tree/main/liquibase-service/src/main/resources/stlt/manual_deployment)
3. Load data and enable Change Data Capture: This one time onboarding step is required after all database objects are created via Liquibase or manual script execution.
   - a. Load metadata rows from NBS_ODSE and NBS_SRTE database tables to the reporting database.
     - Script location: [000-nrt_metadata_load.sql](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/001-master/02_onboarding_script_data_load/000-nrt_metadata_load-001.sql)
   - b. Data load to nrt_<>_key tables
     - Run remaining onboarding scripts starting from `/02_onboarding_script_data_load/001-*`.
     - Script location: [/02_onboarding_script_data_load/001-*.sql](https://github.com/CDCgov/NEDSS-DataReporting/tree/main/liquibase-service/src/main/resources/db/001-master/02_onboarding_script_data_load)
   - c.Enable Change Data Capture on NBS_ODSE and NBS_SRTE databases and tables:
     - i. These are the final scripts that should be run before go-live.
       - [1002-enable_cdc_on_odse_database.sql](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/001-master/02_onboarding_script_data_load/1002-enable_cdc_on_odse_database-001.sql)
       - [1003-enable_cdc_on_srte_database.sql](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/001-master/02_onboarding_script_data_load/1003-enable_cdc_on_srte_database-001.sql)
       - [1004-enable_cdc_on_odse_tables.sql](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/001-master/02_onboarding_script_data_load/1004-enable_cdc_on_odse_tables-001.sql)
       - [1005-enable_cdc_on_srte_tables.sql](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/001-master/02_onboarding_script_data_load/1005-enable_cdc_on_srte_tables-001.sql)

         ```sql
            --Verify change data capture. is_cdc_enabled=1 indicates successful configuration. 
          SELECT name,
            is_cdc_enabled
          FROM sys.databases;
   
         --View ODSE tables with CDC enabled. 
          USE NBS_ODSE;
          SELECT
            name,
            case when is_tracked_by_cdc  = 1 then 'YES'
              else 'NO' end as is_tracked_by_cdc
            FROM sys.tables
            WHERE is_tracked_by_cdc = 1;
   
          -- View SRTE tables with CDC enabled
          USE NBS_SRTE;
          SELECT
            name,
            case when is_tracked_by_cdc  = 1 then 'YES'
              else 'NO' end as is_tracked_by_cdc
            FROM sys.tables
            WHERE is_tracked_by_cdc = 1;
          ```

       ![cdc-enabled-odse-tables](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/cdc_enabled_odse_tables.png "CDC for NBS_ODSE")

       ![cdc-enabled-srte-tables](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/cdc_enabled_srte_tables.png "CDC for NBS_SRTE")

**_Troubleshooting tip:_** After `rdb_modern` is restored, if the Change Data Capture is not producing data, run the following script:

   ```sql
   -- Change DB owner after backup/restore
   USE NBS_ODSE;
   EXEC sp_changedbowner 'sa';
   ```
### Continuous Integration for Real Time Reporting Database
After onboarding, future enhancements will be delivered using these two approaches.

- Option 1: Execute Liquibase with the provided release tag. If Liquibase is the preferred method, please refer to steps in the [Liquibase/liquibase](1_liquibase.md) section.
- Option 2: Manually executing the scripts located under https://github.com/CDCgov/NEDSS-DataReporting/tree/main/liquibase-service/src/main/resources/stlt/manual_deployment. Onboarding scripts are excluded.

---
Real Time Reporting services should be deployed in the following order: 
- liquibase
- debezium-connect
- cp-kafka-connect-server
- observation-reporting-service
- person-reporting-service
- organization-reporting-service
- investigation-reporting-service
- ldfdata-reporting-service
- post-processing-reporting-service. 

Real Time Reporting services leverage Kubernetes secrets for accessing database credentials. Please refer to section [Creating Kubernetes Secrets](/docs/4_initial_kubernetes_deployment/1_creating_kubernetes_secrets.md) section.) for setting up secrets within the cluster.

            
