---
title: Deploy on AWS
layout: page
parent: Deploy cloud infrastructure
nav_order: 1
has_children: true
description: Provision the AWS cloud environment and deploy base infrastructure using Terraform before installing Kubernetes services.
---

# Deploy on AWS
{: .no_toc }

This section walks you through provisioning the AWS cloud environment for NBS 7. You will verify that your AWS account, hardware, software, and network requirements are in place, then use Terraform to provision the VPC, EKS cluster, and supporting AWS services. Complete both steps in order before moving on to [Deploy cluster infrastructure](../../docs/deploy-nbs7/cluster-infrastructure.html).

## What gets provisioned

Terraform creates the following AWS resources during this phase:

| Resource | AWS service | Notes |
|---|---|---|
| Container runtime | EKS | Kubernetes cluster with 3–5 worker nodes |
| Virtual network | VPC and subnets | New VPC with public and private subnets; isolated from existing NBS 6 VPC |
| Persistent file storage | EFS | Shared storage for Kubernetes workloads |
| Object storage | S3 | Stores Terraform state |
| Encryption keys | KMS | Used by EBS, EFS, and RDS storage services |
| Load balancer | ALB | Managed by NGINX Ingress after Kubernetes bootstrapping |
| Managed streaming | MSK (optional) | Required only if you are deploying the Data Ingestion service |

The NBS 6 SQL Server database (RDS or EC2) is not provisioned here — it is reused from your existing NBS 6 deployment. You will configure network access between the new VPC and the existing database during the provisioning step.

## In this section

- [Prerequisites for AWS](aws-infrastructure/prerequisites.html) — Verifies your AWS account, hardware, software, network, and security requirements before provisioning begins.
- [Provision the AWS environment](aws-infrastructure/provision-aws.html) — Runs Terraform to create the VPC, EKS cluster, EFS, and supporting AWS services.
