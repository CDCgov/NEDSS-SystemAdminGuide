---
title: Small jurisdiction, self-managed cloud
layout: page
parent: Deployment scenarios
grand_parent: Before you deploy
nav_order: 1
description: Case study for a small, self-managed AWS deployment based on Montana's experience, covering configuration choices and lessons learned.
---

## Case study: Small jurisdiction, self-managed, AWS

*Based on Montana's deployment.*

1. TOC
{:toc}

---

### Profile

Small STLT with limited IT staff and a cloud-first infrastructure strategy. The jurisdiction prioritized simplicity and maintainability over add-on features.

### Configuration

| Deployment model | Hosting |
|:---|:---|
| NBS core components only | AWS, STLT-managed |

### What was deployed

| Component | Included | Notes |
|:---|:---|:---|
| NBS 7 | Yes | Full core deployment |
| Real-Time Reporting (RTR) | No | Not required at this case volume |
| DI API | No | No existing high-volume ELR or eCR intake |

<!--
### Key configuration decisions

- \[Placeholder: specific AWS configuration choices, e.g. EKS node sizing, VPC setup\]
- \[Placeholder: any components skipped within NBS Core and rationale\]
- \[Placeholder: identity provider integration approach\]

### Lessons learned

- \[Placeholder: what worked well\]
- \[Placeholder: challenges encountered\]
- \[Placeholder: what this jurisdiction would do differently\]
-->

> Best for
>
> Might apply to jurisdictions that have a small IT team, limited cloud experience, or a goal to get NBS 7 running with minimal complexity before adding advanced features.
{: .note-title }
