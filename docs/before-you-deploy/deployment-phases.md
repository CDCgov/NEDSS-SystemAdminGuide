---
title: Deployment phases
layout: page
parent: Before you deploy
nav_order: 5
has_children: true
description: Describes the three NBS 7 deployment phases (the )core deployment, Real-Time Reporting (RTR), and Data Ingestion (DI) API) and when to deploy each.
---

# NBS 7 technical deployment phases
{: .no_toc }

NBS 7 is deployed in phases. The first phase is the [core deployment](#phase-1-nbs-7), which gives your jurisdiction NBS 6 feature parity on modern cloud infrastructure. [Real-Time Reporting (RTR)](#phase-2-real-time-reporting-rtr) and the [Data Ingestion (DI) API](#phase-3-data-ingestion-di-api) follow as subsequent phases. Most jurisdictions complete the core deployment first, then plan RTR and DI API deployment as their team builds operational confidence. Separating the phases reduces initial deployment risk and gives your team time to learn the system before taking on additional complexity.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

After reviewing the phases, see [Assess your readiness](../before-you-deploy/assess-your-readiness.html) to confirm your jurisdiction is ready to begin. If your jurisdiction plans to use a vendor, see the [Vendor-managed deployment](../before-you-deploy/vendor-managed-deployment.html) page.

Before finalizing your configuration, verify that your NBS 6 version is compatible with your target NBS 7 version in the [NBS 6 and NBS 7 compatibility matrix](../compatibility.html).

---

## Phase 1: NBS 7

The first phase is the base deployment. NBS 7 gives your jurisdiction NBS 6 feature parity on modern, cloud-based infrastructure, with foundational improvements such as real-time patient search. Additional modules and functional areas are modernized incrementally across releases.

>When to deploy
>
>Deploy Phase 1 first. All subsequent phases depend on it. Plan your RTR and DI API timelines before you begin so your team can sequence the phases without gaps.
{: .note-title }

NBS 7 core components are organized into three layers: [networking](#networking-layer), [infrastructure](#infrastructure-layer), and [application](#application-layer). For details on what each core component does and when you need it, see [NBS 7 core components](../before-you-deploy/component-reference/nbs-core-components.html) in the Component Reference.

### Networking layer

The networking layer manages traffic routing and secure communication between your NBS 6 and NBS 7 environments.

- DNS infrastructure (Route 53 or equivalent)
- Virtual Private Cloud (VPC) and routing groups
- VPN connectivity between NBS 6 and NBS 7 instances

### Infrastructure layer

The infrastructure layer provides the container orchestration platform and cloud services that host and run NBS 7 components.

- Kubernetes cluster (EKS on AWS, AKS on Azure)
- Traefik Ingress Controller (replaced NGINX as of NBS 7.12)
- AWS or Azure managed services
- Terraform infrastructure automation modules
- Load balancer

### Application layer

The application layer contains the NBS 7 services and legacy NBS 6 components that users and administrators directly interact with.

- [Legacy NBS 6](../before-you-deploy/component-reference/nbs-core-components.html#legacy-nbs-6)
- [NBS Modernization API](../before-you-deploy/component-reference/nbs-core-components.html#nbs-modernization-api)
- [NBS Web UI](../before-you-deploy/component-reference/nbs-core-components.html#nbs-web-ui)
- [NBS Gateway](../before-you-deploy/component-reference/nbs-core-components.html#nbs-gateway)
- [Elasticsearch](../before-you-deploy/component-reference/nbs-core-components.html#elasticsearch)
- [Nifi](../before-you-deploy/component-reference/nbs-core-components.html#nifi)
- [Keycloak](../before-you-deploy/component-reference/nbs-core-components.html#keycloak)
- [Cert Manager, FluentBit](../before-you-deploy/component-reference/nbs-core-components.html#infrastructure-and-networking-layer-components)
- [Database (NBS\_ODSE and NBS\_SRTE)](../before-you-deploy/component-reference/nbs-core-components.html#database-nbs_odse-nbs_srte)

---

## Phase 2: Real-Time Reporting (RTR)

RTR is the second deployment phase. It introduces an event-driven reporting pipeline that runs alongside the legacy MasterETL batch process during the transition, with the goal of eventually decommissioning the batch process.

>When to deploy
>
>Deploy Phase 2 after Phase 1 is stable. RTR is part of the full deployment and should be planned from the start.
{: .note-title }

RTR adds the following components to your NBS 7 deployment. For details, see [Add-on: Real-Time Reporting (RTR)](../before-you-deploy/component-reference/rtr.html).

- [Debezium](../before-you-deploy/component-reference/rtr.html#debezium)
- [Kafka and Kafka Connect](../before-you-deploy/component-reference/rtr.html#kafka-and-kafka-connect)
- [RTR domain services](../before-you-deploy/component-reference/rtr.html#rtr-domain-services)

---

## Phase 3: Data Ingestion (DI) API

The DI API is the third deployment phase. It provides a built-in data transit layer and a REST API interface for writing data to NBS. DI API serves as a secure intermediary between your middleware and the database.

>When to deploy
>
>Jurisdictions that need an API-based ingestion path due to security constraints should plan Phase 3 in parallel with or immediately after Phase 2.
{: .note-title }

The DI API supports two integration methods. The right choice depends on your jurisdiction's security policies and how your middleware is deployed.

| Integration method | Rationale |
| :--- | :--- |
| **Direct SQL Write** | Standard for jurisdictions where middleware such as Rhapsody can access the database directly. |
| **DI API** | Used when security policies prohibit direct database access from third-party tools or when middleware cannot be co-located with NBS. |

{: .important }
The DI API is not a replacement for middleware. An integration engine such as Rhapsody is required to preprocess and format data before it is sent to the DI API.

For more information, see [Data Ingestion (DI) API](../before-you-deploy/component-reference/di-api.html) in the Component Reference.
