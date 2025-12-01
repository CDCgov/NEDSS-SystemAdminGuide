---
title: AWS Infrastructure
layout: page
nav_order: 4
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

# AWS Infrastructure
### Installation Guide & Smoke Tests
{: .no_toc }

Installation of NBS 7 consists of multiple phases:

1. **Set up the AWS infrastructure** - Deploy the cloud environment including Kubernetes, using [Terraform](https://www.terraform.io/)
2. **Bootstrap Kubernetes services** - Install core Kubernetes infrastructure services (NGINX Ingress, Cert Manager, etc.)
3. **Deploy NBS microservices** - Install and configure the NBS application services using [Helm](https://helm.sh/)
4. **Validate the deployment** - Perform smoke tests and inspect monitoring/console/admin interfaces

This section covers the first phase: setting up the AWS infrastructure using Terraform.


### NBS 7 Deployment
This guide provides detailed steps for installing NBS 7 end to end.
Make sure you're using the latest documentation from [NBS Central](https://cdcnbscentral.com/):

1. System Administrator Guide (this document)
2. [User Guide](https://cdcnbscentral.com/)
3. [Release Notes](https://github.com/CDCgov/NEDSS-Helm/releases)

**Installation Steps:**

1. **[Terraform Deployment](/NEDSS-SystemAdminGuide/docs/3_base_application/1_terraform-deployment.html)** - Install the core AWS infrastructure
2. **[Kubernetes Bootstrapping](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/0_kubernetes_bootstrapping.html)** - Deploy core Kubernetes infrastructure services
3. **[Microservices Deployment](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/0_microservices_deployment.html)** - Install and configure NBS microservices (Elasticsearch, Modernization API, NiFi, NBS Gateway, Data Ingestion, and optional services)
