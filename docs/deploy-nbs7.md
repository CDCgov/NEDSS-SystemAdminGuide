---
title: Deploy NBS 7
layout: page
nav_order: 3
has_children: true
description: Step-by-step instructions for deploying NBS 7.
---

# Deploy NBS {{ site.version_latest }}

This section covers the full NBS 7 deployment process, from prerequisites and infrastructure setup through microservices deployment and go-live.

> The procedures in this section reflect NBS {{ site.version_latest }}. For earlier releases, see **Previous Versions** in the sidebar.
{: .note }

<!--
Before you begin, confirm that your NBS 6 version is compatible with your target NBS 7 version in the [NBS 6 and NBS 7 compatibility matrix](before-you-deploy/compatibility.html).
-->

NBS 7 deployment comprises the following main phases that you should complete in order:

1. **[Deploy cloud infrastructure](deploy-nbs7/set-up-cloud-infrastructure.html):** Deploy your {% include term-tooltip.html key="aws" term="AWS" id="aws-deploy-phase" %} or {% include term-tooltip.html key="microsoft-azure" term="Azure" id="azure-deploy-phase" %} cloud environment
1. **[Deploy cluster infrastructure](deploy-nbs7/cluster-infrastructure.html):** Install core {% include term-tooltip.html key="kubernetes" term="Kubernetes" id="kubernetes-deploy-phase" %} infrastructure services
1. **[Deploy NBS 7 microservices](deploy-nbs7/microservices-deployment/deploy-nbs7-microservices.html):** Install and configure NBS 7 application services using {% include term-tooltip.html key="helm" term="Helm" id="helm-deploy-phase" %}
1. **[Deploy real-time reporting](deploy-nbs7/real-time-reporting/real-time-reporting.html):** Install components that stream {% include term-tooltip.html key="ods-odse" term="ODSE" id="odse-deploy-phase" %} and {% include term-tooltip.html key="srt-srte" term="SRTE" id="srte-deploy-phase" %} changes to {% include term-tooltip.html key="rdb" term="RDB" id="rdb-deploy-phase" %}
1. **[Deploy data ingestion (DI) API](deploy-nbs7/data-ingestion/data-ingestion.html):** Install the {% include term-tooltip.html key="di-api" term="DI API" id="di-api-deploy-phase" %} data transit layer for writing data to {% include term-tooltip.html key="nbs" term="NBS" id="nbs-deploy-phase" %}
1. **[Validate the deployment](deploy-nbs7/validate-the-deployment.html):** Perform smoke tests and inspect monitoring, console, and admin interfaces
