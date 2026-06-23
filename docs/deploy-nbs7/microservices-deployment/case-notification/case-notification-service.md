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

This page walks through deploying the Case Notification service using the [case-notification-service][nedss-helm-case-notification-service-chart] Helm chart from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}. Complete [Debezium](./debezium.html) before starting this page. After you finish deploying the notification service, proceed to [API testing](./api-testing.html).

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Configure Keycloak

The notification service requires Keycloak. Complete this configuration before deploying it.

1. In `values.yaml`, confirm the Keycloak auth URI. In the default configuration, this value does not need to change unless the name or namespace of the Keycloak pod is modified:

   ```yaml
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   ```

1. Import the Keycloak profile from case notifications from [NEDSS-Helm/charts/keycloak/extra][nedss-helm-keycloak-extra]:
   1. In the NBS realm, open **Realm settings**, select the **Action** dropdown, and select **Partial Import**.
   1. Upload `09-nbs-users-case-notification-service.json` and select **Create**.

## Deploy the Case Notification service using Helm

1. Use Git to clone your own local copy of the public [NEDSS-Helm repository][nedss-helm]. The following steps use the files in `charts/case-notification-service/` from that repository.
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/case-notification-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Set the JDBC connection, Keycloak auth URI, and Kafka values. The `dbserver` value is the database server endpoint only. Do not include the port number. For help determining these values, see the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-for-nbs-7-microservices). For a full list of environment variables, see the [NEDSS-NNDSS-Case-Notifications README][nndss-case-notifications-readme] and the [case-notification-service deployment template][nedss-helm-case-notification-deployment].

   ```yaml
   ingressHost: "data.EXAMPLE_DOMAIN"

   jdbc:
     dbserver: "EXAMPLE_DB_ENDPOINT"
     username: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"

   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"

   kafka:
     cluster: "EXAMPLE_KAFKA_ENDPOINT"
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

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-case-notification-service-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/case-notification-service>
[nndss-case-notifications-readme]: <https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/blob/{{ site.version_latest_tag }}/README.md>
[nedss-helm-case-notification-deployment]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/charts/case-notification-service/templates/deployment.yaml>
[nedss-helm-keycloak-extra]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/keycloak/extra>
