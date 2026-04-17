---
title: Notification service
layout: page
parent: Case notifications
nav_order: 5
redirect_from:
  - /docs/6_microservices_deployment/9e_case_notification.html
  - /docs/6_microservices_deployment/9e_case_notification/
---

# Deploy Case Notification Service for NBS 7 case notifications

This page walks through deploying the Case Notification Service for case notification processing.

1. Locate the Helm chart at `charts/case-notification-service`.
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/case-notification-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Update JDBC and service configuration values:

   ```yaml
   ingressHost: "data.EXAMPLE_DOMAIN"

   jdbc:
     dbserver: "EXAMPLE_DB_ENDPOINT"
     username: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"

   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"

   kafka:
     cluster: "EXAMPLE_MSK_KAFKA_ENDPOINT"
   ```

   {: .note }

1. Install the service:

   ```bash
   helm install case-notification-service -f ./case-notification-service/values.yaml case-notification-service
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

1. Validate the service:

   ```text
   https://<data.EXAMPLE_DOMAIN>/case-notification/actuator/info
   https://<data.EXAMPLE_DOMAIN>/case-notification/actuator/health
   ```
