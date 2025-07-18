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

Installation of NBS 7 has three major phases. In the first phase you set up the environment and infrastructure, including k8s, in AWS, 
primarily by using Terraform. In the second phase you start up the workloads/pods in k8s, primarily using Helm (with a bit more Terraform).

Finally, you validate the release by performing a smoke test and inspecting monitoring/console/admin interfaces for the NBS service and
NiFi.


### NBS 7 Deployment
This guide sets out the detailed steps to installing NBS 7 end to end.
Make sure you’re using the latest documentation from NBS Central ( NBS Central)
1. System Administrator Guide (this document)
2. User Guide
3. Release Notes

Installation is divided into two sections:

1. **Terraform Deployment** - installs the core infrastructure
2. **Deployment to Kubernetes** - bootstrap core kubernetes infrastructure services & install and configure microservices (elasticSearch, modernization-api, nifi, nbs-gateway, data-ingestion, data-processing, nnd, case-notifcation and optional real-time reporting services)

