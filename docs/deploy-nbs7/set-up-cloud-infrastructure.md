---
title: Deploy cloud infrastructure
layout: page
parent: Deploy NBS 7
nav_order: 4
has_children: true
description: Provision cloud infrastructure for NBS 7 on AWS or Azure before installing Kubernetes services.
---

# Deploy cloud infrastructure

NBS 7 is fully supported on AWS and Azure. This section covers provisioning the underlying cloud infrastructure (the virtual network, container runtime, and storage services) before you install Kubernetes services.

NBS 7 is fully supported on both AWS and Azure. Both providers host the same NBS 7 Kubernetes workloads, and once infrastructure is provisioned, the Bootstrap Kubernetes services and microservices deployment steps are identical. The difference is only in how the underlying cloud environment is provisioned.

Choose the guide that matches your cloud environment.

- [Deploy on AWS](deploy-on-aws.html) - Provision the AWS VPC, Amazon Elastic Kubernetes Service (Amazon EKS) cluster, and supporting services using Terraform.
- [Deploy on Azure](deploy-on-azure.html) - Provision the Azure virtual network, Azure Kubernetes Service (AKS) cluster, and supporting services using Terraform.
