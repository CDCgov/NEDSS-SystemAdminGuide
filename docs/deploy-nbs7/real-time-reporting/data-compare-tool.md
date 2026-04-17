---
title: Data Compare
layout: page
parent: Real-time reporting (preview)
nav_order: 12
redirect_from:
  - /docs/7_feature_preview/6_data_compare_tool.html
  - /docs/7_feature_preview/6_data_compare_tool/
---

# Deploy and use the RTR Data Compare validation tool

This page covers deploying and using the Data Compare tool to validate RTR output against classic ETL results.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Overview

The Data Compare tool is an optional RTR validation service that allows STLT users to compare data processed by RTR against the classic ETL pipeline and identify differences.

> This service is optional. STLTs may choose to install it only if they require RTR validation capabilities.
{: .note }

The tool consists of two containerized services that communicate asynchronously via Kafka:

- **Data Compare API** — pulls and prepares data from designated tables, then uploads it to an S3 bucket
- **Data Compare Processor** — retrieves data from the S3 bucket and performs the comparison logic

Database changes are managed by Liquibase, integrated within the `DataCompareAPI` service. Schema changes are applied automatically during deployment. The database objects in the following directory are for reference only: [NEDSS-DataCompare/DataCompareAPIs/.../db/data_internal](https://github.com/CDCgov/NEDSS-DataCompare/tree/main/DataCompareAPIs/src/main/resources/db/data_internal)

## Prerequisites

- Access to an AWS S3 bucket for data exchange
- Keycloak configured with the Data Compare API profile: [NEDSS-Helm/charts/keycloak/extra](https://github.com/CDCgov/NEDSS-Helm/tree/main/charts/keycloak/extra)

In your `values.yaml`, provide the Keycloak auth URI:

```yaml
authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
```

> This value only needs to change if the Keycloak pod's name or namespace is modified.
{: .note }

## Deploy via Helm

### Data Compare API

Helm chart location: `charts/data-compare-api-service`

1. Validate the image tag in `values.yaml`:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-compare-api-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag>  # e.g. v1.0.1
   ```

1. Update JDBC and other configuration values:

   ```yaml
   ingressHost: "data.EXAMPLE_DOMAIN"
   jdbc:
     dbserver: "EXAMPLE_DB_ENDPOINT"
     username: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   s3:
     region: "AWS REGION"
     bucketName: "S3 BucketName"
   ```

1. Install the Helm chart:

   ```bash
   helm install data-compare-api-service -f ./data-compare-api-service/values.yaml data-compare-api-service
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

1. Validate the service by opening the Swagger UI:

   ```text
   https://<data.EXAMPLE_DOMAIN>/comparison/swagger-ui/index.html
   ```

### Data Compare Processor

Helm chart location: `charts/data-compare-processor-service`

> The Processor is a Kafka consumer microservice and does not expose any API endpoints.
{: .note }

1. Validate the image tag in `values.yaml`:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-compare-processor-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag>  # e.g. v1.0.1
   ```

1. Update JDBC and other configuration values:

   ```yaml
   ingressHost: "data.EXAMPLE_DOMAIN"
   jdbc:
     dbserver: "EXAMPLE_DB_ENDPOINT"
     username: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   s3:
     region: "AWS REGION"
     bucketName: "S3 BucketName"
   ```

1. Install the Helm chart:

   ```bash
   helm install data-compare-processor-service -f ./data-compare-processor-service/values.yaml data-compare-processor-service
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

### Ingress

The Data Compare API uses the same ingress as the data ingestion service. Reuse the ingress config as needed: [dataingestion-service/templates/ingress.yaml](https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml#L99)

## Verify the deployment

Confirm both services are running without crashes:

```bash
kubectl get pods
kubectl logs <pod-name>
```

The system is ready when both services are healthy and the Processor begins consuming from Kafka.

## Use the Data Compare tool

The comparison process relies on the `Data_Compare_Config` table, which is created and populated by Liquibase when the Data Compare API is deployed. The table comes preloaded with records containing table names and queries that determine what data to compare.

To start a comparison, call:

```text
POST /comparison/api/data-compare
```

Pass the `runNowMode` header to control scope:

- `true` — runs only on records in the config table where `runNow = true`; resets `runNow` to `false` when complete
- `false` — runs on all records in the config table

This is an asynchronous endpoint. If authentication passes and there are no logical errors, it returns a success response immediately. The actual comparison runs in the background.

**Data flow:**

```text
API → Pull data from SQL table → Upload to S3 → Kafka → Processor → Pull from S3 → Perform comparison → Upload results to S3
```
