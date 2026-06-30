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
{: .note }

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

1. Choose a database path and use it consistently throughout this guide.

   - **RDB path:** Use `RDB` as the default reporting database. Turn off the classic ETL batch jobs and proceed to the next step. MasterETL remains available for manual recovery runs if needed.
   - **rdb_modern path:** Create a separate reporting database by duplicating your existing reporting database. The exact steps depend on your SQL Server version and where it is hosted. If this process is unfamiliar, see [Microsoft's documentation on backup and restore operations](https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases?view=sql-server-ver17) before moving on to [Create service users and secrets](#create-service-users-and-secrets).

## Set up the rdb_modern database (rdb_modern path only)

If you are on the **rdb_modern path**, complete this section. If you are on the **RDB path**, move on to [Create service users and secrets](#create-service-users-and-secrets). For more information on choosing a path, see Step 3 in the [Prerequisites](#prerequisites) section.

RTR requires a dedicated reporting database. To create `rdb_modern`, you restore a copy of `RDB` under a new name. This keeps the classic ETL-hydrated `RDB` intact and available while `rdb_modern` hosts the data structures the RTR pipeline requires.

## Create service users and secrets

Complete the following steps to create the database users, Kubernetes secrets, and database objects that the RTR pipeline requires before [Change Data Capture](#enable-change-data-capture) can be enabled.

Running the RTR pipeline requires SQL Server login accounts for two distinct purposes: running the bootstrap scripts and schema migrations, and running the application services. Depending on your environment, these can be two separate accounts or collapsed into one.

### Accounts at a Glance

| Account | Purpose | Databases | Key Permissions |
| :--- | :--- | :--- | :--- |
| **Admin account** (e.g. `rtr-admin`) | Liquibase migrations | `NBS_ODSE`, `NBS_SRTE`, `RDB / RDB_MODERN`  | All NBS DBs: `db_owner` |
| **Service account** (e.g. `rtr-service-user`) | Application services reading source data and writing to the reporting database | `NBS_ODSE`, `NBS_SRTE`, `RDB / RDB_MODERN` | ODSE/SRTE: `db_datareader`<br>RDB/RDB_MODERN: `db_owner` |

Two accounts cover everything: `rtr-admin` handles migrations, `rtr-service-user` runs the application. A single account with both sets of permissions also works if your environment doesn't require separation.

1. **Create Kubernetes secrets for each sql user.** Each secret should include the database username and password. Script location: [NEDSS-DataReporting/create-kubernetes-secrets][nedss-helm-k8-secrets-manifest]. For steps to create secrets, see [Create secrets in your cluster](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#create-secrets-in-your-cluster).

## Enable Change Data Capture

Change Data Capture (CDC) streams row-level changes from `NBS_ODSE` and `NBS_SRTE` to Kafka, where RTR services load them into the reporting database. Enabling CDC on these databases does require `sysadmin` level permissions, because of this, we have not automated its installation and have instead provided two scripts to manually apply.  For more information on SQL Server Change Data Capture, please review [Microsoft's official documentation](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/enable-and-disable-change-data-capture-sql-server?view=sql-server-ver17).

1. Apply bootstrap script [101 to enable CDC on NBS_ODSE](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/bootstrap/101-enable_cdc_on_odse_database-001.sql).

1. Apply bootstrap script [102 to enable CDC on NBS_SRTE](https://github.com/CDCgov/NEDSS-DataReporting/blob/main/bootstrap/102-enable_cdc_on_srte_database-001.sql).

## Deploy RTR services

Now that you have completed database setup and onboarding, deploy the RTR services in the following order. Some services depend on the previous ones completing successfully before deployment begins.

> Confirm that Kubernetes secrets exist for each RTR service user and the admin user before deploying.
{: .important }

1. [Debezium](../../deploy-nbs7/real-time-reporting/debezium.html)
1. [Kafka connector](../../deploy-nbs7/real-time-reporting/kafka-connector.html)
1. [Java service](../../deploy-nbs7/real-time-reporting/rtr-java-services.html)

[nedss-helm-k8-secrets-manifest]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/k8-manifests/nbs-secrets.yaml>

---
