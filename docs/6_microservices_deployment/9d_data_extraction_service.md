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

1. Validate the image tag
   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/data-extraction-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag> e.g v1.0.1
   ```
2. Update the jdbc configurations
   ```yaml
   jdbc:
     dbserver: ""
     username: "DBUsername"
     password: "DBPassword"
   
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"

   kafka:
     cluster: ""
   ```
3. Install Pod
   ```bash
   helm install -f ./<replce-with-service-name>/values.yaml <replce-with-service-name> ./<replce-with-service-name>/
   ```
4. Verify Pod
   ```bash
   kubectl get pods
   ```
5. Validate the service
   ```
   https://<exampledomain>/data-extraction/actuator/health
   https://<exampledomain>/data-extraction/actuator/info
   ```
