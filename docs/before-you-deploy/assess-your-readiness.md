---
title: Assess your readiness
layout: page
parent: Before you deploy
nav_order: 2
description: Covers the technical prerequisites an STLT must meet before beginning NBS 7 migration, including cloud, staffing, and network requirements.
---

# Assess your readiness for NBS 7
{: .no_toc }

This section helps you assess whether NBS 7 is a viable option for your jurisdiction before you commit to a migration. 

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

If you work through this section and find that your jurisdiction does not meet one or more prerequisites, you might still be able to move forward. You can address some gaps with planning and lead time, but other gaps might indicate that NBS 7 is not the right fit for your jurisdiction right now.

For more information on migration planning, staffing, and budget, see [Operational considerations](leadership_considerations.html).
{: .note }

## Not sure where to start?

If you are new to NBS 7 deployment, the [Deployment phases](deployment-phases.html) page provides an overview of an example rollout and where this readiness assessment fits within it.

## State IT security approval

Has your jurisdiction obtained state IT security approval for cloud hosting and the software technologies that NBS 7 requires, including Kubernetes, Terraform, and Docker?

- **Yes, or approval is not required** — Continue with the rest of this section.
- **No, or unknown** — Approval timelines vary and can significantly affect your migration schedule. We recommend working with your state IT office while you continue to plan.

## Cloud infrastructure

NBS 7 has not been tested for on-premises deployment and CDC does not plan to support it. You need an active account with a supported cloud provider:

- **Amazon Web Services (AWS)** — The primary supported option. NBS 7 has been fully tested on AWS.
- **Microsoft Azure** — Supported via Terraform. Use this option if your jurisdiction has an existing Azure commitment or a compliance requirement that mandates Azure.

## Technical staff capacity

NBS 7 uses Kubernetes, a container orchestration platform. To deploy and maintain NBS 7, you need staff who can:

- Deploy and manage Kubernetes clusters
- Read and modify Terraform configuration files
- Manage cloud networking, storage, and access control
- Monitor system health and respond to alerts

If your IT team does not have these skills, you have two options:

- **Building capacity** — Train existing staff or hire staff with these skills before you begin deployment.
- **Working with a vendor** — Contract with a vendor to deploy or manage your NBS 7 infrastructure. See [Vendor-managed deployment](1_choose_configuration/3_vendor_managed_deployment.html) for guidance on what to look for in a vendor.

## Network readiness

Before deployment, your network must meet the following requirements:

- **NBS 6 and NBS 7 connectivity** — Each NBS 7 instance requires network connectivity to a corresponding NBS 6 instance. If your NBS 6 runs in a Virtual Private Cloud (VPC), that VPC must be connected to your NBS 7 environment.
- **VM co-location** — Any virtual machines (VMs) that you use for NBS 7 components must exist within the same network.
- **Encryption** — Encryption is required for all virtual network traffic between NBS 6 and NBS 7 components.
- **Outbound access** — Your cloud environment needs outbound internet access to reach CDC systems.
- **TLS/SSL certificate management** — You need a process to provision and renew TLS/SSL certificates for encrypted traffic.

Your specific network configuration will depend on your cloud provider and the existing infrastructure for your jurisdiction.

## NBS 6 status

During migration, NBS 7 components gradually replace NBS 6 functionality while NBS 6 continues to run. This means:

- Your jurisdiction will run both systems in parallel during the transition.
- Your NBS 6 instance must remain operational and accessible during migration.
- You need to know your current NBS 6 hosting setup before you begin. Specifically, whether it is hosted on-premises or in the cloud, and if in the cloud, which provider.
- **You must be running a compatible NBS 6.x version** before you can install any version of NBS 7. For more information, see the [NBS 6 and NBS 7 compatibility](../../2_prerequisites/compatibility.html) table.

## CDC coordination

Reach out to your CDC NBS point of contact before you begin deployment. CDC provides deployment support at no cost and can help you:

- Validate your technical readiness
- Identify the right configuration for your jurisdiction
- Connect you with other jurisdictions that have already migrated

**Contact:** [nbs@cdc.gov](mailto:nbs@cdc.gov)
