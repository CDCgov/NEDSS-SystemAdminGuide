---
title: Kafka connector
layout: page
parent: Real Time Reporting (Preview)
nav_order: 3
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Kafka Connector
1. The helm chart for Kafka connector should be available under charts/kafka-connect-sink.
2. Validate image repository and tag:
   ```yaml
   image: confluentinc/cp-kafka-connect
   tag: <release-version-tag> e.g v1.0.1
   ```
3. Configurations for the following should be on hand to update the values.yaml file- RDB_modern hostname, username, password and kafka bootstrap server names.
   ```yaml
   sqlServerConnector: 
      config: 
         connection.url: jdbc:sqlserver://nbs-db.EXAMPLE_FIXME.nbspreview.com:1433;databaseName=rdb_modern;encrypt=true;trustServerCertificate=true;,
         connection.user: EXAMPLE_FIXME,
         connection.password: EXAMPLE_FIXME,
   kafka:
      bootstrapServers: "EXAMPLE_FIXME"
   ```
4. Install pod
   ```bash
   helm install -f ./kafka-connect-sink/values.yaml cp-kafka-connect-server ./kafka-connect-sink/
   ```
5. Verify if pod is running
   ```bash
   kubectl get pods
   ```
6. Validate service
  - a. This is an internal service with no ingress. Validation should be part of [NBS 7.6 Application Installation Guide  RTR Pipeline Validation](https://cdc-nbs.atlassian.net/wiki/spaces/NM/pages/edit-v2/951255219#RTR-Pipeline-Validation)
  - b. If the service has any trouble connecting with the database, run this command to reset the ConfigMap.
```bash
kubectl delete configmap cp-kafka-connect-sqlserver-connect
```
