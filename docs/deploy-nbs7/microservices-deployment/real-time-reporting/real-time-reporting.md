---
title: Deploy real-time reporting
layout: page
parent: Deploy NBS 7 microservices
nav_order: 10
has_children: true
has_toc: false
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
  - /docs/deploy-nbs7/real-time-reporting/real-time-reporting.html
  - /docs/deploy-nbs7/real-time-reporting/
  - /docs/deploy-nbs7/real-time-reporting/liquibase.html
  - /docs/deploy-nbs7/real-time-reporting/liquibase/
  - /docs/deploy-nbs7/real-time-reporting/data-compare-tool.html
  - /docs/deploy-nbs7/real-time-reporting/data-compare-tool/
---

# Deploy real-time reporting (RTR)

Real-time reporting (RTR) is an NBS 7 capability that reduces reporting latency from as long as 24 hours to between 5 minutes and 1 hour. RTR uses [Change Data Capture](#enable-change-data-capture) to detect row-level changes in source tables, publishes those changes to Kafka topics, and loads the data into the reporting database. This section covers steps to install RTR with Helm charts.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> Complete the sections on this page in order. Each section depends on the previous one. If you encounter issues during database setup, contact support at [nbs@cdc.gov](mailto:nbs@cdc.gov).
{: .note }

## Prerequisites

Before you begin, verify that your environment meets the following requirements and choose a database installation method. The method you choose applies throughout this guide.

> To reduce risk, consider setting up RTR in a testing environment before moving to production. This lets you run RTR alongside MasterETL and compare results, then turn off MasterETL only after you are satisfied with those results.
{: .important }

1. RTR installation requires a supported NBS 6 version. See the [Supported NBS versions](../../../supported-versions.html) page. To verify your NBS release version, run the following query:

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

   - **Use your existing RDB database:** RTR takes over writing to `RDB`. Turn off the classic ETL batch jobs and proceed to the next step. MasterETL remains available for manual recovery runs if needed.

   - **Create a new reporting database (suggested):** Duplicate your existing `RDB`. This lets you run RTR alongside MasterETL to compare results before fully committing. You can use any name for this reporting database, but for the remainder of this guide, we refer to it as `RDB_MODERN`. The exact steps for database duplication depend on your SQL Server version and hosting environment. If your database is on Amazon RDS, see [Back up and restore on Amazon RDS](../../../maintain-nbs7/rds-backup-restore.html). For other environments, see [Microsoft's documentation on backup and restore operations](https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases?view=sql-server-ver17).

   > If you use a new reporting database, you must use the new reporting execution server to run reports.
   {: .note }

## Create service user

Create a database service user that the RTR services use to read source data and write to the reporting database:

1. **Name:** Any name works. A name descriptive of the role, such as `rtr-service-user`, is suggested.
1. **Database permissions:**

   - `NBS_ODSE`: `db_datareader`
   - `NBS_SRTE`: `db_datareader`
   - `RDB` / `RDB_MODERN`: `db_owner`

## Enable Change Data Capture

> In this section, the terms `cdc` and `CDC` appear as part of SQL Server column and parameter names and refer to Change Data Capture, not the Centers for Disease Control and Prevention.
{: .note }

[Change Data Capture](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server?view=sql-server-ver17) (CDC) streams row-level changes from `NBS_ODSE` and `NBS_SRTE` to Kafka, where RTR services load them into the reporting database.

To enable CDC on `NBS_ODSE` and `NBS_SRTE`:

1. Using a `sysadmin` account, apply [Bootstrap script 101][nedss-datareporting-bootstrap-101]. CDC requires `sysadmin` permissions.

## Deploy RTR services

Now that you have completed database setup and onboarding, deploy the RTR services. Some services depend on the previous ones completing successfully, so complete the pages in the following order:

1. [Debezium](debezium.html)
1. [Kafka connector](kafka-connector.html)
1. [Java service](rtr-java-services.html)

[nedss-datareporting-bootstrap-101]: <https://github.com/CDCgov/NEDSS-DataReporting/blob/{{ site.version_latest_tag }}/bootstrap/101-enable_cdc_on_odse_srte_databases-001.sql>
