---
title: Operational considerations
layout: page
parent: Before you deploy
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

For technical deployment guidance, refer to [Assess your readiness](../../docs/before-you-deploy/assess-your-readiness.html) and the rest of this guide.

## Migration is gradual, not a cutover

NBS 7 does not replace NBS 6 in a single switch. Both systems run in parallel during the transition. NBS 7 components gradually take over functionality while NBS 6 continues to operate. The length of this parallel period depends on your jurisdiction's pace of deployment and configuration choices. Planning for the operational complexity and cost of maintaining two systems simultaneously is an integral part of migration preparation. Many jurisdictions provision a separate NBS 6 environment for migration activities and then cut over, rather than making these changes directly on their primary NBS 6 production server.

See also: [Deployment phases](../../docs/before-you-deploy/deployment-phases.html) and [Deployment scenarios](../../docs/before-you-deploy/deployment-scenarios.html).

Version prerequisite: confirm your NBS 6 baseline against the [NBS 6 and NBS 7 compatibility matrix](../../docs/before-you-deploy/compatibility.html) before you finalize migration timelines.

## State IT security approval takes time

State IT security approval is often the longest-lead item in an NBS 7 migration. NBS 7 requires approval for cloud hosting and specific technologies including Kubernetes, Terraform, and Docker. Because NBS handles PII and PHI, state IT review is often required even when a vendor manages parts of the deployment. Jurisdictions that start this process early, even when deployment is still months away, might avoid one of the most common causes of migration delays.

See also: [Assess your readiness](../../docs/before-you-deploy/assess-your-readiness.html), [Set up cloud infrastructure](../../docs/deploy-nbs7/set-up-cloud-infrastructure.html), and [Deploy cloud infrastructure on AWS](../../docs/deploy-nbs7/deploy-on-aws.html) or [Deploy cloud infrastructure on Azure](../../docs/deploy-nbs7/deploy-on-azure.html).

## Cloud infrastructure requires ongoing budget

CDC does not support on-premises installations of NBS 7. Your jurisdiction needs an active cloud account (AWS or Azure) and an ongoing budget to sustain cloud infrastructure costs. Cloud hosting costs scale with usage, so budget planning might account for both normal operations and surge scenarios such as outbreak response. Use the [NBS 7 Resource Estimator (NBS Central login required)](https://nbscentral.cdc.gov/documents/872) to project cloud-hosting costs based on your jurisdiction's record volume.

See also: [Set up cloud infrastructure](../../docs/deploy-nbs7/set-up-cloud-infrastructure.html) and [Deployment scenarios](../../docs/before-you-deploy/deployment-scenarios.html).

## Your cloud provider depends on your existing environment

NBS 7 is fully supported on both AWS and Azure. Both providers host the same NBS 7 Kubernetes workloads, and once infrastructure is provisioned, the Bootstrap Kubernetes services and microservices deployment steps are identical. The difference is only in how the underlying cloud environment is provisioned.

Choose the provider that aligns with your organization's existing infrastructure, contracts, and IT security approvals. If your jurisdiction already runs NBS 6 on AWS or Azure, continuing on the same platform avoids additional procurement and approval steps.

See also: [Deploy cloud infrastructure on AWS](../../docs/deploy-nbs7/deploy-on-aws.html), [Deploy cloud infrastructure on Azure](../../docs/deploy-nbs7/deploy-on-azure.html), and [Cluster infrastructure](../../docs/deploy-nbs7/cluster-infrastructure.html).

## Technical staffing requirements differ from NBS 6

Migrating to NBS 7 involves skills that might differ from what your current NBS 6 team uses, including Kubernetes, Terraform, and cloud infrastructure management. Jurisdictions that assess their team's capacity early are poised to set more accurate migration timelines. Those without the necessary in-house expertise have typically built capacity or engaged a vendor before deployment.

See also: [Assess your readiness](../../docs/before-you-deploy/assess-your-readiness.html) and [Vendor-managed deployment](../../docs/before-you-deploy/choose-your-configuration/vendor-managed-deployment.html).

## Real-Time Reporting adds capability and cost

The Real-Time Reporting (RTR) add-on reduces the time for data to appear in reports from up to 24 hours to between 5 minutes and 1 hour. For jurisdictions managing active outbreaks or time-sensitive disease investigations, this improvement can meaningfully affect response time. RTR also adds infrastructure complexity and requires additional cloud resources. The reporting speed benefit and the additional operating cost are both worth weighing against your jurisdiction's case volume and reporting needs.

See also: [RTR component reference](../../docs/before-you-deploy/component-reference/rtr.html), [Real-time reporting deployment](../../docs/deploy-nbs7/real-time-reporting/real-time-reporting.html), and [Choose your configuration](../../docs/before-you-deploy/choose-your-configuration.html).

## The Data Ingestion API adds a secure integration option

The Data Ingestion (DI) API is a built-in REST API layer that accepts lab reports and case reports through middleware rather than through direct database access. It does not replace middleware such as Rhapsody or Mirth Connect. Instead, it gives jurisdictions an API-based ingestion path, which is especially useful when security constraints prevent middleware or other third-party tools from connecting directly to the NBS database. Jurisdictions that do not already have middleware will still need it before they can use the DI API.

See also: [DI API component reference](../../docs/before-you-deploy/component-reference/di-api.html) and [Data ingestion microservice](../../docs/deploy-nbs7/microservices-deployment/data-ingestion.html).

## Single Sign-On requires early coordination

NBS 7 uses Keycloak for identity management. If your jurisdiction uses a centralized identity provider such as Okta or Active Directory, Keycloak can integrate with it, allowing NBS 7 users to log in with their existing jurisdiction credentials. This integration requires coordination between your NBS deployment team and your identity provider administrators. We recommend that you start that coordination early rather than addressing it later in the deployment process.

See also: [Keycloak installation](../../docs/deploy-nbs7/keycloak/keycloak-installation.html) and [Enable Keycloak authentication](../../docs/deploy-nbs7/keycloak/enable-keycloak-auth.html).
