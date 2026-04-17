---
title: Debezium
layout: page
parent: Real-time reporting (preview)
nav_order: 2
redirect_from:
  - /docs/7_feature_preview/2_debezium-rtr.html
  - /docs/7_feature_preview/2_debezium-rtr/
---

# Deploy Debezium for real-time reporting (RTR)

This page covers deploying the Debezium connector that captures change data from source tables and publishes events to Kafka topics for RTR processing.

1. The Helm chart for debezium-connect should be available under charts/debezium.
2. Validate image repository and tag:

   ```yaml
   image:
     repository: quay.io/debezium/connect
     tag: <release-version-tag> e.g v1.0.1
   ```

3. Configurations for the following should be on hand to update the `values.yaml` file- NBS_ODSE hostname, username, password and kafka bootstrap server names. Replace all `"EXAMPLE_MSK_KAFKA_ENDPOINT"` with Kafka endpoints, Replace all `"nbs-db.private-EXAMPLE_DOMAIN"` with SQL server domain name, Replace all instances of `"EXAMPLE_DB_USER"` with SQL Server user name, Replace all instances of `"EXAMPLE_DB_USER_PASSWORD"` with SQL Server password

   ```yaml
   properties:
     bootstrap_server: "EXAMPLE_MSK_KAFKA_ENDPOINT"

   sqlserverconnector_odse:
     config:
       database.hostname: "nbs-db.private-EXAMPLE_DOMAIN",
       database.port: "1433",
       database.user: "EXAMPLE_ODSE_DB_USER",
       database.password: "EXAMPLE_ODSE_DB_USER_PASSWORD",
       database.dbname: "nbs_odse",
       database.names: "nbs_odse",
       database.server.name: "odse",
       database.history.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT",
       schema.history.internal.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"

   sqlserverconnector_odse_meta:
     config:
       database.hostname: "nbs-db.private-EXAMPLE_DOMAIN",
       database.port: "1433",
       database.user: "EXAMPLE_ODSE_DB_USER",
       database.password: "EXAMPLE_ODSE_DB_USER_PASSWORD",
       database.dbname: "nbs_odse",
       database.names: "nbs_odse",
       database.server.name: "odse",
       database.history.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT",
       schema.history.internal.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"

   sqlserverconnector_srte:
     config:
       database.hostname: "nbs-db.private-EXAMPLE_DOMAIN",
       database.port: "1433",
       database.user: "EXAMPLE_SRTE_DB_USER",
       database.password: "EXAMPLE_SRTE_DB_USER_PASSWORD",
       database.dbname: "nbs_odse",
       database.names: "nbs_odse",
       database.server.name: "odse",
       database.history.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT",
       schema.history.internal.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_ENDPOINT"
   env:
     - name: BOOTSTRAP_SERVERS
       value: "EXAMPLE_MSK_KAFKA_ENDPOINT"
   ```

5. Install pod

   ```bash
   Helm install -f ./debezium/values.yaml debezium-connect ./debezium/
   ```

6. Verify if pod is running

   ```bash
   kubectl get pods
   ```

7. Validate service

- a. This is an internal service with no ingress. Validation should be part of [RTR Pipeline Validation](../../deploy-nbs7/real-time-reporting/pipeline-validation.html)
- b. If the service has any trouble connecting with the database, run this command to reset the ConfigMap.

  ```bash
  kubectl delete configmap cp-kafka-connect-sqlserver-connect
  ```
