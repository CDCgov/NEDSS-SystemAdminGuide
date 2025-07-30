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
3. Validate image repository and tag:
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
4. Update the values.yaml files and run the command to run the Liquibase. Configurations for the following should be on hand to update the values.yaml
   
5. Install pod
   ```bash
   helm install -f ./liquibase/values.yaml liquibase ./liquibase/
   ```
6. Verify if pod is running
   ```bash
   kubectl get pods
   ```
   
7. Validate liquibase update from NBS databases using the DATABASECHANGELOG table:
   
    ```sql
    --Last script executed should be 999-<database_name>_database_object_permission_grants-001.sql.
    USE NBS_ODSE;
    SELECT TOP 1 *
    FROM NBS_ODSE.DBO.DATABASECHANGELOG
    ORDER BY DATEEXECUTED DESC;
    
    USE NBS_SRTE;
    SELECT TOP 1 *
    FROM NBS_SRTE.DBO.DATABASECHANGELOG
    ORDER BY DATEEXECUTED DESC;
    
    USE RDB;
    SELECT TOP 1 *
    FROM RDB.DBO.DATABASECHANGELOG
    ORDER BY DATEEXECUTED DESC;
    
    USE RDB_MODERN;
    SELECT TOP 1 *
    FROM RDB_MODERN.DBO.DATABASECHANGELOG
    ORDER BY DATEEXECUTED DESC;
    ```
8. Troubleshooting for Liquibase: Please note, troubleshooting for Liquibase may vary depending on the database. If the issue persist after the initial troubleshooting, please reach out to our support team.
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
