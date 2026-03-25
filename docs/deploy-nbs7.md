---
title: Deploy NBS 7
layout: page
nav_order: 2
has_children: true
description: Step-by-step instructions for deploying NBS 7 in an AWS environment.
---

# Deploy NBS 7

This section covers the full NBS 7 deployment process, from prerequisites 
and infrastructure setup through microservices deployment and go-live.

NBS 7 deployment consists of four phases:

1. **Set up AWS infrastructure** — Deploy the cloud environment including Kubernetes, using Terraform
2. **Bootstrap Kubernetes services** — Install core Kubernetes infrastructure services (NGINX Ingress, Cert Manager, etc.)
3. **Deploy NBS 7 microservices** — Install and configure NBS 7 application services using Helm
4. **Validate the deployment** — Perform smoke tests and inspect monitoring, console, and admin interfaces
