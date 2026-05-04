---
title: Deploy NBS 7 microservices
layout: page
parent: Deploy NBS 7
nav_order: 6
has_children: true
redirect_from:
  - /docs/6_microservices_deployment/0_microservices_deployment.html
  - /docs/6_microservices_deployment/0_microservices_deployment/
description: Install and configure NBS 7 application services using Helm, including Elasticsearch, NiFi, the Modernization API, and optional add-ons such as Real-Time Reporting.
---

# Deploy NBS 7 microservices
{: .no_toc }

This phase deploys the NBS 7 application services into your Kubernetes cluster using Helm. Deploy services in the order listed — each service has dependencies on the ones before it.

> The pages in this section apply to NBS {{ site.version_latest }}. Github repo links are pinned to `{{ site.version_latest_tag }}`.
{: .note }

After completing this phase, proceed to [Validate the deployment](validate-the-deployment.html).

## Overview

Use the Helm CLI to deploy NBS 7 microservices into your Kubernetes cluster. Deploy the Helm charts in the following order. Verify that each microservice starts successfully before moving to the next service.

- `elasticsearch-efs`
- `modernization-api`
- `nifi-efs`
- [Validate ES, Mapi and Nifi](microservices-deployment/validate-es-mapi-nifi.html)
- `nbs-gateway`
- `dataingestion-service`
- `data-processing`
- `nnd-service` (Data Sync)
- `case-notification`

Have JDBC connection details available for `modernization-api`, `nifi-efs`, `dataingestion-service`, `data-processing`, and `case-notification`.

| Parameter     | Example                                                       |
|---------------|----------------------------------------------------------------|
| db_endpoint   | mySTLT-dbname.abcdefghij.us-east-1.rds.amazonaws.com          |
| port          | 1433                                                           |
| databaseName  | NBS_ODSE                                                       |
| DBUsername    | nbs_ods                                                        |
| DBPassword    | *myrandompassword*                                             |

> Run Helm install commands from the `charts` directory for all microservices. Before you run Helm install commands, verify you are authenticated to AWS by running `aws sts get-caller-identity`.
{: .note }
