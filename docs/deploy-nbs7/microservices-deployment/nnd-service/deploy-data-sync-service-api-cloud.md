---
title: Deploy Data Sync service API (cloud)
layout: page
parent: NND Service (Data Sync)
nav_order: 4
redirect_from:
   - /docs/6_microservices_deployment/8_nnd.html
   - /docs/6_microservices_deployment/8_nnd/
---

# Deploy Data Sync service API (cloud)

This page walks through deploying the NBS 7 Data Sync service API using the `nnd-service` Helm chart from the [NEDSS-Helm][nedss-helm] repository for NBS version {{ site.version_latest }}.

> This page is part of the optional [NND Service (Data Sync)](../nnd-service.html) section. CDC is evaluating long-term support for this service. If your STLT has a use case, contact [nbs@cdc.gov](mailto:nbs@cdc.gov).
{: .important }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

1. Locate the NND Service Helm chart in the [NEDSS-Helm repository][nedss-helm-nnd-service-chart]. Provide values for ECR repository, ECR image tag, database server endpoints, and ingress host in the `values.yaml` file.
1. Confirm that the following DNS entry was created and points to the Network Load Balancer (NLB) in front of your Kubernetes cluster. Use the active NLB provisioned during base install. Do this in your authoritative DNS service, such as Route 53. Replace `example.com` with the appropriate domain name in `values.yaml`:
   - NND service application, for example: `data.example.com`

## Configure values and install

Set the required values in `values.yaml` before installing the chart.

1. Use Git to clone your own local copy of the public [NEDSS-Helm repository][nedss-helm]. The following steps use the files in `charts/nnd-service/` from that repository.
1. Set the image repository and tag:

   ```yaml
   image:
     repository: "quay.io/us-cdcgov/cdc-nbs-modernization/nnd-service"
     pullPolicy: IfNotPresent
     tag: <release-version-tag> # for example, v1.0.1
   ```

1. Set the JDBC connection values. The `dbserver` value is the database server endpoint only. Do not include the port number. For help determining these values, see the [Helm values reference](../deploy-nbs7-microservices.html#helm-values-for-nbs-7-microservices).

   The following screenshot shows the database endpoint in the Amazon RDS console:

   ![Amazon RDS console showing the Connectivity and security tab with the database endpoint highlighted in the Endpoint and port section](../images/nnd-dbendpoint.png)

   ```yaml
   jdbc:
     dbserver: "EXAMPLE_DB_ENDPOINT"
     username: "EXAMPLE_ODSE_DB_USER"
     password: "EXAMPLE_ODSE_DB_USER_PASSWORD"
   ```

1. Set `efsFileSystemId` to the EFS file system ID from the AWS console.

   The following screenshot shows the file system ID in the Amazon EFS console:

   ![Amazon EFS console showing the File systems list with the file system ID highlighted in the File system ID column](../images/nnd-efsid.png)

   ```yaml
   efsFileSystemId: "EXAMPLE_EFS_ID"
   ```

1. Set the Keycloak auth URI. In the default configuration, this value does not change unless the name or namespace of the Keycloak pod is modified:

   ```yaml
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   ```

1. Install the `nnd-service` chart:

   ```bash
   helm install "nnd-service" ./nnd-service -f ./nnd-service/values.yaml
   ```

1. Confirm the pod is running before continuing:

   ```bash
   kubectl get pods
   ```

## Validate the deployment

Use the actuator endpoints to confirm the service is running.

Run the info endpoint to confirm the service version and build details:

```text
https://<data.EXAMPLE_DOMAIN>/extraction/actuator/info
```

Run the health endpoint to confirm the service is running:

```text
https://<data.EXAMPLE_DOMAIN>/extraction/actuator/health
```

To enable Swagger for testing, specify or overwrite `springBootProfile` with `'dev'` in `charts/nnd-service/values.yaml`. Swagger is disabled by default in production.

```text
https://<data.EXAMPLE_DOMAIN>/extraction/swagger-ui/index.html#/
```

[nedss-helm]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}>
[nedss-helm-nnd-service-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/nnd-service>
