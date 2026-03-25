---
title: NBS 7 and available add-ons
layout: page
parent: Choose your configuration
grand_parent: NBS 7 Deployment Decision Guide
nav_order: 1
description: Describes NBS 7 and its two optional add-ons — Real-Time Reporting (RTR) and the Data Ingestion (DI) API — and when each is appropriate.
---

# NBS 7 and available add-ons
{: .no_toc }

NBS 7 is the base product. Two optional add-ons are available: Real-Time Reporting (RTR) and the Data Ingestion (DI) API. You do not have to deploy add-ons at the outset. Most jurisdictions deploy NBS 7 first, then evaluate add-ons as their team builds confidence with the platform. Starting without add-ons reduces deployment risk and gives your team time to learn the system before taking on additional complexity.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

After you review the available options, use the [decision tree](2_decision_tree.html) to identify your recommended starting configuration. If your jurisdiction plans to use a vendor, see the [Vendor-managed deployment](3_vendor_managed_deployment.html) page.

---

## NBS 7

The base deployment. NBS 7 gives your jurisdiction NBS 6 feature parity on modern, cloud-based infrastructure, plus foundational improvements such as real-time patient search.

NBS 7 core components are organized into three layers. For details on what each component does and when you need it, see [NBS 7 core components](../3_component_reference/1_nbs_core_components.html).

### Networking layer

The networking layer manages traffic routing and secure communication between your NBS 6 and NBS 7 environments.

- DNS infrastructure (Route 53 or equivalent)
- Virtual Private Cloud (VPC) and routing groups
- VPN connectivity between NBS 6 and NBS 7 instances

### Infrastructure layer

The infrastructure layer provides the container orchestration platform and cloud services that host and run NBS 7 components.

- Kubernetes cluster (EKS on AWS, AKS on Azure)
- NGINX Ingress Controller (being replaced by Traefik in future releases)
- AWS or Azure managed services
- Terraform infrastructure automation modules
- Load balancer

### Application layer

The application layer contains the NBS 7 services and legacy NBS 6 components that users and administrators directly interact with.

- [Legacy NBS 6](../3_component_reference/1_nbs_core_components.html#legacy-nbs-6)
- [NBS Modernization API](../3_component_reference/1_nbs_core_components.html#nbs-modernization-api)
- [NBS Web UI](../3_component_reference/1_nbs_core_components.html#nbs-web-ui)
- [NBS Gateway](../3_component_reference/1_nbs_core_components.html#nbs-gateway)
- [Page Builder](../3_component_reference/1_nbs_core_components.html#page-builder)
- [Elasticsearch](../3_component_reference/1_nbs_core_components.html#elasticsearch)
- [Nifi](../3_component_reference/1_nbs_core_components.html#nifi)
- [Keycloak](../3_component_reference/1_nbs_core_components.html#keycloak)
- [Cert Manager, FluentBit](../3_component_reference/1_nbs_core_components.html#infrastructure-and-networking-layer-components)
- Database (NBS\_ODSE and NBS\_SRTE)

{: .note-title }
> Best for
>
> Jurisdictions with smaller IT teams, limited cloud experience, or a goal to establish a stable foundation before adding advanced features.

---

## Add-on: Real-Time Reporting (RTR)

RTR is an optional add-on that replaces the legacy MasterETL batch process with an event-driven reporting pipeline. We recommend running RTR alongside MasterETL during transition, with the goal of eventually replacing it.

**With RTR, data is available within 5 minutes to 1 hour instead of 24 hours.**

RTR adds the following components to your NBS 7 deployment. For details, see [Add-on: Real-Time Reporting (RTR)](../3_component_reference/2_rtr.html).

- [Debezium](../3_component_reference/2_rtr.html#debezium)
- [Kafka and Kafka Connect](../3_component_reference/2_rtr.html#kafka-and-kafka-connect)
- [RTR domain services](../3_component_reference/2_rtr.html#rtr-domain-services)
- [RDB\_Modern](../3_component_reference/2_rtr.html#rdb_modern)

{: .note-title }
> Best for
>
> Jurisdictions with higher case volumes, a need for faster data turnaround, or plans to connect to advanced analytics tools.

---

## Add-on: Data Ingestion (DI) API

The DI API is an optional add-on that provides a built-in data transit layer. It accepts incoming public health data in multiple formats and routes it into NBS without requiring third-party middleware.

For details, see [Add-on: Data Ingestion (DI) API](../3_component_reference/3_di_api.html).

{: .note-title }
> Best for
>
> Jurisdictions that do not currently use Rhapsody or Mirth Connect for data ingestion, and want a built-in path for getting data into NBS 7.
