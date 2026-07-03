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
helm install reporting-pipeline-service . -f values.yaml
```

Verify the pods are running:

```bash
kubectl get pods -l app=reporting-pipeline-service
```

Expected output:

```text
NAME                                                         READY   STATUS    RESTARTS   AGE
reporting-pipeline-service-<hash>                            1/1     Running   0          2m
```

Check the service logs to confirm it is processing events:

```bash
kubectl logs -l app=reporting-pipeline-service --tail=50 -f
```

## Monitor seeding progress

The `/actuator/lag` endpoint reports how far behind the service is in consuming its Kafka topics. Use it to determine when initial seeding is complete. When all lag values reach zero, seeding is done.

Use `kubectl port-forward` to reach the endpoint from your local machine:

```bash
kubectl port-forward svc/reporting-pipeline-service 8080:8080
```

Then in a separate terminal:

```bash
curl -s http://localhost:8080/actuator/lag | jq .
```

To poll continuously until lag reaches zero:

```bash
watch -n 10 "curl -s http://localhost:8080/actuator/lag | jq ."
```

When all topic lag values are `0`, seeding is complete. Stop the port-forward (`Ctrl+C`) and proceed to the next step.

## Final deployment

Reinstall the chart with post-processing enabled:

1. Update `values.yaml` to enable post-processing:

   ```yaml
   featureFlag:
     postProcessingEnable: "true"
   ```

1. Upgrade the release:

   ```bash
   helm upgrade reporting-pipeline-service . -f values.yaml
   ```

1. Verify the pods restarted cleanly:

   ```bash
   kubectl rollout status deployment/reporting-pipeline-service
   kubectl get pods -l app=reporting-pipeline-service
   ```

1. Confirm the service is healthy. Replace `<exampledomain>` with your actual domain (see [Deploy Traefik ingress controller](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-traefik-ingress-controller)):

   ```text
   https://data.<exampledomain>/reporting-pipeline-svc/actuator/health
   ```

[nedss-helm-rtr-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/rtr>
