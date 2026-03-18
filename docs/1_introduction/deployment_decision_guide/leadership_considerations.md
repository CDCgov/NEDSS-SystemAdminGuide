---
title: Leadership considerations
layout: page
parent: NBS 7 Deployment Decision Guide
grand_parent: Introduction
nav_order: 0
---

<!-- PAGE TITLE - DON'T INCLUDE HEADER IN TOC -->
## NBS 7 leadership considerations
{: .no_toc }

<!-- INTRO OR OVERVIEW -->
This page is for **health department leaders and decision-makers** who need to understand the organizational, financial, and operational implications of migrating to NBS 7. Each consideration below represents a decision point or planning requirement that leadership should address before your jurisdiction commits to migration.

For technical deployment guidance, refer to the [Assess your readiness](0_assess_readiness.html) section and the rest of this guide.

1. TOC
{:toc}

---

### Migration is gradual, not a cutover

NBS 7 does not replace NBS 6 in a single switch. Your jurisdiction will run both systems in parallel during the transition. NBS 7 components gradually take over functionality while NBS 6 continues to operate. Plan for the operational complexity and cost of maintaining two systems simultaneously. The length of this parallel period depends on your jurisdiction's pace of deployment and configuration choices.

### State IT security approval takes time

State IT security approval is often the longest-lead item in an NBS 7 migration. NBS 7 requires approval for cloud hosting and specific technologies including Kubernetes, Terraform, and Docker. If your jurisdiction has not started this process, start it now, even if deployment is months away. Waiting until you are technically ready to deploy before seeking approval is one of the most common causes of migration delays.

### Cloud infrastructure requires new ongoing budget

NBS 6 could run on-premises, but NBS 7 cannot. NBS 7 is a cloud-only system. Your jurisdiction needs an active cloud account (AWS or Azure) and an ongoing budget to sustain cloud infrastructure costs. Cloud hosting costs scale with usage, so budget planning should account for both normal operations and surge scenarios such as outbreak response.

### Technical staffing requirements are different from NBS 6

Migrating to NBS 7 requires skills your current NBS 6 team may not have, including Kubernetes, Terraform, and cloud infrastructure management. Assess your team's current capacity before committing to a migration timeline. If you underestimate the staffing gap, your migration will take longer than planned. Jurisdictions without the necessary in-house expertise will need to build capacity or engage a vendor.

### Real-Time Reporting adds capability and cost

The Real-Time Reporting (RTR) add-on reduces the time for data to appear in reports from up to 24 hours to between 5 minutes and 1 hour. For jurisdictions managing active outbreaks or time-sensitive disease investigations, this improvement can meaningfully affect response time. However, RTR adds infrastructure complexity and requires additional cloud resources. Weigh the reporting speed benefit against the additional operating cost for your jurisdiction's case volume and reporting needs.

### The Data Ingestion API is not yet a full middleware replacement

The Data Ingestion (DI) API is a built-in data transit layer that can receive lab reports and case reports without third-party middleware. If your jurisdiction currently uses Rhapsody or Mirth Connect, the DI API is not yet a full replacement. Continue to use your existing middleware for now. If your jurisdiction does not have existing middleware, the DI API is worth evaluating. Revisit its capabilities as the product matures.

### Single Sign-On requires early coordination

NBS 7 uses Keycloak for identity management. If your jurisdiction uses a centralized identity provider such as Okta or Active Directory, Keycloak can integrate with it, allowing NBS 7 users to log in with their existing jurisdiction credentials. This integration requires early coordination between your NBS deployment team and your identity provider administrators. Do not leave SSO configuration to the end of the deployment process.
