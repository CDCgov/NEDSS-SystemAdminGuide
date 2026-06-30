---
title: NND Service (Data Sync)
layout: page
parent: Deploy NBS 7 microservices
nav_order: 8
has_children: true
---

# NND Service (Data Sync)

This section covers Data Sync capabilities for National Notifiable Disease (NND) workflows, including cloud service deployment, endpoint validation, and on-premises setup patterns.

> The NND Service (Data Sync) deployment is optional. CDC is evaluating long-term support for this service. If your STLT has a use case, contact [nbs@cdc.gov](mailto:nbs@cdc.gov).
{: .important }

If you are not deploying the NND Service, proceed to [Case notification service](./case-notification.html).

## Terminology

This deployment section uses three related but distinct terms:

- **NND Sync**: The on-premises NNDSS (National Notifiable Diseases Surveillance System) integration workflow that uses Data Sync service outputs to support ongoing message transmission.
- **Data Availability**: A Data Sync service use case that copies selected data to SQL Server, a cloud storage service, or a local directory.
- **Data Sync service**: The NBS 7 service and API that extract data from the NBS cloud environment.

## In this section

The pages in this section cover each component of the NND Service deployment in sequence:

1. [Validate API endpoints](./nnd-service/validating-api-endpoints.html): Verify API connectivity, credential setup, and baseline endpoint responses.
1. [Deploy NND Sync](./nnd-service/on-prem-nnd-sync.html): Configure the on-premises NNDSS integration workflow that uses Data Sync outputs.
1. [Deploy Data Availability (on-premises)](./nnd-service/on-prem-data-sync.html): Configure on-premises options for syncing selected data to SQL Server, Amazon S3, or local storage.
1. [Deploy Data Sync service API (cloud)](./nnd-service/deploy-data-sync-service-api-cloud.html): Install and configure the cloud Data Sync service API with Helm.
