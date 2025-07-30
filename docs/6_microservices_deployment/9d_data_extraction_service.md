---
title: Data Extraction
layout: page
parent: Case Notification
nav_order: 4
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Data Extraction Service

1. Helm chart can be found under chart/data-extraction-service
2. Validate the image tag
   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/data-extraction-service"
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
   ```
4. Install Pod
   ```bash
   helm install data-extraction-service -f ./data-extraction-service/values.yaml data-extraction-service
   ```
5. Verify Pod
   ```bash
   kubectl get pods
   ```
6. Validate the service
   ```
   https://<data.EXAMPLE_DOMAIN>/data-extraction/actuator/health
   https://<data.EXAMPLE_DOMAIN>/data-extraction/actuator/info
   ```
