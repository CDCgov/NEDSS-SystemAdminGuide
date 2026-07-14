---
title: API testing
layout: page
parent: Case notifications
nav_order: 3
redirect_from:
  - /docs/6_microservices_deployment/9f_testing.html
  - /docs/6_microservices_deployment/9f_testing/
---

# Test and integrate case notification APIs

Use this page to validate PHIMNS property configuration and supporting dependencies for case notification services. Deploy the [Notification service](./case-notification-service.html) before starting this page.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Configure PHIMNS properties

The case notification service requires PHINMS (Public Health Information Network Messaging System) properties to route case notifications correctly. Complete the following steps to configure them.

1. Retrieve the following values from your integration engine configuration:
   - **Required** property:
      - `nbs_certificate_url`
   - **Optional** properties:
      - `phin_encryption`
      - `phin_route`
      - `phin_signature`
      - `phin_public_key_address`
      - `phin_public_key_base_dn`
      - `phin_public_key_dn`
      - `phin_recipient`
      - `phin_priority`

1. Share the values with your CDC partners. CDC will update the `NBS_Case_Notification_Config` table in `NBS_MSGOUTE` using the following script:

   ```sql
   USE NBS_MSGOUTE;
 
   UPDATE NBS_Case_Notification_Config
   SET
     nbs_certificate_url     = '<value>',
     phin_encryption         = '<value>',
     phin_route              = '<value>',
     phin_signature          = '<value>',
     phin_public_key_address = '<value>',
     phin_public_key_base_dn = '<value>',
     phin_public_key_dn      = '<value>',
     phin_recipient          = '<value>',
     phin_priority           = '<value>'
   WHERE config_name = 'NON_STD_CASE_NOTIFICATION'
   ```

> If you host NBS on-premises without CDC support, you have full database access and can run this script yourself.
{: .note }

## Verify Kafka configuration

The case notification service uses Kafka to receive events from the Debezium source connector. Correct Kafka configuration ensures that new records inserted into `NBS_ODSE.CN_transportq_out` are detected and routed through the pipeline.

- **Configure Kafka broker:** Use one of the available Kafka broker endpoints (`Private endpoints - Plaintext`) in the values file located in the [NEDSS-Helm/charts/debezium-case-notifications][nedss-helm-debezium-case-notifications] directory. The number of brokers varies by environment.
- **Confirm Debezium connector:** Confirm that the Debezium source connector deployed in [Deploy the Debezium Kafka source connector](./debezium.html) is running on the `NBS_ODSE.CN_transportq_out` table before proceeding.

## Verify deployment and database changes

The case notification service includes a built-in Liquibase integration that automatically applies database changes during deployment. Use the following checks to confirm the service deployed successfully and data is routing correctly.

- **Confirm pod status:** Confirm that the `case-notification-service` pod is stable and running. The pod will not start if Liquibase fails.
- **If Liquibase fails:** Check the pod logs for errors. Database change details can be reviewed in the [NEDSS-NNDSS-Case-Notifications repository][nndss-case-notifications-db].
- **If notifications do not appear:** Check the dead letter table (DLT). Faulty events that cannot be processed are routed to `MSGOUTE.case_notification_dlt`. Check this table if case notifications are not appearing in the expected output tables (`MSGOUTE.transportq_out` or `MSGOUTE.netsstransportq_out`).

After verifying these configurations, proceed to deploy the [data ingestion service (DI API)](../data-ingestion/data-ingestion.html) or [real-time reporting (RTR)](../real-time-reporting/real-time-reporting.html) based on your deployment plan.

[nndss-case-notifications-db]: <https://github.com/CDCgov/NEDSS-NNDSS-Case-Notifications/tree/{{ site.version_latest_tag }}/case-notification-service/src/main/resources/db>
[nedss-helm-debezium-case-notifications]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/debezium-case-notifications>
