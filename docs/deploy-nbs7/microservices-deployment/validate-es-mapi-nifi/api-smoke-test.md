---
title: API smoke test
layout: page
parent: Validate Elasticsearch, Modernization API, NiFi
nav_order: 2
redirect_from:
  - /docs/6_microservices_deployment/5b_api_smoke_test.html
  - /docs/6_microservices_deployment/5b_api_smoke_test/
  - /docs/3_base_application/api-smoke-test.html
  - /docs/3_base_application/api-smoke-test/
---

# API smoke test for Modernization API

The `nbs-test-api.sh` script tests end-to-end API functionality by creating a patient record, searching for it, and marking it inactive. Use this test to confirm the Modernization API is responding correctly after deployment.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

To run the smoke test, you need:

- Authenticated access to your NBS environment
- A database user that can run API calls
- A shell environment with `curl` installed (AWS CloudShell works if you use it, or any system with Bash and `curl` available)

## Run the smoke test

Run the `nbs-test-api.sh` script from the [NEDSS-Infrastructure repository][nedss-infra-nbs-test-api]. See the `README` in that folder for usage instructions and current script status.

After performing a successful smoke test, continue to the [Web UI smoke test for NBS interface and search](./web-ui-smoke-test.html).

[nedss-infra-nbs-test-api]: <https://github.com/CDCgov/NEDSS-Infrastructure/tree/{{ site.version_latest_tag }}/scripts/observability/nbs-test-api>
