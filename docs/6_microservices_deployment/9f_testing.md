---
title: API Testing
layout: page
parent: Case Notification
nav_order: 6
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

### Ingress setup

- All 3 case notification services are using the same data ingestion ingess. Use this existing setup as needed
  - **Data Extraction**: [NEDSS-Helm/charts/dataingestion-service/templates/ingress.yaml at 10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml)

  - **Case Notification**: [NEDSS-Helm/charts/dataingestion-service/templates/ingress.yaml at 10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml)

  - **HL7 Parser**: [NEDSS-Helm/charts/dataingestion-service/templates/ingress.yaml at 10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/10623c0d9788a6513bd51f4b6ed4eb0f79b30a2f/charts/dataingestion-service/templates/ingress.yaml)

### PHIMNS Properties

- For the services to be fully functional, the STLT need to provide CDC their PHIMS properties. This ensures the data in the `TransportQ_Out` table gets updated correctly when the data is being processed by the CDC Case Notification. These data can be pulled from the existing NND Rhapsody route’s Variable Manager on the STLT level.

  - **Require**
    - `nbs_certificate_url` – STLT most likely will have this hardcoded in the Rhapsody Variable Manager

  - **Optional** – these are optional, some STLT might have or need them:
    - `phin_encryption`
    - `phin_route`
    - `phin_signature`
    - `phin_public_key_address`
    - `phin_public_key_base_dn`
    - `phin_public_key_dn`
    - `phin_recipient`
    - `phin_priority`

- Once the data has been provided by the STLT, CDC should update the existing config on the CDC Case Notification config table:

  - **Table Name:** `NBS_Case_Notification_Config`
  - **Update record where config name is:** `NON_STD_CASE_NOTIFICATION`
  - **Update value:** Any values provided by STLT should be matched with the reflected column in the config table

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

### Extra Note and troubleshooting

#### Case Notification Environment Variable

1. **Case-Notification-Service**
   - a. [NEDSS-NNDSS-Case-Notifications/README.md at main · CDCgov/NEDSS-NNDSS-Case-Notifications](https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/blob/main/README.md)  
   - b. [NEDSS-Helm/charts/case-notification-service/templates/deployment.yaml at 521ac8cff59c4f693f5e1af74bed20bd7f3c698 · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/521ac8cff59c4f693f5e1af74bed20bd7f3c698/charts/case-notification-service/templates/deployment.yaml)

2. **Data-Extraction-Service**
   - a. [NEDSS-NNDSS-Case-Notifications/README.md at main · CDCgov/NEDSS-NNDSS-Case-Notifications](https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/blob/main/README.md)  
   - b. [NEDSS-Helm/charts/data-extraction-service/templates/deployment.yaml at 521ac8cff59c4f693f5e1af74bed20bd7f3c698 · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/521ac8cff59c4f693f5e1af74bed20bd7f3c698/charts/data-extraction-service/templates/deployment.yaml)

3. **Xml-Hl7-Parser-Service**
   - a. [NEDSS-NNDSS-Case-Notifications/README.md at main · CDCgov/NEDSS-NNDSS-Case-Notifications](https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/blob/main/README.md)  
   - b. [NEDSS-Helm/charts/xml-hl7-parser-service/templates/deployment.yaml at 521ac8cff59c4f693f5e1af74bed20bd7f3c698 · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/521ac8cff59c4f693f5e1af74bed20bd7f3c698/charts/xml-hl7-parser-service/templates/deployment.yaml)

---

#### Case Notification Liquibase

- Case Notification comes with a built-in Liquibase that automatically handles any DB changes upon deployment.
  - DB changes detail can be reviewed here:  
    - [NEDSS-NNDSS-Case-Notifications/case-notification-service/src/main/resources/db at main · CDCgov/NEDSS-NNDSS-Case-Notifications](https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/tree/main/case-notification-service/src/main/resources/db)
  - Please refer to Deploy Data Ingestion via Helm chart for how to deploy DI.

---

#### Liquibase DB Change Verification

- To verify whether the database changes were applied, first ensure the Case Notification container is stable and running; since the container manages Liquibase, it won't start if Liquibase fails.
- If there is failure by Liquibase, the DI pod will be unstable, and a specific error can be found within the container log.

---

#### Kafka

1. Use either one of the two Kafka broker endpoints (`Private endpoints - Plaintext`) in the Helm values file.

2. Required Debezium Source Connector on `NBS_ODSE..CN_TranportQ_Out` deployed first prior to the services deployment  
   - a. Detail link  
      - i. [NEDSS-Helm/charts/debezium/values.yaml at main · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/debezium/values.yaml)

---

#### Additional Case Notification Technical Documentations

[Technical Document ](https://cdc-nbs.atlassian.net/wiki/spaces/~636279befe5ff375235bc637/pages/1599045634/Technical+Document)
