---
title: Operational considerations
layout: page
parent: Before you deploy
nav_order: 2
description: Summarizes organizational, financial, and operational factors that affect NBS 7 migration planning.
redirect_from:
  - /docs/before-you-deploy/operational_considerations.html
  - /docs/before-you-deploy/operational_considerations/
---

# Operational considerations

This page covers organizational, financial, and operational factors that affect NBS 7 migration planning. Some migration factors involve decisions or timelines that extend beyond the technical team and might be worth raising with others in your organization early in your planning process.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

---

For technical deployment guidance, refer to [Assess your technical readiness](../before-you-deploy/assess-your-readiness.html) and the rest of this guide.

## Plan for parallel operations

Migration from NBS 6 to NBS 7 concludes with a cutover from your existing NBS 6 instance to the new NBS 7 deployment. Both systems run in parallel during the transition, and the length of this parallel period depends on your jurisdiction's pace of deployment and the decisions made along the way. Some jurisdictions opt to provision a separate NBS 6 environment for migration activities before cutting over, rather than making changes directly on their primary NBS 6 production server. Planning for the operational complexity and cost of maintaining two systems simultaneously is an integral part of migration preparation.

See also: [NBS 7 Deployment planning guide](../before-you-deploy/planning.html).

Version prerequisite: confirm your NBS 6 baseline against the [Supported NBS versions](../supported-versions.html) before you finalize migration timelines.

## IT security approval can take time

IT security approval is often one of the longest-lead items in an NBS 7 migration, though timelines vary significantly across jurisdictions. NBS 7 requires approval for cloud hosting and specific technologies including Kubernetes, Terraform, and Docker. Because NBS handles PII and PHI, IT review is often required even when a vendor manages parts of the deployment. Jurisdictions that start this process early, even when deployment is still months away, might avoid one of the most common causes of migration delays.

See also: [Assess your technical readiness](../before-you-deploy/assess-your-readiness.html) and [Provision cloud infrastructure](../deploy-nbs7/full-deploy/provision-cloud-infrastructure.html).

## Cloud infrastructure requires ongoing budget

CDC does not support on-premises installations of NBS 7. Your jurisdiction needs an active cloud account with Amazon Web Services (AWS) or Microsoft Azure and an ongoing budget to sustain cloud infrastructure costs. Cloud hosting costs scale with usage, so budget planning might account for both normal operations and surge scenarios such as outbreak response. Use the [NBS 7 Resource Estimator](https://nbscentral.cdc.gov/documents/872) to project cloud hosting costs based on your jurisdiction's record volume (NBS Central login required; see [Additional resources](../../index.html#additional-resources)).

See also: [Provision cloud infrastructure](../deploy-nbs7/full-deploy/provision-cloud-infrastructure.html).

## Align cloud provider with jurisdictional strategy

NBS 7 is fully supported on both AWS and Azure. While the internal microservices and deployment steps are identical across platforms, the initial environment setup depends on your jurisdiction's existing infrastructure and procurement path.

Choose the provider that best aligns with your organization's current operational state:

- **Existing infrastructure:** If your jurisdiction currently runs NBS 6 or other critical systems on a specific cloud platform, remaining on that platform avoids the need for new IT security approvals.
- **Contractual agreements:** Utilize existing Enterprise Agreements or pre-approved cloud spending to streamline procurement.
- **Staff expertise:** Align the choice with the existing skills of your cloud engineering or IT administration teams.

See also: [Assess your technical readiness > Cloud infrastructure](assess-your-readiness.html#cloud-infrastructure).

## Technical staffing requirements differ from NBS 6

Migrating to NBS 7 requires expertise in Kubernetes, Terraform, and cloud infrastructure management that your current NBS 6 team might not have. Jurisdictions that assess their team's capacity early are poised to set more accurate migration timelines. Those without the necessary in-house expertise have typically built capacity or engaged a vendor before deployment.

See also: [Assess your technical readiness](../before-you-deploy/assess-your-readiness.html) and [Vendor-managed deployment](../before-you-deploy/vendor-managed-deployment.html).

## Real-Time Reporting can be deployed as a follow-on

The Real-Time Reporting (RTR) pipeline reduces the time for data to appear in reports from up to 24 hours to between 5 minutes and 1 hour. For jurisdictions managing active outbreaks or time-sensitive disease investigations, this improvement can meaningfully affect response time. RTR adds infrastructure complexity and requires additional cloud resources. Jurisdictions that find RTR a significant lift at the time of initial deployment can choose to deploy core NBS 7 functionality first and adopt RTR as a follow-on. The reporting speed benefit and the additional operating cost are both worth weighing against your jurisdiction's case volume and reporting needs.

See also: [RTR component reference](../before-you-deploy/component-reference/rtr.html), [Deploy real-time reporting](../deploy-nbs7/microservices-deployment/real-time-reporting/real-time-reporting.html), and [Deployment phases](../before-you-deploy/deployment-phases.html).

## The Data Ingestion API adds a secure integration option

The Data Ingestion (DI) API is a built-in REST API layer that accepts lab reports and case reports. It gives jurisdictions an API-based ingestion path, which is useful when security constraints prevent middleware or other third-party tools from connecting directly to the NBS database.

See also: [DI API component reference](../before-you-deploy/component-reference/di-api.html) and [Deploy data ingestion service (DI API)](../deploy-nbs7/microservices-deployment/data-ingestion/data-ingestion.html).

## Single Sign-On requires early coordination

NBS 7 uses Keycloak for identity management. If your jurisdiction uses a centralized identity provider such as Okta or Active Directory, Keycloak can integrate with it, allowing NBS 7 users to log in with their existing jurisdiction credentials. This integration requires coordination between your NBS deployment team and your identity provider administrators. We recommend that you start that coordination early rather than addressing it later in the deployment process.

See also: [Deploy and configure Keycloak](../deploy-nbs7/full-deploy/kubernetes-setup/deploy-keycloak.html).
