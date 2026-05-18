---
title: XML HL7 parser
layout: page
parent: Case notifications
nav_order: 3
redirect_from:
  - /docs/6_microservices_deployment/9c_xml_hl7_parser.html
  - /docs/6_microservices_deployment/9c_xml_hl7_parser/
---

# Deploy XML HL7 Parser Service for NBS 7 case notifications

This page walks through deploying the XML HL7 Parser Service used by case notification workflows.

1. Locate the Helm chart at `charts/xml-hl7-parser-service`.
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/xml-hl7-parser-service"
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
   ```

1. Install the service:

   ```bash
   helm install xml-hl7-parser-service -f ./xml-hl7-parser-service/values.yaml xml-hl7-parser-service
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

1. Validate the service:

   ```text
   https://<data.EXAMPLE_DOMAIN>/hl7-parser/actuator/info
   https://<data.EXAMPLE_DOMAIN>/hl7-parser/actuator/health
   ```
