---
title: Medium jurisdiction, hybrid hosting
layout: page
parent: Deployment scenarios
grand_parent: Before you deploy
nav_order: 2
description: Case study for a medium jurisdiction with existing Rhapsody middleware deploying NBS Core + RTR, based on Kentucky's experience.
---

## Case study: RTR with middleware

1. TOC
{:toc}

---

### Profile

Medium STLT with an existing Rhapsody middleware investment and a need for faster data turnaround than NBS 6 batch processing provides. The jurisdiction retained Rhapsody for data ingestion.

### Configuration

| Deployment model | Hosting |
|:---|:---|
| NBS 7 + RTR | Hybrid: cloud-hosted NBS 7, on-premises Rhapsody middleware |

### What was deployed

| Component | Included | Notes |
|:---|:---|:---|
| NBS 7 | Yes | Full core deployment |
| Real-Time Reporting (RTR) | Yes | Added for faster reporting turnaround |
| DI API | No | Rhapsody for data ingestion |

<!--
### Key configuration decisions

- Rhapsody integrates directly with the NBS database rather than routing through the DI API. Jurisdictions with existing Rhapsody investments should follow this pattern.
- \[Placeholder: RTR configuration specifics for this scale\]
- \[Placeholder: how the hybrid hosting model was structured\]
- \[Placeholder: custom integration points between Rhapsody and NBS 7\]

### Lessons learned

- \[Placeholder: integration patterns that worked well\]
- \[Placeholder: performance considerations at this scale\]
- \[Placeholder: challenges encountered\]
-->

> Best for
>
> Might apply to jurisdictions that have existing middleware such as Rhapsody or Mirth Connect that you want to retain, and you need faster reporting turnaround than NBS 6 provides.
{: .note-title }
