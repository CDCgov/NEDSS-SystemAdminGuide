---
title: API smoke test
layout: page
parent: Validate ES, MAPI, and NiFi
grand_parent: Deploy NBS 7 microservices
nav_order: 2
redirect_from:
  - /docs/6_microservices_deployment/5b_api_smoke_test.html
  - /docs/6_microservices_deployment/5b_api_smoke_test/
  - /docs/3_base_application/api-smoke-test.html
  - /docs/3_base_application/api-smoke-test/
---

# API smoke test for Modernization API

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

The `nbs-test-api.sh` script is included in the infrastructure zip file at `scripts/observability/nbs-test-api`.

This script will:

- Create a patient
- Search for the patient
- Delete that patient (the record still exists but is inactive)

This Bash script can run using CloudShell if NBS is hosted in AWS, or on any system with Bash installed. It requires a database user that can run API calls.

`curl` is the only other dependency.

## Usage

```bash
nbs-test-api.sh [-h] [-?] [-d] [-D] [-P] [-B BASE_URL] [-U USER] [-c count]
```

For the initial smoke test run:

```bash
nbs-test-api.sh -B https://app.<your-site>.<your-domain>.com -U <apiuser> -c 10
```

This command verifies API functionality and populates the observability dashboards with initial traffic.
