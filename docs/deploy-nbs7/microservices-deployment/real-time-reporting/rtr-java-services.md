---
title: Java service
layout: page
parent: Real-time reporting
nav_order: 3
description: Covers deployment of the RTR Java service that transforms Kafka events and loads reporting datamarts.
redirect_from:
  - /docs/7_feature_preview/4_rtr_java_reporting_services.html
  - /docs/7_feature_preview/4_rtr_java_reporting_services/
  - /docs/deploy-nbs7/real-time-reporting/rtr-java-services.html
  - /docs/deploy-nbs7/real-time-reporting/rtr-java-services/
---

# Deploy the RTR Java service for NBS 7

This page walks through deploying the real-time reporting ([[rtr]]) Java service using the `reporting-pipeline-service` [[helm-chart|Helm chart]] from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}. The service processes streamed events from [[kafka]] and loads domain-specific reporting data.

Deploying the Java service is a two-phase process. The first deployment seeds the `nrt_*` caching tables that RTR depends on. Once seeding is complete, you upgrade the release with post-processing enabled. If you are reinstalling RTR after a backup and restore and need to reseed those tables, see [Delete Kafka topics before reinstalling RTR](#delete-kafka-topics-before-reinstalling-rtr) first.

> Schedule a maintenance window and notify users that NBS will be unavailable. Database changes made while the RTR service is being deployed might not propagate to your reporting database.
{: .important }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

This page assumes you've completed [Before you begin](../deploy-nbs7-microservices.html#before-you-begin) for the microservices phase and each microservice deployment page before this one, in order. The page immediately before this one is [Kafka connector](./kafka-connector.html).

Confirm the following before you continue:

- You are connected to the correct [[kubernetes]] cluster. Run `kubectl config current-context` to confirm.
- You have your database credentials and domain values available. See the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) if you need help determining any values.

> Deploying the Java service takes significant time and database space. Before you deploy, verify that the Kafka cluster you created in [Provision cloud environment](../../full-deploy/provision-cloud-infrastructure/provision-cloud-environment.html) is scaled for your database size. An undersized Kafka cluster can cause the deployment to fail.
{: .important }

### Delete Kafka topics before reinstalling RTR

This section applies only if after a backup and restore, you need to re-seed the `nrt_*` tables. Otherwise, skip to [Deploy the RTR Java service using Helm](#deploy-the-rtr-java-service-using-helm).

Before you reinstall, delete the following Kafka topics. This ensures Debezium fully reruns the seeding process.

- `odse-main.history`
- `odse-main-schema-history`
- `odse-act-rel.history`
- `odse-act-rel-schema-history`
- `history.odse_meta`
- `odse-meta-schema-history`
- `history.srte`
- `srte-schema-history`

> Deleting these topics is irreversible. Delete them only if you are reinstalling RTR.
{: .warning }

After you delete these topics, continue to [Deploy the RTR Java service using Helm](#deploy-the-rtr-java-service-using-helm).

## Deploy the RTR Java service using Helm

Complete the following steps to deploy the [`reporting-pipeline-service` Helm chart][nedss-helm-reporting-pipeline-service-chart] from the `charts/reporting-pipeline-service/` directory of your cloned NEDSS-Helm repository:

1. Search `values.yaml` for `EXAMPLE` and fill in your environment-specific values. See the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) for help determining values.
1. Confirm that post-processing is disabled in `values.yaml` for the initial deployment:

   ```yaml
   featureFlag:
     postProcessingEnable: "false"
   ```

1. Install the Helm chart:

   ```bash
   helm install -f reporting-pipeline-service/values.yaml reporting-pipeline-service ./reporting-pipeline-service/
   ```

1. Verify the pods are running:

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

Retrieve information on reporting-pipeline-service lag in your browser. Replace `<exampledomain>` with your actual domain (see [Deploy Traefik ingress controller](../../full-deploy/kubernetes-setup/deploy-core-services.html#deploy-traefik-ingress-controller)):

```text
https://data.<exampledomain>/reporting-pipeline-svc/actuator/lag
```

When all `messagesQueued` values are `0`, seeding is complete.

## Enable post-processing

After seeding is complete, upgrade the release with post-processing enabled:

1. Update `values.yaml` to enable post-processing:

   ```yaml
   featureFlag:
     postProcessingEnable: "true"
   ```

1. Upgrade the release:

   ```bash
   helm upgrade -f reporting-pipeline-service/values.yaml reporting-pipeline-service ./reporting-pipeline-service/
   ```

1. Verify the pods restarted cleanly:

   ```bash
   kubectl rollout status deployment/reporting-pipeline-service
   kubectl get deployment reporting-pipeline-service
   ```

1. Confirm the service is healthy. Replace `<exampledomain>` with your actual domain (see [Deploy Traefik ingress controller](../../full-deploy/kubernetes-setup/deploy-core-services.html#deploy-traefik-ingress-controller)):

   ```text
   https://data.<exampledomain>/reporting-pipeline-svc/actuator/health
   ```

## Next steps

Continue to [Validate RTR installation](rtr-validation.html).

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-reporting-pipeline-service-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/reporting-pipeline-service>
