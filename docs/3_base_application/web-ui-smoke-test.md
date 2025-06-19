---
title: Web UI Smoke Test (Scripted)
layout: page
parent: Validate ES, Mapi and Nifi
nav_order: 3
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Web UI Smoke Test (Scripted)

`nbs-test-webui.sh` script is included in the infrastructure zip file (`scripts/observability/nbs-test-webui`)

It will:
- login  
- save all needed tokens  
- navigate to advanced search  
- search for all female patients and check count  
- if count is 0, note error; if greater than zero, good!

It is a bash script that can be run via CloudShell if NBS is hosted in AWS or by any system with bash installed. **Curl** is the only other dependency.

---

## USAGE

nbs-test-webui.sh [-h] [-?] [-d] [-D] [-P] [-H BASE_HOST] [-U USER ] [-c count ]

e.g. ./nbs-test-webui.sh -d -H http://app.demo.nbspreview.com  -U exampleuser

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
