---
title: Quickstart
layout: page
nav_order: 1
nav_enabled: true
---

# Quickstart
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


This quick guide provides a simple step-by-step approach for deploying the NBS 7 infrastructure and microservices in an AWS environment. It is intended for experienced administrators who are familiar with AWS, Kubernetes, Helm, and Terraform. 

This guide is NOT meant for a production deployment. Please review [System Administrator Guide](https://NEDSS-SystemAdminGuide/docs/3_base_application/0_base_application.html) for a full production deployment and guidelines.

### Following resources will be installed and configured with this guide

#### Terraform
- Modern VPC, Subnets, Route Tables
- EKS Cluster, Nodes
- Network Load Balancer
- MSK
- Amazon Prometheus
- Amazon Grafana
- EFS
- KMS
- S3 Bucket

#### Manual
- Route53 Updates: Need to create dns entries in route53 to point app and data urls to network load balancer

#### NBS7 Core Services
1. **Elasticsearch** - For lightning-fast searches.
2. **Modernization API** - This service incorporates essential modern NBS features such as patient search, event search, patient profile, investigations, etc.
3. **Nifi** - Populates Elasticsearch indices from the NBS database.
4. **NBS Gateway** - Efficiently manages intricate strangler routing logic between modern and legacy NBS.
5. **Data Ingestion** - Enables NBS to seamlessly ingest HL7 data from labs and other entities into the NBS system.
6. **Keycloak** - Primary Identity Provider (IDP). Also used for token management and SSO integration, for example, OAuth, SAML integration with Okta, etc.

## Prerequisites
Tools to Install
- [AWS CLI](https://aws.amazon.com/cli/) (v2.15+)
- [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) (v1.5.5)
- [Helm](https://helm.sh/docs/intro/install/) (v3.12+)
- [kubectl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html) (v1.27+)
- [eksctl](https://eksctl.io/installation/) (optional but recommended)

## Environment Requirements
- AWS Account with NBS 6.0.16 access (or newer)
- DNS routing infrastructure: Domain info for modernized nbs application (e.g app.site_name.domain.com)
- IAM Roles for Terraform and Kubernetes
- Access to NBS 6 (sql server) databases to run scripts
- S3 bucket for Terraform state

## Set Up AWS Infrastructure - Terraform
 <br>
![NBS7_Infrastructure](/NEDSS-SystemAdminGuide/docs/quick_install_nbs7_architecture.png)

### Prepare the Directory
{: .no_toc }
```bash
mkdir -p ~/nbs-setup/terraform/aws/nbs7-mySTLT-test
cd ~/nbs-setup/terraform/aws/nbs7-mySTLT-test
```

### Download Terraform Configuration
{: .no_toc }
Clone the infrastructure repo:
```bash
git clone https://github.com/CDCgov/NEDSS-Infrastructure.git
```
Copy standard template:
```bash
cp -pr terraform/aws/samples/NBS7_standard terraform/aws/nbs7-mySTLT-test
```

### Customize Variables
{: .no_toc }
- Update the terraform.tfvars and terraform.tf with your environment-specific values by following the instructions [here](https://github.com/CDCgov/NEDSS-Infrastructure/blob/main/terraform/aws/samples/NBS7_standard/README.md).

> ℹ️ **Review the inbound rules** on the security groups attached to your database instance and ensure that the CIDR you intend to use with your NBS 7 VPC (`modern-cidr`) is allowed to access the database.

### Initialize and Apply Terraform
{: .no_toc }
```js
terraform init
terraform plan
terraform apply
```

### Validate Infrastructure
{: .no_toc }
- Confirm VPC, EKS cluster, subnets, and node groups are created.
- Verify EKS cluster authentication and running pods & nodes:
```bash
aws eks --region us-east-1 update-kubeconfig --name <clustername> e.g. cdc-nbs-sandbox
kubectl get pods --namespace=cert-manager
kubectl get nodes
```

## Deploy Core Kubernetes Services - Helm
### Install NGINX Ingress
{: .no_toc }
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx
kubectl --namespace ingress-nginx get services -o wide -w ingress-nginx-controller
kubectl get pods -n=ingress-nginx
```

### Create DNS Entries in Route53
{: .no_toc }
- Modernized NBS application pointed to the new network load balancer in front of your Kubernetes cluster
```bash
app.<site_name>.<domain>.com
```
- Data Services pointed to the new network load balancer in front of your Kubernetes cluster
```bash
data.<site_name>.<domain>.com
```

### Install Cert Manager (Optional)
{: .no_toc }
```bash
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true
```

### Install and Verify LinkerD (Optional)
{: .no_toc }
```bash
kubectl annotate namespace default "linkerd.io/inject=enabled"
kubectl get namespace default -o=jsonpath='{.metadata.annotations}'
```

### Install Cluster Autoscaler (Optional)
{: .no_toc }
```bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler
helm install cluster-autoscaler autoscaler/cluster-autoscaler -n kube-system
```

### Verify Services are Running
{: .no_toc }
```bash
kubectl get pods -A
```

## Install Keycloak
**Create Keycloak Database. Make sure to update the database password.**
```sql
use master
    IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'keycloak')
    BEGIN
        CREATE DATABASE keycloak
    END
GO
    USE keycloak
GO

BEGIN
    CREATE LOGIN NBS_keycloak WITH PASSWORD = 'EXAMPLE_KCDB_PASS8675309';
    CREATE USER NBS_keycloak FOR LOGIN NBS_keycloak;
    EXEC sp_addrolemember N'db_owner', N'NBS_keycloak'
END
```

### Install Keycloak Container

Edit the following parameters in `<helm extract directory>/charts/keycloak/values.yml`:

- `kcDbPassword`
- `kcDbUrl`
- `keycloakAdminPassword`
- `efsFileSystemId`
```bash
helm install keycloak --namespace default --create-namespace -f keycloak/values.yaml
```

### Port forward to access Keycloak admin interface
```bash
kubectl --namespace default port-forward "$POD_NAME" 8080;
http://127.0.0.1:8080/auth
```

### Configure Realm, Users and Clients
- Login as Keycloak admin user
- Upload <helm extract directory>/charts/keycloak/extra/01-NBS-realm-with-DI-client.json
- Upload <helm extract directory>/charts/keycloak/extra/05-nbs-users-nnd-client.json
- Upload NBS Users helm from <helm extract directory>/charts/keycloak/extra/02-nbs-users-realm.json
- Run partial import from nbs-users realm for <helm extract directory>/charts/keycloak/extra/03-nbs-users-base-users.json
- Run partial import from nbs-users realm for <helm extract directory>/charts/keycloak/extra/04-nbs-users-development-clients.json

## Deploy NBS Microservices - Helm
**Deploy the helm charts in the following order.**
1. `elasticsearch-efs`
2. `modernization-api`
3. `nifi-efs`
4. `nbs-gateway`
5. `dataingestion`

> ℹ️ Run the below commands from `<helm extract directory>/charts` directory

### Deploy Elasticsearch
{: .no_toc }
Update the required parameters in `values.yaml` by following the table [here](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/elasticsearch-efs/README.md)
```bash
helm install elasticsearch -f ./elasticsearch-efs/values.yaml elasticsearch-efs
```

### Deploy Modernization API
{: .no_toc }
Update the required parameters in `values.yaml` by following the table [here](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/modernization-api/README.md)
```bash
helm install modernization-api -f ./modernization-api/values.yaml modernization-api
```

### Deploy NiFi
{: .no_toc }
Update the required parameters in `values.yaml` by following the table [here](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/nifi-efs/README.md)
```bash
helm install nifi -f ./nifi-efs/values.yaml nifi-efs
```

### Deploy NBS Gateway
{: .no_toc }
Update the required parameters in `values.yaml` by following the table [here](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/nbs-gateway/README.md)
```bash
helm install nbs-gateway -f ./nbs-gateway/values.yaml nbs-gateway
```

### Deploy DataIngestion
{: .no_toc }
Data Ingest DB creation and user permission should be executed prior to the deployment of the data ingestion:
```sql
IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'NBS_DataIngest')
BEGIN
    CREATE DATABASE NBS_DataIngest
END
GO
USE NBS_DataIngest
GO
```
```sql
use [NBS_ODSE];
GO
USE [NBS_DataIngest]
GO
CREATE USER [nbs_ods] FOR LOGIN [nbs_ods]
GO
USE [NBS_DataIngest]
GO
ALTER USER [nbs_ods] WITH DEFAULT_SCHEMA=[dbo]
GO
USE [NBS_DataIngest]
GO
ALTER ROLE [db_owner] ADD MEMBER [nbs_ods]
GO
```
Update the required parameters in `values.yaml` by following the table [here](https://github.com/CDCgov/NEDSS-Helm/blob/main/charts/dataingestion-service/README.md)
```bash
helm install dataingestion-service -f ./dataingestion-service/values.yaml dataingestion-service
```

### Verify Services
{: .no_toc }
- Confirm all pods are running before moving on.
```bash
kubectl get pods -A
```

## Validate Installation
### Manual Tests
{: .no_toc }
- Login to the NBS UI (e.g., [https://app.example.com/nbs/login](https://app.example.com/nbs/login))
- Check basic patient search functionality.

### Automated Tests
{: .no_toc }
- Use nbs-test-api.sh and nbs-test-webui.sh for basic API and UI smoke tests.


## Cleanup
Follow the steps below to cleanup environment

```bash
# Remove DNS entries
1. app.<site_name>.<domain>.com
2. data.<site_name>.<domain>.com

# Remove nlb and ingress routing
helm list --namespace ingress-nginx
helm uninstall --namespace ingress-nginx ingress-nginx

# Empty fluentbit s3 bucket manually

terraform destroy
```

## Go Live
We recommend before going live, review the [System Administrator Guide](https://cdc-nbs.atlassian.net/wiki/spaces/NM/pages/1592754177/NBS+7.10+System+Administrator+Guide).

## Support
- For support, contact NBSSupport@cdc.gov.
- For ongoing updates, check the GitHub repo for new releases.
