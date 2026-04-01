---
title: "Add-on: Real-Time Reporting (RTR)"
layout: page
parent: Component reference
grand_parent: Before you deploy
nav_order: 2
description: "Details the four components added by the Real-Time Reporting (RTR) add-on: Debezium, Kafka, RTR domain services, and RDB_Modern."
nav_enabled: true
---

# Component reference: Real-Time Reporting (RTR) add-on

RTR is an optional add-on that provides an event-driven reporting pipeline for near-real-time reporting. RTR replaces the legacy MasterETL batch process. During validation, both might run briefly in parallel to confirm that RTR output is accurate. Once validation is complete, retire MasterETL.

The following components are added to your NBS 7 deployment when you choose to deploy the RTR add-on.

For information on benefits and impact on operating costs, see [Operational considerations](../../before-you-deploy/operational_considerations.html).
{: .note }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Debezium

An open-source Change Data Capture (CDC) platform.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Monitors the NBS database for changes in real time and streams those changes to Kafka as they occur. Debezium is the entry point for the RTR pipeline. Without it, downstream RTR components have no data to process. |
| Dependencies | Requires the NBS database (NBS\_ODSE) as its source. Streams data to the Kafka cluster. |

## Kafka and Kafka Connect

Apache Kafka is an open source event-streaming platform. Kafka Connect is the framework that moves data between Kafka and other systems.

If your jurisdiction chooses to use RTR but continue with batch reporting, Kafka is not required for that reporting path. Only near-real-time RTR reporting requires Kafka and Kafka Connect.
{: .note }

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Acts as the message bus for the RTR pipeline. Kafka receives change events from Debezium and delivers them to the RTR domain services. Kafka Connect writes the processed output to RDB\_Modern staging tables for post-processing and reporting. |
| Dependencies | Receives events from Debezium. Delivers messages to RTR domain services. Kafka Connect writes processed data to RDB\_Modern. Requires sufficient cluster resources; Kafka is one of the more operationally demanding components in the RTR stack. |

## RTR domain services

A unified Spring Boot service that transforms streaming data from Kafka into reportable public health records. Previously implemented as five separate entity-specific services (investigation, person, observation, organization, and LDF data), these are being consolidated into a single `reporting-pipeline-service` application to reduce deployment complexity and operational overhead.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Consumes Kafka messages for each entity type (investigations, patients, organizations, observations, and LDF data), runs stored procedures to retrieve and format the data, and produces processed records for downstream storage in RDB\_Modern. A post-processing service then populates analytical datamarts and fact tables from the staging data. |
| Dependencies | Requires Kafka (message source) and NBS\_ODSE (operational data store). Populates RDB\_Modern staging tables, which are then consumed by the post-processing service. |

> The five entity-specific RTR services (investigation-service, person-service, observation-service, organization-service, ldfdata-service) are being consolidated into a single `reporting-pipeline-service` as of early 2026. Check with your CDC NBS point of contact for the current deployment state.
{: .note }

<!--
## RDB\_Modern

The modern reporting database introduced by RTR.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Stores processed, structured public health records produced by the RTR domain services. Runs alongside the legacy RDB during migration. Downstream reporting and analytics tools connect to RDB\_Modern rather than directly to the operational database. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Populated by RTR domain services. Required by any reporting or analytics tools that your jurisdiction connects to NBS 7. |
-->
