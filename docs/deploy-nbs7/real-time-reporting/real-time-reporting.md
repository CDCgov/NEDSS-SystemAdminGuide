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

1. Run the ETL jobs one final time and make sure they complete successfully.
   - `PHCMartETL.bat`
   - `MasterETL.bat`
   - `covid19ETL.bat`

1. Choose a reporting database. RTR can write to your existing `RDB` database, or to a new database you create by duplicating `RDB`. Pick one option and use it consistently throughout this guide.

   > Back up the `RDB` database before you proceed. This step cannot be undone.
   {: .warning }

   - **Use your existing RDB database** — RTR takes over writing to `RDB`. Turn off the classic ETL batch jobs and proceed to the next step. MasterETL remains available for manual recovery runs if needed.

   - **Create a new reporting database** (recommended) — Duplicate your existing `RDB`, this lets you run RTR alongside MasterETL to compare results before fully committing.  You can use any name for this reporting database, but for the remainder of this guide, we'll refer to it as `RDB_MODERN`.  The exact steps for database duplication depend on your SQL Server version and hosting environment.  If this process is unfamiliar, see [Microsoft's documentation on backup and restore operations](https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases?view=sql-server-ver17).

   > If using a new reporting database, you must use the new reporting execution server to run reports (TODO: add link)
   {: .note }

## Create service user

Complete the following steps to create the database user that the RTR requires.

Running RTR requires a SQL Server login account for two distinct purposes: configuring the database and running the application services.

### Account Permissions

1. **Name**: Any name works, but we recommend using a name descriptive to the role, such as `rtr-service-user`.
1. **Purpose**: The application services reading source database and writing to the reporting database.
1. **Databases Permissions**:
  - `NBS_ODSE`: `db_datareader`
  - `NBS_SRTE`: `db_datareader`
  - `RDB` / `RDB_MODERN`: `db_owner`

## Enable Change Data Capture

Change Data Capture (CDC) streams row-level changes from `NBS_ODSE` and `NBS_SRTE` to Kafka, where RTR services load them into the reporting database. Enabling CDC on these databases does require `sysadmin` level permissions, so be sure to run the bootstrap script with a `sysadmin`account.  For more information on SQL Server Change Data Capture, please review [Microsoft's official documentation](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/enable-and-disable-change-data-capture-sql-server?view=sql-server-ver17).

1. Apply bootstrap script [101 to enable CDC on NBS_ODSE and NBS_SRTE](https://github.com/CDCgov/NEDSS-DataReporting/blob/v7.13/bootstrap/101-enable_cdc_on_odse_srte_databases-001.sql).

## Deploy RTR services

Now that you have completed database setup and onboarding, deploy the RTR services in the following order. Some services depend on the previous ones completing successfully before deployment begins.

1. [Debezium](../../deploy-nbs7/real-time-reporting/debezium.html)
1. [Kafka connector](../../deploy-nbs7/real-time-reporting/kafka-connector.html)
1. [Java service](../../deploy-nbs7/real-time-reporting/rtr-java-services.html)

---
