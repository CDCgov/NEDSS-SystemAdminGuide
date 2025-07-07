---
title: Liquibase
layout: page
parent: Real Time Reporting (Preview)
nav_order: 1
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Liquibase Deployment
The liquibase job runs once and goes to sleep. The job will update necessary SQL Server scripts for Real Time Reporting.

1. The helm chart for Liquibase should be available under charts/liquibase.
2. In the values.yaml, replace all occurrences of app.EXAMPLE_DOMAIN with the URL of your modern app as shown in [Table](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/1_nginx_ingress_deployment.html#deploy-nginx-ingress-controller-on-the-kubernetes-cluster).
   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/liquibase-service"
     tag: <release-version-tag> e.g v1.0.1
   ```
4. Validate image repository and tag:
   ```yaml
   jdbc:
     master_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT.nbspreview.com:1433;databaseName=master;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
     srte_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=nbs_srte;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
     odse_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT.nbspreview.com:1433;databaseName=nbs_odse;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
     rdb_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT.nbspreview.com:1433;databaseName=rdb;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
     rdb_modern_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT.nbspreview.com:1433;databaseName=rdb_modern;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
     username: ""
     password: ""
     srte_username: ""
     srte_password: ""
   odse:
      bname: "NBS_ODSE"
   rdb:
     dbname: "rdb_modern"
   ```
5. Update the values.yaml files and run the command to run the Liquibase. Configurations for the following should be on hand to update the values.yaml
   
6. Install pod
   ```bash
   helm install -f ./liquibase/values.yaml liquibase ./liquibase/
   ```
7. Verify if pod is running
   ```bash
   kubectl get pods
   ```
8. Validate liquibase update from NBS databases using the DATABASECHANGELOG table:
    ```sql
    USE NBS_ODSE;
    --The query should return 34 rows. If there are fewer rows, please check step 8.
    SELECT COUNT(*) 
    FROM NBS_ODSE.DBO.DATABASECHANGELOG;
    
    USE RDB;
    --The query should return 2 rows. If there are fewer rows, please check step 8.
    SELECT COUNT(*)
    FROM RDB.DBO.DATABASECHANGELOG;  
    
    USE NBS_SRTE;
    --The query should return 3 rows. If there are fewer rows, please check step 8.
    SELECT COUNT(*)
    FROM NBS_SRTE.DBO.DATABASECHANGELOG;  
    
    USE RDB_MODERN;
    --The query should return 330 rows. If there are fewer rows, please check step 8.
    SELECT COUNT(*)
    FROM RDB_MODERN.DBO.DATABASECHANGELOG;
    ```
9. Provide permissions for Real Time Reporting microservice user logins after successful execution of liquibase. Please run the following scripts to provide permissions.
   - [Organization service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/002-create_organization_service_user.sql)
   - [Observation service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/003-create_observation_service_user.sql)
   - [Person service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/004-create_person_service_user.sql)
   - [Investigation service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/005-create_investigation_service_user.sql)
   - [LDF service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/006-create_ldf_service_user.sql)
   - [Postprocessing service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/007-create_post_processing_service_user.sql)
   - [Kafka sync connector](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/008-create_kafka_sync_connector_service_user.sql)
   - [Debezium service user](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/db/upgrade/master/routines/009-create_debezium_service_user.sql)
10. Execute data load scripts: For the initial setup of Real Time Reporting, please run these integration scripts ([NEDSS-DataReporting/data-load](https://github.com/CDCgov/NEDSS-DataReporting/tree/main/liquibase-service/src/main/resources/db/rdb_modern/data_load)) to migrate key-uid mapping into key generation tables.
11. Troubleshooting for Liquibase: Please note, troubleshooting for Liquibase may vary depending on the database. If the issue persist after the initial troubleshooting, please reach out to our support team.
    - a. If NBS_SRTE or any liquibase execution fails due to user permission issue. Run this script:
        ```sql
        USE [NBS_SRTE]
        GO
        ALTER USER [nbs_ods] WITH DEFAULT_SCHEMA=[dbo]
        GO
        USE [NBS_SRTE]
        GO
        ALTER ROLE [db_owner] ADD MEMBER [nbs_ods]
        GO
        ```
    - b. If you see “Migration failed” or “Invalid object name” errors while running liquibase. please run the following script:
        ```sql
        Use rdb_modern;
        IF NOT EXISTS (SELECT 1 FROM sysobjects WHERE name = 'nrt_odse_Page_cond_mapping' and xtype = 'U')
           BEGIN
                CREATE TABLE [dbo].[nrt_odse_Page_cond_mapping] (
                    [page_cond_mapping_uid] [bigint] NOT NULL,
                    [wa_template_uid] [bigint] NOT NULL,
                    [condition_cd] [varchar](20) NOT NULL,
                    [add_time] [datetime] NOT NULL,
                    [add_user_id] [bigint] NOT NULL,
                    [last_chg_time] [datetime] NOT NULL,
                    [last_chg_user_id] [bigint] NOT NULL,
                    CONSTRAINT [PK_nrt_odse_Page_cond_mapping] PRIMARY KEY CLUSTERED (
                        [page_cond_mapping_uid] ASC
                    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
                ) ON [PRIMARY];
            END;

        USE RDB_MODERN;
        IF NOT EXISTS (SELECT 1 FROM sysobjects WHERE name = 'nrt_odse_NBS_page' and xtype = 'U')
           BEGIN
                CREATE TABLE [dbo].[nrt_odse_NBS_page] (
                    [nbs_page_uid] [bigint] NOT NULL,
                    [wa_template_uid] [bigint] NOT NULL,
                    [form_cd] [varchar](50) NULL,
                    [desc_txt] [varchar](2000) NULL,
                    [jsp_payload] [image] NULL,
                    [datamart_nm] [varchar](21) NULL,
                    [local_id] [varchar](50) NULL,
                    [bus_obj_type] [varchar](50) NOT NULL,
                    [last_chg_user_id] [bigint] NOT NULL,
                    [last_chg_time] [datetime] NOT NULL,
                    [record_status_cd] [varchar](20) NOT NULL,
                    [record_status_time] [datetime] NOT NULL,
                    CONSTRAINT [PK_nrt_odse_NBS_page] PRIMARY KEY CLUSTERED (
                        [nbs_page_uid] ASC
                    )
                    WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
                ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY];
           END;

        USE RDB_MODERN;
        IF NOT EXISTS (SELECT 1 FROM sysobjects WHERE name = 'nrt_odse_NBS_rdb_metadata' and xtype = 'U')
           BEGIN
                CREATE TABLE [dbo].[nrt_odse_NBS_rdb_metadata] (
                    [nbs_rdb_metadata_uid] [bigint] NOT NULL,
                    [nbs_page_uid] [bigint] NULL,
                    [nbs_ui_metadata_uid] [bigint] NOT NULL,
                    [rdb_table_nm] [varchar](30) NULL,
                    [user_defined_column_nm] [varchar](30) NULL,
                    [record_status_cd] [varchar](20) NOT NULL,
                    [record_status_time] [datetime] NOT NULL,
                    [last_chg_user_id] [bigint] NOT NULL,
                    [last_chg_time] [datetime] NOT NULL,
                    [local_id] [varchar](50) NULL,
                    [rpt_admin_column_nm] [varchar](50) NULL,
                    [rdb_column_nm] [varchar](30) NULL,
                    [block_pivot_nbr] [int] NULL,
                    CONSTRAINT [PK_nrt_odse_NBS_rdb_metadata] PRIMARY KEY CLUSTERED (
                        [nbs_rdb_metadata_uid] ASC
                    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
                ) ON [PRIMARY];

                CREATE NONCLUSTERED INDEX [RDB_PERF_RDB_TBL_NM] ON [dbo].[nrt_odse_NBS_rdb_metadata] (
                    [rdb_table_nm] ASC
                )
                INCLUDE (
                    [nbs_ui_metadata_uid],
                    [rdb_column_nm]
                ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
                ON [PRIMARY];

                CREATE NONCLUSTERED INDEX [RDB_PERF_UID_RDB_TBL_NM] ON [dbo].[nrt_odse_NBS_rdb_metadata] (
                    [nbs_ui_metadata_uid] ASC,
                    [rdb_table_nm] ASC
                )
                INCLUDE (
                    [rdb_column_nm]
                ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
                ON [PRIMARY];

                CREATE NONCLUSTERED INDEX [RDB_PERF_UID] ON [dbo].[nrt_odse_NBS_rdb_metadata](
                    [nbs_ui_metadata_uid] ASC
                )
                INCLUDE (
                    [rdb_column_nm]
                ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
                ON [PRIMARY];

           END;
        
        ```
    - c. NBS_ODSE, RDB, NBS_SRTE  and rdb_modern: If the expected values are not returned and the update is incomplete, the DATABASECHANGELOG should be cleared out (query below) and Liquibase should be rerun.
        ```sql
        USE NBS_ODSE;
        DELETE FROM NBS_ODSE.dbo.DATABASECHANGELOG;
        
        USE NBS_SRTE;
        DELETE FROM NBS_ODSE.dbo.DATABASECHANGELOG;
        
        USE RDB;
        DELETE FROM RDB.dbo.DATABASECHANGELOG;
        	
        USE rdb_modern;
        DELETE FROM rdb_modern.dbo.DATABASECHANGELOG;
        ```
