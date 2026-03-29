---
title: Deploy NBS 7
layout: page
nav_order: 3
has_children: true
description: Step-by-step instructions for deploying NBS 7 in an AWS environment.
---

# Deploy NBS 7

This section covers the full NBS 7 deployment process, from prerequisites and infrastructure setup through microservices deployment and go-live.

NBS 7 deployment comprises four main phases:

1. **[Deploy cloud infrastructure](../docs/deploy-nbs7/set-up-cloud-infrastructure.html):** Deploy your AWS or Azure cloud environment
1. **[Deploy cluster infrastructure](../docs/deploy-nbs7/cluster-infrastructure.html):** Install core Kubernetes infrastructure services (NGINX Ingress, Cert Manager, etc.)
1. **[Deploy NBS 7 microservices](../docs/deploy-nbs7/deploy-nbs7-microservices.html):** Install and configure NBS 7 application services using Helm
1. **[Validate the deployment](../docs/deploy-nbs7/validate-the-deployment.html):** Perform smoke tests and inspect monitoring, console, and admin interfaces
