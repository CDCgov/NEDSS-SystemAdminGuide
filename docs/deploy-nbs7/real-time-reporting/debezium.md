---
title: Debezium
layout: page
parent: Deploy real-time reporting
nav_order: 2
description: Describes deploying Debezium to capture SQL Server changes and publish RTR events to Kafka.
redirect_from:
  - /docs/7_feature_preview/2_debezium-rtr.html
  - /docs/7_feature_preview/2_debezium-rtr/
---

# Deploy Debezium for real-time reporting (RTR)

This page covers steps to deploy the Debezium connector that captures change data from source tables and publishes events to Kafka topics for RTR processing.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> These steps require a Unix-compatible shell. On Windows, use Git Bash, WSL, or an equivalent terminal emulator.
{: .note }

## Installing Debezium

Follow these steps to configure and deploy the Debezium Helm chart for RTR.

> Verify that you are connected to the correct Kubernetes cluster before proceeding. To confirm, run `kubectl config current-context`.
{: .important }

1. Locate the Debezium Helm chart in the [NEDSS-Helm repository][nedss-helm-debezium-chart].

1. Configure `values.yaml`. Replace all placeholder values before installation.

   To retrieve your Kafka bootstrap server endpoints, see [Get bootstrap brokers](https://docs.aws.amazon.com/msk/latest/developerguide/msk-get-bootstrap-brokers.html) in the AWS MSK documentation.

   ```yaml
   image:
     # Debezium connector image
     repository: quay.io/debezium/connect
     # Replace with the target release version tag, e.g. v1.0.1
     tag: <release-version-tag>

   properties:
     # Kafka bootstrap server endpoint from AWS MSK
     bootstrap_server: "EXAMPLE_MSK_KAFKA_ENDPOINT"

   # Connector for NBS_ODSE transactional data
   sqlserverconnector_odse:
     config:
       database.hostname: "nbs-db.private-EXAMPLE_DOMAIN"
       database.port: "1433"
       database.user: "EXAMPLE_ODSE_DB_USER"
       database.password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
       database.dbname: "nbs_odse"
       database.names: "nbs_odse"
       database.server.name: "odse"
       database.history.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"
       schema.history.internal.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"

   # Connector for NBS_ODSE metadata
   sqlserverconnector_odse_meta:
     config:
       database.hostname: "nbs-db.private-EXAMPLE_DOMAIN"
       database.port: "1433"
       database.user: "EXAMPLE_ODSE_DB_USER"
       database.password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
       database.dbname: "nbs_odse"
       database.names: "nbs_odse"
       database.server.name: "odse-meta"
       database.history.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"
       schema.history.internal.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"

   # Connector for NBS_SRTE reference and terminology data
   sqlserverconnector_srte:
     config:
       database.hostname: "nbs-db.private-EXAMPLE_DOMAIN"
       database.port: "1433"
       database.user: "EXAMPLE_SRTE_DB_USER"
       database.password: "EXAMPLE_SRTE_DB_USER_PASSWORD"
       database.dbname: "nbs_srte"
       database.names: "nbs_srte"
       database.server.name: "srte"
       database.history.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"
       schema.history.internal.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"

   env:
     # Kafka bootstrap server endpoint from AWS MSK
     - name: BOOTSTRAP_SERVERS
       value: "EXAMPLE_MSK_KAFKA_ENDPOINT"
   ```

1. Install the pod:

   ```bash
   helm install -f ./debezium/values.yaml debezium-connect ./debezium/
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

1. Validate the service.

   > Debezium is an internal service with no ingress. Validate it as part of [RTR pipeline validation](../../deploy-nbs7/real-time-reporting/pipeline-validation.html).
   {: .note }

After Debezium deploys successfully, continue to [Deploy Kafka connector](../../deploy-nbs7/real-time-reporting/kafka-connector.html).

## Troubleshooting

If issues persist after initial troubleshooting, contact support at <mailto:nbs@cdc.gov>.

### Database connection errors

If the service has trouble connecting to the database, run the following command to reset the ConfigMap:

```bash
kubectl delete configmap cp-kafka-connect-sqlserver-connect
```

[nedss-helm-debezium-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/debezium>
