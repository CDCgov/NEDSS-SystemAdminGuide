---
title: Validate deployment
layout: page
parent: Deploy NBS 7
nav_order: 9
has_children: true
description: Confirm that all deployed NBS 7 components are functioning correctly before go-live, including microservice health, data ingestion pipelines, and NBS UI behavior.
---

# Validate your NBS 7 deployment

Before go-live, confirm that all deployed components are functioning correctly and that data flows as expected from ingestion through to the NBS interface. Work through validation in sequence: start with core microservices, then confirm ingestion and notification pipelines, then run system-level checks across the NBS UI.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Before you validate

Confirm the following before starting:

- Deployment of all required microservices is complete for your chosen configuration
- A development or staging environment is available with representative test data
- You have admin credentials to access the NBS UI
- Your NBS 6 database refresh is complete and accessible from the test environment

## Validation sequence

Work through the areas in this table in order. Resolve failures before moving to the next area.

| Validation area | What it confirms | Documentation |
|:---|:---|:---|
| Elasticsearch, Modernization API, and NiFi (manual validation) | Name resolution is working; routing between NBS 6 and NBS 7 subsystems is correct; database connectivity from NBS 7 components is working; search indices are created and populated | [Manual validation](microservices-deployment/validate-es-mapi-nifi/manual-validation.html) |
| Modernization API smoke test | API endpoints respond and return expected results | [API smoke test](microservices-deployment/validate-es-mapi-nifi/api-smoke-test.html) |
| NBS UI and patient search smoke test | The NBS interface is accessible and patient search returns results | [Web UI smoke test](microservices-deployment/validate-es-mapi-nifi/web-ui-smoke-test.html) |
| Data ingestion smoke test | Individual ELR and eCR messages are accepted and routed correctly | [Smoke test](data-ingestion/smoke-test.html) |
| Data ingestion API testing | Data ingestion API endpoints are reachable and functioning | [API testing](data-ingestion/api-testing.html) |
| Data processing RTI integration | Real Time Ingestion processes ELR data correctly and returns expected status codes | [API testing and integration](microservices-deployment/data-processing/api-testing.html) |
| Case notification API testing | Case notification service is processing and routing notifications correctly | [API testing](microservices-deployment/case-notification/api-testing.html) |
| NND service API endpoints | Data sync API endpoints are reachable and credentials are valid | [Validate API endpoints](microservices-deployment/nnd-service/validating-api-endpoints.html) |
| RTR pipeline validation | Streaming updates flow from ingestion through to reporting datamart tables | [Pipeline validation](real-time-reporting/pipeline-validation.html) |

## System-level checks

After all component-level validation passes, confirm overall system behavior before proceeding to go-live:

1. Log in to the NBS UI (for example, `https://app.example.com/nbs/login`).
1. Verify that patient search returns results using test records.
1. Create a test investigation and confirm it appears correctly in the UI.
1. Confirm that ELR data ingested during testing is visible and correctly attributed.
1. Review application logs across services for unexpected errors or warnings.
1. Confirm that monitoring and alerting are configured and capturing baseline metrics.

## Next steps

When all validation areas pass, finalize your cutover checklist and launch NBS 7 in production.
