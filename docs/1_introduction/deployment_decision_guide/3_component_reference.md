---
title: Component reference
layout: page
parent: NBS 7 Deployment Decision Guide
grand_parent: Introduction
nav_order: 4
has_children: true
---

This section describes each component in NBS 7. Use it to understand what each component does, why it is included in your configuration, and how it relates to other components.

Components in this reference are organized by configuration tier:

- [NBS Core components](3_component_reference/1_nbs_core_components/)
- [Add-on: Real-Time Reporting (RTR)](3_component_reference/2_rtr/)
- [Add-on: Data Ingestion (DI) API](3_component_reference/3_di_api/)

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
