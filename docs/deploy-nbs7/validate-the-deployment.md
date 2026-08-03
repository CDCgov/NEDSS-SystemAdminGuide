---
title: Validate deployment
layout: page
parent: Deploy NBS 7
nav_order: 5
has_toc: false
description: Confirm that every deployed NBS 7 component was validated, then run system-level checks across the full deployment before go-live.
---

# Validate your NBS 7 deployment

Each NBS 7 component includes its own validation steps as part of its deployment page. This page has two purposes: to confirm that you completed the validation for every component you deployed, and to run the system-level checks that can only be done once the full deployment is in place.

<!-- [SME REVIEW] The system-level checks in this page are drafted from the components and data flows documented elsewhere in the guide. -->

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Before you validate

Confirm the following before you start:

- Deployment of all required components is complete.
- A development or staging environment is available with representative test data.
- You have admin credentials to access the NBS UI.
- Your NBS 6 database refresh is complete and accessible from the test environment.

## Confirm component validation

Each deployment page includes validation steps for that component. If you followed the full deployment, you completed these steps as you deployed each service. If you used the quick deployment path, or skipped any validation, complete it now using the linked pages.

Confirm that each component you deployed passed its validation:

| Component | What its validation confirms | Validation steps |
|:---|:---|:---|
| Elasticsearch, Modernization API, and NiFi | Name resolution works, routing between NBS 6 and NBS 7 is correct, database connectivity from NBS 7 components works, and search indices are created and populated | [Manual validation](microservices-deployment/validate-es-mapi-nifi/manual-validation.html) |
| Modernization API | API endpoints respond and return expected results | [API smoke test](microservices-deployment/validate-es-mapi-nifi/api-smoke-test.html) |
| NBS UI and patient search | The NBS interface is accessible and patient search returns results | [Web UI smoke test](microservices-deployment/validate-es-mapi-nifi/web-ui-smoke-test.html) |
| Data ingestion | Individual ELR and eCR messages are accepted and routed correctly | [Smoke test](microservices-deployment/data-ingestion/smoke-test.html) |
| Data ingestion API | Data ingestion API endpoints are reachable and functioning | [API testing](microservices-deployment/data-ingestion/api-testing.html) |
| Data processing | Data processing handles ELR data correctly and returns expected status codes | [API testing and integration](microservices-deployment/data-processing/api-testing.html) |
| Case notifications | The Case Notification service processes and routes notifications correctly | [API testing](microservices-deployment/case-notification/api-testing.html) |
| NND service (Data Sync) | Data Sync API endpoints are reachable and credentials are valid | [Validate API endpoints](microservices-deployment/nnd-service/validating-api-endpoints.html) |

<!-- [SME REVIEW] Add rows for any component whose validation is not yet represented (eg, RTR). -->

## Run system-level checks

The following system-level checks confirm that the services work together and that data flows correctly across the full deployment. Run them after all component validation passes:

1. Log in to the NBS UI, for example at `https://app.<your-domain>/nbs/login`.
1. Confirm that patient search returns results using test records.
1. Create a test investigation and confirm that it appears correctly in the UI.
1. Confirm that ELR data ingested during testing is visible in the UI and correctly attributed. This confirms the full ingestion path, from the Data Ingestion API through to display.
1. Review application logs across services for unexpected errors or warnings.
1. Confirm that monitoring and alerting are configured and capturing baseline metrics across the deployment.

<!-- [SME REVIEW] End-to-end data-flow tracing is the highest-value go-live check but is drafted here at a high level. Confirm with engineering the specific path a test ELR should follow and what a healthy result looks like at each stage, and whether an equivalent end-to-end check exists for the case notification and reporting paths. -->

## Confirm monitoring and go-live readiness

When all component validation and system-level checks pass, your deployment is ready for go-live. To remove temporary deployment artifacts and tighten access, continue to [Post-deploy cleanup](full-deploy/post-deploy-cleanup.html).
