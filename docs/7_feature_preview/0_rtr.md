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

## Deploy Real Time Reporting via helm chart

>  ℹ️ **Note:** ***This feature is optional and in beta and not production ready. Please follow the steps if you would like to install it in your environment.***

This guide details steps to install NBS 7 Real Time Reporting end to end. Real Time Reporting provides rapid transformation and delivery of data from transactional database NBS_ODSE to the reporting database `rdb_modern`. Changes are captured by enabling Change Data Capture on select NBS_ODSE and NBS_SRTE tables (listed below). Row-level changes from these tables are published into Kafka topics and consumed by domain-specific Java services that extract and load data into `rdb_modern`.

---

### Database Setup and Validation

The database scripts referenced in the guide are maintained in the [DataReporting](https://github.com/CDCgov/DataReporting) repository. The required database objects can be configured either by database change management tool Liquibase or manually executed. Both references will be provided within the same sections.

If there are problems encountered during Database Setup, please reach out to our support team (email: nbs@cdc.gov).

1. SQL Server Compatibility Level: Functionality within Real Time Reporting requires SQL Server 2016 or higher to set Compatibility Level at 130. The level is set during the Liquibase Service deployment (Section: Liquibase). Compatibility Level can be reviewed by running the query below:
   ```sql
   --View Compatibility Level
   USE NBS_ODSE;  
   SELECT compatibility_level  
   FROM sys.databases WHERE name = 'nbs_odse';
   ```
2. Database Release Version: Verify the underlying database release version returned is 6.0.16 or higher. Execute the following query to verify the baseline NBS Release version:
   ```sql
   --Verify NBS Release version
   USE NBS_ODSE; 
   SELECT max(Version) current_version
   FROM NBS_ODSE.dbo.NBS_Release;
   
   or use the below query to check the config value
   
   use [NBS_ODSE];
   select * from NBS_configuration where config_key = 'CODE_BASE'
   ```
3. Create rdb_modern database: In accordance with the strangler fig strategy, a new database, rdb_modern, is introduced to ensure availability of classic ETL hydrated RDB and to host necessary components for Real Time Reporting. RDB_Modern database needs to be created from RDB database backup. If you have AWS RDS, optionally you follow the steps to create a backup of RDB and Restoring it as RDB_Modern using RDS and S3.
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
4. Create admin user: Create a dedicated user account for Liquibase operations. The user provides Liquibase with the required permissions to maintain necessary database components for Real Time Reporting, and enable change data capture for tables. Please review the steps and update the PASSWORD field for before executing. This script enables change data capture on the database level and provides validation queries.
   - a. Script location: [NEDSS-DataReporting/create-rtr-admin-user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/liquibase-service/src/main/resources/db/master/routines/000-create_rtr_admin_user-001.sql)
5. Create Real Time Reporting microservice user logins: Create dedicated user accounts for each Real Time Reporting microservice. After the database objects are created, each user will be provided with permissions it needs to do its job and nothing more! Please review the steps and update the PASSWORD field for before executing.
   - a. Script location: [NEDSS-DataReporting/service-user-login-script](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/001-service_users_login_creation.sql)
6. Manually Enable Change Data Capture on NBS_ODSE and NBS_SRTE databases: If Step 4 is executed, Step 5 can be skipped. The query below can be used to enable Change Data Capture on the RDS SQL Server databases. sysadmin permissions are required to run it. The subsequent query can be used to verify configuration.
   ```sql
   -- Enable change data capture in ODSE
   exec msdb.dbo.rds_cdc_enable_db 'NBS_ODSE';
   -- Enable change data capure in SRTE
   exec msdb.dbo.rds_cdc_enable_db 'NBS_SRTE';
   
   --Verify change data capture. is_cdc_enabled=1 indicates successful configuration. 
   SELECT name,
     is_cdc_enabled
   FROM sys.databases;
   ```
7. Enable Change Data Capture for tables in NBS_ODSE and NBS_SRTE: Insert, updates and deletes to database tables are tracked by Change Data Capture as events. These events are used to rapidly transform and deliver data to target tables in rdb_modern. To enable Change Data Capture, please execute the following scripts. Once completed, the validation query below can be run to validate the tables being tracked.
- NBS_ODSE script location: [NEDSS-DataReporting/enable-cdc-for-odse-table](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/odse/000-odse-db-general.sql)
- NBS_SRTE Script location: [NEDSS-DataReporting/enable-cdc-for-srte-table](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/srte/000-srte-db-general.sql)

  ```sql
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

   ![cdc-enabled-odse-tables](/just-the-doc/docs/7_feature_preview/images/cdc_enabled_odse_tables.png)
   
   ![cdc-enabled-srte-tables](/just-the-doc/docs/7_feature_preview/images/cdc_enabled_srte_tables.png)

8. Manual creation of scripts for Real Time Reporting: As an alternative to Liquibase, scripts required for Real Time Reporting can be executed manually. If Liquibase is the preferred methodology, please refer to steps in the Liquibase/liquibase section.
   - a. Script location: [NEDSS-DataReporting/db-upgrade](https://github.com/CDCgov/NEDSS-DataReporting/tree/main/db/upgrade/rdb_modern#database-upgrade-script)
   - b. Provide permissions for Real Time Reporting microservice user logins after successful execution of all required script. Please run the following scripts to provide permissions.
     -   i. [Organization service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/002-create_organization_service_user.sql)
     -   ii. [Observation service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/003-create_observation_service_user.sql)
     -   iii. [Person service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/004-create_person_service_user.sql)
     -   iv. [Investigation service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/005-create_investigation_service_user.sql)
     -   v. [LDF service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/006-create_ldf_service_user.sql)
     -   vi. [Postprocessing service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/007-create_post_processing_service_user.sql)
     -   vii. [Kafka sync connector](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/008-create_kafka_sync_connector_service_user.sql)
     -   viii. [Debezium service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/009-create_debezium_service_user.sql)

**_Troubleshooting tip:_** After `rdb_modern` is restored, if the Change Data Capture is not producing data, run the following script:

   ```sql
   -- Change DB owner after backup/restore
   USE NBS_ODSE;
   EXEC sp_changedbowner 'sa';
   ```

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

            
