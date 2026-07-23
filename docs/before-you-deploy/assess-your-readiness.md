---
title: Readiness assessment
layout: page
parent: Before you deploy NBS 7
nav_order: 1
description: Covers the technical prerequisites an STLT should meet before beginning NBS 7 migration, including cloud, staffing, and network requirements.
---

# Assess your technical readiness for NBS 7

This page covers the technical conditions your jurisdiction should review before committing to an NBS 7 migration, including cloud infrastructure, staffing, network readiness, and NBS 6 compatibility.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

If you work through this page and find that your jurisdiction does not meet one or more prerequisites, you might still be able to move forward. You can address some gaps with planning and lead time, but other gaps might indicate that NBS 7 is not the right fit for your jurisdiction right now.

For more information on migration planning, staffing, and budget, see [Operational considerations](../before-you-deploy/operational-considerations.html) in this guide, and the [NBS 7 Migration Info Sheet](https://nbscentral.cdc.gov/documents/731) and [NBS 7 Resource Estimator](https://nbscentral.cdc.gov/documents/872) on NBS Central (NBS Central login required; see [Additional resources](../../index.html#additional-resources)).
{: .note }

## Not sure where to start?

If you are new to NBS 7 deployment, the [Deployment planning guide](../before-you-deploy/planning.html) provides example stages in a typical rollout and where this readiness assessment fits.

## IT security approval

Has your jurisdiction obtained IT security approval for cloud hosting and the software technologies that NBS 7 requires, including Kubernetes, Terraform, and Docker?

- **Yes, or approval is not required**: Continue with the rest of this section.
- **No, or unknown**: Approval timelines vary and can significantly affect your migration schedule. We recommend working with your IT office while you continue to plan.

See also: [Operational considerations](../before-you-deploy/operational-considerations.html) and [Provision cloud infrastructure](../deploy-nbs7/full-deploy/provision-cloud-infrastructure.html).

## Cloud infrastructure

NBS 7 requires a cloud-based environment for deployment; CDC does not support on-premises installations. To deploy with CDC support, you need an active account with one of the following supported cloud providers:

### Amazon Web Services (AWS)

- **Strategic fit:** Preferred by jurisdictions with established AWS environments or those with existing AWS contract vehicles or organizational policies that standardize on AWS.
- **Technical readiness:** Aligns with teams experienced in managing container-native architectures via Amazon Elastic Kubernetes Service (Amazon EKS) and mature Terraform workflows.

### Microsoft Azure

- **Strategic fit:** Preferred by jurisdictions with significant Microsoft ecosystem investments, such as those using Microsoft Entra ID (formerly Azure Active Directory) or existing Enterprise Agreements.
- **Technical readiness:** Provides a streamlined experience for organizations running Windows-based workloads or requiring integration with Microsoft 365 and Power Platform tools.

See also: [Provision cloud infrastructure](../deploy-nbs7/full-deploy/provision-cloud-infrastructure.html) and the [Supported NBS versions](../supported-versions.html).

## Staff Kubernetes expertise

NBS 7 uses Kubernetes, a container orchestration platform. To deploy and maintain NBS 7, you need staff who can:

- Deploy and manage Kubernetes clusters
- Read and modify Terraform configuration files
- Manage cloud networking, storage, and access control
- Monitor system health and respond to alerts

If your IT team does not have these skills, you have two options:

- **Build capacity**: Train existing staff or hire staff with these skills before you begin deployment.
- **Work with a vendor**: Contract with a vendor to deploy or manage your NBS 7 infrastructure. See [Vendor-managed deployment](../before-you-deploy/vendor-managed-deployment.html) for guidance on what to look for in a vendor.

See also: [Operational considerations](../before-you-deploy/operational-considerations.html) and [Deployment phases](../before-you-deploy/deployment-phases.html).

## Network readiness

Before deployment, your network must meet the following requirements:

- **Encryption**: Encryption is required for all virtual network traffic between NBS 6 and NBS 7 components.
- **Outbound access**: Your cloud environment needs outbound internet access to reach CDC systems.
- **TLS/SSL certificate management**: You need a process to provision and renew TLS/SSL certificates for encrypted traffic.

Your specific network configuration will depend on your cloud provider and the existing infrastructure for your jurisdiction.

See also: [NBS 7 architecture and microservices](../nbs7-introduction/architecture-and-microservices.html), [Deploy cluster services](../deploy-nbs7/full-deploy/kubernetes-setup.html), and [Provision cloud infrastructure](../deploy-nbs7/full-deploy/provision-cloud-infrastructure.html).

## NBS 6 status

Migration from NBS 6 to NBS 7 concludes with a cutover from your existing NBS 6 instance to the new NBS 7 deployment. This means that:

- Your jurisdiction will run both systems in parallel during the transition.
- Your NBS 6 instance must remain operational and accessible during migration.
- Some jurisdictions provision a separate NBS 6 environment for migration activities and then cut over, rather than deploying NBS 7 changes directly against their primary NBS 6 production server.
- You need to know your current NBS 6 hosting setup before you begin. Specifically, whether it is hosted on-premises or in the cloud, and if in the cloud, which provider.
- **You must be running a compatible NBS 6.x version** before you can install any version of NBS 7. For more information, see the [Supported NBS versions](../supported-versions.html).

See also: [Deployment planning guide](../before-you-deploy/planning.html) and [Operational considerations](../before-you-deploy/operational-considerations.html).

## Data migration

NBS 7 uses your existing NBS 6 database and does not require a schema migration. Unless you choose to move your database from on premises to the cloud, no data migration should be needed.

If your current NBS 6 database is hosted on-premises and you plan to move it to the cloud as part of your migration, you will need to copy the data from your existing environment and restore it to the new environment using a standard database backup and restore process. If you are not moving your NBS 6 database, no data migration action is required.

See also: [Prerequisites for NBS 7 deployment](../deploy-nbs7/full-deploy/prerequisites.html#nbs-6-readiness) and [Deployment planning guide](../before-you-deploy/planning.html).

## CDC coordination

Reach out to your CDC NBS point of contact before you begin deployment. CDC provides deployment support at no cost and can help you:

- Validate your technical readiness
- Connect you with other jurisdictions that have already migrated

See also: [Deployment phases](../before-you-deploy/deployment-phases.html) and [Operational considerations](../before-you-deploy/operational-considerations.html).

**Contact:** [nbs@cdc.gov](mailto:nbs@cdc.gov)
