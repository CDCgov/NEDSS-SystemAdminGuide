---
title: Data Compare
layout: page
parent: Deploy real-time reporting
nav_order: 6
description: Explains deployment and use of Data Compare to validate RTR output against classic ETL results.
redirect_from:
  - /docs/7_feature_preview/6_data_compare_tool.html
  - /docs/7_feature_preview/6_data_compare_tool/
  - /docs/deploy-nbs7/real-time-reporting/data-compare-tool.html
  - /docs/deploy-nbs7/real-time-reporting/data-compare-tool/
---

# Deploy and use the RTR Data Compare validation tool

This page covers deploying and using the Data Compare tool to validate RTR output against classic ETL results.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Overview

The Data Compare tool is an optional RTR validation service that allows STLT users to compare data processed by RTR against the classic ETL pipeline and identify differences.

> This service is optional. STLTs can choose to install it only if they require RTR validation capabilities.
{: .note }

The tool consists of two containerized services that communicate asynchronously through Kafka:

- **Data Compare API** - pulls and prepares data from designated tables, then uploads it to a cloud storage bucket
- **Data Compare Processor** - retrieves data from the cloud storage bucket and performs the comparison logic

Database changes are managed by Liquibase, integrated within the `DataCompareAPI` service. Schema changes are applied automatically during deployment. The database objects in the following directory are for reference only: [NEDSS-DataCompare/DataCompareAPIs/.../db/data_internal](https://github.com/CDCgov/NEDSS-DataCompare/tree/main/DataCompareAPIs/src/main/resources/db/data_internal)

## Prerequisites

Before deploying the Data Compare tool, verify the following:

- Access to a cloud storage bucket for data exchange between the API and Processor services. These steps currently use Amazon S3. If you are not using Amazon S3, consult your cloud administrator for equivalent storage configuration.

  For AWS deployments, an IAM role granting the Data Compare pods access to S3 must be provisioned before deployment. Terraform in NEDSS-Infrastructure creates this role when you enable the Data Compare resources in the `1-nbs7` layer. The role is named `<eks-cluster-name>-datacompare-role`. See [Prepare Terraform files and configuration](../../full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html#prepare-terraform-files-and-configuration) for details.

- Keycloak configured with the Data Compare API profile: [NEDSS-Helm/charts/keycloak/extra][nedss-helm-keycloak-extra]

If your Keycloak pod uses a name or namespace other than the default, update the `authUri` in your `values.yaml`:

```yaml
authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
```

> These steps require a Unix-compatible shell. On Windows, use Git Bash, WSL, or an equivalent terminal emulator.
{: .note }
> Verify that you are connected to the correct Kubernetes cluster before proceeding. To confirm, run `kubectl config current-context`.
{: .important }

## Deploy the Data Compare API

Follow these steps to configure and deploy the Data Compare API Helm chart.

The Helm chart is located in `charts/data-compare-api-service` in the [NEDSS-Helm repository][nedss-helm-data-compare-api-chart].

1. Configure `values.yaml`. Replace all placeholder values before installation:

   ```yaml
   image:
     # Data Compare API image
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-compare-api-service"
     pullPolicy: IfNotPresent
     # Replace with the target release version tag, e.g. v1.0.1
     tag: <release-version-tag>

   ingressHost: "data.EXAMPLE_DOMAIN"
   jdbc:
     # SQL Server endpoint
     dbserver: "EXAMPLE_DB_ENDPOINT"
     username: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   s3:
     # AWS-specific: replace with your AWS Region and S3 bucket name
     region: "AWS REGION"
     bucketName: "S3 BucketName"
   ```

1. For AWS deployments, add the IRSA role ARN to `values.yaml` to grant the pod access to S3:

   ```yaml
   serviceAccount:
     annotations:
       eks.amazonaws.com/role-arn: "arn:aws:iam::<ACCOUNT_ID>:role/<eks-cluster-name>-datacompare-role"
   ```

   Replace `<ACCOUNT_ID>` and `<eks-cluster-name>` with your values. The role is created during infrastructure provisioning. See [Provision the AWS environment](../../full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html) for details.

1. Install the Helm chart:

   ```bash
   helm install data-compare-api-service -f ./data-compare-api-service/values.yaml data-compare-api-service
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

1. Validate the service by opening the Swagger UI. Replace `<data.EXAMPLE_DOMAIN>` with your actual domain:

   ```text
   https://<data.EXAMPLE_DOMAIN>/comparison/swagger-ui/index.html
   ```

## Deploy the Data Compare Processor

Follow these steps to configure and deploy the Data Compare Processor Helm chart.

The Helm chart is located in `charts/data-compare-processor-service` in the [NEDSS-Helm repository][nedss-helm-data-compare-processor-chart].

> The Processor is a Kafka consumer microservice and does not expose any API endpoints.
{: .note }

1. Configure `values.yaml`. Replace all placeholder values before installation:

   ```yaml
   image:
     # Data Compare Processor image
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-compare-processor-service"
     pullPolicy: IfNotPresent
     # Replace with the target release version tag, e.g. v1.0.1
     tag: <release-version-tag>

   ingressHost: "data.EXAMPLE_DOMAIN"
   jdbc:
     # SQL Server endpoint
     dbserver: "EXAMPLE_DB_ENDPOINT"
     username: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   s3:
     # AWS-specific: replace with your AWS Region and S3 bucket name
     region: "AWS REGION"
     bucketName: "S3 BucketName"
   ```

1. For AWS deployments, add the IRSA role ARN to `values.yaml` to grant the pod access to S3:

   ```yaml
   serviceAccount:
     annotations:
       eks.amazonaws.com/role-arn: "arn:aws:iam::<ACCOUNT_ID>:role/<eks-cluster-name>-datacompare-role"
   ```

   Replace `<ACCOUNT_ID>` and `<eks-cluster-name>` with your values. The role is created during infrastructure provisioning. See [Provision the AWS environment](../../full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html) for details.

1. Install the Helm chart:

   ```bash
   helm install data-compare-processor-service -f ./data-compare-processor-service/values.yaml data-compare-processor-service
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

## Configure ingress

The Data Compare API uses the same ingress as the data ingestion service. Reuse the ingress configuration as needed: [dataingestion-service/templates/ingress.yaml](https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml#L99)

## Verify the deployment

Confirm both services are running without errors:

```bash
kubectl get pods
kubectl logs <pod-name>
```

Both services are ready when they are healthy and the Processor begins consuming from Kafka.

## Use the Data Compare tool

The comparison process relies on the `Data_Compare_Config` table, which Liquibase creates and populates when the Data Compare API deploys. The table comes preloaded with records containing table names and queries that determine what data to compare.

To start a comparison, call:

```text
POST /comparison/api/data-compare
```

Pass the `runNowMode` header to control scope:

- `true` - runs only on records in the config table where `runNow = true`; resets `runNow` to `false` when complete
- `false` - runs on all records in the config table

This is an asynchronous endpoint. If authentication passes and there are no logical errors, it returns a success response immediately. The comparison runs in the background.

The following diagram shows the end-to-end data flow:

```text
API → Pull data from SQL table → Upload to S3 → Kafka → Processor → Pull from S3 → Perform comparison → Upload results to S3
```

> This data flow uses Amazon S3 as the storage provider. If you are not using Amazon S3, the upload and retrieval steps differ based on your cloud provider.
{: .note }

[nedss-helm-keycloak-extra]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/keycloak/extra>
[nedss-helm-data-compare-api-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/data-compare-api-service>
[nedss-helm-data-compare-processor-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/data-compare-processor-service>
