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

1. Search `values.yaml` for EXAMPLE and fill in your environment-specific values. See the [Helm values reference][deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices] for help determining values.

   To retrieve your Kafka bootstrap server endpoints, see [Get bootstrap brokers](https://docs.aws.amazon.com/msk/latest/developerguide/msk-get-bootstrap-brokers.html) in the AWS MSK documentation.

1. Install the pod:

   ```bash
   helm install -f ./debezium/values.yaml debezium-connect ./debezium/
   ```

1. Verify the pod is running:

   ```bash
   kubectl get deployment debezium-debezium-rtr-connect
   ```

After Debezium deploys successfully, continue to [Deploy Kafka connector](../../deploy-nbs7/real-time-reporting/kafka-connector.html).

## Troubleshooting

If issues persist after initial troubleshooting, contact support at <mailto:nbs@cdc.gov>.

### Database connection errors

If the service has trouble connecting to the database, run the following command to reset the ConfigMap:

```bash
kubectl delete configmap debezium-rtr-connect
```

[nedss-helm-debezium-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/debezium>
