---
title: Deploy NBS 7
layout: page
nav_order: 3
has_children: true
description: Step-by-step instructions for deploying NBS {{ site.version_latest }}.
---

# Deploy NBS {{ site.version_latest }}

This section covers the full NBS 7 deployment process, from prerequisites and infrastructure setup through microservices deployment and go-live.

> The procedures in this section reflect NBS {{ site.version_latest }}. For earlier releases, see **Previous Versions** in the sidebar.
{: .note }

<!--
Before you begin, confirm that your NBS 6 version is compatible with your target NBS 7 version in the [NBS 6 and NBS 7 compatibility matrix](before-you-deploy/compatibility.html).
-->

NBS 7 deployment comprises four main phases that you should complete in order:

1. **[Deploy cloud infrastructure](deploy-nbs7/set-up-cloud-infrastructure.html):** Deploy your AWS or Azure cloud environment
1. **[Deploy cluster infrastructure](deploy-nbs7/cluster-infrastructure.html):** Install core Kubernetes infrastructure services (NGINX Ingress, Cert Manager, etc.)
1. **[Deploy NBS 7 microservices](deploy-nbs7/deploy-nbs7-microservices.html):** Install and configure NBS 7 application services using Helm
1. **[Validate the deployment](deploy-nbs7/validate-the-deployment.html):** Perform smoke tests and inspect monitoring, console, and admin interfaces
