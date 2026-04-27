---
title: Liquibase
layout: page
parent: Real-time reporting (preview)
nav_order: 1
redirect_from:
  - /docs/7_feature_preview/1_liquibase.html
  - /docs/7_feature_preview/1_liquibase/
---

# Deploy Liquibase for real-time reporting (RTR)

In RTR deployments, the Liquibase job runs once and applies required SQL Server database changes for onboarding and upgrades. This page covers steps to deploy the Liquibase Helm chart.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Installing Liquibase

Follow these steps to configure and deploy the Liquibase Helm chart for RTR.

> Verify that you are connected to the correct Kubernetes cluster before proceeding. To confirm, run `kubectl config current-context`.
{: .important }

1. Locate the Liquibase Helm chart in the [NEDSS-Helm repository](https://github.com/CDCgov/NEDSS-Helm/tree/main/charts/liquibase).
1. Configure `values.yaml`. Replace all placeholder values before installation:

   Replace `app.EXAMPLE_DOMAIN` with the URL of your modern app (see [Deploy NGINX ingress controller](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-nginx-ingress-controller-on-your-cluster)):

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/liquibase-service"
     tag: <release-version-tag>  # Example: v1.0.1
   ```

   Replace `EXAMPLE_DB_ENDPOINT` with your SQL Server endpoint and set credentials.
   For `username`, use `db_deploy_admin`. <!-- [SME REVIEW: confirm db_deploy_admin is correct for all environments] -->

   To retrieve your Kafka bootstrap server endpoints, see [Get bootstrap brokers](https://docs.aws.amazon.com/msk/latest/developerguide/msk-get-bootstrap-brokers.html) in the AWS MSK documentation.

   The following fields define the JDBC connection strings for each NBS database. Each URL
   identifies the SQL Server endpoint, the database name, and the connection security settings.

    ```yaml
    jdbc:
       # SQL Server system database
       master_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=master;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
       # NBS transactional database
       odse_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=nbs_odse;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
       # NBS reference and terminology database
       srte_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=nbs_srte;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
       # Legacy reporting database (RDB path)
       rdb_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=rdb;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
       # Separate reporting database (rdb_modern path only)
       rdb_modern_db_url: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=rdb_modern;integratedSecurity=false;encrypt=true;trustServerCertificate=true"
       # db_deploy_admin user created in prerequisites
       username: "EXAMPLE_DB_USER"
       password: "EXAMPLE_DB_USER_PASSWORD"
       # Separate credentials for NBS_SRTE if applicable
       srte_username: "EXAMPLE_SRTE_DB_USER"
       srte_password: "EXAMPLE_SRTE_DB_USER_PASSWORD"
    ```

1. Install the pod:

   ```bash
   helm install -f ./liquibase/values.yaml liquibase ./liquibase/
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

1. Validate Liquibase updates from NBS databases using the `DATABASECHANGELOG` table:

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

If validation fails or returns unexpected results, see [Troubleshooting Liquibase installation](#troubleshooting-liquibase-installation).

> If you arrived here from [Create service users and database objects](../real-time-reporting/#create-service-users-and-database-objects), return there to continue after Liquibase completes successfully.
{: .note }

## Troubleshooting Liquibase installation

Troubleshooting can vary by database. If issues persist after initial troubleshooting, contact support at <mailto:nbs@cdc.gov>.

### User permission errors

If a Liquibase execution fails due to a user permission error, run the following script:

```sql
USE [NBS_SRTE]
GO
ALTER USER [nbs_ods] WITH DEFAULT_SCHEMA=[dbo]
GO
USE [NBS_SRTE]
GO
ALTER ROLE [db_owner] ADD MEMBER [nbs_ods]
```

### Migration errors

If you see `Migration failed` or `Invalid object name` errors, run the following script:

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

### Incomplete migration

If the expected values are not returned for the `NBS_ODSE`, `RDB`, `NBS_SRTE` or `rdb_modern` database and the update is incomplete, clear the `DATABASECHANGELOG` table. Then rerun Liquibase:

```sql
USE NBS_ODSE;
DELETE FROM NBS_ODSE.dbo.DATABASECHANGELOG;

USE NBS_SRTE;
DELETE FROM NBS_SRTE.dbo.DATABASECHANGELOG;

USE RDB;
DELETE FROM RDB.dbo.DATABASECHANGELOG;

USE rdb_modern;
DELETE FROM rdb_modern.dbo.DATABASECHANGELOG;
```
