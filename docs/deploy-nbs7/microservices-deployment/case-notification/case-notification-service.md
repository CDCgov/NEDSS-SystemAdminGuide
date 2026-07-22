---
title: Notification service
layout: page
parent: Case notifications
nav_order: 2
redirect_from:
  - /docs/6_microservices_deployment/9e_case_notification.html
  - /docs/6_microservices_deployment/9e_case_notification/
---

# Deploy the Case Notification service for NBS 7

This page walks through deploying the Case Notification service using the [case-notification-service][nedss-helm-case-notification-service-chart] Helm chart from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

This page assumes you've completed [Before you begin](../deploy-nbs7-microservices.html#before-you-begin) for the microservices phase and each microservice deployment page before this one, in order. The page immediately before this one is [Debezium Kafka connector deployment](./debezium.html) for case notifications.

- Have your database credentials, domain values, and Kafka endpoint available. See the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) for help determining any values.
- Confirm that the `case-notification-service` Keycloak client has been imported. See [Import service clients and retrieve secrets](../../full-deploy/kubernetes-setup/deploy-keycloak.html#import-service-clients-and-retrieve-secrets) if you need help.

## Deploy the Case Notification service using Helm

Complete the following steps to deploy the ['case-notification-service' Helm chart][nedss-helm-case-notification-service-chart] from the `charts/case-notification-service/` directory of your cloned NEDSS-Helm repository:

1. In the `case-notification-service/values.yaml` file, search for `EXAMPLE` and fill in your environment-specific values for the ingress host, JDBC connection, and Kafka cluster endpoint. The `dbserver` value is the database server endpoint only; do not include the port number. The [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) lists the values to use. For a full list of environment variables, see the [NEDSS-NNDSS-Case-Notifications README][nndss-case-notifications-readme] and the [case-notification-service deployment template][nedss-helm-case-notification-deployment].
1. <!-- [SME REVIEW] This value isn't in the Helm values reference table yet. Confirm whether to add it there or keep it documented here before removing this walkthrough. -->
   Set the Keycloak auth URI:

   ```yaml
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   ```

1. Install the Case Notification service:

   ```bash
   helm install "case-notification-service" ./case-notification-service -f ./case-notification-service/values.yaml
   ```

1. Confirm the pod is running before continuing:

   ```bash
   kubectl get pods
   ```

## Validate the deployment

Use the actuator endpoints to confirm the service is running.

Run the info endpoint to confirm the service version and build details:

```text
https://<data.EXAMPLE_DOMAIN>/case-notification/actuator/info
```

Run the health endpoint to confirm the service is running:

```text
https://<data.EXAMPLE_DOMAIN>/case-notification/actuator/health
```

After confirming a successful deployment, you can [test and integrate case notification APIs](./api-testing.html), and then proceed to deploy the [data ingestion service (DI API)](../data-ingestion/data-ingestion.html) or [real-time reporting (RTR)](../real-time-reporting/real-time-reporting.html) based on your deployment plan.

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-case-notification-service-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/case-notification-service>
[nndss-case-notifications-readme]: <https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/blob/{{ site.version_latest_tag }}/README.md>
[nedss-helm-case-notification-deployment]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/case-notification-service/templates/deployment.yaml>
