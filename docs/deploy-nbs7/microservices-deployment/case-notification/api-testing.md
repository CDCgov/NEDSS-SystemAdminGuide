---
title: API testing
layout: page
parent: Case notifications
nav_order: 6
redirect_from:
  - /docs/6_microservices_deployment/9f_testing.html
  - /docs/6_microservices_deployment/9f_testing/
---

# Test and integrate case notification APIs

Use this page to validate ingress, PHIMNS property configuration, and supporting dependencies for case notification services.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Ingress setup

- Each notification service uses the same Data Ingestion ingress. Reuse the existing setup as needed.
  - **Data Extraction**: [NEDSS-Helm/charts/dataingestion-service/templates/ingress.yaml at 10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml)

  - **Case Notification**: [NEDSS-Helm/charts/dataingestion-service/templates/ingress.yaml at 10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml)

## PHIMNS properties

- For services to be fully functional, STLT partners must provide CDC their PHIMS properties. This ensures data in the `TransportQ_Out` table is updated correctly when processed by CDC Case Notification. These values can be pulled from the existing NND Rhapsody route Variable Manager at the STLT level.

  - **Required**
    - `nbs_certificate_url`: STLTs commonly keep this value hardcoded in the Rhapsody Variable Manager.

  - **Optional**: Some STLTs may have or need these:
    - `phin_encryption`
    - `phin_route`
    - `phin_signature`
    - `phin_public_key_address`
    - `phin_public_key_base_dn`
    - `phin_public_key_dn`
    - `phin_recipient`
    - `phin_priority`

- Once STLT values are provided, CDC should update the existing configuration in the case notification config table:

  - **Table Name:** `NBS_Case_Notification_Config`
  - **Update record where config name is:** `NON_STD_CASE_NOTIFICATION`
  - **Update value:** Match STLT-provided values to the corresponding columns in the config table.

  - **Update Script - DB:** `NBS_MSGOUTE`

    ```sql
    UPDATE NBS_Case_Notification_Config
    SET
      nbs_certificate_url    = 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED',
      phin_encryption        = 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED',
      phin_route             = 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED',
      phin_signature         = 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED',
      phin_public_key_address= 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED',
      phin_public_key_base_dn= 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED',
      phin_public_key_dn     = 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED',
      phin_recipient         = 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED',
      phin_priority          = 'REPLACE WITH VALUE, REMOVE IF NON IS PROVIDED'
    WHERE config_name = 'NON_STD_CASE_NOTIFICATION'
    ```

## Additional notes and troubleshooting

### Case notification environment variables

1. **Case-Notification-Service**
   - [NEDSS-NNDSS-Case-Notifications/README.md at main · CDCgov/NEDSS-NNDSS-Case-Notifications](https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/blob/main/README.md)
   - [NEDSS-Helm/charts/case-notification-service/templates/deployment.yaml at main · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/case-notification-service/templates/deployment.yaml)

1. **Data-Extraction-Service**
   - [NEDSS-NNDSS-Case-Notifications/README.md at main · CDCgov/NEDSS-NNDSS-Case-Notifications](https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/blob/main/README.md)
   - [NEDSS-Helm/charts/data-extraction-service/templates/deployment.yaml at main · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/data-extraction-service/templates/deployment.yaml)

### Case notification Liquibase

- Case Notification includes a built-in Liquibase integration that automatically applies database changes during deployment.
- DB changes detail can be reviewed here:
  - [NEDSS-NNDSS-Case-Notifications/case-notification-service/src/main/resources/db at main · CDCgov/NEDSS-NNDSS-Case-Notifications](https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/tree/main/case-notification-service/src/main/resources/db)
  - See Deploy Data Ingestion using Helm for Data Ingestion deployment guidance.

### Liquibase DB change verification

- To verify database changes were applied, first ensure the case notification container is stable and running. Because the container manages Liquibase, it will not start if Liquibase fails.
- If Liquibase fails, the DI pod will be unstable, and specific errors can be found in container logs.

### Kafka

1. Use either one of the two Kafka broker endpoints (`Private endpoints - Plaintext`) in the Helm values file.

1. Deploy the required Debezium Source Connector on `NBS_ODSE..CN_TranportQ_Out` before deploying the services.
   - Details: [NEDSS-Helm/charts/debezium/values.yaml at main · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/debezium/values.yaml)

### Additional case notification technical documentation

[Technical Document](../images/Technical%20Document.pdf)
