---
title: Debezium Case Notification
layout: page
parent: Case Notification
nav_order: 1
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy Debezium Case Notifications Kafka Source Connector

1. Enable Change Data Capture on NBS_ODSE databases for Case Notification: The query below can be used to enable Change Data Capture. sysadmin permissions are required to run it. The subsequent query can be used to verify configuration.
   ```sql
   exec msdb.dbo.rds_cdc_enable_db 'NBS_ODSE';

   --Verify change data capture. is_cdc_enabled=1 indicates successful configuration.
   SELECT name,
   is_cdc_enabled
   FROM sys.databases;
   ```
2. Enable Change Data Capture for select tables in NBS_ODSE: To enable Change Data Capture for ODSE tables, the query below needs to be executed.
   ```sql
   exec sys.sp_cdc_enable_table @source_schema = N'dbo',@source_name = N'CN_transportq_out', @role_name = NULL;
   ```
3. Verify if Change Data Capture is enabled for tables in ODSE.
   ```sql
   --View ODSE tables with CDC enabled. 
   USE NBS_ODSE;
   SELECT
    name,
    case when is_tracked_by_cdc  = 1 then 'YES'
      else 'NO' end as is_tracked_by_cdc
    FROM sys.tables
    WHERE is_tracked_by_cdc = 1;
   ```
4. The helm chart for service debezium-case-notification-service-connect should be available under charts/debezium-case-notifications.
5. Validate image repository and tag:
   ```yaml
   image:
     repository: quay.io/debezium/connect
     tag: <release-version-tag> e.g v1.0.1
   ```
6. Configurations for the following should be on hand to update the values.yaml file- NBS_ODSE hostname, username, password and kafka bootstrap server names.
   ```yaml
   properties:
      bootstrap_server: "EXAMPLE_MSK_KAFKA_ENDPOINT"
   sqlserverconnector: 
      config: 
         database.hostname: nbs-db.private-EXAMPLE_DOMAIN,
         database.port: 1433,
         database.user: EXAMPLE_DB_USER,
         database.password: EXAMPLE_DB_USER_PASSWORD,
         database.dbname: nbs_odse,
         database.names: nbs_odse,
         database.server.name: odse,
         database.history.kafka.bootstrap.servers: EXAMPLE_MSK_KAFKA_ENDPOINT,
         schema.history.internal.kafka.bootstrap.servers: EXAMPLE_MSK_KAFKA_ENDPOINT
   Env:
         name: BOOTSTRAP_SERVERS
         value: "EXAMPLE_MSK_KAFKA_ENDPOINT"
   ```
7. Install pod
   ```bash
   helm install -f ./debezium-case-notifications/values.yaml debezium-case-notification-service-connect ./debezium-case-notifications/
   ```
8. Verify if pod is running
    ```bash
    kubectl get pods
    ```
9. Validate service
    - This is an internal service with no ingress.
    - If the service has any trouble connecting with the database, run this command to reset the ConfigMap.
    ```bash
    kubectl delete configmap case-notification-connectb
    ```
