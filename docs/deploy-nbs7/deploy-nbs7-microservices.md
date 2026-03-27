---
title: Deploy NBS 7 microservices
layout: page
parent: Deploy NBS 7
nav_order: 5
has_children: true
description: Install and configure NBS 7 application services using Helm, including Elasticsearch, NiFi, the Modernization API, and optional add-ons such as Real-Time Reporting.
---

# Deploy NBS 7 microservices
{: .no_toc }

This phase deploys the NBS 7 application services into your Kubernetes cluster using Helm. Deploy services in the order listed — each service has dependencies on the ones before it.

After completing this phase, proceed to [Validate the deployment](validate-the-deployment.html).

## Overview

We will use HELM CLI to deploy NBS microservices into Kubernetes cluster. Please deploy the helm charts in the following order. Verify that each microservice has started successfully before moving on to the next service.

- elasticsearch-efs
- modernization-api
- nifi-efs
- nbs-gateway
- dataingestion
- data-processing
- nnd (data-sync)
- case notifications

Have the jdbc connection details handy for modernization-api, nifi-efs, data-ingestion, data processing and case notifications services

| Parameter     | Example                                                       |
|---------------|----------------------------------------------------------------|
| db_endpoint   | mySTLT-dbname.abcdefghij.us-east-1.rds.amazonaws.com          |
| port          | 1433                                                           |
| databaseName  | NBS_ODSE                                                       |
| DBUsername    | nbs_ods                                                        |
| DBPassword    | *myrandompassword*                                             |

**NOTE** - Run the helm install commands from the charts directory for all the microservices. And before running the helm install commands, make sure you are authenticated to aws with aws sts get-caller-identity
