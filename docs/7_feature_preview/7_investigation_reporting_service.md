---
title: Investigation Reporting
layout: page
parent: Real Time Reporting (Preview)
nav_order: 7
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Investigation-reporting-service
1. The helm chart for investigation service should be available under charts/investigation-reporting-service.
2. In the values.yaml, replace all occurrences of app.EXAMPLE_DOMAIN with the URL of your modern app as shown in [Table](/just-the-doc/docs/4_initial_kubernetes_deployment/1_nginx_ingress_deployment.html#deploy-nginx-ingress-controller-on-the-kubernetes-cluster).
3. Validate image repository and tag:
   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service/investigation-reporting-service"
     tag: <release-version-tag> e.g v1.0.1
   ```
4. Update jdbc, odse, rdb and kafka configurations. The rdb configuration should point to rdb_modern.
   ```yaml
   jdbc:
     username: "EXAMPLE_DB_USER"
     password: "EXAMPLE_DB_USER_PASSWORD"

   odse:
     dburl: "jdbc:sqlserver://<EXAMPLE_DB_ENDPOINT>:<PORT>;databaseName=NBS_ODSE;encrypt=true;trustServerCertificate=true;"
    
   rdb:
     dburl: "jdbc:sqlserver://<EXAMPLE_DB_ENDPOINT>:<PORT>;databaseName=rdb_modern;encrypt=true;trustServerCertificate=true;"
    
   kafka:
     cluster: "EXAMPLE_KAFKA_CLUSTER"
   ```
5. Enabling RTR datamarts: Please make sure that phcDatamartEnable feature flag is set to ‘''true’'' with triple single quotes. The featuresFlags can be removed if present. This will start hydration for ODSE’s PUBLICHEALTHCASEFACT_Modern table.
   ```yaml
   featureFlag:
     phcDatamartEnable: '''true'''
   ``` 
6. Install pod
   ```bash
   helm install -f ./investigation-reporting-service/values.yaml investigation-reporting-service ./investigation-reporting-service/
   ```
7. Verify if pod is running
   ```bash
   kubectl get pods
   ```
8. Validate service (on browser)
   ```
   https://data.<exampledomain>/reporting/investigation-svc/status
   Expected: Investigation Service Status OK
   ```
