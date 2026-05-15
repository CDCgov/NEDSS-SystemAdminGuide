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

1. Locate the Case Notification Service Helm chart in the [NEDSS-Helm repository][nedss-helm-case-notification-service-chart].
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

   api:
     host: "https://<data.EXAMPLE_DOMAIN>/hl7-parser"
     clientId: "EXAMPLE_XML-HL7-Parser_CLIENT_ID"
     secret: "EXAMPLE_XML-HL7-Parser_CLIENT_SECRET"
   ```

   The `api.clientId` and `api.secret` fields must match the Keycloak client credentials for the XML HL7 Parser service, not this service. Retrieve them from the `xml-hl7-parser-keycloak-client` credentials in the NBS realm.
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

[nedss-helm-case-notification-service-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/case-notification-service>
