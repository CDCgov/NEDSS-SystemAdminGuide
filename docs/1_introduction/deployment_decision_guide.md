---
title: NBS 7 Deployment Decision Guide
layout: page
parent: Introduction
nav_order: 2
---

# NBS 7 Deployment Decision Guide
{: .no_toc }

This guide helps your jurisdiction decide whether to adopt NBS 7 and, if so, plan your deployment configuration. Use it before you begin migration planning.

This guide is written for **STLT IT administrators** who currently operate NBS 6 and are evaluating whether to migrate to NBS 7.

Use this guide to:

- Assess whether NBS 7 is the right fit for your jurisdiction
- Understand what components make up NBS 7 and what each one does
- Identify which configuration would be right for your jurisdiction if you move forward
- Prepare a recommendation for your leadership

If you are a **health department leader** trying to understand whether migrating to NBS 7 is the right decision for your jurisdiction, look for the **What leadership needs to know** callout boxes throughout this guide. These summarize the key points you need to make an informed go/no-go decision.

## In this guide
{: .no_toc }

1. [Before you start](#before-you-start) — Readiness checks and prerequisites
2. [Choose your configuration](#choose-your-configuration) — Decision framework and decision tree
3. [Deploy NBS 7](#deploy-nbs-7) — Real-world deployment scenarios and a link to the [NBS 7 System Administrator Guide](https://cdcgov.github.io/NEDSS-SystemAdminGuide/)
4. [Component reference](#component-reference) — Documentation for each NBS 7 component

## How this guide fits into the NBS 7 process
{: .no_toc }

Three documents support the NBS 6 to NBS 7 transition. Each serves a different purpose:

| Document | Purpose | When to use |
|:---|:---|:---|
| **NBS 7 Deployment Decision Guide** (this guide) | Helps IT administrators and leadership evaluate NBS 7, understand hosting requirements, and choose a component configuration | Use first |
| **NBS 7 Migration Info Sheet** | Guides your jurisdiction through the migration process, including timelines, roles, a compatibility checklist, and cutover planning | Use after confirming NBS 7 is the right fit |
| **NBS 7 System Administrator Guide** | Provides step-by-step deployment instructions for your chosen configuration | Use when ready to deploy |

Some prerequisites covered in this guide are also covered in the Migration Info Sheet. This guide reinforces the prerequisites so that your IT team can use it independently, before beginning the migration process.

> NBS 7 is under active development. Component availability and configuration options will change as development continues. Make sure you are reading the latest version of this guide before you begin to plan.
{: .note }

---

## Before you start
{: .no_toc }

---
layout: default
title: Before you start
parent: NBS 7 Deployment Decision Guide
nav_order: 1
---

# Before you start
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

This section helps you assess whether NBS 7 is a viable option for your jurisdiction before you commit to a migration. Some prerequisites in this section are also covered in the **NBS 7 Migration Info Sheet**. If your jurisdiction has already begun the migration process, use that document alongside this one.

If you work through this section and find that your jurisdiction does not meet one or more prerequisites, you might still be able to move forward. You can address some gaps with planning and lead time, but other gaps might indicate that NBS 7 is not the right fit for your jurisdiction right now.

> NBS 7 does not replace NBS 6 in a single cutover. You deploy NBS 7 components alongside your existing NBS 6 instance, and NBS 7 gradually takes over functionality while both systems run in parallel. Several of the prerequisites reflect this reality: your NBS 6 instance must remain operational during migration, and your network must support communication between both systems.
{: .note }

---

## State IT security approval

Has your jurisdiction obtained state IT security approval for cloud hosting and the software technologies that NBS 7 requires, including Kubernetes, Terraform, and Docker?

- **Yes, or approval is not required** — Continue with the rest of this section.
- **No, or unknown** — Begin the approval process now. Approval timelines vary and can significantly affect your migration schedule. Work with your state IT office while you continue planning.

> State IT security approval is often the longest-lead item in an NBS 7 migration. If your jurisdiction has not started this process, start it now even if deployment is months away. Waiting until you are technically ready to deploy before you seek approval is one of the most common causes of migration delays.
{: .highlight }

---

## Cloud infrastructure

NBS 7 is a cloud-only system. It does not support on-premises deployment.

You need an active account with a supported cloud provider:

- **Amazon Web Services (AWS)** — The primary supported option. NBS 7 has been fully tested on AWS.
- **Microsoft Azure** — Supported via Terraform. Use this option if your jurisdiction has an existing Azure commitment or a compliance requirement that mandates Azure.

> NBS 6 could run on-premises. NBS 7 cannot. Your jurisdiction needs a cloud account and ongoing budget to sustain cloud infrastructure costs. Cloud hosting costs scale with usage, which means your budget planning should account for both normal operations and surge scenarios such as outbreak response.
{: .highlight }

---

## Technical staff capacity

NBS 7 uses Kubernetes, a container orchestration platform. To deploy and maintain NBS 7, you need staff who can:

- Deploy and manage Kubernetes clusters
- Read and modify Terraform configuration files
- Manage cloud networking, storage, and access control
- Monitor system health and respond to alerts

If your IT team does not have these skills, you have two options:

- **Build capacity** — Train existing staff or hire staff with these skills before you begin deployment.
- **Use a vendor** — Contract with a vendor to deploy or manage your NBS 7 infrastructure. See [Vendor-managed deployment](#vendor-managed-deployment) for guidance on what to look for in a vendor.

> Migrating to NBS 7 requires different technical skills than running NBS 6. Assess the current capacity of your team before you commit to a migration timeline. If you underestimate the staffing requirement, it will likely result in your migration taking longer than expected.
{: .highlight }

---

## Network readiness

Before deployment, your network must meet the following requirements:

- **NBS 6 and NBS 7 connectivity** — Each NBS 7 instance requires network connectivity to a corresponding NBS 6 instance. If your NBS 6 runs in a Virtual Private Cloud (VPC), that VPC must be connected to your NBS 7 environment.
- **VM co-location** — Any virtual machines (VMs) that you use for NBS 7 components must exist within the same network.
- **Encryption** — Encryption is required for all virtual network traffic between NBS 6 and NBS 7 components.
- **Outbound access** — Your cloud environment needs outbound internet access to reach CDC systems.
- **TLS/SSL certificate management** — You need a process to provision and renew TLS/SSL certificates for encrypted traffic.

Your specific network configuration will depend on your cloud provider and the existing infrastructure for your jurisdiction.

---

## NBS 6 status

During migration, NBS 7 components gradually replace NBS 6 functionality while NBS 6 continues to run. This means:

- Your jurisdiction will run both systems in parallel during the transition.
- Your NBS 6 instance must remain operational and accessible during migration.
- You need to know your current NBS 6 hosting setup before you begin — specifically, whether it is hosted on-premises or in the cloud, and if in the cloud, which provider.
- **You must be running NBS 6.0.16.1 or higher** before you can install any version of NBS 7. Verify your current NBS 6 version before you begin planning your migration timeline.

> Migration to NBS 7 is a gradual process, not a hard cutover. Plan for the operational complexity and cost of running two systems simultaneously for a period of time.
{: .highlight }

---

## CDC coordination

Contact your CDC NBS point of contact before you begin deployment. CDC provides deployment support at no cost and can help you:

- Validate your technical readiness
- Identify the right configuration for your jurisdiction
- Connect you with other jurisdictions that have already migrated

**Contact:** [nbs@cdc.gov](mailto:nbs@cdc.gov)

---

## Choose your configuration
{: .no_toc }

---
layout: default
title: Choose your configuration
parent: NBS 7 Deployment Decision Guide
nav_order: 2
has_children: true
has_toc: false
---

# Choose your configuration
{: .no_toc }

NBS 7 is modular. Rather than a single fixed system, it is a set of components that you assemble based on the size, technical capacity, and public health needs of your jurisdiction. This section helps you understand your options and identify the right starting configuration for your jurisdiction.

Work through the following sections in order:

1. [Configuration tiers](#configuration-tiers) — Understand the four NBS 7 configuration options
2. [Vendor-managed deployment](#vendor-managed-deployment) — Guidance if your jurisdiction plans to use a vendor
3. [Decision tree](#decision-tree) — Answer a series of questions to get a recommended starting configuration

---

## Configuration tiers

There are four ways to deploy NBS 7:

- [NBS Core](#nbs-core)
- [NBS Core + Real-Time Reporting (RTR)](#nbs-core--real-time-reporting-rtr)
- [NBS Core + Data Ingestion (DI) API](#nbs-core--data-ingestion-di-api)
- [NBS Complete](#nbs-complete)

> You do not have to deploy everything at once. Most jurisdictions will start with NBS Core, then add RTR or the DI API as their team builds confidence with the platform. Starting smaller reduces deployment risk and gives your team time to learn the system before taking on additional complexity.
{: .highlight }

### NBS Core

The minimum viable deployment. NBS Core gives your jurisdiction NBS 6 feature parity on modern, cloud-based infrastructure, plus foundational NBS 7 improvements such as real-time patient search.

NBS Core components are organized into three layers. For details on what each component does and when you need it, see [NBS Core components](#nbs-core-components).

**Networking layer**

The networking layer manages traffic routing and secure communication between your NBS 6 and NBS 7 environments.

- DNS infrastructure (Route 53 or equivalent)
- Virtual Private Cloud (VPC) and routing groups
- VPN connectivity between NBS 6 and NBS 7 instances

**Infrastructure layer**

The infrastructure layer provides the container orchestration platform and cloud services that host and run NBS 7 components.

- Kubernetes cluster (EKS on AWS, AKS on Azure)
- NGINX Ingress Controller (being replaced by Traefik in future releases)
- AWS or Azure managed services
- Terraform infrastructure automation modules
- Load balancer

**Application layer**

The application layer contains the NBS 7 services and legacy NBS 6 components that users and administrators directly interact with.

- [Legacy NBS 6](#legacy-nbs-6)
- [NBS Modernization API](#nbs-modernization-api)
- [NBS Web UI](#nbs-web-ui)
- [NBS Gateway](#nbs-gateway)
- [Page Builder](#page-builder)
- [Elasticsearch](#elasticsearch)
- [Nifi](#nifi)
- [Keycloak](#keycloak)
- [ArgoCD, Cert Manager, FluentBit](#infrastructure-and-networking-layer-components)
- Database (NBS\_ODSE and NBS\_SRTE)

> Best for jurisdictions with smaller IT teams, limited cloud experience, or a goal to establish a stable foundation before adding advanced features.
{: .best-for }

---

### NBS Core + Real-Time Reporting (RTR)

Core plus modern analytics. This configuration adds the Real-Time Reporting (RTR) pipeline, which we recommend using alongside the legacy MasterETL batch process during transition, with the goal of eventually replacing it.

**With RTR, data is available within 5 minutes to 1 hour instead of 24 hours.**

RTR adds the following components. For details, see [Add-on: Real-Time Reporting (RTR)](#add-on-real-time-reporting-rtr).

- [Debezium](#debezium)
- [Kafka and Kafka Connect](#kafka-and-kafka-connect)
- [RTR domain services](#rtr-domain-services)
- [RDB\_Modern](#rdb_modern)

> Best for jurisdictions with higher case volumes, a need for faster data turnaround, or plans to connect to advanced analytics tools.
{: .best-for }

---

### NBS Core + Data Ingestion (DI) API

Core plus a built-in data transit layer. This configuration adds the Data Ingestion (DI) API, which accepts incoming public health data in multiple formats and routes it into NBS without requiring third-party middleware.

For details, see [Add-on: Data Ingestion (DI) API](#add-on-data-ingestion-di-api).

> Best for jurisdictions that do not currently use Rhapsody or Mirth Connect for data ingestion, and want a built-in path for getting data into NBS 7.
{: .best-for }

---

### NBS Complete

The full NBS 7 deployment. NBS Complete includes NBS Core, RTR, and the DI API.

> Best for jurisdictions with larger IT teams, high case volumes, and advanced reporting or analytics needs.
{: .best-for }

---

## Vendor-managed deployment

If you plan to use a vendor to host or maintain NBS 7, the guidance in this section applies to you.

Before you engage a vendor, confirm that they can:

- Deploy Kubernetes-based applications on AWS or Azure
- Manage Terraform-based infrastructure provisioning
- Support ongoing cloud infrastructure operations, including monitoring and incident response

> NBS 7 is a recent system with limited deployment history. Do not expect vendors to have direct NBS 7 experience. Evaluate vendors on their Kubernetes and cloud infrastructure expertise instead. You can share the [component reference](#component-reference) section of this guide with vendors to help them scope the work accurately.
{: .note }

Share the following with your vendor before scoping work:

- The [component reference](#component-reference) section of this guide
- The **NBS 7 Migration Info Sheet** (available from CDC)
- Your current NBS 6 hosting setup and data volumes

Then:

1. Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) to let CDC know you are planning a vendor-managed deployment and to access vendor coordination resources.
2. Work with your vendor to complete steps 4–8 of the [decision tree](#decision-tree) to identify your recommended configuration tier.
3. Return to the [component reference](#component-reference) for the configuration parameters your vendor will need.

> Vendors with Kubernetes and cloud infrastructure expertise can deploy NBS 7, but they will need detailed technical guidance from CDC and from this guide to do it accurately. Plan for a close working relationship between your vendor and the CDC NBS team, especially during initial deployment. Also plan for the funding needed to sustain vendor support beyond initial deployment. Ongoing maintenance costs are a common planning gap.
{: .highlight }

---

## Decision tree

Use this decision tree to identify your recommended starting configuration. Answer each question in order, then validate your recommendation with the CDC NBS team before you begin deployment.

> The decision tree identifies a recommended starting point, not a final answer. CDC provides free pre-deployment consultation to help jurisdictions validate their configuration choice. Do not begin deployment without first connecting with the CDC NBS team at [nbs@cdc.gov](mailto:nbs@cdc.gov).
{: .highlight }

### Step 1: Hosting model

Is your jurisdiction planning to self-host and self-maintain NBS 7, or will you use a vendor to host or maintain it?

- **Self-hosted, self-maintained** — Go to [Step 2](#step-2-state-it-security-approval).
- **Vendor-hosted or vendor-maintained** — Go to [Vendor-managed deployment](#vendor-managed-deployment).

### Step 2: State IT security approval

Has your jurisdiction obtained state IT security approval for cloud hosting and the required software technologies (Kubernetes, Terraform, Docker)?

- **Yes, or approval is not required** — Go to [Step 3](#step-3-internal-technical-capacity).
- **No, or unknown** — Begin the approval process now, then continue planning. Approval is required before deployment. Go to [Step 3](#step-3-internal-technical-capacity).

### Step 3: Internal technical capacity

Does your jurisdiction have IT staff with skills in Kubernetes, Terraform, and cloud infrastructure management, roughly half or more of the required skill set?

- **Yes** — Go to [Step 4](#step-4-current-nbs-6-hosting).
- **No** — Go to [Step 3a](#step-3a-external-assistance).

### Step 3a: External assistance

Will your jurisdiction obtain external assistance from a contractor, vendor, or consultant for deployment and ongoing maintenance?

- **Yes** — Go to [Step 4](#step-4-current-nbs-6-hosting). Note that your vendor or contractor must be capable of Kubernetes-based deployments on AWS or Azure. See [Vendor-managed deployment](#vendor-managed-deployment) for what to look for.
- **No** — **Stop.** Build internal capacity or identify a vendor before proceeding. Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) for support resources.

### Step 4: Current NBS 6 hosting

Where does your NBS 6 currently run?

- **Already on AWS** — Lowest migration complexity. Go to [Step 5](#step-5-case-volume).
- **Already on Azure** — Low migration complexity; you will follow the Azure-specific deployment path. Go to [Step 5](#step-5-case-volume).
- **On-premises** — Your migration includes a cloud migration as well as an NBS 7 deployment. Plan for additional time and resources. Go to [Step 5](#step-5-case-volume).

### Step 5: Case volume

What is the approximate annual reportable disease case volume in your jurisdiction?

- **Lower volume** (fewer than approximately 50,000 cases per year) — Go to [Step 6](#step-6-data-intake-needs-lower-volume-jurisdictions).
- **Higher volume** (50,000+ cases per year), or significant growth expected — Go to [Step 7](#step-7-reporting-needs-higher-volume-jurisdictions).

> The 50,000 case threshold is a planning guideline, not a hard rule. Validate your volume assessment with CDC before making a final configuration decision.
{: .note }

### Step 6: Data intake needs (lower-volume jurisdictions)

Does your jurisdiction currently receive high volumes of electronic lab reports (ELRs) or electronic case reports (eCRs)?

- **No** — Recommended configuration: **NBS Core**. Validate with CDC before deploying.
- **Yes** — Recommended configuration: **NBS Core + DI API**. Validate with CDC before deploying.

### Step 7: Reporting needs (higher-volume jurisdictions)

Does your jurisdiction need near-real-time reporting — data available within minutes to hours, rather than 24 hours?

- **No** — Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) to discuss your specific needs. **NBS Core or NBS Core + DI API** may be appropriate starting points.
- **Yes** — Go to [Step 8](#step-8-data-intake-needs-higher-volume-jurisdictions).

### Step 8: Data intake needs (higher-volume jurisdictions)

Does your jurisdiction currently receive high volumes of ELRs or eCRs?

- **No** — Recommended configuration: **NBS Core + RTR**. Validate with CDC before deploying.
- **Yes** — Recommended configuration: **NBS Complete**. Validate with CDC before deploying.

---

## Deploy NBS 7
{: .no_toc }

---
layout: default
title: Deploy NBS 7
parent: NBS 7 Deployment Decision Guide
nav_order: 3
has_children: true
has_toc: false
---

# Deploy NBS 7
{: .no_toc }

Once you have chosen your configuration, use the [**NBS 7 System Administrator Guide**](https://cdcgov.github.io/NEDSS-SystemAdminGuide/) for step-by-step deployment instructions.

The following sections cover actual NBS 7 deployment scenarios as example use cases. No two jurisdictions have identical infrastructure, staffing, or data needs, so your configuration will not match any of these exactly. Use the examples to identify which profile is closest to your situation and to understand the tradeoffs that other jurisdictions encountered.

---

### Deployment scenario: Small jurisdiction, self-managed, AWS

*Based on Montana's deployment.*

**Profile**

Small STLT with limited IT staff and a cloud-first infrastructure strategy. The jurisdiction prioritized simplicity and maintainability over advanced features.

**Configuration**

| Setting | Value |
|:---|:---|
| Tier | NBS Core only |
| Hosting | AWS, STLT-managed |
| Middleware | No third-party middleware |

**What was deployed**

| Component | Included | Notes |
|:---|:---|:---|
| NBS Core | Yes | Full core deployment |
| Real-Time Reporting (RTR) | No | Not required at this case volume |
| DI API | No | No existing high-volume ELR or eCR intake |

**Key configuration decisions**

- \[Placeholder: specific AWS configuration choices, e.g. EKS node sizing, VPC setup\]
- \[Placeholder: any components skipped within NBS Core and rationale\]
- \[Placeholder: identity provider integration approach\]

**Lessons learned**

- \[Placeholder: what worked well\]
- \[Placeholder: challenges encountered\]
- \[Placeholder: what this jurisdiction would do differently\]

> Might apply to jurisdictions that have a small IT team, limited cloud experience, or a goal to get NBS 7 running with minimal complexity before adding advanced features.
{: .best-for }

---

### Deployment scenario: Medium jurisdiction, existing middleware, RTR

*Based on Kentucky's deployment.*

**Profile**

Medium STLT with an existing Rhapsody middleware investment and a need for faster data turnaround than NBS 6 batch processing provides. The jurisdiction retained Rhapsody for data ingestion rather than replacing it with the DI API.

**Configuration**

| Setting | Value |
|:---|:---|
| Tier | NBS Core + RTR |
| Hosting | Hybrid — cloud-hosted NBS 7, on-premises Rhapsody middleware |
| Middleware | Rhapsody (retained) |

**What was deployed**

| Component | Included | Notes |
|:---|:---|:---|
| NBS Core | Yes | Full core deployment |
| Real-Time Reporting (RTR) | Yes | Added for faster reporting turnaround |
| DI API | No | Rhapsody retained for data ingestion |

**Key configuration decisions**

- Rhapsody integrates directly with the NBS database rather than routing through the DI API. Jurisdictions with existing Rhapsody investments should follow this pattern.
- \[Placeholder: RTR configuration specifics for this scale\]
- \[Placeholder: how the hybrid hosting model was structured\]
- \[Placeholder: custom integration points between Rhapsody and NBS 7\]

**Lessons learned**

- \[Placeholder: integration patterns that worked well\]
- \[Placeholder: performance considerations at this scale\]
- \[Placeholder: challenges encountered\]

> Might apply to jurisdictions that have existing middleware such as Rhapsody or Mirth Connect that you want to retain, and you need faster reporting turnaround than NBS 6 provides.
{: .best-for }

---

### Deployment scenario: Large jurisdiction, high volume, vendor-managed

*Based on an enterprise-scale deployment.*

**Profile**

Large STLT with high case volumes, sophisticated analytics needs, and a vendor-managed infrastructure model. This jurisdiction required high-availability configuration and advanced security hardening.

**Configuration**

| Setting | Value |
|:---|:---|
| Tier | NBS Complete (NBS Core + RTR + DI API) |
| Hosting | Cloud vendor-managed, or hybrid with significant cloud presence |
| Middleware | DI API (primary ingestion path) |

**What was deployed**

| Component | Included | Notes |
|:---|:---|:---|
| NBS Core | Yes | Full core deployment |
| Real-Time Reporting (RTR) | Yes | Required for high case volume and analytics needs |
| DI API | Yes | Primary path for ELR and eCR ingestion |
| DataSync | — | Verify with CDC NBS point of contact |

> DataSync is not currently documented in this guide because it is only used by one jurisdiction and is not expected to be used long-term. Confirm with your CDC NBS point of contact before planning any DataSync integration.
{: .note }

**Key configuration decisions**

- \[Placeholder: high-availability configuration specifics\]
- \[Placeholder: performance optimization decisions\]
- \[Placeholder: advanced security hardening approach\]
- \[Placeholder: vendor coordination model and responsibilities\]

**Lessons learned**

- \[Placeholder: scaling considerations\]
- \[Placeholder: cost management approach\]
- \[Placeholder: challenges encountered with vendor-managed deployment\]

> Might apply to jurisdictions that have a large IT team or vendor support, high case volumes, advanced reporting or analytics needs, and require high-availability infrastructure.
{: .best-for }

---

## Component reference
{: .no_toc }

---
layout: default
title: Component reference
parent: NBS 7 Deployment Decision Guide
nav_order: 4
has_children: true
has_toc: false
---

# Component reference
{: .no_toc }

This section describes each component in NBS 7. Use it to understand what each component does, why it is included in your configuration, and how it relates to other components.

Components in this reference are organized by configuration tier:

- [NBS Core components](#nbs-core-components)
- [Add-on: Real-Time Reporting (RTR)](#add-on-real-time-reporting-rtr)
- [Add-on: Data Ingestion (DI) API](#add-on-data-ingestion-di-api)

For deployment configuration details including configuration parameters, Helm chart values, and step-by-step setup instructions, see the **NBS 7 System Administrator Guide**.

---

## Quick reference

The following table shows which components are included in each configuration tier.

| Component | NBS Core | Core + RTR | Core + DI API | NBS Complete |
|:---|:---:|:---:|:---:|:---:|
| Legacy NBS 6 | ✓ | ✓ | ✓ | ✓ |
| NBS Modernization API | ✓ | ✓ | ✓ | ✓ |
| NBS Web UI | ✓ | ✓ | ✓ | ✓ |
| NBS Gateway | ✓ | ✓ | ✓ | ✓ |
| Page Builder | ✓ | ✓ | ✓ | ✓ |
| Elasticsearch | ✓ | ✓ | ✓ | ✓ |
| Nifi | ✓ | ✓ | ✓ | ✓ |
| Keycloak | ✓ | ✓ | ✓ | ✓ |
| Database (NBS\_ODSE, NBS\_SRTE) | ✓ | ✓ | ✓ | ✓ |
| Infrastructure and networking layer | ✓ | ✓ | ✓ | ✓ |
| Debezium | | ✓ | | ✓ |
| Kafka and Kafka Connect | | ✓ | | ✓ |
| RTR domain services | | ✓ | | ✓ |
| RDB\_Modern | | ✓ | | ✓ |
| DI API | | | ✓ | ✓ |

> NBS Core components are required for all NBS 7 deployments. RTR and DI API are optional add-ons, so their components are only required if your jurisdiction chooses a configuration tier that includes them.
{: .note }

---

## NBS Core components

NBS Core includes three layers of components: the application layer, the infrastructure layer, and the networking layer. The application layer components are documented individually below. [Infrastructure and networking layer components](#infrastructure-and-networking-layer-components) are summarized as a group.

\[architecture diagram\]

> The NBS Modernization API, NBS Web UI, NBS Gateway, and Page Builder are deployed together from the NEDSS-Modernization repository. Each serves a distinct function, but vendors and admins scoping deployment work should be aware that they share a single deployment unit.
{: .note }

---

### Legacy NBS 6

The existing NBS 6 application. A WildFly-based UI and backend that most STLTs currently run.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | NBS Core does not replace NBS 6 immediately. Instead, it runs alongside it. During migration, the NBS Gateway routes requests between the legacy NBS 6 application and new NBS 7 services. NBS 6 continues to handle all functionality that has not yet been replaced by a modern NBS 7 equivalent. |
| When you need it | Always. An operational NBS 6 instance is a prerequisite for any NBS 7 deployment. You must be running NBS 6.0.16.1 or newer before installing NBS 7. |
| Dependencies | Required by NBS Gateway, Elasticsearch (via Nifi), and the NBS Modernization API. Must maintain network connectivity to your NBS 7 environment throughout the migration period. |

---

### NBS Modernization API

The modern backend API layer for NBS 7, built to replace NBS 6 functionality incrementally.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Provides modernized versions of core NBS features including patient search, event search, patient profile, and investigation management. As NBS 7 development progresses, additional NBS 6 features will migrate into this API layer. |
| When you need it | Always. The Modernization API is a core component of NBS Core and is required for all NBS 7 configurations. |
| Dependencies | Requires Legacy NBS 6 and NBS Gateway. Exposes functionality to the NBS Web UI. |

---

### NBS Web UI

The modern React/TypeScript frontend for NBS 7 features.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Provides the user interface for modernized NBS 7 functionality. STLT users see a composite interface — some screens are served by the new NBS Web UI, while others continue to be served by the legacy NBS 6 UI. The NBS Gateway manages which interface handles each request. |
| When you need it | Always. The NBS Web UI is a core component of NBS Core and is required for all NBS 7 configurations. |
| Dependencies | Requires NBS Gateway and the NBS Modernization API. |

---

### NBS Gateway

A routing service (built on Spring Cloud Gateway) that manages traffic between the legacy NBS 6 application and modern NBS 7 services.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Implements the strangler fig pattern by routing requests based on path. Requests for modernized features (such as patient search and Page Builder) go to NBS 7 services. All other requests go to Legacy NBS 6. This routing layer is what allows NBS 6 and NBS 7 to run simultaneously during migration without users needing to switch between systems. |
| When you need it | Always. NBS Gateway is a core component of NBS Core and is required for all NBS 7 configurations. |
| Dependencies | Requires Legacy NBS 6, the NBS Modernization API, and the NBS Web UI. Sits behind the infrastructure layer ingress controller. |

---

### Page Builder

A tool for creating and editing the investigation forms used by STLT epidemiologists and disease investigators.

> This component is not yet confirmed for production. Verify current status with your CDC NBS point of contact before planning any Page Builder integrations.
{: .note }

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Allows authorized users to configure the data collection forms associated with specific diseases and conditions. Maintains the ability to customize forms to meet jurisdiction-specific reporting requirements. |
| When you need it | Always, if your jurisdiction uses NBS to manage investigation forms. Page Builder is included in NBS Core. |
| Dependencies | Requires the NBS Modernization API. |

---

### Report Execution API

A Python FastAPI service intended to replace SAS-based report execution in NBS 7. SAS 9.4 is currently required for report execution and must be carried forward into NBS 7 deployments until this component is production-ready. Jurisdictions with significant SAS infrastructure or licensing costs should monitor this component as NBS 7 matures.

> This component is not yet confirmed for production. Check with your CDC NBS point of contact to find out whether it affects your deployment plan.
{: .note }

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | \[Pending SME verification\] |
| Dependencies | \[Pending SME verification\] |

---

### Elasticsearch

An open source search and analytics engine optimized for speed and scalability.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Powers real-time patient and event search in NBS 7. NBS 6 required batch processing before search results reflected recent data, so this is a key improvement. [Nifi](#nifi) populates Elasticsearch indices from the NBS database. |
| When you need it | Always. Elasticsearch is a core component of NBS Core and is required for all NBS 7 configurations. |
| Dependencies | Requires Nifi to populate its indices from the NBS database. Search functionality in the NBS Web UI and Modernization API depends on Elasticsearch. |

---

### Nifi

An open source data flow automation tool for moving and transforming data between systems.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Continuously moves data from the NBS database into Elasticsearch, keeping search indices current. Without Nifi, Elasticsearch indices would not reflect recent changes to patient and investigation records. |
| When you need it | Always. Nifi is a core component of NBS Core and is required for all NBS 7 configurations. |
| Dependencies | Requires the NBS database (NBS\_ODSE) as its data source and Elasticsearch as its destination. |

---

### Keycloak

An open source identity and access management platform.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Handles authentication for NBS 7, including token management and single sign-on (SSO) integration. Keycloak supports OAuth and SAML, which means your jurisdiction can integrate NBS 7 with an existing identity provider such as Okta or Active Directory Federation Services (ADFS) rather than managing a separate set of NBS credentials. |
| When you need it | Always. Keycloak is a core component of NBS Core and is required for all NBS 7 configurations. |
| Dependencies | Requires network access to your identity provider if you are integrating with an existing SSO system. All NBS 7 services that require authentication depend on Keycloak. |

> If your jurisdiction uses a centralized identity provider (such as Okta or Active Directory), Keycloak can integrate with it. This means NBS 7 users can log in with their existing jurisdiction credentials rather than managing a separate NBS login. Coordinate with your identity management team early. SSO integration configuration requires input from both the NBS deployment team and your identity provider administrators.
{: .highlight }

---

### Database (NBS\_ODSE, NBS\_SRTE)

The core SQL Server databases that store operational and reference data for NBS.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | NBS\_ODSE (Operational Data Store) is the primary transactional database where case, patient, investigation, and event records are stored. NBS\_SRTE (System Reference Tables) stores reference and metadata used across NBS, including LOINC, SNOMED CT, and other code sets used for data validation and mapping. |
| When you need it | Always. Both databases are required for all NBS 7 configurations. |
| Dependencies | Required by Legacy NBS 6, the Modernization API, Nifi, Debezium (if using RTR), and the DI API (if using the DI API add-on). |

---

### Infrastructure and networking layer components

The following components make up the infrastructure and networking layers of NBS Core. They are provisioned and managed primarily through Terraform and Helm, and most do not require configuration decisions from IT admins during the planning phase. They are documented here for awareness.

Full configuration guidance is in the [NBS 7 System Administrator Guide](https://cdcgov.github.io/NEDSS-SystemAdminGuide/).

| Component | What it does in NBS 7 |
|:---|:---|
| Kubernetes (EKS/AKS) | Container orchestration platform that hosts and manages all NBS 7 services. EKS is used on AWS; AKS is used on Azure. |
| NGINX Ingress Controller | Manages inbound traffic routing into the Kubernetes cluster. Currently being replaced by Traefik in future releases — confirm current status with your CDC NBS point of contact. |
| Terraform modules | Infrastructure-as-code tooling that provisions your cloud environment, including VPC, Kubernetes cluster, storage, and managed services. Four modules cover network/VPC, NBS 6 database layer, NBS 7 cluster, and application services. |
| ArgoCD | Continuous deployment tool that manages application delivery to the Kubernetes cluster. Keeps deployed services in sync with their defined configurations. |
| Cert Manager | Automates provisioning and renewal of TLS/SSL certificates for encrypted traffic within and into the NBS 7 environment. |
| FluentBit | Lightweight log forwarding agent that collects and routes logs from NBS 7 services for monitoring and troubleshooting. |
| Linkerd | Service mesh (provisioned via Terraform) that manages encrypted communication between NBS 7 services inside the Kubernetes cluster. |
| DNS (Route 53 or equivalent) | Routes user traffic to your NBS 7 environment. On AWS, Route 53 is the standard option; Azure and on-premises DNS services are also supported. |

---

## Add-on: Real-Time Reporting (RTR)

RTR works alongside the legacy MasterETL batch process during transition, with the goal of eventually replacing it. The following components are added to your NBS Core deployment when you choose NBS Core + RTR or NBS Complete.

> The primary benefit of RTR is speed. Data that previously took up to 24 hours to appear in reports is available within 5 minutes to 1 hour. For jurisdictions managing active outbreaks or time-sensitive disease investigations, this can meaningfully affect response time. But RTR adds infrastructure complexity and requires additional cloud resources, which will impact your operating costs.
{: .highlight }

---

### Debezium

An open-source Change Data Capture (CDC) platform.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Monitors the NBS database for changes in real time and streams those changes to Kafka as they occur. Debezium is the entry point for the RTR pipeline. Without it, downstream RTR components have no data to process. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Requires the NBS database (NBS\_ODSE) as its source. Streams data to the Kafka cluster. |

---

### Kafka and Kafka Connect

Apache Kafka is an open source event-streaming platform. Kafka Connect is the framework that moves data between Kafka and other systems.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Acts as the message bus for the RTR pipeline. Kafka receives change events from Debezium and delivers them to the RTR domain services. Kafka Connect writes the processed output to RDB\_Modern staging tables for post-processing and reporting. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Receives events from Debezium. Delivers messages to RTR domain services. Kafka Connect writes processed data to RDB\_Modern. Requires sufficient cluster resources — Kafka is one of the more operationally demanding components in the RTR stack. |

---

### RTR domain services

A unified Spring Boot service that transforms streaming data from Kafka into reportable public health records. Previously implemented as five separate entity-specific services (investigation, person, observation, organization, and LDF data), these are being consolidated into a single `reporting-service` application to reduce deployment complexity and operational overhead.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Consumes Kafka messages for each entity type (investigations, patients, organizations, observations, and LDF data), runs stored procedures to retrieve and format the data, and produces processed records for downstream storage in RDB\_Modern. A post-processing service then populates analytical datamarts and fact tables from the staging data. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Requires Kafka (message source) and NBS\_ODSE (operational data store). Populates RDB\_Modern staging tables, which are then consumed by the post-processing service. |

> The five entity-specific RTR services (investigation-service, person-service, observation-service, organization-service, ldfdata-service) are being consolidated into a single `reporting-service` as of early 2026. Check with your CDC NBS point of contact for the current deployment state.
{: .note }

---

### RDB\_Modern

The modern reporting database introduced by RTR.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Stores processed, structured public health records produced by the RTR domain services. Runs alongside the legacy RDB during migration. Downstream reporting and analytics tools connect to RDB\_Modern rather than directly to the operational database. |
| When you need it | When your jurisdiction chooses NBS Core + RTR or NBS Complete. |
| Dependencies | Populated by RTR domain services. Required by any reporting or analytics tools that your jurisdiction connects to NBS 7. |

---

## Add-on: Data Ingestion (DI) API

The DI API is a data transit layer built into NBS 7 that accepts incoming public health data and routes it into NBS without requiring third-party middleware. The DI API is added to your NBS Core deployment when you choose NBS Core + DI API or NBS Complete.

> The DI API is relevant if your jurisdiction uses middleware like Rhapsody to route incoming lab reports and case reports into NBS. While the DI API has the potential to reduce middleware licensing costs and simplify your data intake architecture, it is not yet a full replacement for existing middleware solutions. Jurisdictions with Rhapsody or Mirth Connect in place should continue using them for now. If your jurisdiction does not have existing middleware, the DI API is worth evaluating. Consider revisiting its viability as the product matures and new features are released.
{: .highlight }

---

### DI API

A modern data ingestion layer that accepts incoming public health data in multiple formats and routes it into NBS.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Accepts Electronic Case Reports (eCR), HL7 v2.x electronic lab reports (ELRs), and Public Health Document Container (PHDC) files. Validates, transforms, and routes incoming data to the appropriate NBS services. The DI API is designed to be more flexible and maintainable than legacy middleware solutions. |
| When you need it | When your jurisdiction receives high volumes of ELRs or eCRs, or when you want to replace or evaluate alternatives to your current middleware (such as Rhapsody). Required for NBS Core + DI API and NBS Complete configurations. |
| Dependencies | Requires NBS Core. Integrates with external data senders (laboratories, EHR systems, health information exchanges). Routes processed data into the NBS database via the Modernization API. |
