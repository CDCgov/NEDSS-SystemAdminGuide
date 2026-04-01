---
title: Data processing
layout: page
parent: Deploy NBS 7 microservices
nav_order: 7
has_children: true
redirect_from:
  - /docs/6_microservices_deployment/7_data_processing.html
  - /docs/6_microservices_deployment/7_data_processing/
---

# Deploy the Data Processing service for NBS 7

This page walks through deploying the Real Time Ingestion (RTI) data processing service.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Overview

RTI is a microservice that picks up ELR data after it has been ingested and queued in the NBS Interface table. It processes each record and either marks it as successful or delivers it to the NBS queue. Events are handled through Kafka — there is no direct user interaction with RTI. RTI is triggered through the Data Ingestion ELR endpoint and can work alongside the ELR importer batch job or replace it, providing near-real-time ELR processing without requiring a STLT-managed batch job.

![data-processing-flow-diagram](images/data-processing-flow-diagram.png)

## Deploy RTI using Helm

This section covers installing the NBS 7 RTI service.

### RTI microservice

1. Use the `values.yaml` file supplied in the `nbs-helm-vX.Y.Z.zip` release package. Set the **ECR repository**, **ECR image tag**, **database server endpoints**, and **ingress host** values.
   1. Navigate to the [NEDSS-Helm/releases](https://github.com/CDCgov/NEDSS-Helm/releases) page.
   1. Scroll down to the Assets listed for the latest or previous releases.
   1. Download the zip file for the release.
   1. Find the `values.yaml` file under `charts\data-processing-service`.

1. Confirm that a DNS entry for the following host was created and points to the network load balancer in front of your Kubernetes cluster (this must be the **ACTIVE NLB** provisioned by `nginx-ingress` in the base install steps). Make this change in your authoritative DNS service (for example, Route 53). Replace `example.com` with your domain name in `values.yaml`.

   Data processing service application: `dataprocessingservice.example.com`
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-processing-service"
     pullPolicy: IfNotPresent
      tag: <release-version-tag> # for example, v1.0.1
   ```

1. Set the auth user. RTI uses a valid NBS user to process data. Set `nbs.authuser` to a valid user from `ODSE.Auth_User`:

   ```yaml
   nbs:
     authuser: "superuser"
   ```

   To find valid auth users, query the ODSE database:

   ```sql
   SELECT * FROM [NBS_ODSE].[dbo].[Auth_user]
   ```

1. Set the JDBC connection values. The `dbserver` value is the database server endpoint only — do not include the port number. You can ignore the `ingress`, `ingressHost`, and other unrelated fields.
   ![data-processing-dbendpoint](images/data-processing-dbendpoint.png)

    ```yaml
    jdbc:
       dbserver: "EXAMPLE_DB_ENDPOINT"
       username: "EXAMPLE_ODSE_DB_USER"
       password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
    nbs:
       authuser: "EXAMPLE_NBS_AUTHUSER"
    kafka:
       cluster: "EXAMPLE_MSK_KAFKA_ENDPOINT"
    dataingestion:
       uri: "data.EXAMPLE.DOMAIN"
    keycloak:
       srte:
          clientId: "EXAMPLE_SRTE_CLIENT_ID"
          clientSecret: "EXAMPLE_SRTE_CLIENT_SECRET"
    ```

1. Install the data processing service:

   ```bash
   helm install data-processing-service -f ./data-processing-service/values.yaml data-processing-service
   ```

   Confirm the pod is running before continuing:

   ```bash
   kubectl get pods
   ```

1. See [RTI API testing and integration](../../deploy-nbs7/microservices-deployment/data-processing/api-testing.html) for API testing guidance.
1. Validate the service:

   ```text
   https://<data.EXAMPLE_DOMAIN>/rti/actuator/info
   https://<data.EXAMPLE_DOMAIN>/rti/actuator/health
   ```
