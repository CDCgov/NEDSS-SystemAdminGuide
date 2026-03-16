---
title: Large jurisdiction, high volume, vendor-managed
layout: page
parent: Deploy NBS 7
grand_parent: About this guide
nav_order: 3
---

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
