---
title: NiFi
layout: page
parent: Deploy NBS 7 microservices
nav_order: 3
redirect_from:
  - /docs/6_microservices_deployment/3_nifi.html
  - /docs/6_microservices_deployment/3_nifi/
  - /docs/3_base_application/nifi.html
  - /docs/3_base_application/nifi/
---

# Deploy NiFi for NBS 7

This page walks through deploying NiFi using the `nifi` Helm chart from the [NEDSS-Helm][nedss-helm-nifi-chart] repository for NBS version {{ site.version_latest }}. Complete [Modernization API](./modernization-api.html) before starting this page. After you finish, proceed to [Validate ES, MAPI, and NiFi](./validate-es-mapi-nifi.html).

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy NiFi using Helm

Use the [nifi Helm chart][nedss-helm-nifi-chart] to deploy NiFi into your Kubernetes cluster. Before you begin, have your database credentials and domain values available. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-for-nbs-7-microservices) if you need help determining any values.

> `nifi.EXAMPLE_DOMAIN` only needs to be set if you enable the NiFi ingress. The NiFi ingress is disabled by default due to known security vulnerabilities. If you need access to the NiFi admin UI, use a private domain name.
{: .important }

1. Use Git to clone your own local copy of the public [NEDSS-Helm repository][nedss-helm-nifi-chart]. The following steps use the files in `charts/nifi/` from that repository.
1. Set `efsFileSystemId` to your file system ID. See the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-for-nbs-7-microservices) for instructions.
1. Set the JDBC connection string using the database endpoint and credentials from the [Helm values reference](./deploy-nbs7-microservices.html#helm-values-for-nbs-7-microservices):

```yaml
   jdbcConnectionString: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=EXAMPLE_DB_NAME;user=EXAMPLE_ODSE_DB_USER;password=EXAMPLE_ODSE_DB_USER_PASSWORD;encrypt=true;trustServerCertificate=true;"
```

1. Set `nifiSensitivePropsKey` to a strong, randomly generated string of at least 12 characters:

```yaml
   nifiSensitivePropsKey: "EXAMPLE_NIFI_SENSITIVE_PROPS"
```

1. Set the image repository and tag:

```yaml
   image:
     repository: quay.io/us-cdcgov/cdc-nbs-modernization/nifi
     tag: <release-version-tag> # for example, v1.0.1
```

1. If you are enabling the NiFi ingress, replace `nifi.EXAMPLE_DOMAIN` in `values.yaml` with your domain name. Use the value from the [DNS records table](../../deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#create-dns-records):

```yaml
   ingress:
     enabled: true
```

1. Install NiFi:

```bash
   helm install "nifi" ./nifi -f ./nifi/values.yaml
```

1. Confirm the pod is running before proceeding to the next deployment:

```bash
   kubectl get pods
```

If the pod is not in a running state, wait and troubleshoot before continuing to [validate Elasticsearch, Modernization API, and NiFi](./validate-es-mapi-nifi.html).

[nedss-helm-nifi-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/nifi>
