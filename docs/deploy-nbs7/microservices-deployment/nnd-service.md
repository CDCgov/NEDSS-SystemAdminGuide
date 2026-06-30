---
title: NND Service (Data Sync)
layout: page
parent: Deploy NBS 7 microservices
nav_order: 8
has_children: true
---

# Deploy NND Service (Data Sync) for NBS 7

This section covers Data Sync capabilities for  NND (National Notifiable Disease)  workflows, including cloud service deployment, endpoint validation, and on-premises setup patterns.

> The NND Service (Data Sync) deployment is optional. CDC is evaluating long-term support for this service. If your STLT has a use case, contact [nbs@cdc.gov](mailto:nbs@cdc.gov).
{: .important }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Understand service names in this section

Use the following terms consistently in this section:

- **Data Sync service**: The NBS 7 service and API that extract data from the NBS cloud environment.
- **NND Sync**: The on-premises  NNDSS (National Notifiable Diseases Surveillance System) integration workflow that uses Data Sync service outputs to support ongoing message transmission.
- **Data Availability**: A Data Sync service use case that copies selected data to SQL Server, a cloud storage service, or a local directory.

## In this section

- [Validate API endpoints](../../deploy-nbs7/microservices-deployment/nnd-service/validating-api-endpoints.html): Verify API connectivity, credential setup, and baseline endpoint responses.
- [Deploy NND Sync](../../deploy-nbs7/microservices-deployment/nnd-service/on-prem-nnd-sync.html): Configure the on-premises NNDSS integration workflow that uses Data Sync outputs.
- [Deploy Data Availability (on-premises)](../../deploy-nbs7/microservices-deployment/nnd-service/on-prem-data-sync.html): Configure on-premises options for syncing selected data to SQL Server, S3, or local storage.
- [Deploy Data Sync service API (cloud)](../../deploy-nbs7/microservices-deployment/nnd-service/deploy-data-sync-service-api-cloud.html): Install and configure the cloud Data Sync service API with Helm.
