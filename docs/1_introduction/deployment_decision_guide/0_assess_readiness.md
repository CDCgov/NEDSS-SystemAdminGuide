---
title: Assess your readiness
layout: page
parent: NBS 7 Deployment Decision Guide
grand_parent: Introduction
nav_order: 1
---

<!-- PAGE TITLE - DON'T INCLUDE HEADER IN TOC -->
## Assess your readiness for NBS 7
{: .no_toc }

<!-- INTRO OR OVERVIEW -->
This section helps you assess whether NBS 7 is a viable option for your jurisdiction before you commit to a migration. Some prerequisites in this section are also covered in the **NBS 7 Migration Info Sheet**. If your jurisdiction has already begun the migration process, use that document alongside this one.

{: .important-title }
> What leadership needs to know
> 
> NBS 7 does not replace NBS 6 in a single cutover. You deploy NBS 7 components alongside your existing NBS 6 instance, and NBS 7 gradually takes over functionality while both systems run in parallel. Several of the prerequisites reflect this reality: your NBS 6 instance must remain operational during migration, and your network must support communication between both systems.

If you work through this section and find that your jurisdiction does not meet one or more prerequisites, you might still be able to move forward. You can address some gaps with planning and lead time, but other gaps might indicate that NBS 7 is not the right fit for your jurisdiction right now.

1. TOC
{:toc}

---

## State IT security approval

Has your jurisdiction obtained state IT security approval for cloud hosting and the software technologies that NBS 7 requires, including Kubernetes, Terraform, and Docker?

- **Yes, or approval is not required** — Continue with the rest of this section.
- **No, or unknown** — Begin the approval process now. Approval timelines vary and can significantly affect your migration schedule. Work with your state IT office while you continue planning.

{: .important-title }
> What leadership needs to know
> 
> State IT security approval is often the longest-lead item in an NBS 7 migration. If your jurisdiction has not started this process, start it now even if deployment is months away. Waiting until you are technically ready to deploy before you seek approval is one of the most common causes of migration delays.


## Cloud infrastructure

NBS 7 is a cloud-only system. It does not support on-premises deployment.

You need an active account with a supported cloud provider:

- **Amazon Web Services (AWS)** — The primary supported option. NBS 7 has been fully tested on AWS.
- **Microsoft Azure** — Supported via Terraform. Use this option if your jurisdiction has an existing Azure commitment or a compliance requirement that mandates Azure.

{: .important-title }
> What leadership needs to know
> 
> NBS 6 could run on-premises. NBS 7 cannot. Your jurisdiction needs a cloud account and ongoing budget to sustain cloud infrastructure costs. Cloud hosting costs scale with usage, which means your budget planning should account for both normal operations and surge scenarios such as outbreak response.


## Technical staff capacity

NBS 7 uses Kubernetes, a container orchestration platform. To deploy and maintain NBS 7, you need staff who can:

- Deploy and manage Kubernetes clusters
- Read and modify Terraform configuration files
- Manage cloud networking, storage, and access control
- Monitor system health and respond to alerts

If your IT team does not have these skills, you have two options:

- **Build capacity** — Train existing staff or hire staff with these skills before you begin deployment.
- **Use a vendor** — Contract with a vendor to deploy or manage your NBS 7 infrastructure. See [Vendor-managed deployment](../1_choose_configuration/2_vendor_managed_deployment/) for guidance on what to look for in a vendor.

{: .important-title }
> What leadership needs to know
> 
> Migrating to NBS 7 requires different technical skills than running NBS 6. Assess the current capacity of your team before you commit to a migration timeline. If you underestimate the staffing requirement, it will likely result in your migration taking longer than expected.


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
- You need to know your current NBS 6 hosting setup before you begin — specifically, whether it is hosted on-premises or in the cloud, and if in the cloud, which provider.
- **You must be running NBS 6.0.16.1 or higher** before you can install any version of NBS 7. Verify your current NBS 6 version before you begin planning your migration timeline.

{: .important-title }
> What leadership needs to know
> 
> Migration to NBS 7 is a gradual process, not a hard cutover. Plan for the operational complexity and cost of running two systems simultaneously for a period of time.


## CDC coordination

Contact your CDC NBS point of contact before you begin deployment. CDC provides deployment support at no cost and can help you:

- Validate your technical readiness
- Identify the right configuration for your jurisdiction
- Connect you with other jurisdictions that have already migrated

**Contact:** [nbs@cdc.gov](mailto:nbs@cdc.gov)
