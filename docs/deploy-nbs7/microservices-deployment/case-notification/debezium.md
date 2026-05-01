---
title: Debezium
layout: page
parent: Case notifications
nav_order: 1
redirect_from:
  - /docs/6_microservices_deployment/9a_debezium_case_notifications.html
  - /docs/6_microservices_deployment/9a_debezium_case_notifications/
---

# Deploy the Debezium Kafka source connector for NBS 7 case notifications

This page walks through enabling Change Data Capture (CDC) and deploying the Debezium source connector used by case notification services.

> This page applies to NBS {{ site.version_latest }}. Helm chart links are pinned to `{{ site.version_latest_tag }}`.
{: .note }

1. Enable Change Data Capture on `NBS_ODSE` for case notification. Sysadmin permissions are required. Then verify the configuration:

   ```sql
   exec msdb.dbo.rds_cdc_enable_db 'NBS_ODSE';

   --Verify change data capture. is_cdc_enabled=1 indicates successful configuration.
   SELECT name,
   is_cdc_enabled
   FROM sys.databases;
   ```

1. Enable Change Data Capture for selected tables in `NBS_ODSE`:

   ```sql
   exec sys.sp_cdc_enable_table @source_schema = N'dbo',@source_name = N'CN_transportq_out', @role_name = NULL;
   ```

1. Verify Change Data Capture is enabled for ODSE tables:

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

1. Locate the Debezium Helm chart in the [NEDSS-Helm repository][nedss-helm-debezium-case-notifications-chart].
1. Set the image repository and tag:

   ```yaml
   image:
     repository: quay.io/debezium/connect
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Update `values.yaml` with `NBS_ODSE` hostname, username, password, and Kafka bootstrap server values:

   ```yaml
   properties:
      bootstrap_server: "EXAMPLE_MSK_KAFKA_ENDPOINT"
   sqlserverconnector:
      config:
         database.hostname: "EXAMPLE_DB_ENDPOINT",
         database.port: 1433,
         database.user: "EXAMPLE_DB_USER",
         database.password: "EXAMPLE_DB_USER_PASSWORD",
         database.dbname: nbs_odse,
         database.names: nbs_odse,
         database.server.name: odse,
         database.history.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_MULTI_CLUSTER_ENDPOINTS",
         schema.history.internal.kafka.bootstrap.servers: "EXAMPLE_MSK_KAFKA_MULTI_CLUSTER_ENDPOINTS"
   Env:
         name: BOOTSTRAP_SERVERS
         value: "EXAMPLE_MSK_KAFKA_ENDPOINT"
   ```

1. Install the connector:

   ```bash
   helm install -f ./debezium-case-notifications/values.yaml debezium-case-notification-service-connect ./debezium-case-notifications/
   ```

1. Verify the pod is running:

    ```bash
    kubectl get pods
    ```

1. Validate the service:
   - This is an internal service with no ingress.
   - If the service has trouble connecting to the database, run this command to reset the ConfigMap:

    ```bash
    kubectl delete configmap case-notification-connectb
    ```

[nedss-helm-debezium-case-notifications-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/debezium-case-notifications>
