---
title: Data Processing
layout: page
parent: Microservices Deployment
nav_order: 7
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Data Processing Service Introduction
This guide is designed to assist clients who are working with RTI. RTI is a service that is highly dependent on Data Ingestion. It is designed to pick up ELR data once it has been ingested and queued in the NBS Interface table. RTI will process the data and either mark it as successful or deliver it into the NBS queue. RTI is a microservice where events are handled by Kafka events. There will be no direct interaction between the end user and RTI. RTI can only be triggered via the data ingestion ELR endpoint. This guide will highlight the steps on how to make that happen.

## Flow Diagram

![data-processing-flow-diagram](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/images/data-processing-flow-diagram.png)

## Deploy RTI ( Real Time Ingestion “data-processing-service”) via helm chart
This guide outlines the detailed steps to install the NBS 7 RTI service, which will process ELR data after it is ingested by data ingestion. RTI can work side by side with the ELR importer batch job or replace it. RTI provides a seamless way to process ELR in near real-time instead of depending on the system-bounded ELR batch job. This eliminates the need for the STLT to set up a batch job on their system.

### RTI micro service
1. Please use the values file supplied as part of nbs-helm-vX.Y.Z.zip file. Use this [link](https://github.com/CDCgov/nbs-helm/releases) to download the zip file (scroll down to the Assets listed for the latest or previous releases). The values.yaml file should be under charts\data-processing-service\values.yaml .
Values for ECR repository, ECR image tag, db server endpoints, and ingress host should be provided in the values.yaml file.
2. Confirm that the following DNS entry were created and pointed to the network load balancer in front of your Kubernetes cluster (Make sure this is the ACTIVE NLB provisioned via nginx-ingress in the base install steps ). This should be done in your authoritative DNS service(e.g. Route 53). Please replace http://example.com with the appropriate domain name in the values.yaml file.
data processing service Application - e.g. dataprocessingservice.example.com
3. Update the image repository and tag with the following:
   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-processing-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag> e.g v1.0.1
   ```
4. Update auth user in value files, this variable allow RTI to use the valid NBS user to process the data
  - a. List of Auth user can be found in ODSE.Auth_User
    ```yaml
    nbs:
      authuser: "superuser"
    ```
  - b. ```sql
      SELECT * FROM [NBS_ODSE].[dbo].[Auth_user]
    ```
5. Update the values file with the jdbc connection values in the following format:
   - The dbserver value is just a database server endpoint. Please don't include the port number
   ![data-processing-dbendpoint](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/images/data-processing-dbendpoint.png)
   - Note: Please ignore all the other values such as ingress, ingressHost, etc.
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

6. Data processing service helm chart:
   After updating the values file, Run the following command to install data-processing-service.
    ```bash
    helm install data-processing-service -f ./data-processing-service/values.yaml data-processing-service
    ```
    - Note: Check to see if the pod for data-processing-service is running using kubectl get pods
7. API Testing Guide: [RTI API Testing and Integration](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/7a_data_processing_api_testing.html#data-processing-api-testing-and-integration)
8. Validate the service
   ```
   https://<data.EXAMPLE_DOMAIN>/rti/actuator/info
   https://<data.EXAMPLE_DOMAIN>/rti/actuator/health
   ```

