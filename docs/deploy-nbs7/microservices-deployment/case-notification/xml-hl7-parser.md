---
title: Xml Hl7 parser
layout: page
parent: Case notifications
nav_order: 3
nav_enabled: true
redirect_from:
  - /docs/6_microservices_deployment/9c_xml_hl7_parser.html
  - /docs/6_microservices_deployment/9c_xml_hl7_parser/
---

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Xml Hl7 Parser Service

1. Helm chart can be found under chart/xml-hl7-parser-service
2. Validate the image tag

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/xml-hl7-parser-service"
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
   ```

4. Install Pod

   ```bash
   helm install xml-hl7-parser-service -f ./xml-hl7-parser-service/values.yaml xml-hl7-parser-service
   ```

5. Verify Pod

   ```bash
   kubectl get pods
   ```

6. Validate the service

   ```text
   https://<data.EXAMPLE_DOMAIN>/hl7-parser/actuator/info
   https://<data.EXAMPLE_DOMAIN>/hl7-parser/actuator/health
   ```
