---
title: Kafka connector
layout: page
parent: Real-time reporting (preview)
nav_order: 3
redirect_from:
  - /docs/7_feature_preview/3_kafka_connector.html
  - /docs/7_feature_preview/3_kafka_connector/
---

# Deploy the Kafka connector for real-time reporting (RTR)

This page covers deploying the Kafka sink connector that consumes RTR topics and writes transformed data into reporting tables.

1. The helm chart for Kafka connector should be available under `charts/kafka-connect-sink`.

1. Validate the image repository and tag:

   ```yaml
   image: confluentinc/cp-kafka-connect
   tag: <release-version-tag> e.g v1.0.1
   ```

1. Update `values.yaml` with the RDB_modern hostname, username, password, and Kafka bootstrap server names:

   ```yaml
   sqlServerConnector:
     config:
       connection.url: jdbc:sqlserver://nbs-db.EXAMPLE_FIXME.nbspreview.com:1433;databaseName=rdb;encrypt=true;trustServerCertificate=true;,
       connection.user: EXAMPLE_FIXME,
       connection.password: EXAMPLE_FIXME,
   kafka:
     bootstrapServers: "EXAMPLE_FIXME"
   ```

1. Install the pod:

   ```bash
   helm install -f ./kafka-connect-sink/values.yaml cp-kafka-connect-server ./kafka-connect-sink/
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

1. Validate the service:

   - This is an internal service with no ingress. Validation should be part of [RTR Pipeline Validation](../../deploy-nbs7/real-time-reporting/pipeline-validation.html).
   - If the service has trouble connecting to the database, run this command to reset the ConfigMap:

   ```bash
   kubectl delete configmap cp-kafka-connect-sqlserver-connect
   ```
