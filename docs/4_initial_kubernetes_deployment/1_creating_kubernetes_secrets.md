---
title: Creating Kubernetes Secrets
layout: page
parent: Initial Kubernetes Deployment
nav_order: 1
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
## Create Kubernetes Secret Within Cluster

1. Obtain the sample Kubernetes manifest to create secrets expected to be available on the cluster from k8-manifests/nbs-secrets.yaml.
2. Replace string values wherever there is an “EXAMPLE_”
  {: .no_toc }

  | **Parameter**                           | **Template Value**                         | **Example/Description**                      |
  |----------------------------------------|-----------------------------------------------------|--------------------------------------|
  | odse_url |"jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=EXAMPLE_ODSE_DB_NAME;encrypt=true;trustServerCertificate=true;" | jdbc:sqlserver://mydbendpoint:1433;databaseName=nbs_odse;encrypt=true;trustServerCertificate=true; |
  | rdb_url |"jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=EXAMPLE_RDB_DB_NAME;encrypt=true;trustServerCertificate=true;" |  jdbc:sqlserver://mydbendpoint:1433;databaseName=nbs_rdb;encrypt=true;trustServerCertificate=true; |
  | odse_user | "EXAMPLE_ODSE_DB_USER" | ODSE database user |
  | odse_pass | "EXAMPLE_ODSE_DB_USER_PASSWORD" | ODSE database password |
  | rdb_user  | "EXAMPLE_RDB_DB_USER" | RDB database user |
  | rdb_pass  | "EXAMPLE_RDB_DB_PASSWORD" | RDB database password |
  | srte_user | "EXAMPLE_SRTE_DB_USER" | SRTE database user |
  | srte_pass | "EXAMPLE_SRTE_DB_PASSWORD" | SRTE database password |
  | investigation_reporting_user | "EXAMPLE_INVESTIGATION_REPORTING_DB_USER" | RTR investiation reporting database user |
  | investigation_reporting_pass | "EXAMPLE_INVESTIGATION_REPORTING_DB_PASSWORD" | RTR investiation reporting database password |
  | ldfdata_reporting_user | "EXAMPLE_LDFDATA_REPORTING_DB_USER" | RTR ldfdata reporting database user |
  | ldfdata_reporting_pass | "EXAMPLE_LDFDATA_REPORTING_DB_PASSWORD" | RTR ldfdata reporting database password |
  | observation_reporting_user | "EXAMPLE_OBSERVATION_REPORTING_DB_USER" | RTR observation reporting database user |
  | observation_reporting_pass | "EXAMPLE_OBSERVATION_REPORTING_DB_PASSWORD" | RTR observation reporting database password |
  | organization_reporting_user | "EXAMPLE_ORGANIZATION_REPORTING_DB_USER" | RTR organiztion reporting  database user |
  | organization_reporting_pass | "EXAMPLE_ORGANIZATION_REPORTING_DB_PASSWORD" | RTR organization reporting database password |
  | person_reporting_user | "EXAMPLE_PERSON_REPORTING_DB_USER" | RTR person reporting database user |
  | person_reporting_pass | "EXAMPLE_PERSON_REPORTING_DB_PASSWORD" | RTR person database password |
  | post_processing_reporting_user | "EXAMPLE_POST_PROCESSING_REPORTING_DB_USER" | RTR post processing reporting database user |
  | post_processing_reporting_pass | "EXAMPLE_POST_PROCESSING_REPORTING_DB_PASSWORD" | RTR post processing database password |

3. Deploy the secrets to the cluster.
```bash
kubectl apply -f k8-manifests/nbs-secrets.yaml
```
![kubernetes-secretes-within-cluster](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/images/kubernetes-secrets-within-cluster.png)
