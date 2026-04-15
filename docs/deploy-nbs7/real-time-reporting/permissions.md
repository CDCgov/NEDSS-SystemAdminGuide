---
title: Service permissions
layout: page
parent: Real-time reporting (preview)
nav_order: 5
description: Reference matrix for real-time reporting service roles and required database permissions.
---

# RTR service permissions

This page provides a reference matrix for real-time reporting roles and required permissions.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## User permissions by service

Each RTR microservice connects to one or more NBS databases using a dedicated SQL login. The following tables list required permissions grouped by service.

Jump to service:

- [Liquibase service](#liquibase)
- [Organization service](#organization)
- [Observation service](#observation)
- [Person service](#person)
- [Investigation service](#investigation)
- [LDF service](#ldf)
- [Post Processing service](#post-processing)
- [Kafka Sync service](#kafka-sync)
- [Debezium service](#debezium)

### Liquibase

Liquibase requires elevated permissions during initial onboarding to create service users and enable Change Data Capture (CDC). After onboarding is complete, Liquibase continues to run migration scripts with the same login.

| Database | Permissions | SQL Login |
|---|---|---|
| `master` | `setupadmin`, `processadmin`, `ALTER ANY CREDENTIAL`, `ALTER ANY LOGIN`, `CREATE ANY DATABASE`, `VIEW SERVER STATE`<br>**AWS RDS only:** `SELECT` on `msdb.dbo.sysjobs`, `EXECUTE` on `msdb.dbo.rds_cdc_enable_db`, `EXECUTE` on `msdb.dbo.rds_cdc_disable_db`<br>**On-premises or Azure only:** `ALTER SERVER ROLE`, `EXECUTE` on `sys.sp_cdc_enable_db`, `EXECUTE` on `sys.sp_cdc_disable_db` | `db_deploy_admin` |
| `NBS_ODSE` | `db_owner` | `db_deploy_admin` |
| `NBS_SRTE` | `db_owner` | `db_deploy_admin` |
| `NBS_MSGOUTE` | `db_owner` | `db_deploy_admin` |
| `RDB` | `db_owner` | `db_deploy_admin` |
| `rdb_modern` | `db_owner` | `db_deploy_admin` |

### Organization

The Organization service queries organization data and related context from `NBS_ODSE` and writes it to the Kafka broker.

| Database | Permissions | SQL Login |
|---|---|---|
| `NBS_ODSE` | `db_datareader`, `EXECUTE sp_organization_event`, `EXECUTE sp_place_event` | `organization_service_rdb` |
| `NBS_SRTE` | `db_datareader` | `organization_service_rdb` |
| `RDB` | `public`, `INSERT` on `job_flow_log` | `organization_service_rdb` |
| `rdb_modern` | `public`, `INSERT` on `job_flow_log` | `organization_service_rdb` |

### Observation

The Observation service queries observation data and related context from `NBS_ODSE` and writes it to the Kafka broker.

| Database | Permissions | SQL Login |
|---|---|---|
| `NBS_ODSE` | `db_datareader`, `EXECUTE sp_observation_event` | `observation_service_rdb` |
| `NBS_SRTE` | `db_datareader` | `observation_service_rdb` |
| `RDB` | `public`, `INSERT` on `job_flow_log` | `observation_service_rdb` |
| `rdb_modern` | `public`, `INSERT` on `job_flow_log` | `observation_service_rdb` |

### Person

The Person service queries person data and related context from `NBS_ODSE` and writes it to the Kafka broker.

| Database | Permissions | SQL Login |
|---|---|---|
| `NBS_ODSE` | `db_datareader`, `EXECUTE sp_patient_event`, `EXECUTE sp_patient_race_event`, `EXECUTE sp_provider_event`, `EXECUTE sp_auth_user_event` | `person_service_rdb` |
| `NBS_SRTE` | `db_datareader` | `person_service_rdb` |
| `RDB` | `public`, `INSERT` on `job_flow_log` | `person_service_rdb` |
| `rdb_modern` | `public`, `INSERT` on `job_flow_log` | `person_service_rdb` |

### Investigation

The Investigation service queries case data and related context from `NBS_ODSE` and writes it to the Kafka broker. It also updates `publichealthcasefact` datamart tables, which was previously performed by the `PHCmartETL.bat` job.

| Database | Permissions | SQL Login |
|---|---|---|
| `NBS_ODSE` | `db_datareader`, `db_datawriter` | `investigation_service_rdb` |
| `NBS_SRTE` | `db_datareader` | `investigation_service_rdb` |
| `RDB` | `db_datareader`, `db_datawriter` | `investigation_service_rdb` |
| `rdb_modern` | `db_datareader`, `db_datawriter` | `investigation_service_rdb` |

### LDF

The LDF service queries locally defined field (LDF) data and related context from `NBS_ODSE` and writes it to the Kafka broker.

| Database | Permissions | SQL Login |
|---|---|---|
| `NBS_ODSE` | `db_datareader`, `EXECUTE sp_ldf_data_event`, `EXECUTE sp_ldf_patient_event`, `EXECUTE sp_ldf_provider_event`, `EXECUTE sp_ldf_organization_event`, `EXECUTE sp_ldf_observation_event`, `EXECUTE sp_ldf_phc_event`, `EXECUTE sp_ldf_intervention_event` | `ldf_service_rdb` |
| `NBS_SRTE` | `db_datareader` | `ldf_service_rdb` |
| `RDB` | `public`, `INSERT` on `job_flow_log` | `ldf_service_rdb` |
| `rdb_modern` | `db_datareader`, `INSERT` on `job_flow_log` | `ldf_service_rdb` |

### Post Processing

The Post Processing service listens for completion events from upstream RTR services and executes stored procedures to update fact, dimension, and datamart tables with data from the `nrt` staging tables. It requires access to either `RDB` or `rdb_modern` depending on your deployment stage. Use `RDB` if you are live with RTR, or `rdb_modern` if you are evaluating or testing RTR deployment.

| Database | Permissions | SQL Login |
|---|---|---|
| `NBS_ODSE` | `db_datareader` | `post_processing_service_rdb` |
| `NBS_SRTE` | `db_datareader` | `post_processing_service_rdb` |
| `RDB` (production RTR only) | `db_owner` | `post_processing_service_rdb` |
| `rdb_modern` (dev RTR only) | `db_owner` | `post_processing_service_rdb` |

### Kafka Sync

The Kafka Sync service stores data received from RTR services into `nrt` staging tables, similar to the staging table concept in MasterETL. It requires access to either `RDB` or `rdb_modern` depending on your deployment stage. Use `RDB` if you are live with RTR, or `rdb_modern` if you are evaluating or testing RTR deployment.

| Database | Permissions | SQL Login |
|---|---|---|
| `RDB` (production RTR only) | `db_datareader`, `db_datawriter` | `kafka_sync_connector_service_rdb` |
| `rdb_modern` (dev RTR only) | `db_datareader`, `db_datawriter` | `kafka_sync_connector_service_rdb` |

### Debezium

The Debezium service monitors `NBS_ODSE` and `NBS_SRTE` tables for row-level changes and writes those changes to the Kafka broker.

| Database | Permissions | SQL Login |
|---|---|---|
| `NBS_ODSE` | `db_datareader` | `debezium_service_rdb` |
| `NBS_SRTE` | `db_datareader` | `debezium_service_rdb` |

## Stored procedures by service

The following stored procedures must be executable by their respective service users. These are granted individually rather than through a role.

<!-- [SME REVIEW] Confirm all SP names are current and complete. Source doc had inconsistent capitalization (e.g., `Sp_ldf_data_event`) — standardized to lowercase here per SQL Server convention. Verify against actual database objects before publishing. -->

Jump to stored procedures:

- [Organization service](#organization-stored-procedures)
- [Observation service](#observation-stored-procedures)
- [Person service](#person-stored-procedures)
- [Investigation service](#investigation-stored-procedures)
- [LDF service](#ldf-stored-procedures)

### Organization service - `NBS_ODSE`
{: #organization-stored-procedures }

- `sp_organization_event`
- `sp_place_event`

### Observation service - `NBS_ODSE`
{: #observation-stored-procedures }

- `sp_observation_event`

### Person service - `NBS_ODSE`
{: #person-stored-procedures }

- `sp_patient_event`
- `sp_patient_race_event`
- `sp_provider_event`
- `sp_auth_user_event`

### Investigation service - `NBS_ODSE`
{: #investigation-stored-procedures }

- `sp_investigation_event`
- `sp_contact_record_event`
- `sp_interview_event`
- `sp_notification_event`
- `sp_treatment_event`
- `sp_vaccination_event`
- `sp_public_health_case_fact_datamart_event`

### LDF service - `NBS_ODSE`
{: #ldf-stored-procedures }

- `sp_ldf_data_event`
- `sp_ldf_patient_event`
- `sp_ldf_provider_event`
- `sp_ldf_organization_event`
- `sp_ldf_observation_event`
- `sp_ldf_phc_event`
- `sp_ldf_intervention_event`
