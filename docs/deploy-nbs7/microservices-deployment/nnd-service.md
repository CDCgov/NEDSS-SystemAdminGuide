---
title: NND Service (Data Sync)
layout: page
parent: Deploy NBS 7 microservices
nav_order: 8
has_children: true
---

# Deploy NND Service (Data Sync) for NBS 7

This section covers Data Sync capabilities for NND workflows, including cloud service deployment, endpoint validation, and on-premises setup patterns.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Understand service names in this section

Use the following terms consistently in this section:

- **Data Sync service**: The NBS 7 service and API that extract data from the NBS cloud environment.
- **NND Sync**: The on-premises NNDSS integration workflow that uses Data Sync service outputs to support ongoing message transmission.
- **Data Availability**: A Data Sync service use case that copies selected data to SQL Server, Amazon S3, or a local directory.

## In this section

- [Validate API endpoints](../../../docs/deploy-nbs7/microservices-deployment/nnd-service/validating-api-endpoints.html): Verify API connectivity, credential setup, and baseline endpoint responses.
- [Deploy NND Sync](../../../docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-nnd-sync.html): Configure the on-premises NNDSS integration workflow that uses Data Sync outputs.
- [Deploy Data Availability (on-premises)](../../../docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-data-sync.html): Configure on-premises options for syncing selected data to SQL Server, S3, or local storage.
- [Deploy Data Sync service API (cloud)](../../../docs/deploy-nbs7/microservices-deployment/nnd-service/deploy-data-sync-service-api-cloud.html): Install and configure the cloud Data Sync service API with Helm.
