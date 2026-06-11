---
title: Deploy real-time reporting
layout: page
parent: Deploy NBS 7
nav_order: 7
has_children: true
description: Guides deployment of RTR components that stream ODSE and SRTE changes to RDB through Kafka.
redirect_from:
  - /docs/7_feature_preview/(DEPRECATED)4_observation_reporting_service/
  - /docs/7_feature_preview/(DEPRECATED)5_person_reporting_service/
  - /docs/7_feature_preview/(DEPRECATED)6_organization_reporting_service/
  - /docs/7_feature_preview/(DEPRECATED)7_investigation_reporting_service/
  - /docs/7_feature_preview/(DEPRECATED)8_ldfdata_reporting_service/
  - /docs/7_feature_preview/(DEPRECATED)9_post_processing_reporting_service/
  - /docs/7_feature_preview/0_rtr.html
  - /docs/7_feature_preview/0_rtr/
---

# Deploy real-time reporting (RTR)

> This feature is in Beta preview and not production ready.
{: .important }

Real-time reporting (RTR) is an NBS 7 capability that reduces reporting latency from as long as 24 hours to between 5 minutes and 1 hour. RTR uses [Change Data Capture](#enable-change-data-capture) to detect row-level changes in source tables, publishes those changes to Kafka topics, and loads the data into the reporting database. This section covers steps to install RTR with Helm charts.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

Complete the sections on this page in order. Each section depends on the previous one. If you encounter issues during database setup, contact support at <mailto:nbs@cdc.gov>.

## Prerequisites

Before you begin, verify that your environment meets the following requirements and choose a database installation method. The method you choose applies throughout this guide.

To reduce risk, consider setting up RTR in a testing environment before moving to production. This lets you run RTR alongside MasterETL and compare results, then turn off MasterETL only after you are satisfied with those results.
{: .important }

1. RTR installation requires NBS 6.0.18.1 or higher. Running the latest NBS 6 release is suggested before proceeding. To verify your baseline NBS release version, run one of the following queries:

   ```sql
   USE NBS_ODSE;
   SELECT max(Version) current_version
   FROM NBS_ODSE.dbo.NBS_Release;
   ```

   Or:

   ```sql
   USE [NBS_ODSE];
   SELECT * FROM NBS_Configuration WHERE config_key = 'CODE_BASE';
   ```

1. Verify that the following classic ETL batch jobs have completed successfully:
   - `MasterETL.bat`
   - `PHCMartETL.bat`
   - `covid19ETL.bat`

   > Back up the `RDB` database before you proceed. This step cannot be undone.
   {: .warning }

1. Choose a database path and use it consistently throughout this guide. Both paths support Liquibase or script-based installation.

   - **RDB path:** Use `RDB` as the default reporting database. Turn off the classic ETL batch jobs and proceed to the next step. MasterETL remains available for manual recovery runs if needed.
   - **rdb_modern path:** Create a separate reporting database. To create the database, see [Create rdb_modern database](#set-up-the-rdb_modern-database) before moving on to [Create service users and database objects](#create-service-users-and-database-objects).

1. Set the environment variable for your chosen path.

   - **RDB path:** Insert the following value into `NBS_Configuration`:

      ```sql
      IF NOT EXISTS(SELECT 1 FROM NBS_ODSE.DBO.NBS_Configuration WHERE config_key ='ENV' AND config_value ='PROD')
      INSERT INTO NBS_ODSE.dbo.NBS_Configuration
      (config_key, config_value, short_name, desc_txt, default_value, valid_values, category, add_release, version_ctrl_nbr, add_user_id, add_time, last_chg_user_id, last_chg_time, status_cd, status_time, admin_comment, system_usage, config_value_large)
      VALUES(N'ENV', N'PROD', N'RTR reporting database', N'Indicates scripts should be run against RDB database', NULL, N'UAT, PROD', N'RTR', N'7.12.0', 1, 0, getdate(), 0, getdate(), N'A', getdate(), NULL, NULL, NULL);
      ```

   - **rdb_modern path:** This setting overrides the default `RDB` during script execution unless a script explicitly prompts for a database.

      ```sql
      IF NOT EXISTS(SELECT 1 FROM NBS_ODSE.DBO.NBS_Configuration WHERE config_key ='ENV' AND config_value ='UAT')
      INSERT INTO NBS_ODSE.dbo.NBS_Configuration
      (config_key, config_value, short_name, desc_txt, default_value, valid_values, category, add_release, version_ctrl_nbr, add_user_id, add_time, last_chg_user_id, last_chg_time, status_cd, status_time, admin_comment, system_usage, config_value_large)
      VALUES(N'ENV', N'UAT', N'RTR reporting database', N'Indicates scripts should be run against UAT rdb_modern database', NULL, N'UAT, PROD', N'RTR', N'7.12.0', 1, 0, getdate(), 0, getdate(), N'A', getdate(), NULL, NULL, NULL);
      ```

## Set up the rdb_modern database

If you are on the **rdb_modern path**, complete this section. If you are on the **RDB path**, move on to [Create service users and database objects](#create-service-users-and-database-objects). For more information on choosing a path, see Step 3 in the [Prerequisites](#prerequisites) section.

RTR requires a dedicated reporting database. To create `rdb_modern`, you restore a copy of `RDB` under a new name. This keeps the classic ETL-hydrated `RDB` intact and available while `rdb_modern` hosts the data structures the RTR pipeline requires.

> Full setup procedures for **SQL Server on Amazon EC2 and Azure SQL** deployments are not yet available in this guide. Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) for guidance.
{: .important }

### Enable Backup and Restore on Amazon RDS

If you host your NBS 6 database on Amazon RDS, verify that the ****Backup and Restore** option is enabled before proceeding. Complete the following steps to verify your current setup and enable the configuration if needed.

1. Sign in to the AWS Management Console and navigate to the **Aurora and RDS** service console.
1. Navigate to **Databases**, choose your SQL Server instance, and view the **Summary** and **Configuration** sections to find the **Engine** and **Engine version** values that you need in the next steps.
1. Select **Option groups** from the navigation sidebar and choose the option group attached to your DB instance.
1. Review the **Options** section and confirm that **SQLSERVER_BACKUP_RESTORE** is listed.
   - If it is listed, no action is needed. Proceed to [Enable ad hoc distributed queries](#enable-ad-hoc-distributed-queries).
   - If it is not listed, continue with the next steps to create a custom option group.
1. Navigate to **Option groups** and select **Create group**. Configure the following:
   - **Name:** Enter a descriptive name for your custom option group such as `sqlserver-backup-restore-se-15-00`.
   - **Engine:** Select the SQL Server engine edition that matches your DB instance.
   - **Major engine version:** Select the version that matches your DB instance.
1. Select **Create** to save the empty group.
1. Select your new option group from the list, choose **Add option**, and configure the following:
   - **Option name:** Select **SQLSERVER_BACKUP_RESTORE**.
   - **S3 bucket:** Select the S3 bucket where backups will be stored.
   - **IAM role:** Select or create an Amazon IAM role that has permission to access the S3 bucket you use for backups.
1. Select **Add option** to finish configuring the option group.
1. Navigate to **Databases** and select your SQL Server DB instance.
1. Select **Modify**.
1. In the **Additional configuration** section, locate the **Option group** field and select your new custom option group.
1. Select **Continue** and choose whether to apply the change immediately or during the next scheduled maintenance window. If your NBS 6 instance is running, applying immediately might cause a brief outage. Schedule the change during a maintenance window and notify users before proceeding.
1. Select **Modify DB instance** to confirm your changes.

### Enable ad hoc distributed queries

This parameter is required to enable Change Data Capture on Amazon RDS. Complete the following steps to verify your current setting and enable the parameter if needed.

1. Sign in to the AWS Management Console and navigate to the **Aurora and RDS** service console.
1. Navigate to **Databases**, choose your SQL Server instance, and view the **Summary** and **Configuration** sections to find the **Engine**, **Engine version**, and **DB instance parameter group** values that you need in the next steps.
1. Select **Parameter groups** from the navigation sidebar and choose the parameter group attached to your DB instance.
1. Search for the `ad hoc distributed queries` parameter and confirm it is set to `1`.
   - If the parameter is set to `1`, no action is needed. Proceed to [Back up and restore RDB on Amazon RDS](#back-up-and-restore-rdb-on-amazon-rds).
   - If the parameter is set to `0` and your instance uses a custom parameter group, update the value to `1`, select **Save changes**, and proceed to [Back up and restore RDB on Amazon RDS](#back-up-and-restore-rdb-on-amazon-rds).
   - If your instance uses the default parameter group, you cannot edit it directly. Continue with the next steps to create a custom parameter group.
1. Select **Create parameter group** and configure the following:
   - **Name:** Enter a descriptive name such as `enable-ad-hoc-distributed-queries`.
   - **Engine type:** Select the SQL Server engine edition that matches your DB instance.
   - **Parameter group family:** Select the engine and version that matches your DB instance.
1. Select **Create** to save the parameter group.
1. Open the new parameter group and select **Edit**.
1. Search for `ad hoc distributed queries` and set the value to `1`.
1. Navigate to **Databases** and select your SQL Server DB instance.
1. Select **Modify**.
1. In the **Additional configuration** section, locate the **Parameter group** field and select your new custom parameter group.
1. Select **Continue** and choose whether to apply the change immediately or during the next scheduled maintenance window. If your NBS 6 instance is running, applying immediately might cause a brief outage. Schedule the change during a maintenance window and notify users before proceeding.
1. Select **Modify DB instance** to confirm your changes.

### Back up and restore RDB on Amazon RDS

The following steps create a new database within an existing instance. Restoring `RDB` under a new name within the same instance requires the RDS backup and restore stored procedures. Note that the AWS Management Console snapshot restore functionality creates an entirely new DB instance and cannot be used for this purpose.

Use the following steps to perform a backup and restore of your NBS 6 database on Amazon RDS.

1. Open a SQL client and connect to your SQL Server instance.
1. Run the following procedure to back up `RDB` to Amazon S3:

   ```sql
   exec msdb.dbo.rds_backup_database
   @source_db_name='RDB',
   @s3_arn_to_backup_to='arn:aws:s3:::<s3-bucket-name>/<s3-path-prefix>/<rdb_backup_filename.bak>',
   @type='FULL'
   ```

   > Use the same filename for `<rdb_backup_filename.bak>` in both the backup and restore procedures. The restore procedure retrieves the file that the backup procedure wrote to Amazon S3.
   {: .note }

1. Run the following procedure to check the status:

   ```sql
   exec msdb.dbo.rds_task_status;
   ```

1. Run the following procedure to restore `RDB` as `rdb_modern`:

   ```sql
   exec msdb.dbo.rds_restore_database
   @restore_db_name='rdb_modern',
   @s3_arn_to_restore_from='arn:aws:s3:::<s3-bucket-name>/<s3-path-prefix>/<rdb_backup_filename.bak>',
   @type='FULL';
   ```

1. Run the following procedure to check the status:

   ```sql
   exec msdb.dbo.rds_task_status;
   ```

## Create service users and database objects

Complete the following steps to create the database users, Kubernetes secrets, and database objects that the RTR pipeline requires before [Change Data Capture](#enable-change-data-capture) can be enabled.

> Generate passwords for each service user before running the scripts. Password generation scripts can take several minutes to run. Do not use spaces, equal signs (`=`), or colons (`:`). These characters cause script execution failures.
{: .important }

1. **Create admin user.** Run [000-create_rtr_admin_user-001.sql][nedss-datareporting-onboarding-user-scripts] from the NEDSS-DataReporting onboarding user creation scripts. This user provides Liquibase permissions to maintain required database components for RTR and enable Change Data Capture. Review the script and update the `PASSWORD` value before execution.

1. **Create RTR microservice user logins.** Run [001-service_users_login_creation-001.sql and 002-service_database_user_creation-001.sql][nedss-datareporting-onboarding-user-scripts] from the same directory. These scripts create dedicated user accounts for each RTR microservice, which are referenced in Helm values for RTR services. Review the scripts and update the `PASSWORD` values before execution.

1. **Create Kubernetes secrets for each service user.** Include the admin user from step 1. Each secret should include the database username and password. Script location: [NEDSS-DataReporting/create-kubernetes-secrets][nedss-helm-k8-secrets-manifest]. For steps to create secrets, see [Create secrets in your cluster](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#create-secrets-in-your-cluster).

1. **Create required database objects.** Run the scripts for your chosen path:

   The database scripts referenced throughout this guide are maintained in the [NEDSS-DataReporting][nedss-datareporting-liquibase-service] repository. You can create the required database objects through Liquibase, which will automatically implement database schema changes, or you can use the provided scripts to install database schema changes. Both options are referenced in the relevant sections.
   {: .important }

   - **Liquibase:** See [Deploy Liquibase](../../deploy-nbs7/real-time-reporting/liquibase.html) to create all necessary objects, then return here to continue. Liquibase also handles future database upgrades automatically, so no manual intervention is needed when you update NBS 7.

   - **Upgrade scripts:** See the script execution sequence and `db_upgrade` script in [NEDSS-DataReporting/db-upgrade][nedss-datareporting-manual-deployment]. Clone or download the repository, then run:

      ```bash
      upgrade_db.bat <server_name> <database> <username> <password>
      ```

      When you update NBS 7 to a new release version, you will need to run the upgrade scripts again. See [After onboarding: database upgrades](#after-onboarding-database-upgrades).

## Enable Change Data Capture

Change Data Capture (CDC) streams row-level changes from `NBS_ODSE` and `NBS_SRTE` to Kafka, where RTR services load them into the reporting database. Complete the following steps to load the initial data, enable Change Data Capture, and verify the configuration before deploying RTR services.

1. **Load data and enable Change Data Capture.** This one-time step is required after all database objects are created.

   - **Liquibase:** The `--load-data` flag is not required when using Liquibase. Proceed to step 2.

   - **Upgrade scripts:** Navigate to [02_onboarding_script_data_load][nedss-datareporting-onboarding-data-load] and clone or download the repository, then run:

      ```bash
      upgrade_db.bat --load-data <server_name> master <username> <password>  
      ```

1. **Verify Change Data Capture.** `is_cdc_enabled=1` indicates successful configuration.

   > In the following statements, `cdc` appears as part of SQL Server column and parameter names and refers to **Change Data Capture**, not the Centers for Disease Control and Prevention.
   {: .note }

   ```sql
   SELECT name, is_cdc_enabled
   FROM sys.databases;

   -- View ODSE tables with Change Data Capture enabled
   USE NBS_ODSE;
   SELECT
     name,
     CASE WHEN is_tracked_by_cdc = 1 THEN 'YES' ELSE 'NO' END AS is_tracked_by_cdc
   FROM sys.tables
   WHERE is_tracked_by_cdc = 1;

   -- View SRTE tables with Change Data Capture enabled
   USE NBS_SRTE;
   SELECT
     name,
     CASE WHEN is_tracked_by_cdc = 1 THEN 'YES' ELSE 'NO' END AS is_tracked_by_cdc
   FROM sys.tables
   WHERE is_tracked_by_cdc = 1;
   ```

   The following images show expected query results for a successful Change Data Capture configuration.

   <div style="display: flex; gap: 2rem;">
     <figure>
       <figcaption><strong>Change Data Capture tables (NBS_ODSE)</strong></figcaption>
       <img src="images/cdc_enabled_odse_tables.png" alt="Query results showing 19 Change Data Capture enabled tables in NBS_ODSE, all with is_tracked_by_cdc set to YES">
     </figure>
     <figure>
       <figcaption><strong>Change Data Capture tables (NBS_SRTE)</strong></figcaption>
       <img src="images/cdc_enabled_srte_tables.png" alt="Query results showing 44 Change Data Capture enabled tables in NBS_SRTE, all with is_tracked_by_cdc set to YES">
     </figure>
   </div>

1. **Back up all databases.** Before going live, take backups of `NBS_ODSE`, `NBS_SRTE`, `RDB`, and `rdb_modern` (if applicable).

## Deploy RTR services

Now that you have completed database setup and onboarding, deploy the RTR services in the following order. Each service depends on the previous one completing successfully before deployment begins.

> Confirm that Kubernetes secrets exist for each RTR service user and the admin user before deploying. If you have not yet created them, see [Create service users and database objects](#create-service-users-and-database-objects).
{: .important }

1. [Liquibase](../../deploy-nbs7/real-time-reporting/liquibase.html): Skip this step if you used the upgrade script path in [Create required database objects](#create-service-users-and-database-objects).
1. [Debezium](../../deploy-nbs7/real-time-reporting/debezium.html)
1. [Kafka connector](../../deploy-nbs7/real-time-reporting/kafka-connector.html)
1. [Java services](../../deploy-nbs7/real-time-reporting/rtr-java-services.html)

[nedss-datareporting-liquibase-service]: <https://github.com/CDCgov/NEDSS-DataReporting/tree/{{ site.version_latest_tag }}/liquibase-service>
[nedss-datareporting-onboarding-user-scripts]: <https://github.com/CDCgov/NEDSS-DataReporting/tree/{{ site.version_latest_tag }}/liquibase-service/src/main/resources/db/001-master/01_onboarding_scripts_user_creation>
[nedss-helm-k8-secrets-manifest]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/k8-manifests/nbs-secrets.yaml>
[nedss-datareporting-manual-deployment]: <https://github.com/CDCgov/NEDSS-DataReporting/tree/{{ site.version_latest_tag }}/liquibase-service/src/main/resources/stlt/manual_deployment>
[nedss-datareporting-onboarding-data-load]: <https://github.com/CDCgov/NEDSS-DataReporting/tree/{{ site.version_latest_tag }}/liquibase-service/src/main/resources/db/001-master/02_onboarding_script_data_load>

---

## After onboarding: database upgrades

Database upgrades apply schema changes required by each NBS 7 release. Run database upgrades when you update NBS 7 to a new release version.

- If you chose the **Liquibase** path during onboarding, no action is needed. The Liquibase container applies schema changes automatically with each release.
- If you chose the **upgrade scripts** path, navigate to [02_onboarding_script_data_load][nedss-datareporting-onboarding-data-load] and run all of the scripts in the order listed in the repository. Onboarding scripts are excluded from upgrade runs.
