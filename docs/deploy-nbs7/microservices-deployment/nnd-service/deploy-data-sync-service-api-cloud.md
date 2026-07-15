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

Complete the following before you begin this page:

- If you haven't already, complete [Before you begin](../deploy-nbs7-microservices.html#before-you-begin) for the microservices phase.
- Complete [Data Processing](../data-processing.html) deployment.

## Configure values and install

Complete the following steps to deploy the ['nnd-service' Helm chart][nedss-helm-nnd-service-chart] from the `charts/nnd-service/` directory of your cloned NEDSS-Helm repository:

1. Confirm that the following DNS entry was created and points to the Network Load Balancer (NLB) in front of your Kubernetes cluster. Use the active NLB provisioned during base install. Do this in your authoritative DNS service, such as Route 53. Replace `example.com` with the appropriate domain name in `values.yaml`:
   - NND service application, for example: `data.example.com`
1. Search `values.yaml` for `EXAMPLE` and fill in the JDBC connection values and EFS file system ID. The `dbserver` value is the database server endpoint only; do not include the port number. The [Helm values reference](../deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices) lists the values to use.

   The following screenshot shows the database endpoint in the Amazon RDS console:

   ![Amazon RDS console showing the Connectivity and security tab with the database endpoint highlighted in the Endpoint and port section](../images/nnd-dbendpoint.png)

   The following screenshot shows the file system ID in the Amazon EFS console:

   ![Amazon EFS console showing the File systems list with the file system ID highlighted in the File system ID column](../images/nnd-efsid.png)

1. <!-- [SME REVIEW] This value isn't in the Helm values reference table yet. Confirm whether to add it there or keep it documented here before removing this walkthrough. -->
   Set the Keycloak auth URI. In the default configuration, this value does not change unless the name or namespace of the Keycloak pod is modified:

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
