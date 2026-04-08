---
title: Large jurisdiction, vendor-managed cloud
layout: page
parent: Deployment scenarios
grand_parent: Before you deploy
nav_order: 3
description: Case study for a large, vendor-managed NBS Complete deployment at enterprise scale, covering high-availability and advanced configuration decisions.
---

## Case study: Large jurisdiction, high volume, vendor-managed
{: .no_toc }

*Based on an enterprise-scale deployment.*

1. TOC
{:toc}

---

### Profile

Large STLT with high case volumes, sophisticated analytics needs, and a vendor-managed infrastructure model. This jurisdiction required high-availability configuration and advanced security hardening.

### Configuration

| Deployment model | Hosting |
|:---|:---|
| NBS 7 + RTR + DI API | Cloud vendor-managed, or hybrid with significant cloud presence |

### What was deployed

| Component | Included | Notes |
|:---|:---|:---|
| NBS 7 | Yes | Full core deployment |
| Real-Time Reporting (RTR) | Yes | Required for high case volume and analytics needs |
| DI API | Yes | Primary path for ELR and eCR ingestion |

<!--
### Key configuration decisions

- \[Placeholder: high-availability configuration specifics\]
- \[Placeholder: performance optimization decisions\]
- \[Placeholder: advanced security hardening approach\]
- \[Placeholder: vendor coordination model and responsibilities\]

### Lessons learned

- \[Placeholder: scaling considerations\]
- \[Placeholder: cost management approach\]
- \[Placeholder: challenges encountered with vendor-managed deployment\]
-->

> Best for
>
> Might apply to jurisdictions that have a large IT team or vendor support, high case volumes, advanced reporting or analytics needs, and require high-availability infrastructure.
{: .note-title }
