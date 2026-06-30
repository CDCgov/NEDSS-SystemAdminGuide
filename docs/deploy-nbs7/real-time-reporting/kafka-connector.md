---
title: Kafka connector
layout: page
parent: Deploy real-time reporting
nav_order: 3
description: Shows how to deploy the Kafka sink connector that writes RTR topics into reporting tables.
redirect_from:
  - /docs/7_feature_preview/3_kafka_connector.html
  - /docs/7_feature_preview/3_kafka_connector/
---

# Deploy the Kafka connector for real-time reporting (RTR)

This page covers steps to deploy the Kafka sink connector that consumes RTR topics and writes transformed data into reporting tables.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> These steps require a Unix-compatible shell. On Windows, use Git Bash, WSL, or an equivalent terminal emulator.
{: .note }

## Installing the Kafka connector

Follow these steps to configure and deploy the Kafka connector Helm chart for RTR.

> Verify that you are connected to the correct Kubernetes cluster before proceeding. To confirm, run `kubectl config current-context`.
{: .important }

1. Locate the Kafka connector Helm chart in the [NEDSS-Helm repository][nedss-helm-kafka-connect-sink-chart].

1. Configure `values.yaml`. Replace all placeholder values before installation.

   To retrieve your Kafka bootstrap server endpoints, see [Get bootstrap brokers](https://docs.aws.amazon.com/msk/latest/developerguide/msk-get-bootstrap-brokers.html) in the AWS MSK documentation.

   ```yaml
   image:
     # Kafka Connect image
     repository: confluentinc/cp-kafka-connect
     # Replace with the target release version tag, e.g. v1.0.1
     tag: <release-version-tag>

   kafka:
     # Kafka bootstrap server endpoint from AWS MSK
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

1. Validate the service.

   > The Kafka connector is an internal service with no ingress. Validate it as part of [RTR pipeline validation](../../deploy-nbs7/real-time-reporting/pipeline-validation.html).
   {: .note }

After Debezium deploys successfully, continue to [Deploy Java services](../../deploy-nbs7/real-time-reporting/rtr-java-services.html).

## Troubleshooting

If issues persist after initial troubleshooting, contact support at <mailto:nbs@cdc.gov>.

### Database connection errors

If the service has trouble connecting to the database, run the following command to reset the ConfigMap:

```bash
kubectl delete configmap cp-kafka-connect-sqlserver-connect
```

[nedss-helm-kafka-connect-sink-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/kafka-connect-sink>
