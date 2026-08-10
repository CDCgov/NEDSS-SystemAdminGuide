---
title: Kafka connector
layout: page
parent: Real-time reporting
nav_order: 2
description: Shows how to deploy the Kafka sink connector that writes RTR topics into reporting tables.
redirect_from:
  - /docs/7_feature_preview/3_kafka_connector.html
  - /docs/7_feature_preview/3_kafka_connector/
  - /docs/deploy-nbs7/real-time-reporting/kafka-connector.html
  - /docs/deploy-nbs7/real-time-reporting/kafka-connector/
---

# Deploy the Kafka connector for real-time reporting (RTR)

This page walks through deploying the Kafka sink connector using the ['kafka-connect-sink' Helm chart][nedss-helm-kafka-connect-sink-chart] from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}. The connector consumes RTR topics and writes transformed data into reporting tables.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

This page assumes you've completed [Before you begin](../deploy-nbs7-microservices.html#before-you-begin) for the microservices phase and each RTR deployment page before this one, in order. The page immediately before this one is [Debezium](debezium.html).

Have your database credentials and Kafka endpoint values available. See the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) if you need help determining any values.

## Deploy the Kafka connector using Helm

Complete the following steps to deploy the [Kafka connector Helm chart][nedss-helm-kafka-connect-sink-chart] from the `charts/kafka-connect-sink/` directory of your cloned NEDSS-Helm repository:

1. In the `kafka-connect-sink` chart directory, open the values file for your cloud provider:
   - **AWS:** `kafka-connect-sink/values.yaml`
   - **Azure:** `kafka-connect-sink/values-azure.yaml`
1. Search the values file for `EXAMPLE` and fill in your environment-specific values. See the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) for help determining values.

1. Install the Helm chart:
   - **AWS:**

      ```bash
      helm install -f ./kafka-connect-sink/values.yaml cp-kafka-connect-server ./kafka-connect-sink/
      ```

   - **Azure:**

      ```bash
      helm install -f ./kafka-connect-sink/values-azure.yaml cp-kafka-connect-server ./kafka-connect-sink/
      ```

1. Verify the pod is running:

   ```bash
   kubectl get deployment cp-kafka-connect-server
   ```

After the Kafka connector deploys successfully, continue to [Java service](rtr-java-services.html).

## Troubleshoot the Kafka connector

If the service has trouble connecting to the database, run the following command to reset the ConfigMap:

```bash
kubectl delete configmap cp-kafka-connect-sqlserver-connect
```

If issues persist, email [nbs@cdc.gov](mailto:nbs@cdc.gov).

## Next steps

Continue to [Java service](./rtr-java-services.html).

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-kafka-connect-sink-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/kafka-connect-sink>
