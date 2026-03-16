---
title: Configuration tiers
layout: page
parent: Choose your configuration
grand_parent: About this guide
nav_order: 1
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

There are four ways to deploy NBS 7:

- [NBS Core](#nbs-core)
- [NBS Core + Real-Time Reporting (RTR)](#nbs-core--real-time-reporting-rtr)
- [NBS Core + Data Ingestion (DI) API](#nbs-core--data-ingestion-di-api)
- [NBS Complete](#nbs-complete)

> You do not have to deploy everything at once. Most jurisdictions will start with NBS Core, then add RTR or the DI API as their team builds confidence with the platform. Starting smaller reduces deployment risk and gives your team time to learn the system before taking on additional complexity.
{: .highlight }

### NBS Core

The minimum viable deployment. NBS Core gives your jurisdiction NBS 6 feature parity on modern, cloud-based infrastructure, plus foundational NBS 7 improvements such as real-time patient search.

NBS Core components are organized into three layers. For details on what each component does and when you need it, see [NBS Core components](../../3_component_reference/1_nbs_core_components/).

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

RTR adds the following components. For details, see [Add-on: Real-Time Reporting (RTR)](../../3_component_reference/2_rtr/).

- [Debezium](#debezium)
- [Kafka and Kafka Connect](#kafka-and-kafka-connect)
- [RTR domain services](#rtr-domain-services)
- [RDB\_Modern](#rdb_modern)

> Best for jurisdictions with higher case volumes, a need for faster data turnaround, or plans to connect to advanced analytics tools.
{: .best-for }

---

### NBS Core + Data Ingestion (DI) API

Core plus a built-in data transit layer. This configuration adds the Data Ingestion (DI) API, which accepts incoming public health data in multiple formats and routes it into NBS without requiring third-party middleware.

For details, see [Add-on: Data Ingestion (DI) API](../../3_component_reference/3_di_api/).

> Best for jurisdictions that do not currently use Rhapsody or Mirth Connect for data ingestion, and want a built-in path for getting data into NBS 7.
{: .best-for }

---

### NBS Complete

The full NBS 7 deployment. NBS Complete includes NBS Core, RTR, and the DI API.

> Best for jurisdictions with larger IT teams, high case volumes, and advanced reporting or analytics needs.
{: .best-for }

---

See the [Vendor-managed deployment](../2_vendor_managed_deployment/) page if your jurisdiction plans to use a vendor, or the [decision tree](../3_decision_tree/) to identify your recommended starting configuration.
