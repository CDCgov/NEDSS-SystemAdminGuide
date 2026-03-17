---
title: Medium jurisdiction, existing middleware, RTR
layout: page
parent: Deploy NBS 7
grand_parent: NBS 7 Deployment Decision Guide
nav_order: 2
---

*Based on Kentucky's deployment.*

**Profile**

Medium STLT with an existing Rhapsody middleware investment and a need for faster data turnaround than NBS 6 batch processing provides. The jurisdiction retained Rhapsody for data ingestion rather than replacing it with the DI API.

**Configuration**

| Setting | Value |
|:---|:---|
| Tier | NBS Core + RTR |
| Hosting | Hybrid — cloud-hosted NBS 7, on-premises Rhapsody middleware |
| Middleware | Rhapsody (retained) |

**What was deployed**

| Component | Included | Notes |
|:---|:---|:---|
| NBS Core | Yes | Full core deployment |
| Real-Time Reporting (RTR) | Yes | Added for faster reporting turnaround |
| DI API | No | Rhapsody retained for data ingestion |

**Key configuration decisions**

- Rhapsody integrates directly with the NBS database rather than routing through the DI API. Jurisdictions with existing Rhapsody investments should follow this pattern.
- \[Placeholder: RTR configuration specifics for this scale\]
- \[Placeholder: how the hybrid hosting model was structured\]
- \[Placeholder: custom integration points between Rhapsody and NBS 7\]

**Lessons learned**

- \[Placeholder: integration patterns that worked well\]
- \[Placeholder: performance considerations at this scale\]
- \[Placeholder: challenges encountered\]

> Might apply to jurisdictions that have existing middleware such as Rhapsody or Mirth Connect that you want to retain, and you need faster reporting turnaround than NBS 6 provides.
{: .best-for }
