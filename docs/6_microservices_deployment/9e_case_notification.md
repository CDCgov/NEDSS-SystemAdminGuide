---
title: Case Notification Service
layout: page
parent: Case Notification
nav_order: 5
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Case Notification Service

1. Validate the image tag
   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/case-notification-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag> e.g v1.0.1
   ```
2. Update the jdbc configurations
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
3. Install Pod
   ```bash
   helm install case-notification-service -f ./case-notification-service/values.yaml case-notification-service
   ```
4. Verify Pod
   ```bash
   kubectl get pods
   ```
5. Validate the service
   ```
   https://<data.EXAMPLE_DOMAIN>/case-notification/swagger-ui/index.html#/
   https://<data.EXAMPLE_DOMAIN>/case-notification/actuator/info
   https://<data.EXAMPLE_DOMAIN>/case-notification/actuator/health
   ```
