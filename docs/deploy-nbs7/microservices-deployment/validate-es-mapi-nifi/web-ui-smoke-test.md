---
title: Web UI smoke test
layout: page
parent: Validate Elasticsearch, Modernization API, NiFi
nav_order: 3
redirect_from:
  - /docs/6_microservices_deployment/5c_web_ui_smoke_test.html
  - /docs/6_microservices_deployment/5c_web_ui_smoke_test/
  - /docs/3_base_application/web-ui-smoke-test.html
  - /docs/3_base_application/web-ui-smoke-test/
---

# Web UI smoke test for NBS interface and search

The `nbs-test-webui.sh` script tests end-to-end functionality through the NBS web interface by logging in, navigating to **Advanced Search**, and searching for patient records. Use this test to confirm that the NBS UI, search, and authentication are working correctly after deployment.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

- Authenticated access to your NBS environment
- A database user with access to patient records
- Bash (the script can run in AWS CloudShell or on any system with Bash installed)
- `curl`

## Run the smoke test

Run the `nbs-test-webui.sh` script from the [NEDSS-Infrastructure repository][nedss-infra-nbs-test-webui]. See the README in that folder for usage instructions and current script status.

[nedss-infra-nbs-test-webui]: <https://github.com/CDCgov/NEDSS-Infrastructure/tree/{{ site.version_latest_tag }}/scripts/observability/nbs-test-webui>
