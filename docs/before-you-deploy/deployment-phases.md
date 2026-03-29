---
title: Deployment overview
layout: page
parent: Before you deploy
nav_order: 1
description: An overview of the five phases involved in an NBS 7 deployment, from planning through steady state operations.
---

# Deployment overview

NBS 7 deployments vary significantly by jurisdiction. If you are just getting started, this page might help you understand where the  [Assess your readiness](assess-your-readiness.html) checklist fits in the overall process.

<!--
## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}
-->

## Example deployment phases

The phases in this table represent an example rollout scenario based on deployments to date. Your jurisdiction's timeline, activities, and sequence might differ depending on your infrastructure, staffing, and security requirements. For more information, see [Operational considerations](../../docs/before-you-deploy/operational_considerations.html).

| Phase | Goal | Minimum duration |
|:---|:---|:---|
| [Planning](#planning) | Establish your project team, [assess your readiness](assess-your-readiness.html), and create a customized migration plan | 2-3 months |
| [Install](#install) | Provision cloud environments and deploy NBS 7 based on your [chosen configuration](choose-your-configuration.html) |  3-4 months |
| [Test](#test) | Validate ingestion, egress, and system readiness before go-live | 3-4 months |
| [Go-live](#go-live) | Complete cutover and launch NBS 7 in production | 1-2 months |
| [Steady state](#steady-state) | Monitor live operations and maintain the system ongoing | Ongoing |

{: .note }
These are minimum estimates based on typical deployments. Actual timelines vary by jurisdiction. Security approval processes are the most common source of extended timelines in the Planning and Install phases.

For detailed checklists and deliverables for each phase, see the [NBS 7 Migration Info Sheet](https://nbscentral.cdc.gov/documents/731) on NBS Central.

---

## Planning

The Planning phase covers discovery, environment setup, and project preparation. Security approval for cloud hosting and required technologies including Kubernetes, Terraform, and Docker is frequently the longest-lead item in this phase and the most common source of delay across the entire deployment. Starting that process early tends to reduce overall deployment time.

| Activity | Description | Resource |
|:---|:---|:---|
| Readiness check-in | Initial planning and review of frequently asked questions. See [Assess your readiness](../../docs/before-you-deploy/assess-your-readiness.html) for the technical checklist | [Migration Info Sheet](https://nbscentral.cdc.gov/documents/731) |
| Identify project team | Define roles, responsibilities, and key stakeholders. See [Operational considerations](../../docs/before-you-deploy/operational_considerations.html) for staffing guidance | [Migration Info Sheet](https://nbscentral.cdc.gov/documents/731) |
| NBS 7 orientation | Review NBS 7 features with your migration team. See [Component reference](../../docs/before-you-deploy/component-reference.html) for a full component overview | [Choose your configuration](../../docs/before-you-deploy/choose-your-configuration.html) |
| Create project plan | Draft a customized migration plan from the playbook checklists, including a migration risk registry | [Deployment scenarios](../../docs/before-you-deploy/deployment-scenarios.html) |
| Communications plan | Develop and implement a communications plan customized to your timeline and needs | Communications plan |
| Training plan | Implement an NBS 7 training plan customized for your jurisdiction | STLT user training plan |
| Draft test plan | Customize a UAT plan for your requirements | STLT user acceptance test plan |

---

## Install

The Install phase covers provisioning your cloud environments and deploying NBS 7 across development, staging, and production. This phase has a dependency on security approval processes, which might extend the timeline.

| Activity | Description | Resource |
|:---|:---|:---|
| Data migration plan | Agree on and review the data migration plan, coordinate the data migration solution and test files | [Assess your readiness: Data migration](../../docs/before-you-deploy/assess-your-readiness.html#data-migration) |
| Dev environment deployment | Create and deploy an initial NBS 7 development environment build | [Set up cloud infrastructure](../../docs/deploy-nbs7/set-up-cloud-infrastructure.html) |
| Staging environment deployment | Create and deploy an initial NBS 7 test environment build | [Set up cloud infrastructure](../../docs/deploy-nbs7/set-up-cloud-infrastructure.html) |
| Production environment deployment | Create and deploy an initial NBS 7 production environment build | [Deploy NBS 7 microservices](../../docs/deploy-nbs7/deploy-nbs7-microservices.html) |
| Complete database transfer | Complete customizations, user file sharing setup, and integration with your user management system | STLT database refresh procedure |
| Roles and permissions migration | Map user roles and configure permissions in NBS 7 | User migration mapping |
| SSO setup | Review state SSO and login requirements and integrate Keycloak with your existing login tools. See [Operational considerations](../../docs/before-you-deploy/operational_considerations.html) for SSO planning guidance | [Enable Keycloak authentication](../../docs/deploy-nbs7/keycloak/enable-keycloak-auth.html) |

---

## Test

The Test phase validates that your NBS 7 environment is ready for production use. This phase also has a dependency on security processes and might run concurrently with some Install activities.

| Activity | Description | Resource |
|:---|:---|:---|
| Database restore process | Review and test the database restore process in the development environment | STLT database refresh procedure |
| Ingestion and egress validation | Integrate and validate data ingestion and notification APIs to confirm pipelines | [Data ingestion API testing](../../docs/deploy-nbs7/microservices-deployment/data-ingestion/api-testing.html) |
| ELR ingestion testing | Test ingestion for individual ELRs and at scale | [Data ingestion smoke test](../../docs/deploy-nbs7/microservices-deployment/data-ingestion/smoke-test.html) |
| Notifications testing | Coordinate with the MVPs team to validate notifications readiness | TBD |
| Regression testing | Run test scripts across environments to validate readiness for UAT | [Validate the deployment](../../docs/deploy-nbs7/validate-the-deployment.html) |
| Cutover and rollback review | Review and approve cutover and rollback plans | [Go-live](../../docs/deploy-nbs7/go-live.html) |
| UAT | Complete the agreed UAT plan across dev, test, and production environments | UAT test plan |

---

## Go-live

The Go-live phase covers final preparation, cutover, and launch. This phase is shorter than the others but involves time-sensitive coordination across your team.

| Activity | Description | Resource |
|:---|:---|:---|
| NBS 7 training | Perform scheduled training sessions and share materials with end users | NBS 7 training presentations |
| Go/no-go decision | Make the final go-live decision and schedule the cutover date | [Go-live](../../docs/deploy-nbs7/go-live.html) |
| Lock database and refresh | Freeze the database backup and finalize the cutover checklist | STLT production cut-over checklist |
| Go-live day | Complete the cutover checklist and launch NBS 7 | [Go-live](../../docs/deploy-nbs7/go-live.html) |

---

## Steady state

After go-live, your jurisdiction enters steady state operations. This phase is ongoing and includes monitoring, support, and periodic upgrades as new NBS 7 releases become available.

| Activity | Description | Resource |
|:---|:---|:---|
| Monitor live operations | Implement the NBS 7 support process and track system performance | [Support](../../docs/deploy-nbs7/support.html) |
| Complete retrospective | Conduct a go-live retrospective to capture lessons learned | Retro Mural |
| Upgrade to new releases | Test and upgrade to new NBS 7 releases periodically | [Maintain NBS 7](../../docs/maintain-nbs7.html) |
