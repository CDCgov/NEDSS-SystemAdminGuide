---
title: Azure quick deploy
layout: page
parent: NBS 7 quick deployment
nav_order: 2
description: Streamlined path for experienced administrators to deploy NBS 7 infrastructure and microservices in a Microsoft Azure environment.
---

# Quick deployment of NBS {{ site.version_latest }} in a Microsoft Azure environment

This page provides a streamlined path to deploy NBS 7 infrastructure and microservices in a Microsoft Azure hosting environment. It is a condensed form of the [NBS 7 full deployment](../full-deploy.html), intended for experienced administrators who are familiar with Azure, Kubernetes, Helm, and Terraform. For a detailed walkthrough with an explanation at each step, use the full deployment instead. Both paths create the same infrastructure and services.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Scope and limitations

Before you begin, verify that your NBS 6 version is supported for your target NBS 7 version. See the [Supported NBS versions](../../supported-versions.html) page.

> This quick deployment condenses the full procedure and omits most of the validation steps. Use the [NBS 7 full deployment](../full-deploy.html) for production deployments and for first-time deployments.
{: .important }

## Prerequisites

Confirm the general [Prerequisites](../full-deploy/prerequisites.html) and the [Cloud prerequisites](../full-deploy/provision-cloud-infrastructure/cloud-prerequisites.html) before you begin. On your management workstation or in Azure Cloud Shell, install the following tools:

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) (the `az` command)
- [kubelogin](https://github.com/Azure/kubelogin), which `kubectl` requires for Azure authentication
- [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) (the `terraform` command)
- [Helm CLI](https://helm.sh/docs/intro/install/) (the `helm` command)
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) (the Kubernetes CLI)

You also need an authenticated Azure session and network access to your existing NBS 6 SQL Server database. For version requirements and full details, see the [Cloud prerequisites](../full-deploy/provision-cloud-infrastructure/cloud-prerequisites.html) page.

## Provision cloud infrastructure

Use Terraform to provision the virtual network, the Azure Kubernetes Service (AKS) cluster, and the supporting Azure services for NBS 7.

1. Authenticate to your Azure subscription and confirm the session:

   ```text
   az login
   az account show
   ```

1. Navigate to the [NEDSS-Infrastructure {{ site.version_latest_tag }} release page][nedss-infra-release-page]. Under **Assets**, download the `nbs-infrastructure-{{ site.version_latest_tag }}.zip` file, then unzip it.
1. From the directory where you unzipped the file, create an environment directory and copy the sample layers into it:

   ```bash
   cd terraform/azure
   mkdir nbs7-mySTLT-test
   cp -pr samples/* ./nbs7-mySTLT-test
   cd nbs7-mySTLT-test
   ```

   The samples contain a numbered directory for each Terraform layer: `0-landing-zone`, `1-nbs7`, and `2-applications`. Apply the layers in that numeric order. The [README in the NEDSS-Infrastructure repository][nedss-infra-readme] explains the layered design.

1. In each layer directory, update the `terraform.tfvars` and `terraform.tf` files with your environment-specific values. Then apply each layer in numeric order:

   ```bash
   terraform init
   terraform plan -out=tfplan
   terraform apply tfplan
   ```

   > Review the full plan output and confirm that the changes match your intention before you apply. Use caution with `terraform apply -auto-approve`, because it applies changes without review.
   {: .important }

1. Configure `kubectl` to connect to the provisioned cluster:

   ```bash
   az aks get-credentials --resource-group <RESOURCE_GROUP_NAME> --name <MANAGED_CLUSTER_NAME>
   ```

1. Confirm the cluster is ready. Each core pod should have a `STATUS` of `Running`, and each node should have a `STATUS` of `Ready`:

   ```bash
   kubectl get pods --namespace=kube-system
   kubectl get nodes
   ```

Save your `nbs7-mySTLT-test` directory. You need it for future maintenance of the infrastructure you provisioned.

## Enable Linkerd for the default namespace

Linkerd provides mutual Transport Layer Security (mTLS) between the NBS 7 microservices, which deploy into the default Kubernetes namespace. Terraform deploys the Linkerd service during provisioning. Annotate the default namespace so that Linkerd injects a sidecar into each microservice pod:

```bash
kubectl annotate namespace default "linkerd.io/inject=enabled"
```

Verify that the annotation is in place. The output should include `"linkerd.io/inject":"enabled"`:

```bash
kubectl get namespace default -o=jsonpath='{.metadata.annotations}'
```

## Deploy core services

Download the Helm charts, then deploy the Traefik ingress controller and cert-manager.

1. Navigate to the [NEDSS-Helm {{ site.version_latest_tag }} release page][nedss-helm-release-page]. Under **Assets**, download the **Source code (zip)** file, then unzip it.
1. Change into the `charts` directory from the unzipped file. Run all `helm` commands from this directory.

### Deploy the Traefik ingress controller

The Traefik controller creates an internal load balancer in Azure and routes traffic to the NBS 7 services.

1. Add the Traefik Helm chart repository and update it:

   ```bash
   helm repo add traefik https://traefik.github.io/charts
   helm repo update
   ```

1. Deploy the Traefik controller with the Azure values file:

   ```bash
   helm install traefik traefik/traefik --namespace traefik --create-namespace -f ./traefik/values-azure.yaml
   ```

   > If your AKS cluster has Windows node pools, for example for NBS 6, append the following option so that Traefik is scheduled on a Linux node: `--set nodeSelector."kubernetes\.io/os"=linux`
   {: .note }

1. Confirm that the Traefik pod has a `STATUS` of `Running` and that the two numbers in the `READY` column match:

   ```bash
   kubectl get pods -n traefik
   ```

### Deploy NBS ingress resources

The `nbs-ingress` chart manages ingress routing between the NBS 7 applications.

1. In `nbs-ingress/values.yaml`, search for `EXAMPLE` and fill in your environment-specific values. The [Helm values reference for NBS 7 microservices][helm-values-table] lists the values to use.
1. Deploy the ingress resources:

   ```bash
   helm install nbs-ingress ./nbs-ingress -n default -f ./nbs-ingress/values.yaml
   ```

### Configure cert-manager (optional)

Terraform deploys cert-manager during provisioning. It creates and renews Transport Layer Security (TLS) certificates for the Apache NiFi and modernization-api services. Skip this section if you use manual certificates stored in Kubernetes secrets.

1. In the NEDSS-Helm repository, open [`k8-manifests/cluster-issuer-prod.yaml`][nedss-helm-cluster-issuer-manifest] and update the email address to a valid operations address.
1. From the `k8-manifests` directory in the unzipped file, apply the manifest:

   ```bash
   kubectl apply -f cluster-issuer-prod.yaml
   ```

1. Verify that the cluster issuer is ready. The `letsencrypt-production` issuer should have a `READY` status of `True`:

   ```bash
   kubectl get clusterissuer
   ```

> AKS clusters usually include a built-in cluster autoscaler, so no separate Cluster Autoscaler deployment is required for Azure.
{: .note }

## Create DNS records

Create the Domain Name System (DNS) A records in Azure DNS that point to the IP address of your Application Gateway.

1. Retrieve the load balancer address from the `EXTERNAL-IP` column:

   ```bash
   kubectl get svc -n traefik
   ```

1. In the Azure Portal, navigate to **DNS Zones** and select your DNS zone. Create an A record for each hostname in the following table so that it points to the IP address of your Application Gateway. Replace `<DOMAIN_NAME.TLD>` with your site and domain names from the [Helm values reference for NBS 7 microservices][helm-values-table]:

   | Subdomain description | Hostname | Example |
   |-----------------------|----------|---------|
   | NBS application | `app.<DOMAIN_NAME.TLD>` | `app.nbsdemo.com` |
   | Data services | `data.<DOMAIN_NAME.TLD>` | `data.nbsdemo.com` |
   | NiFi (use with caution) | `nifi.<DOMAIN_NAME.TLD>` | `nifi.nbsdemo.com` |

   > Apache NiFi has known security vulnerabilities. Add a NiFi DNS record only if you need to administer NiFi directly. Otherwise, omit it.
   {: .warning }

1. Verify that each record resolves to the IP address of your Application Gateway without an error such as `server can't find`. Records typically propagate within 60 seconds:

   ```bash
   nslookup app.<DOMAIN_NAME.TLD>
   ```

## Install and configure Keycloak

Keycloak is the authentication service that allows users to sign in to the NBS 7 web UI.

1. Create the Keycloak database and database user. Run the SQL script in [Create the Keycloak database][keycloak-db-setup] on your NBS 6 database. Replace `EXAMPLE_KCDB_PASS8675309` with a complex password and store it securely. You need it in the Helm values file.
1. In `keycloak/values.yaml`, set the admin credentials, the database connection values, and the `KC_DB_PASSWORD` to match the password you set in the script.
1. Install the Keycloak Helm chart. This step takes at least 5 minutes while the init container becomes available:

   ```bash
   helm install keycloak ./keycloak -n default -f keycloak/values.yaml
   ```

1. Verify that the Keycloak pod is running:

   ```bash
   kubectl get pods -n default
   ```

1. Set up port forwarding, then navigate to `http://127.0.0.1:8080/auth` in a browser and select **Administration Console**. Sign in with the admin credentials from the values file:

   ```bash
   kubectl port-forward deploy/keycloak-deployment 8080
   ```

   > Port forwarding is not supported by Azure Cloud Shell by default. Run this command from a system that has both network access to your cluster endpoint and a browser.
   {: .note }

1. Create the two NBS 7 realms. For each file, select **Create realm**, upload the file, and select **Create**:

   | Realm | Import file |
   |-------|-------------|
   | NBS | `01-NBS-realm-with-DI-client.json` |
   | nbs-users | `02-nbs-users-realm.json` |

   All import files are in the `keycloak/extra/` directory of the NEDSS-Helm charts.

   > A `02-nbs-users-realm_with_mfa_option.json` file is available as an alternative to `02-nbs-users-realm.json` if you want to enable multifactor authentication (MFA) for the nbs-users realm.
   {: .note }

1. Import the base users and development clients into the **nbs-users** realm. Select the realm, navigate to **Realm settings** > **Action** > **Partial Import**, and import each file:
   - `03-nbs-users-base-users.json` (select the three users: `msa`, `nbs-users-admin`, `superuser`)
   - `04-nbs-users-development-clients.json` (select the `nbs-development` client)

1. Import the additional service clients and retrieve their secrets. The NBS realm seeds `di-keycloak-client` with the realm import, so it needs no separate import. For each client in the following table that requires an import, select the listed realm, navigate to **Realm settings** > **Action** > **Partial Import**, and import the file. Then navigate to **Clients**, select the client, open the **Credentials** tab, and store the secret in your organization's secrets manager, such as Azure Key Vault:

   | Client | Realm | Import needed | Import file |
   |--------|-------|---------------|-------------|
   | `di-keycloak-client` | NBS | No | Seeded with the NBS realm |
   | `nnd-keycloak-client` | NBS | Yes | `05-nbs-users-nnd-client.json` |
   | `srte-data-keycloak-client` | NBS | Yes | `06-nbs-users-srte-data-client.json` |
   | `case-notification-service` | NBS | Yes | `08-nbs-users-case-notification-service.json` |

1. Verify Traefik and Keycloak together. In a browser, navigate to `https://app.<DOMAIN_NAME.TLD>`, confirm that the NBS 7 Welcome page is shown, select **Login**, and confirm that the Keycloak login page is shown.

## Deploy NBS 7 microservices

Run each command from the `charts` directory, in the order shown. Before each command, search the service's values file for `EXAMPLE` and fill in your environment-specific values from the [Helm values reference for NBS 7 microservices][helm-values-table]. Verify that each service starts before you deploy the next one.

1. Elasticsearch:

   ```bash
   helm install elasticsearch -f ./elasticsearch/values.yaml elasticsearch
   ```

1. Modernization API:

   ```bash
   helm install "modernization-api" ./modernization-api -f ./modernization-api/values.yaml
   ```

1. Apache NiFi:

   ```bash
   helm install "nifi" ./nifi -f ./nifi/values.yaml
   ```

1. NBS Gateway:

   ```bash
   helm install "nbs-gateway" ./nbs-gateway -f ./nbs-gateway/values.yaml
   ```

1. Data processing service:

   ```bash
   helm install "data-processing-service" ./data-processing-service -f ./data-processing-service/values.yaml
   ```

1. Case notification service. Deploy the Debezium connector first with the Azure values file, then the service:

   ```bash
   helm install "debezium-case-notification-service-connect" ./debezium-case-notifications -f ./debezium-case-notifications/values-azure.yaml
   helm install "case-notification-service" ./case-notification-service -f ./case-notification-service/values.yaml
   ```

1. Data Ingestion API (DI API):

   ```bash
   helm install dataingestion-service -f ./dataingestion-service/values.yaml dataingestion-service
   ```

1. Real-time reporting (RTR). Complete the database setup and change data capture (CDC) bootstrap steps on the [Deploy real-time reporting](../microservices-deployment/real-time-reporting/real-time-reporting.html) page first, then deploy the RTR services in order:

   ```bash
   helm install -f ./debezium/values-azure.yaml debezium-connect ./debezium/
   helm install -f ./kafka-connect-sink/values-azure.yaml cp-kafka-connect-server ./kafka-connect-sink/
   helm install -f reporting-pipeline-service/values.yaml reporting-pipeline-service ./reporting-pipeline-service/
   ```

## Clean up

To decommission this environment, follow [Undeploy NBS 7](../../undeploy-nbs7.html). That page covers removing DNS entries, removing the Helm ingress resources, emptying the OpenTelemetry (OTEL) collector storage, and destroying the Terraform-managed infrastructure.

## Support

For support, email [nbs@cdc.gov](mailto:nbs@cdc.gov).

[nedss-infra-release-page]: <https://github.com/CDCgov/NEDSS-Infrastructure/releases/tag/{{ site.version_latest_tag }}>
[nedss-infra-readme]: <https://github.com/CDCgov/NEDSS-Infrastructure/blob/{{ site.version_latest_tag }}/README.md>
[nedss-helm-release-page]: <https://github.com/CDCgov/NEDSS-Helm/releases/tag/{{ site.version_latest_tag }}>
[nedss-helm-cluster-issuer-manifest]: <https://github.com/CDCgov/NEDSS-Helm/blob/{{ site.version_latest_tag }}/k8-manifests/cluster-issuer-prod.yaml>
[keycloak-db-setup]: <../full-deploy/kubernetes-setup/deploy-keycloak.html#create-the-keycloak-database>
[helm-values-table]: <../microservices-deployment/deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices>
