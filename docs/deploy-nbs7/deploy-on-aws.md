---
title: Deploy on AWS
layout: page
parent: Deploy cloud infrastructure
nav_order: 1
has_children: true
description: Provision the AWS cloud environment and deploy base infrastructure using Terraform before installing Kubernetes services.
redirect_from:
  - /docs/3_base_application/0_base_application.html
  - /docs/3_base_application/0_base_application/
---

# Deploy on AWS

This section walks you through provisioning the Amazon Web Services (AWS) cloud environment for NBS 7. You will verify that your AWS account, hardware, software, and network requirements are in place, then use Terraform to provision the VPC, Amazon Elastic Kubernetes Service (Amazon EKS) cluster, and supporting AWS services. Complete both steps in order before moving on to [Deploy cluster infrastructure](../deploy-nbs7/cluster-infrastructure.html).

Before provisioning infrastructure, verify that your NBS 6 version is compatible with your target NBS 7 version in the [NBS 6 and NBS 7 compatibility matrix](../compatibility.html).

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## What gets provisioned

Terraform creates the following AWS resources during the provisioning step. For details about each service, see [AWS services reference](#aws-services-reference).

| Resource | AWS service | Notes |
|---|---|---|
| Container runtime | Amazon EKS | Kubernetes cluster with 3-5 worker nodes |
| Virtual network | Amazon VPC and subnets | New VPC with public and private subnets; isolated from existing NBS 6 VPC |
| Persistent file storage | Amazon EFS | Shared storage for Kubernetes workloads |
| Object storage | Amazon S3 | Stores Terraform state |
| Encryption keys | AWS KMS | Used by Amazon EBS, EFS, and RDS storage services |
| Load balancer | AWS ALB | Managed by Traefik after Kubernetes bootstrapping |
| Managed streaming | Amazon MSK | Required for the RTR pipeline and Data Ingestion service |
| Metrics collection | Amazon Managed Service for Prometheus (AMP) | Collects infrastructure and application metrics |
| Metrics visualization | Amazon Managed Grafana (AMG) | Visualizes metrics from AMP |

The NBS 6 SQL Server database is not provisioned here. It is reused from your existing NBS 6 deployment, whether hosted on Amazon RDS or on a self-managed Amazon EC2 instance.
{: .note }

## AWS services reference
{: #aws-services-reference }

The following AWS services are used in NBS 7 deployments. For a summary of which services Terraform provisions during this phase, see [What gets provisioned](#what-gets-provisioned).

### Terraform-provisioned services

Terraform provisions the following services in your AWS account during the [provisioning step](deploy-on-aws/provision-aws.html).

- **[Amazon Elastic Kubernetes Service (Amazon EKS)](https://docs.aws.amazon.com/eks/)**: An AWS managed Kubernetes service. Hosts NBS 7 containerized services. Amazon EKS manages the Kubernetes control plane; you manage the worker nodes through managed node groups.
- **[Amazon Virtual Private Cloud (Amazon VPC)](https://docs.aws.amazon.com/vpc/)**: An isolated cloud network in AWS. NBS 7 runs inside a dedicated VPC, separate from the Classic NBS environment. VPC peering connects the two environments so that NBS 7 components can communicate with the NBS 6 application and database.
- **[Amazon Elastic File System (Amazon EFS)](https://docs.aws.amazon.com/efs/)**: AWS-managed network file storage. NBS 7 uses Amazon EFS for persistent storage shared across Kubernetes workloads, including Elasticsearch indices.
- **[Amazon Simple Storage Service (Amazon S3)](https://docs.aws.amazon.com/s3/)**: AWS object storage. Used to store Terraform state files and NBS 7 logs.
- **[AWS Key Management Service (AWS KMS)](https://docs.aws.amazon.com/kms/)**: An AWS service for creating and managing encryption keys. Amazon EKS, Amazon EFS, Amazon EBS, and Amazon RDS use AWS KMS to encrypt data at rest.
- **[AWS Application Load Balancer (AWS ALB)](https://docs.aws.amazon.com/elasticloadbalancing/)**: An AWS managed load balancer. Distributes incoming traffic to the Kubernetes ingress controller. In NBS 7 deployments, AWS ALB is managed by Traefik after Kubernetes bootstrapping.
- **[Amazon Managed Streaming for Apache Kafka (Amazon MSK)](https://docs.aws.amazon.com/msk/)**: An AWS managed Kafka service. Amazon MSK handles event streaming between NBS 7 microservices. Required for the RTR pipeline and Data Ingestion service.
- **[Amazon Managed Service for Prometheus (AMP)](https://docs.aws.amazon.com/prometheus/)**: An AWS managed Prometheus service. Collects infrastructure and application metrics from NBS 7 components.
- **[Amazon Managed Grafana (AMG)](https://docs.aws.amazon.com/grafana/)**: An AWS managed Grafana service. Visualizes metrics collected by Amazon Managed Service for Prometheus. The default NBS 7 deployment includes dashboards for error rates, request volume, and latency.

### Admin-provided services

These services are not provisioned by Terraform. You bring them to the deployment from your existing NBS 6 environment.

#### SQL Server hosting options

- **[Amazon Relational Database Service (Amazon RDS)](https://docs.aws.amazon.com/rds/)**: A managed SQL Server hosting option. STLTs that host the NBS 6 database on Amazon RDS use AWS-native stored procedures for backup and restore operations, which appear in later steps of this guide.
- **[SQL Server on Amazon EC2](https://docs.aws.amazon.com/sql-server-ec2/latest/userguide/sql-server-on-ec2-overview.html)**: A self-managed SQL Server installation on an Amazon EC2 virtual machine. STLTs that host the NBS 6 database on Amazon EC2 use standard SQL Server backup and restore procedures instead of the AWS-native stored procedures.

Your deployment uses one or the other. The NBS 6 SQL Server database is reused by NBS 7 — it is not replaced or re-provisioned during deployment. If you are unsure which approach your environment uses, confirm with your database administrator before proceeding.

#### Identity and access management

- **[AWS Identity and Access Management (AWS IAM)](https://docs.aws.amazon.com/iam/)**: An AWS service for controlling access to cloud resources. IAM roles and permissions must be configured in your existing AWS account before Terraform provisioning begins.

## Next steps

- **[Prerequisites for AWS](deploy-on-aws/prerequisites.html)** — Verifies your AWS account, hardware, software, network, and security requirements before provisioning begins.
- **[Provision the AWS environment](deploy-on-aws/provision-aws.html)** — Runs Terraform to create the VPC, Amazon EKS cluster, EFS, and supporting AWS services.
