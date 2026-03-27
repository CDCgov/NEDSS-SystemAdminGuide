---
title: Notification service
layout: page
parent: Case notifications
nav_order: 5
nav_enabled: true
---

# Case Notification Service
{: .no_toc }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

1. Helm chart can be found under chart/case-notification-service
2. Validate the image tag

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/case-notification-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag> e.g v1.0.1
   ```

3. Update the jdbc configurations

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

   > The `api.clientId` and `api.secret` fields must match the Keycloak client credentials for the XML HL7 Parser service, not this service. Retrieve them from the `xml-hl7-parser-keycloak-client` credentials in the NBS realm.
   {: .note }

4. Install Pod

   ```bash
   helm install case-notification-service -f ./case-notification-service/values.yaml case-notification-service
   ```

5. Verify Pod

   ```bash
   kubectl get pods
   ```

6. Validate the service

   ```text
   https://<data.EXAMPLE_DOMAIN>/case-notification/actuator/info
   https://<data.EXAMPLE_DOMAIN>/case-notification/actuator/health
   ```
