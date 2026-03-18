---
title: "Add-on: Real-Time Reporting (RTR)"
layout: page
parent: Component reference
grand_parent: NBS 7 Deployment Decision Guide
nav_order: 2
---


<!-- PAGE TITLE - DON'T INCLUDE HEADER IN TOC -->
## Component reference: Real-Time Reporting (RTR) add-on
{: .no_toc }

RTR works alongside the legacy MasterETL batch process during transition, with the goal of eventually replacing it. The following components are added to your NBS Core deployment when you choose NBS Core + RTR or NBS Complete.

1. TOC
{:toc}

--- 

{: .note }
**Health department leaders:** See [Leadership considerations](../leadership_considerations.html) for guidance on evaluating RTR for your jurisdiction.

---

### Debezium

An open-source Change Data Capture (CDC) platform.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Monitors the NBS database for changes in real time and streams those changes to Kafka as they occur. Debezium is the entry point for the RTR pipeline. Without it, downstream RTR components have no data to process. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Requires the NBS database (NBS\_ODSE) as its source. Streams data to the Kafka cluster. |

---

### Kafka and Kafka Connect

Apache Kafka is an open source event-streaming platform. Kafka Connect is the framework that moves data between Kafka and other systems.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Acts as the message bus for the RTR pipeline. Kafka receives change events from Debezium and delivers them to the RTR domain services. Kafka Connect writes the processed output to RDB\_Modern staging tables for post-processing and reporting. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Receives events from Debezium. Delivers messages to RTR domain services. Kafka Connect writes processed data to RDB\_Modern. Requires sufficient cluster resources — Kafka is one of the more operationally demanding components in the RTR stack. |

---

### RTR domain services

A unified Spring Boot service that transforms streaming data from Kafka into reportable public health records. Previously implemented as five separate entity-specific services (investigation, person, observation, organization, and LDF data), these are being consolidated into a single `reporting-service` application to reduce deployment complexity and operational overhead.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Consumes Kafka messages for each entity type (investigations, patients, organizations, observations, and LDF data), runs stored procedures to retrieve and format the data, and produces processed records for downstream storage in RDB\_Modern. A post-processing service then populates analytical datamarts and fact tables from the staging data. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Requires Kafka (message source) and NBS\_ODSE (operational data store). Populates RDB\_Modern staging tables, which are then consumed by the post-processing service. |

> The five entity-specific RTR services (investigation-service, person-service, observation-service, organization-service, ldfdata-service) are being consolidated into a single `reporting-service` as of early 2026. Check with your CDC NBS point of contact for the current deployment state.
{: .note }

---

### RDB\_Modern

The modern reporting database introduced by RTR.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Stores processed, structured public health records produced by the RTR domain services. Runs alongside the legacy RDB during migration. Downstream reporting and analytics tools connect to RDB\_Modern rather than directly to the operational database. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Populated by RTR domain services. Required by any reporting or analytics tools that your jurisdiction connects to NBS 7. |
