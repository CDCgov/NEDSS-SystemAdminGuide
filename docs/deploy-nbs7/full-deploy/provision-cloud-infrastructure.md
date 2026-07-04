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

# Deploy cloud infrastructure

This section covers provisioning the underlying cloud infrastructure (the virtual network, container runtime, and storage services) before you install Kubernetes services.

NBS 7 is fully supported on both AWS and Azure. Both providers host the same NBS 7 Kubernetes workloads, and once infrastructure is provisioned, the Bootstrap Kubernetes services and microservices deployment steps are identical. The difference is only in how the underlying cloud environment is provisioned.

Choose the guide that matches your cloud environment.

- [Deploy on AWS](#deploy-on-aws) - Provision the AWS VPC, Amazon Elastic Kubernetes Service (Amazon EKS) cluster, and supporting services using Terraform.
- [Deploy on Azure](provision-cloud-infrastructure/cloud-prerequisites.html) - Provision the Azure virtual network, Azure Kubernetes Service (AKS) cluster, and supporting services using Terraform.

<!-- MERGE (chunk 2): content absorbed from deploy-on-aws.md. Integrate with the page above, then delete this divider. -->

# Deploy on AWS

This section walks you through provisioning the AWS cloud environment for NBS 7. You will verify that your AWS account, hardware, software, and network requirements are in place, then use Terraform to provision the VPC, Amazon Elastic Kubernetes Service (Amazon EKS) cluster, and supporting AWS services. Complete both steps in order before moving on to [Deploy cluster infrastructure](kubernetes-setup.html).

<!--
Before provisioning infrastructure, verify that your NBS 6 version is compatible with your target NBS 7 version in the [NBS 6 and NBS 7 compatibility matrix](../before-you-deploy/compatibility.html).
-->

## What gets provisioned

Terraform creates the following AWS resources during this phase:

| Resource | AWS service | Notes |
|---|---|---|
| Container runtime | Amazon EKS | Kubernetes cluster with 3–5 worker nodes |
| Virtual network | VPC and subnets | New VPC with public and private subnets; isolated from existing NBS 6 VPC |
| Persistent file storage | EFS | Shared storage for Kubernetes workloads |
| Object storage | S3 | Stores Terraform state |
| Encryption keys | KMS | Used by EBS, EFS, and RDS storage services |
| Load balancer | ALB | Managed by NGINX Ingress after Kubernetes bootstrapping |
| Managed streaming | MSK (optional) | Required only if you are deploying the Data Ingestion service |

The NBS 6 SQL Server database (RDS or EC2) is not provisioned here — it is reused from your existing NBS 6 deployment. You will configure network access between the new VPC and the existing database during the provisioning step.

## In this section

- **[Prerequisites for AWS](provision-cloud-infrastructure/cloud-prerequisites.html)** — Verifies your AWS account, hardware, software, network, and security requirements before provisioning begins.
- **[Provision the AWS environment](provision-cloud-infrastructure/provision-cloud-environment.html)** — Runs Terraform to create the VPC, Amazon EKS cluster, EFS, and supporting AWS services.
