---
title: Observation Reporting
layout: page
parent: Real Time Reporting (Preview)
nav_order: 4
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Real Time Reporting(RTR) Java services
1. The helm chart for all RTR java services should be available under charts/rtr.
2. In the values.yaml, replace all occurrences of app.EXAMPLE_DOMAIN with the URL of your modern app as shown in [Table](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/1_nginx_ingress_deployment.html#deploy-nginx-ingress-controller-on-the-kubernetes-cluster).
3. Validate image repository and tag:
   ```yaml
    investigation-reporting-servic:
      image:
         repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service/investigation-reporting-service"
         tag: <release-version-tag> e.g v1.0.1
    person-reporting-service:
        image:
             repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service/person-reporting-service"
             tag: <release-version-tag> e.g v1.0.1
    observation-reporting-service:
         image:
                repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service/observation-reporting-service"
                tag: <release-version-tag> e.g v1.0.1
    organization-reporting-servic:
            image:
                repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service/organization-reporting-service"
                tag: <release-version-tag> e.g v1.0.1
    ldfdata-reporting-servic:
            image:
                repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service/ldfdata-reporting-service"
                tag: <release-version-tag> e.g v1.0.1
    post-processing-reporting-servic:
            image:
                repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service/post-processing-reporting-service"
                tag: <release-version-tag> e.g v1.0.1
   ```
4. Update odse and kafka configurations
   ```yaml
   
   dburl:
    odse: "jdbc:sqlserver://<EXAMPLE_DB_ENDPOINT>:<PORT>;databaseName=NBS_ODSE;encrypt=true;trustServerCertificate=true;"
    rdb: "jdbc:sqlserver://<EXAMPLE_DB_ENDPOINT>:<PORT>;databaseName=rdb;encrypt=true;trustServerCertificate=true;"
   
   kafka:
    cluster: "EXAMPLE_KAFKA_CLUSTER"
   ```
5. Update the JDBC username and password for each of the services:
    ```yaml
       investigation-reporting:
         jdbc:
           username: "EXAMPLE_DB_USER"
           password: "EXAMPLE_DB_USER_PASSWORD"
       person-reporting:
         jdbc:
           username: "EXAMPLE_DB_USER"
           password: "EXAMPLE_DB_USER_PASSWORD"
       observation-reporting:
         jdbc:
           username: "EXAMPLE_DB_USER"
           password: "EXAMPLE_DB_USER_PASSWORD"
       organization-reporting:
         jdbc:
           username: "EXAMPLE_DB_USER"
           password: "EXAMPLE_DB_USER_PASSWORD"
       ldfdata-reporting:
         jdbc:
           username: "EXAMPLE_DB_USER"
           password: "EXAMPLE_DB_USER_PASSWORD"
       post-processing-reporting:
         jdbc:
           username: "EXAMPLE_DB_USER"
           password: "EXAMPLE_DB_USER_PASSWORD"
   ```
6. Update the feature flag for each of the services:
   ```yaml
   featureFlag:
     investigation-reporting:
        phcDatamartEnable: '''true'''
   ```
   
7.Install helm chart for all the RTR java services
   ```bash
   helm install rtr . -f values.yaml
   ```
8.Verify if pods are all running
   ```bash
   kubectl get pods
   ```
     Example Expected output:
      ```
      NAME                                                READY   STATUS           RESTARTS             AGE 
      rtr-java-services-investigation-reporting-<hash>    1/1     Running            0                  2m6s
      rtr-java-services-ldfdata-reporting-<hash>          1/1     Running            0                  2m6s
      rtr-java-services-observation-reporting-<hash>      1/1     Running            0                  2m6s
      rtr-java-services-organization-reporting-<hash>     1/1     Running            0                  2m6s
      rtr-java-services-person-reporting-<hash>           1/1     Running            0                  2m6s
      rtr-java-services-post-processing-reporting-<hash>  1/1     Running            0                  2m6s
      
9.Validate services (on browser)
   a. investigation-svc
   ```
   https://data.<exampledomain>/reporting/investigation-svc/status
   Expected: Investigation Service Status OK
   ```
    
   b. person-svc
   ```
   https://data.<exampledomain>/reporting/person-svc/status
   Expected: Person Service Status OK
   ```
   c. person-svc
   ```
   https://data.<exampledomain>/reporting/observation-svc/status
   Expected: Observation Service Status OK
   ```
   d. organization-svc
   ```
   https://data.<exampledomain>/reporting/organization-svc/status
   Expected: Organization Service Status OK
   ```
   e. ldfdata-svc
  ```
  https://data.<exampledomain>/reporting/ldfdata-svc/status
  Expected: LDFData Service Status OK
  ```
   f. post-processing-svc
  ```
  https://data.<exampledomain>/reporting/post-processing-svc/status
  Expected: Post Processing Service Status OK
  ```
