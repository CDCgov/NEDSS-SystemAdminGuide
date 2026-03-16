---
title: Small jurisdiction, self-managed, AWS
layout: page
parent: Deploy NBS 7
grand_parent: About this guide
nav_order: 1
---

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
