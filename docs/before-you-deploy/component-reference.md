---
title: Component reference
layout: page
parent: Before you deploy
nav_order: 4
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
| Legacy NBS 6 | ✓ | ✓ | ✓ |
| NBS Modernization API | ✓ | ✓ | ✓ |
| NBS Web UI | ✓ | ✓ | ✓ |
| NBS Gateway | ✓ | ✓ | ✓ |
| Page Builder | ✓ | ✓ | ✓ |
| Elasticsearch | ✓ | ✓ | ✓ |
| Nifi | ✓ | ✓ | ✓ |
| Keycloak | ✓ | ✓ | ✓ |
| Database (NBS\_ODSE, NBS\_SRTE) | ✓ | ✓ | ✓ |
| Infrastructure and networking layer | ✓ | ✓ | ✓ |
| Debezium | | ✓ | |
| Kafka and Kafka Connect | | ✓ | |
| RTR domain services | | ✓ | |
| RDB\_Modern | | ✓ | |
| DI API | | | ✓ |

> NBS 7 core components are required for all deployments. RTR and DI API are optional add-ons. Components for the add-ons are only required if your jurisdiction chooses to include them.
{: .note }
