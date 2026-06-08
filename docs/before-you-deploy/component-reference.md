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

NBS 7 is deployed in phases. Components in this reference are organized by deployment phase:

- [NBS 7 core deployment](../before-you-deploy/component-reference/nbs-core-components.html)
- [Real-Time Reporting (RTR) deployment](../before-you-deploy/component-reference/rtr.html)
- [Data Ingestion (DI) API deployment](../before-you-deploy/component-reference/di-api.html)

For deployment configuration details including configuration parameters, Helm chart values, and step-by-step setup instructions, see the [Deploy NBS 7](../deploy-nbs7.html) section of this guide.

---

## Quick reference

The following table shows which components are included in NBS 7. RTR and DI API are deployed separately from the core NBS 7 components.

| Component | NBS 7 | RTR | DI API |
|:---|:---:|:---:|:---:|
| [Legacy NBS 6](../before-you-deploy/component-reference/nbs-core-components.html#legacy-nbs-6) | ✓ |  |  |
| [NBS Modernization API](../before-you-deploy/component-reference/nbs-core-components.html#nbs-modernization-api) | ✓ |  |  |
| [NBS Web UI](../before-you-deploy/component-reference/nbs-core-components.html#nbs-web-ui) | ✓ |  |  |
| [NBS Gateway](../before-you-deploy/component-reference/nbs-core-components.html#nbs-gateway) | ✓ |  |  |
| [Elasticsearch](../before-you-deploy/component-reference/nbs-core-components.html#elasticsearch) | ✓ |  |  |
| [Nifi](../before-you-deploy/component-reference/nbs-core-components.html#nifi) | ✓ |  |  |
| [Keycloak](../before-you-deploy/component-reference/nbs-core-components.html#keycloak) | ✓ |  |  |
| [Database (NBS\_ODSE, NBS\_SRTE)](../before-you-deploy/component-reference/nbs-core-components.html#database-nbs_odse-nbs_srte) | ✓ |  |  |
| [Infrastructure and networking layer](../before-you-deploy/component-reference/nbs-core-components.html#infrastructure-and-networking-layer-components) | ✓ |  |  |
| [Debezium](../before-you-deploy/component-reference/rtr.html#debezium) | | ✓ | |
| [Kafka and Kafka Connect](../before-you-deploy/component-reference/rtr.html#kafka-and-kafka-connect) | | ✓ | ✓ |
| [RTR domain services](../before-you-deploy/component-reference/rtr.html#rtr-domain-services) | | ✓ | |
| [DI API](../before-you-deploy/component-reference/di-api.html#di-api) | | | ✓ |
