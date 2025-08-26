---
title: Data Compare Tool
layout: page
parent: Real Time Reporting (Preview)
nav_order: 12
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Deploy Data Compare (Optional Validation Tool for RTR)

### Overview

The validation tool for **RTR (Real-Time Reporting)** allows **STLT** users to compare and identify differences between data processed by RTR and the classic ETL pipeline.

> This service is *optional*. STLTs may choose to install it only if they require RTR validation capabilities.

---

### Requirements

- Users must have access to an **AWS S3 bucket** for data exchange.

---

### Components

#### 1. Data Compare API

- A containerized service that:
  - Pulls and prepares data from designated tables
  - Uploads the data to a specified AWS S3 bucket

#### 2. Data Compare Processor

- A containerized service that:
  - Retrieves data from the S3 bucket
  - Performs data comparison logic

> The two services communicate asynchronously using **Kafka**.

---

### Database Setup

- Database changes are managed by **Liquibase**, integrated within the `DataCompareAPI` service.
- Schema changes are automatically applied during deployment.
- The database objects listed in the following directory are for reference only:

[https://github.com/CDCgov/NEDSS-DataCompare/tree/main/DataCompareAPIs/src/main/resources/db/data\_internal](https://github.com/CDCgov/NEDSS-DataCompare/tree/main/DataCompareAPIs/src/main/resources/db/data_internal)


---

### Keycloak Configuration

Provide the Keycloak Auth URI in your `values.yaml` file:

```yaml
authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
```

> This value only needs to change if the Keycloak pod's name or namespace is modified.

- The Data Compare API requires a Keycloak profile:

[https://github.com/CDCgov/NEDSS-Helm/tree/main/charts/keycloak/extra](https://github.com/CDCgov/NEDSS-Helm/tree/main/charts/keycloak/extra)

---

## Deploy via Helm

### Data Compare API

**Helm Chart Location:** `charts/data-compare-api-service`

#### Validate the image tag

```yaml
image:
  repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-compare-api-service"
  pullPolicy: IfNotPresent
  tag: <release-version-tag>  # e.g. v1.0.1
```

#### Update JDBC and other configurations

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

#### Install Pod

```bash
helm install data-compare-api-service -f ./data-compare-api-service/values.yaml data-compare-api-service
```

#### Verify Pod

```bash
kubectl get pods
```

#### Validate the service

Open:

```
https://<data.EXAMPLE_DOMAIN>/comparison/swagger-ui/index.html
```

---

### Data Compare Processor

**Helm Chart Location:** `charts/data-compare-processor-service`

#### Validate the image tag

```yaml
image:
  repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-compare-processor-service"
  pullPolicy: IfNotPresent
  tag: <release-version-tag>  # e.g. v1.0.1
```

#### Update JDBC and other configurations

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

#### Install Pod

```bash
helm install data-compare-processor-service -f ./data-compare-processor-service/values.yaml data-compare-processor-service
```

#### Verify Pod

```bash
kubectl get pods
```

> **Note:** The Processor service is a Kafka consumer microservice and **does not expose any API endpoints**.

---

### Ingress Setup

- The Data Compare API uses the same ingress as the data ingestion service.
- Reuse the following ingress config as needed:

[https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml#L99](https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml#L99)

---

## Spot Testing & Validation

- Ensure both containers are running without crashes:

```bash
kubectl get pods
kubectl logs <pod-name>
```

> ✅ The system is ready when both services are healthy and the processor begins consuming from Kafka.

---

## How to Use Data Compare

- The Data Compare process requires the `Data_Compare_Config` table, which is created and managed by Liquibase when the Data Compare API is deployed.
- The `Data_Compare_Config` table comes preloaded with several records containing table names and queries. These records are crucial, as the comparison process relies on them to determine what data to compare.

### Invoke Comparison Endpoint

Users must call the following endpoint to start the comparison process:

```
POST /comparison/api/data-compare
```

#### Required Headers:

- `runNowMode`: `true` or `false`
  - If `true`: The comparison will run **only on records** in the config table where `runNow = true`. Once completed, `runNow` will automatically be reset to `false`.
  - If `false`: The comparison will run **on all records** found in the configuration table.

> 🛈 This is an **asynchronous endpoint** — if authentication passes and there are no logical errors, it will return a success response immediately. However, the actual comparison process may take time as it involves:

### Data Flow

```
API → Pull data from SQL table → Upload to S3 → Kafka → Processor → Pull from S3 → Perform comparison → Upload results to S3
```
