---
title: Java service
layout: page
parent: Deploy real-time reporting
nav_order: 4
description: Covers deployment of the RTR Java service that transforms Kafka events and loads reporting datamarts.
redirect_from:
  - /docs/7_feature_preview/4_rtr_java_reporting_services.html
  - /docs/7_feature_preview/4_rtr_java_reporting_services/
---

# Deploy real-time reporting (RTR) Java service

This page covers deploying the RTR Java service that processes streamed events from Kafka and loads domain-specific reporting data.

Deploying the Java service is a two-phase process. The first deployment seeds the `nrt_*` caching tables that RTR depends on. Once seeding is complete, you reinstall the chart with post-processing enabled.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> These steps require a Unix-compatible shell. On Windows, use Git Bash, WSL, or an equivalent terminal emulator.
{: .note }

> Verify that you are connected to the correct Kubernetes cluster before proceeding. To confirm, run `kubectl config current-context`.
{: .important }

## Configure values.yaml

1. Locate the Helm chart for the RTR Java service in the [NEDSS-Helm repository][nedss-helm-rtr-chart].

1. Copy the default `values.yaml` from the chart and fill in the required values for your environment — database connection, Kafka cluster, image repository, and any environment-specific overrides.

1. Set `featureFlag.postProcessingEnable` to `"false"` for the initial deployment. This is required so that the first run seeds the `nrt_*` caching tables without triggering post-processing before the data is ready:

   ```yaml
   featureFlag:
     postProcessingEnable: "false"
   ```

## Initial deployment

Install the Helm chart with post-processing disabled:

```bash
helm install -f reporting-pipeline-service/values.yaml reporting-pipeline-service ./reporting-pipeline-service/
```

Verify the pods are running:

```bash
kubectl get deployment reporting-pipeline-service
```

Expected output:

```text
NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
reporting-pipeline-service   1/1     1            1           16m
```

## Monitor seeding progress

The `/actuator/lag` endpoint reports how far behind the service is in consuming its Kafka topics. Use it to determine when initial seeding is complete.

Retrieve information on reporting-pipeline-service lag in your browser. Replace `<exampledomain>` with your actual domain (see [Deploy Traefik ingress controller](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-traefik-ingress-controller)):

```text
   https://data.<exampledomain>/reporting-pipeline-svc/actuator/lag
```

When all "messagesQueued" values are `0`, seeding is complete.

## Final deployment

Reinstall the chart with post-processing enabled:

1. Update `values.yaml` to enable post-processing:

   ```yaml
   featureFlag:
     postProcessingEnable: "true"
   ```

1. Upgrade the release:

   ```bash
   helm upgrade -f reporting-pipeline-service/values.yaml reporting-pipeline-service ./reporting-pipeline-service/


1. Verify the pods restarted cleanly:

   ```bash
   kubectl rollout status deployment/reporting-pipeline-service
   kubectl get deployment reporting-pipeline-service
   ```

1. Confirm the service is healthy. Replace `<exampledomain>` with your actual domain (see [Deploy Traefik ingress controller](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-traefik-ingress-controller)):

   ```text
   https://data.<exampledomain>/reporting-pipeline-svc/actuator/health
   ```

[nedss-helm-rtr-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/rtr>
