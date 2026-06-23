---
title: Case notifications
layout: page
parent: Deploy NBS 7 microservices
nav_order: 9
has_children: true
nav_enabled: true
redirect_from:
  - /docs/6_microservices_deployment/9_case_notification.html
  - /docs/6_microservices_deployment/9_case_notification/
  - /docs/6_microservices_deployment/9b_keycloak_configuration.html
---

# Deploy case notifications for NBS 7

This page walks through deploying the NBS 7 case notification service for NBS version {{ site.version_latest }}. Complete the [Data Processing](./data-processing.html) and optional [NND Service (Data Sync)](./nnd-service.html) deployments before starting this page. After you finish, proceed to deploy the [data ingestion service (DI API)](../data-ingestion/data-ingestion.html) or [real-time reporting (RTR)](../real-time-reporting/real-time-reporting.html) based on your deployment plan.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Overview

The case notification pipeline begins with a Debezium source connector monitoring the `ODSE.CN_transportq_out` table. When new data is inserted, the connector publishes it to a Kafka topic, which the case notification service consumes. The service processes each event and routes output to either `MSGOUTE.transportq_out` or `MSGOUTE.netsstransportq_out` depending on event type. Faulty events are routed to `MSGOUTE.case_notification_dlt` (Dead Letter Table) for investigation.

> **Case notifications and [real-time reporting (RTR)](../real-time-reporting/real-time-reporting.html) must use the same Kafka cluster.** If you have not yet deployed RTR, note the Kafka cluster that you configure here and use it when you deploy RTR.
{: .important }

## Considerations

Your jurisdiction can use either the NBS 7 case notification service or route case notifications through an integration engine like Rhapsody.

- **If you are using an alternative integration engine**, skip this section. Do not deploy the notification service, and do not enable it in Kubernetes.
- **If you are moving to NBS 7 case notifications**, complete the steps in this section.

## Deployment overview

To deploy the notification service, complete the steps in the following order:

1. [Deploy the Debezium Kafka source connector](../../deploy-nbs7/microservices-deployment/case-notification/debezium.html)
1. [Deploy the case notification service](../../deploy-nbs7/microservices-deployment/case-notification/case-notification-service.html)
1. [Test and integrate case notification APIs](../../deploy-nbs7/microservices-deployment/case-notification/api-testing.html)
