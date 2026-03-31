---
title: API Smoke Test (Scripted)
layout: page
parent: Validate ES, Mapi and Nifi
grand_parent: Deploy NBS 7 microservices
nav_order: 2
nav_enabled: true
redirect_from:
  - /docs/6_microservices_deployment/5b_api_smoke_test.html
  - /docs/6_microservices_deployment/5b_api_smoke_test/
  - /docs/3_base_application/api-smoke-test.html
  - /docs/3_base_application/api-smoke-test/
---

# API Smoke Test (Scripted)
{: .no_toc }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

`nbs-test-api.sh` script is included in the infrastructure zip file (`scripts/observability/nbs-test-api`)

It will:

- create a patient
- search for the patient
- delete that patient (note: record still exists but is inactive)

It is a bash script that can be run via CloudShell if NBS is hosted in AWS or by any system with bash installed. It requires a user in the database that can run API calls.

**Curl** is the only other dependency.

---

## USAGE

nbs-test-api.sh [-h] [-?] [-d] [-D] [-P] [-B BASE_URL] [-U USER ] [-c count ]

For the initial smoke test run

nbs-test-api.sh -B `https://app.<your-site>.<your-domain>.com` -U <apiuser> -c 10

This will verify api functionality AND populate the observability dashboards with some initial traffic
