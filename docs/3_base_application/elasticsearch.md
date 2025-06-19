---
title: Elastisearch
layout: page
parent: Microservices Deployment
nav_order: 1
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy Elasticsearch-efs via helm chart

1. The helm chart for elasticsearch-efs should be available under charts/elasticsearch-efs.
2. Update the values.yaml to populate efsFileSystemId which is the EFS file system id from the AWS console.  See image below.

   ![elasticsearch](/just-the-doc/docs/3_base_application/images/elasticsearch.png)

3. Make sure the correct image repository and tags are populated before executing the following helm install command. The image repository and tag in the values file should point to the following:
   ```yaml
   image:
      repository: "quay.io/us-cdcgov/cdc-nbs-modernization/elasticsearch"
      tag: <release-version-tag> e.g v1.0.1
   ```
  After updating the values file, Run the following command from the charts directory to install Elasticsearch.
   ```bash
   helm install elasticsearch -f ./elasticsearch-efs/values.yaml elasticsearch-efs
   ```
4. IMPORTANT: Confirm the pod is running before proceeding with the next deployment using the below command. If the pod is still creating (or in any other state other than running), wait and/or troubleshoot.
   ```bash
   kubectl get pods
   ```
