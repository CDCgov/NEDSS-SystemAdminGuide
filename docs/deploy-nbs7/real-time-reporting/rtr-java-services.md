---
title: Java services
layout: page
parent: Deploy real-time reporting
nav_order: 4
description: Covers deployment of RTR Java services that transform Kafka events and load reporting datamarts.
redirect_from:
  - /docs/7_feature_preview/4_rtr_java_reporting_services.html
  - /docs/7_feature_preview/4_rtr_java_reporting_services/
---

# Deploy real-time reporting (RTR) Java services

> The Java reporting services are being consolidated in an upcoming release. The service validation URLs reflect the NBS 7.12 configuration.
{: .warning }

This page covers deploying the RTR Java services that process streamed events from Kafka and load domain-specific reporting data. Before proceeding, schedule a maintenance window and notify users that NBS will be unavailable. Database changes made while RTR services are being deployed might not propagate to your reporting database.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> These steps require a Unix-compatible shell. On Windows, use Git Bash, WSL, or an equivalent terminal emulator.
{: .note }

## Installing RTR Java services

Follow these steps to configure and deploy the RTR Java services Helm chart.

> Verify that you are connected to the correct Kubernetes cluster before proceeding. To confirm, run `kubectl config current-context`.
{: .important }

1. Locate the Helm chart for all RTR Java services in the [NEDSS-Helm repository][nedss-helm-rtr-chart].

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
   global.image.repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service"
   ```

1. Update feature flags for each service. Verify that `PHCMartETL.bat` is turned off before enabling updates to the PublicHealthCaseFact datamart via RTR:

   ```yaml
   featureFlag:
     investigation-reporting:
       phcDatamartEnable: '''true'''
   ```

1. Install the Helm chart for all RTR Java services:

   ```bash
   helm install rtr . -f values.yaml
   ```

1. Verify the pods are running:

   ```bash
   kubectl get pods
   ```

   Expected output:

   ```text
   NAME                                                READY   STATUS    RESTARTS   AGE
   rtr-java-services-investigation-reporting-<hash>    1/1     Running   0          2m6s
   rtr-java-services-ldfdata-reporting-<hash>          1/1     Running   0          2m6s
   rtr-java-services-observation-reporting-<hash>      1/1     Running   0          2m6s
   rtr-java-services-organization-reporting-<hash>     1/1     Running   0          2m6s
   rtr-java-services-person-reporting-<hash>           1/1     Running   0          2m6s
   rtr-java-services-post-processing-reporting-<hash>  1/1     Running   0          2m6s
   ```

1. Validate the services. Replace `<exampledomain>` with your actual domain (see [Deploy Traefik ingress controller](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-traefik-ingress-controller)):

   **investigation-svc**

   ```text
   https://data.<exampledomain>/reporting/investigation-svc/status
   Expected: Investigation Service Status OK
   ```

   **person-svc**

   ```text
   https://data.<exampledomain>/reporting/person-svc/status
   Expected: Person Service Status OK
   ```

   **observation-svc**

   ```text
   https://data.<exampledomain>/reporting/observation-svc/status
   Expected: Observation Service Status OK
   ```

   **organization-svc**

   ```text
   https://data.<exampledomain>/reporting/organization-svc/status
   Expected: Organization Service Status OK
   ```

   **ldfdata-svc**

   ```text
   https://data.<exampledomain>/reporting/ldfdata-svc/status
   Expected: LDFData Service Status OK
   ```

   **post-processing-svc**

   ```text
   https://data.<exampledomain>/reporting/post-processing-svc/status
   Expected: Post Processing Service Status OK
   ```

[nedss-helm-rtr-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/rtr>
[nedss-helm-k8-secrets-manifest]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/k8-manifests/nbs-secrets.yaml>
