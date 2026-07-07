---
title: Deploy NBS 7
layout: page
nav_order: 3
has_children: true
description: Step-by-step instructions for deploying NBS 7 on AWS or Azure.
---

# Deploy NBS {{ site.version_latest }}

This section covers the NBS 7 deployment process, from prerequisites and infrastructure setup through microservices deployment and go-live. You can follow either of two deployment paths. Both paths create all of the same infrastructure and services:

- **[Quick start](deploy-nbs7/quickstart.html):** Condensed content with a concise level of detail. Intended for administrators who are familiar with deploying NBS 7, or who are familiar with their cloud provider, Terraform, Kubernetes, and Helm.
- **[NBS 7 full deployment](deploy-nbs7/full-deploy.html):** Complete step-by-step instructions with detailed explanations at each phase. Intended for administrators deploying NBS 7 for the first time.

> The procedures in this section reflect NBS {{ site.version_latest }}. For earlier releases, see **Previous Versions** in the sidebar.
{: .note }

## Additional deployment sections

<!-- INTERIM (STLT-538): these sections relocate under Deploy NBS 7 microservices in the deferred microservices pass. Remove this block when they move. -->

After you complete the steps in the full deployment or quick start, continue with the following sections in order:

If you followed the Quick start, you have already completed the data ingestion and validation steps. Complete only the sections you have not yet finished.
{: .note }

1. **[Deploy real-time reporting](deploy-nbs7/real-time-reporting/real-time-reporting.html):** Install components that stream `ODSE` and `SRTE` changes to the reporting database.
1. **[Deploy data ingestion (DI) API](deploy-nbs7/data-ingestion/data-ingestion.html):** Install the DI API data transit layer for writing data to NBS.
1. **[Validate the deployment](deploy-nbs7/validate-the-deployment.html):** Perform smoke tests and inspect monitoring, console, and admin interfaces.
