---
title: Web UI smoke test
layout: page
parent: Validate ES, MAPI, and NiFi
grand_parent: Deploy NBS 7 microservices
nav_order: 3
redirect_from:
  - /docs/6_microservices_deployment/5c_web_ui_smoke_test.html
  - /docs/6_microservices_deployment/5c_web_ui_smoke_test/
  - /docs/3_base_application/web-ui-smoke-test.html
  - /docs/3_base_application/web-ui-smoke-test/
---

# Web UI smoke test for NBS interface and search

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

The `nbs-test-webui.sh` script is in the [NEDSS-Infrastructure repository][nedss-infra-nbs-test-webui].

This script will:

- Log in
- Save required tokens
- Navigate to Advanced Search
- Search for all female patients and check the count
- Report an error if the count is 0

This Bash script can run using CloudShell if NBS is hosted in AWS, or on any system with Bash installed. `curl` is the only other dependency.

## Usage

```bash
nbs-test-webui.sh [-h] [-?] [-d] [-D] [-P] [-H BASE_HOST] [-U USER] [-c count]
```

For example:

```bash
./nbs-test-webui.sh -d -H http://app.<your-site>.<your-domain>.com -U exampleuser
```

| **Flag** | **Description** |
|----------|------------------|
| `-h`     | will echo usage |
| `-?`     | will echo usage |
| `-d`     | will turn on debugging |
| `-D`     | will turn on debugging |
| `-P`     | will prompt at each step |
| `-H`     | base host for hitting webui |
| `-B`     | baseurl url for hitting API |
| `-U`     | user in the database with access to create and delete patients |
| `-c`     | count number of iterations, default is 1 |

[nedss-infra-nbs-test-webui]: <https://github.com/CDCgov/NEDSS-Infrastructure/tree/{{ site.version_latest_tag }}/scripts/observability/nbs-test-webui>
