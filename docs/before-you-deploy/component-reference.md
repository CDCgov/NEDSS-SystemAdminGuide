---
title: Component reference
layout: page
parent: Before you deploy
nav_order: 6
has_children: true
description: Describes each NBS 7 component — what it does, when it is needed, and how it relates to other components — organized by NBS 7 core components and available add-ons.
---

# NBS 7 component reference
{: .no_toc }

The pages in this section describe each component in NBS 7. Use it to understand what each component does, why it is included in your deployment, and how it relates to other components.

Components in this reference are organized by deployment scope:

- [NBS 7 core components](3_component_reference/1_nbs_core_components/)
- [Add-on: Real-Time Reporting (RTR)](3_component_reference/2_rtr/)
- [Add-on: Data Ingestion (DI) API](3_component_reference/3_di_api/)

For deployment configuration details including configuration parameters, Helm chart values, and step-by-step setup instructions, see the **NBS 7 System Administrator Guide**.

---

## Quick reference

The following table shows which components are included in NBS 7 and its available add-ons.

| Component | NBS 7 | + RTR add-on | + DI API add-on |
|:---|:---:|:---:|:---:|
| [Legacy NBS 6](../../docs/before-you-deploy/component-reference/nbs-core-components.html#legacy-nbs-6) | ✓ | ✓ | ✓ |
| [NBS Modernization API](../../docs/before-you-deploy/component-reference/nbs-core-components.html#nbs-modernization-api) | ✓ | ✓ | ✓ |
| [NBS Web UI](../../docs/before-you-deploy/component-reference/nbs-core-components.html#nbs-web-ui) | ✓ | ✓ | ✓ |
| [NBS Gateway](../../docs/before-you-deploy/component-reference/nbs-core-components.html#nbs-gateway) | ✓ | ✓ | ✓ |
| [Page Builder](../../docs/before-you-deploy/component-reference/nbs-core-components.html#page-builder) | ✓ | ✓ | ✓ |
| [Elasticsearch](../../docs/before-you-deploy/component-reference/nbs-core-components.html#elasticsearch) | ✓ | ✓ | ✓ |
| [Nifi](../../docs/before-you-deploy/component-reference/nbs-core-components.html#nifi) | ✓ | ✓ | ✓ |
| [Keycloak](../../docs/before-you-deploy/component-reference/nbs-core-components.html#keycloak) | ✓ | ✓ | ✓ |
| [Database (NBS\_ODSE, NBS\_SRTE)](../../docs/before-you-deploy/component-reference/nbs-core-components.html#database-nbs_odse-nbs_srte) | ✓ | ✓ | ✓ |
| [Infrastructure and networking layer](../../docs/before-you-deploy/component-reference/nbs-core-components.html#infrastructure-and-networking-layer-components) | ✓ | ✓ | ✓ |
| [Debezium](../../docs/before-you-deploy/component-reference/rtr.html#debezium) | | ✓ | |
| [Kafka and Kafka Connect](../../docs/before-you-deploy/component-reference/rtr.html#kafka-and-kafka-connect) | | ✓ | |
| [RTR domain services](../../docs/before-you-deploy/component-reference/rtr.html#rtr-domain-services) | | ✓ | |
| [DI API](../../docs/before-you-deploy/component-reference/di-api.html#di-api) | | | ✓ |

> NBS 7 core components are required for all deployments. RTR and DI API are optional add-ons. Components for the add-ons are only required if your jurisdiction chooses to include them.
{: .note }
