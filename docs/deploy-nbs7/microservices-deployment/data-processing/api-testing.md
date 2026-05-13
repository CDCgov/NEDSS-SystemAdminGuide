---
title: API testing and integration
layout: page
parent: Data processing
nav_order: 1
redirect_from:
  - /docs/6_microservices_deployment/7a_data_processing_api_testing.html
  - /docs/6_microservices_deployment/7a_data_processing_api_testing/
---

# Test RTI API integration for Data Processing

Use this page to validate Real Time Ingestion (RTI) by sending ELR data through the Data Ingestion endpoint and verifying RTI processing outcomes.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Run the integration test

1. Follow the [Data Ingestion API testing guide](../../data-ingestion/api-testing.html) to submit ELR payloads.
1. Add the `version` request header in the ELR ingestion API call:
   - `version: 1` uses the legacy batch importer flow.
   - `version: 2` bypasses the legacy batch importer and triggers RTI.

   For RTI testing, this header is the only required API change.

   ![data-processing-api-testing-1](../images/data-processing-api-testing-1.jpg)

## Validate ingestion and RTI processing status

Use the DI status endpoint to verify processing status after submission.

- Legacy flow status values in `NBS_Interface`: `QUEUED`, `FAILED`, `SUCESS`.
- RTI flow status values in `NBS_Interface`: `RTI_QUEUED`, `RTI_FAILURE`, `RTI_SUCESS_STEP_N`.

RTI processing can complete in three status steps:

- `RTI_SUCESS_STEP_1`: Data passed through core processing and should be available in the ODSE database.
- `RTI_SUCESS_STEP_2`: Applies when a WDS algorithm is configured; the service runs WDS comparison.
- `RTI_SUCESS_STEP_3`: Triggered after WDS completes; the service assigns the appropriate action for the ingested payload.

![data-processing-flow-diagram](../images/data-processing-api-testing-2.jpg)

![data-processing-flow-diagram](../images/data-processing-api-testing-3.jpg)
