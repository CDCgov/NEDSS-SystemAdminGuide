---
title: 2. Provision cloud infrastructure
layout: page
parent: NBS 7 full deployment
nav_order: 2
has_children: true
description: Provision cloud infrastructure for NBS 7 on AWS or Azure before installing Kubernetes services.
redirect_from:
  - /docs/3_base_application/0_base_application.html
  - /docs/3_base_application/0_base_application/
  - /docs/deploy-nbs7/set-up-cloud-infrastructure.html
  - /docs/deploy-nbs7/set-up-cloud-infrastructure/
  - /docs/deploy-nbs7/deploy-on-aws.html
  - /docs/deploy-nbs7/deploy-on-aws/
  - /docs/deploy-nbs7/deploy-on-azure.html
  - /docs/deploy-nbs7/deploy-on-azure/
---

# Provision cloud infrastructure for NBS 7

This section covers how to provision the underlying cloud infrastructure for NBS 7: the virtual network, the container runtime, and the storage services that your Kubernetes cluster needs before you can deploy containerized applications to it.

NBS 7 is fully supported on both AWS and Azure. Both providers host the same NBS 7 Kubernetes workloads. After the infrastructure is provisioned, the core services and NBS 7 microservices deployment steps are the same. The differences are mainly in how the underlying cloud environment is provisioned.

The pages in this section walk you through verifying and provisioning your cloud environment:

- **AWS:** Verify that your AWS account, hardware, software, and network requirements are in place, then use Terraform to provision the VPC, Amazon EKS cluster, and supporting AWS services.
- **Azure:** Verify that your Azure subscription, hardware, software, and network requirements are in place, then use Terraform to provision the VNet, AKS cluster, and supporting Azure services.

## What gets provisioned

This section uses Terraform to create the following resources in these managed cloud provider services:

| Resource | AWS service | Azure service | Description |
|----------|-------------|---------------|-------|
| Container runtime | Amazon Elastic Kubernetes Service ([Amazon EKS](https://docs.aws.amazon.com/eks/)) | Azure Kubernetes Service ([AKS](https://learn.microsoft.com/en-us/azure/aks/)) | The Kubernetes cluster and worker nodes that run the NBS 7 workloads. Your cloud provider manages the Kubernetes control plane for you. |
| Virtual network | Amazon Virtual Private Cloud ([Amazon VPC](https://docs.aws.amazon.com/vpc/)) and subnets | Azure Virtual Network ([VNet](https://learn.microsoft.com/en-us/azure/virtual-network/)) and subnets | NBS 7 runs inside this virtual network, and NBS 6 runs in a separate network. The two networks are connected so that NBS 7 microservices can communicate with the NBS 6 application and database. |
| Persistent file storage | Amazon Elastic File System ([Amazon EFS](https://docs.aws.amazon.com/efs/)) | Azure Files | Shared file storage that persists data for the NBS 7 microservices that require it. |
| Object storage | Amazon Simple Storage Service ([Amazon S3](https://docs.aws.amazon.com/s3/)) | Storage account | Storage for objects such as Terraform state files. |
| Encryption keys | AWS Key Management Service ([AWS KMS](https://docs.aws.amazon.com/kms/)) | Azure Key Vault ([AKV](https://learn.microsoft.com/en-us/azure/key-vault/)) | Encryption keys that various other managed services from your cloud provider use to ensure a robust layer of security. |
| Load balancer | Network Load Balancer ([NLB](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)) | Azure Application Gateway ([AGW](https://learn.microsoft.com/en-us/azure/application-gateway/)) | Traefik manages the load balancer and distributes incoming traffic to the Kubernetes ingress controller. |
| Apache Kafka | Amazon Managed Streaming for Apache Kafka ([Amazon MSK](https://docs.aws.amazon.com/msk/)) | [HDInsight Kafka cluster](https://learn.microsoft.com/en-us/azure/hdinsight/kafka/apache-kafka-introduction) | Message streaming that the RTR pipeline and Data Ingestion API require. |
| Metrics collection | Amazon Managed Service for Prometheus ([AMP](https://docs.aws.amazon.com/prometheus/)) | [Azure Monitor managed service for Prometheus](https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/prometheus-metrics-overview) | Collects infrastructure and application metrics from NBS 7 components. |
| Metrics visualization | Amazon Managed Grafana ([AMG](https://docs.aws.amazon.com/grafana/)) | [Azure Managed Grafana](https://learn.microsoft.com/en-us/azure/managed-grafana/) | Visualizes metrics from AMP. The default NBS 7 deployment includes dashboards for error rates, request volume, and latency. |

> The NBS 6 SQL Server database is not provisioned here. NBS 7 reuses the database from your existing NBS 6 deployment. You configure network access between the new VPC or VNet and the existing database in the [Network access requirements](provision-cloud-infrastructure/cloud-prerequisites.html#network-access-requirements) section of Cloud prerequisites.
{: .note }

## In this section

Complete the pages in this section in order:

- **[Cloud prerequisites](provision-cloud-infrastructure/cloud-prerequisites.html)**: Verify your AWS or Azure account, hardware, software, network, and security requirements before provisioning begins.
- **[Provision cloud environment](provision-cloud-infrastructure/provision-cloud-environment.html)**: Use Terraform to create the virtual network, Kubernetes cluster, and supporting services for NBS 7.
