---
title: Operational considerations
layout: page
parent: NBS 7 Deployment Decision Guide
grand_parent: Before you deploy
nav_order: 0
description: Summarizes organizational, financial, and operational factors that affect NBS 7 migration planning.
---

# Operational considerations
{: .no_toc }

This page covers organizational, financial, and operational factors that affect NBS 7 migration planning. Some of these factors involve decisions or timelines that extend beyond the technical team and might be worth raising with others in your organization early in your planning process.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

---

For technical deployment guidance, refer to the [Assess your readiness](0_assess_readiness.html) section and the rest of this guide.

## Migration is gradual, not a cutover

NBS 7 does not replace NBS 6 in a single switch. Both systems run in parallel during the transition. NBS 7 components gradually take over functionality while NBS 6 continues to operate. The length of this parallel period depends on your jurisdiction's pace of deployment and configuration choices. Planning for the operational complexity and cost of maintaining two systems simultaneously is a common part of migration preparation.

## State IT security approval takes time

State IT security approval is often the longest-lead item in an NBS 7 migration. NBS 7 requires approval for cloud hosting and specific technologies including Kubernetes, Terraform, and Docker. Jurisdictions that start this process early, even when deployment is still months away, might avoid one of the most common causes of migration delays.

## Cloud infrastructure requires ongoing budget

NBS 6 could run on-premises, but NBS 7 is a cloud-only system. Your jurisdiction needs an active cloud account (AWS or Azure) and an ongoing budget to sustain cloud infrastructure costs. Cloud hosting costs scale with usage, so budget planning might account for both normal operations and surge scenarios such as outbreak response.

## Technical staffing requirements differ from NBS 6

Migrating to NBS 7 involves skills that might differ from what your current NBS 6 team uses, including Kubernetes, Terraform, and cloud infrastructure management. Jurisdictions that assess their team's capacity early are poised to set more accurate migration timelines. Those without the necessary in-house expertise have typically built capacity or engaged a vendor before deployment.

## Real-Time Reporting adds capability and cost

The Real-Time Reporting (RTR) add-on reduces the time for data to appear in reports from up to 24 hours to between 5 minutes and 1 hour. For jurisdictions managing active outbreaks or time-sensitive disease investigations, this improvement can meaningfully affect response time. RTR also adds infrastructure complexity and requires additional cloud resources. The reporting speed benefit and the additional operating cost are both worth weighing against your jurisdiction's case volume and reporting needs.

## The Data Ingestion API is not yet a full middleware replacement

The Data Ingestion (DI) API is a built-in data transit layer that can receive lab reports and case reports without third-party middleware. If your jurisdiction currently uses Rhapsody or Mirth Connect, the DI API is not yet a full replacement. Continuing to use your existing middleware for now is the current guidance. If your jurisdiction does not have existing middleware, the DI API is worth evaluating. Its capabilities are expected to expand as the product matures.

## Single Sign-On requires early coordination

NBS 7 uses Keycloak for identity management. If your jurisdiction uses a centralized identity provider such as Okta or Active Directory, Keycloak can integrate with it, allowing NBS 7 users to log in with their existing jurisdiction credentials. This integration requires coordination between your NBS deployment team and your identity provider administrators. We recommend that you start that coordination early rather than addressing it later in the deployment process.
