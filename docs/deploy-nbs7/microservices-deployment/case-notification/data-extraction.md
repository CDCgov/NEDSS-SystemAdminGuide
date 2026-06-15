---
title: Data extraction
layout: page
parent: Case notifications
nav_order: 4
redirect_from:
  - /docs/6_microservices_deployment/9d_data_extraction_service.html
  - /docs/6_microservices_deployment/9d_data_extraction_service/
---

# Deploy Data Extraction Service for NBS 7 case notifications

This page walks through deploying the Data Extraction Service for case notification workflows.

1. Locate the Data Extraction Service Helm chart in the [NEDSS-Helm repository][nedss-helm-data-extraction-service-chart].
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-case-notification-service/data-extraction-service"
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
     cluster: "EXAMPLE_KAFKA_ENDPOINT"
   ```

1. Install the service:

   ```bash
   helm install data-extraction-service -f ./data-extraction-service/values.yaml data-extraction-service
   ```

1. Verify the pod is running:

   ```bash
   kubectl get pods
   ```

1. Validate the service:

   ```text
   https://<data.EXAMPLE_DOMAIN>/data-extraction/actuator/health
   https://<data.EXAMPLE_DOMAIN>/data-extraction/actuator/info
   ```

[nedss-helm-data-extraction-service-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/data-extraction-service>
