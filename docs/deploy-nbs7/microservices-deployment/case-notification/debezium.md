---
title: Debezium Kafka connector
layout: page
parent: Case notifications
nav_order: 1
redirect_from:
  - /docs/6_microservices_deployment/9a_debezium_case_notifications.html
  - /docs/6_microservices_deployment/9a_debezium_case_notifications/
---

# Deploy the Debezium Kafka source connector for NBS 7 case notifications

This page walks through enabling Change Data Capture (CDC) and deploying the Debezium source connector used by case notification services. Complete [Case notifications](../case-notification.html) before starting this page. After you finishthe connector deployment, proceed to deploying the [case notification service](./case-notification-service.html).

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Enable Change Data Capture

Enable Change Data Capture on `NBS_ODSE` before deploying the connector. Sysadmin permissions are required.

1. Enable Change Data Capture on `NBS_ODSE`:

   ```sql
   exec msdb.dbo.rds_cdc_enable_db 'NBS_ODSE';
   ```

1. Verify the configuration. A value of `is_cdc_enabled=1` indicates successful configuration:

   ```sql
   SELECT name,
   is_cdc_enabled
   FROM sys.databases;
   ```

1. Enable Change Data Capture for the required table in `NBS_ODSE`:

   ```sql
   USE NBS_ODSE;
   exec sys.sp_cdc_enable_table @source_schema = N'dbo', @source_name = N'CN_transportq_out', @role_name = NULL;
   ```

1. Verify Change Data Capture is enabled for ODSE tables:

   ```sql
   USE NBS_ODSE;
   SELECT
    name,
    case when is_tracked_by_cdc = 1 then 'YES'
      else 'NO' end as is_tracked_by_cdc
    FROM sys.tables
    WHERE is_tracked_by_cdc = 1;
   ```

## Deploy the Debezium connector using Helm

Use the [debezium-case-notifications Helm chart][nedss-helm-debezium-case-notifications-chart] to deploy the connector into your Kubernetes cluster.

1. Use Git to clone your own local copy of the public [NEDSS-Helm repository][nedss-helm]. The following steps use the files in `charts/debezium-case-notifications/` from that repository.
1. Set the image repository and tag:

   ```yaml
   image:
     repository: quay.io/debezium/connect
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Update `values.yaml` with `NBS_ODSE` hostname, username, password, and Kafka bootstrap server values. For help determining these values, see the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices).

   ```yaml
   properties:
     bootstrap_server: "EXAMPLE_KAFKA_ENDPOINT"
   sqlserverconnector:
     config:
       database.hostname: "EXAMPLE_DB_ENDPOINT"
       database.port: 1433
       database.user: "EXAMPLE_DB_USER"
       database.password: "EXAMPLE_DB_USER_PASSWORD"
       database.dbname: nbs_odse
       database.names: nbs_odse
       database.server.name: odse
       database.history.kafka.bootstrap.servers: "EXAMPLE_KAFKA_MULTI_CLUSTER_ENDPOINTS"
       schema.history.internal.kafka.bootstrap.servers: "EXAMPLE_KAFKA_MULTI_CLUSTER_ENDPOINTS"
   Env:
       name: BOOTSTRAP_SERVERS
       value: "EXAMPLE_KAFKA_ENDPOINT"
   ```

1. Install the connector:

   ```bash
   helm install "debezium-case-notification-service-connect" ./debezium-case-notifications -f ./debezium-case-notifications/values.yaml
   ```

1. Confirm the pod is running:

   ```bash
   kubectl get pods
   ```

If the pod is not in a running state, wait and troubleshoot before continuing to [deploy the case notification service](./case-notification-service.html).

## Troubleshooting

If the service has trouble connecting to the database, delete the ConfigMap and then reinstall the chart to recreate it:

1. Delete the ConfigMap:

   ```bash
   kubectl delete configmap case-notification-connect
   ```

1. Reinstall the chart:

   ```bash
   helm upgrade "debezium-case-notification-service-connect" ./debezium-case-notifications -f ./debezium-case-notifications/values.yaml
   ```

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-debezium-case-notifications-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/debezium-case-notifications>
