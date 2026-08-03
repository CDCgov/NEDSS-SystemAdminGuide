---
title: Debezium
layout: page
parent: Deploy real-time reporting
nav_order: 1
description: Describes deploying Debezium to capture SQL Server changes and publish RTR events to Kafka.
redirect_from:
  - /docs/7_feature_preview/2_debezium-rtr.html
  - /docs/7_feature_preview/2_debezium-rtr/
  - /docs/deploy-nbs7/real-time-reporting/debezium.html
  - /docs/deploy-nbs7/real-time-reporting/debezium/
---

# Deploy Debezium for real-time reporting (RTR)

This page walks through deploying the Debezium connector using the [Debezium Helm chart][nedss-helm-debezium-chart] from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}. The connector captures change data from source tables and publishes events to Kafka topics for RTR processing.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

This page assumes you've completed [Before you begin](../deploy-nbs7-microservices.html#before-you-begin) for the microservices phase and the database setup on [Deploy real-time reporting](real-time-reporting.html), including enabling Change Data Capture.

Have your database credentials and Kafka endpoint values available. See the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) if you need help determining any values.

## Deploy Debezium using Helm

Complete the following steps to deploy the [Debezium Helm chart][nedss-helm-debezium-chart] from the `charts/debezium/` directory of your cloned NEDSS-Helm repository:

1. In the `debezium` chart directory, open the values file for your cloud provider:
   - **AWS:** `debezium/values.yaml`
   - **Azure:** `debezium/values-azure.yaml`
1. Search the values file for `EXAMPLE` and fill in your environment-specific values. See the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) for help determining values.

1. Install the Helm chart:

   ```bash
   helm install -f ./debezium/values.yaml debezium-connect ./debezium/
   ```

1. Verify the pod is running:

   ```bash
   kubectl get deployment debezium-connect-debezium-rtr-connect
   ```

After Debezium deploys successfully, continue to [Kafka connector](kafka-connector.html).

## Troubleshoot Debezium

If the service has trouble connecting to the database, run the following command to reset the ConfigMap:

```bash
kubectl delete configmap debezium-rtr-connect
```

If issues persist, email [nbs@cdc.gov](mailto:nbs@cdc.gov).

## Next steps

Continue to [Kafka connector](./kafka-connector.html).

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-debezium-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/debezium>
