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

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> These steps require a Unix-compatible shell. On Windows, use Git Bash, WSL, or an equivalent terminal emulator.
{: .note }

## Installing the RTR Java service

Follow these steps to configure and deploy the RTR Java service Helm chart.

> Verify that you are connected to the correct Kubernetes cluster before proceeding. To confirm, run `kubectl config current-context`.
{: .important }

1. Locate the Helm chart for the RTR Java service in the [NEDSS-Helm repository][nedss-helm-rtr-chart].

1. Validate the Kubernetes secret for database credentials:

   ```bash
   kubectl get secret/database-access -o yaml
   ```

   > Verify that the secret contains the correct database username and password, Kafka cluster, and other required configuration values. If the secret does not exist, create it by applying the provided YAML file. Replace all placeholder values before running:
   >
   > Script location: [NEDSS-Helm/nbs-secrets.yaml][nedss-helm-k8-secrets-manifest]
   >
   > ```bash
   > kubectl apply -f k8-manifests/nbs-secrets.yaml
   > ```
   >
   {: .note }

1. Validate the image repository: <!-- [SME REVIEW: confirm data-reporting-service is the correct consolidated image name] -->

   ```yaml
   global.image.repository: "quay.io/us-cdcgov/cdc-nbs-modernization/"
   ```

1. Install the Helm chart for the RTR Java service:

   ```bash
   helm install reporting-pipeline-service . -f values.yaml
   ```

1. Verify the pods are running:

   ```bash
   kubectl get pods
   ```

   Expected output:

   ```text
   NAME                                                READY   STATUS    RESTARTS   AGE
   rtr-java-services-reporting-pipeline-service-<hash>    1/1     Running   0          2m6s
   ```

1. Validate the service. Replace `<exampledomain>` with your actual domain (see [Deploy Traefik ingress controller](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-traefik-ingress-controller)):

   **reporting-pipeline-service**

   ```text
   https://data.<exampledomain>/reporting-pipeline-svc/actuator/health
   ```

[nedss-helm-rtr-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/rtr>
[nedss-helm-k8-secrets-manifest]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/k8-manifests/nbs-secrets.yaml>
