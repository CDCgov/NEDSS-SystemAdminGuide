---
title: Microservices Deployment
layout: page
nav_order: 7
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## NBS Microservices Deployment
We will use HELM CLI to deploy NBS microservices into Kubernetes cluster. Please deploy the helm charts in the following order. Verify that each microservice has started successfully before moving on to the next service.
- elasticsearch-efs
- modernization-api
- nifi-efs
- nbs-gateway
- dataingestion
- data-processing
- nnd (data-sync)
- case notifications

Have the jdbc connection details handy for page-builder-api, modernization-api, and nifi-efs

| Parameter     | Example                                                       |
|---------------|----------------------------------------------------------------|
| db_endpoint   | mySTLT-dbname.abcdefghij.us-east-1.rds.amazonaws.com          |
| port          | 1433                                                           |
| databaseName  | NBS_ODSE                                                       |
| DBUsername    | nbs_ods                                                        |
| DBPassword    | *myrandompassword*                                             |

**NOTE** - Run the helm install commands from the charts directory for all the microservices. And before running the helm install commands, make sure you are authenticated to aws with aws sts get-caller-identity
