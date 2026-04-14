---
title: Assess your readiness
layout: page
parent: Before you deploy
nav_order: 2
description: Covers the technical prerequisites an STLT should meet before beginning NBS 7 migration, including cloud, staffing, and network requirements.
---

# Assess your readiness for NBS 7
{: .no_toc }

This page helps you assess whether NBS 7 is a viable option for your jurisdiction before you commit to a migration.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

If you work through this page and find that your jurisdiction does not meet one or more prerequisites, you might still be able to move forward. You can address some gaps with planning and lead time, but other gaps might indicate that NBS 7 is not the right fit for your jurisdiction right now.

For more information on migration planning, staffing, and budget, see [Operational considerations](../before-you-deploy/operational-considerations.html) in this guide, and the [NBS 7 Migration Info Sheet](https://nbscentral.cdc.gov/documents/731) and [NBS 7 Resource Estimator](https://nbscentral.cdc.gov/documents/872) on NBS Central (NBS Central login required).
{: .note }

## Not sure where to start?

If you are new to NBS 7 deployment, [Deployment phases](../before-you-deploy/deployment-phases.html) provides an overview of an example rollout and where this readiness assessment fits.

## State IT security approval

Has your jurisdiction obtained state IT security approval for cloud hosting and the software technologies that NBS 7 requires, including Kubernetes, Terraform, and Docker?

- **Yes, or approval is not required**: Continue with the rest of this section.
- **No, or unknown**: Approval timelines vary and can significantly affect your migration schedule. We recommend working with your state IT office while you continue to plan.

See also: [Operational considerations](../before-you-deploy/operational-considerations.html) and [Set up cloud infrastructure](../deploy-nbs7/set-up-cloud-infrastructure.html).

## Cloud infrastructure

NBS 7 requires a cloud-based environment for deployment. NBS 7 has not been tested for on-premises deployment, and CDC does not plan to support it. To deploy with CDC support, you need an active account with one of the following supported cloud providers:

**Amazon Web Services (AWS)**

  - **Strategic fit:** Preferred by jurisdictions with established AWS environments or those prioritizing a broad ecosystem of third-party security and data tools.
  - **Technical readiness:** Aligns with teams experienced in managing container-native architectures via Amazon Elastic Kubernetes Service (EKS) and mature Terraform workflows.
  - **Surveillance context:** Core components are extensively validated in AWS to ensure performance at peak ingestion volumes.

**Microsoft Azure**

  - **Strategic fit:** Preferred by jurisdictions with significant Microsoft ecosystem investments, such as those using Microsoft Entra ID (formerly Azure Active Directory) or existing Enterprise Agreements.
  - **Technical readiness:** Provides a streamlined experience for organizations running Windows-based workloads or requiring integration with Microsoft 365 and Power Platform tools.
  - **Surveillance context:** Supported via Terraform for configuration parity with AWS, allowing jurisdictions to meet internal mandates for Azure-hosted health data.

See also: [Deploy cloud infrastructure on AWS](../deploy-nbs7/deploy-on-aws.html), [Deploy cloud infrastructure on Azure](../deploy-nbs7/deploy-on-azure.html), and [Compatibility matrix](../before-you-deploy/compatibility.html).

## Technical staff capacity

NBS 7 uses Kubernetes, a container orchestration platform. To deploy and maintain NBS 7, you need staff who can:

- Deploy and manage Kubernetes clusters
- Read and modify Terraform configuration files
- Manage cloud networking, storage, and access control
- Monitor system health and respond to alerts

If your IT team does not have these skills, you have two options:

- **Building capacity**: Train existing staff or hire staff with these skills before you begin deployment.
- **Working with a vendor**: Contract with a vendor to deploy or manage your NBS 7 infrastructure. See [Vendor-managed deployment](../before-you-deploy/choose-your-configuration/vendor-managed-deployment.html) for guidance on what to look for in a vendor.

See also: [Operational considerations](../before-you-deploy/operational-considerations.html) and [Choose your configuration](../before-you-deploy/choose-your-configuration.html).

## Network readiness

Before deployment, your network must meet the following requirements:

- **NBS 6 and NBS 7 connectivity**: Each NBS 7 instance requires network connectivity to a corresponding NBS 6 instance. If your NBS 6 runs in a Virtual Private Cloud (VPC), that VPC must be connected to your NBS 7 environment.
- **VM co-location**: Any virtual machines (VMs) that you use for NBS 7 components must exist within the same network.
- **Encryption**: Encryption is required for all virtual network traffic between NBS 6 and NBS 7 components.
- **Outbound access**: Your cloud environment needs outbound internet access to reach CDC systems.
- **TLS/SSL certificate management**: You need a process to provision and renew TLS/SSL certificates for encrypted traffic.

Your specific network configuration will depend on your cloud provider and the existing infrastructure for your jurisdiction.

See also: [Architecture and microservices](../deploy-nbs7/architecture-and-microservices.html), [Cluster infrastructure](../deploy-nbs7/cluster-infrastructure.html), and [Set up cloud infrastructure](../deploy-nbs7/set-up-cloud-infrastructure.html).

## NBS 6 status

During migration, NBS 7 components gradually replace NBS 6 functionality while NBS 6 continues to run. This means:

- Your jurisdiction will run both systems in parallel during the transition.
- Your NBS 6 instance must remain operational and accessible during migration.
- Many jurisdictions provision a separate NBS 6 environment for migration activities and then cut over, rather than deploying NBS 7 changes directly against their primary NBS 6 production server.
- You need to know your current NBS 6 hosting setup before you begin. Specifically, whether it is hosted on-premises or in the cloud, and if in the cloud, which provider.
- **You must be running a compatible NBS 6.x version** before you can install any version of NBS 7. For more information, see [Compatibility matrix](../before-you-deploy/compatibility.html).

See also: [Deployment phases](../before-you-deploy/deployment-phases.html) and [Operational considerations](../before-you-deploy/operational-considerations.html).

## Data migration

NBS 7 uses your existing NBS 6 database and does not require a schema migration. In most cases, no data migration is needed.

If your current NBS 6 database is hosted on-premises and you plan to move it to the cloud as part of your migration, you will need to copy the data from your existing environment and restore it to the new environment using a standard database backup and restore process. If you are not moving your NBS 6 database, no data migration action is required.

See also: [Prerequisites for NBS 7 deployment](../deploy-nbs7/prerequisites.html#nbs-6-readiness), [Deployment scenarios](../before-you-deploy/deployment-scenarios.html), and [Deployment phases](../before-you-deploy/deployment-phases.html).

## CDC coordination

Reach out to your CDC NBS point of contact before you begin deployment. CDC provides deployment support at no cost and can help you:

- Validate your technical readiness
- Identify the right configuration for your jurisdiction
- Connect you with other jurisdictions that have already migrated

See also: [Choose your configuration](../before-you-deploy/choose-your-configuration.html) and [Operational considerations](../before-you-deploy/operational-considerations.html).

**Contact:** [nbs@cdc.gov](mailto:nbs@cdc.gov)
