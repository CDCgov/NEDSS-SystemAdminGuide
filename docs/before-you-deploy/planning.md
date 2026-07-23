---
title: Deployment planning guide
layout: page
parent: Before you deploy NBS 7
nav_order: 3
description: An overview of the five stages involved in an NBS 7 deployment, from planning through steady state operations.
---

# NBS 7 deployment planning guide

NBS 7 deployments vary significantly by jurisdiction. If you are just getting started, this page can help you understand where the [Assess your technical readiness](assess-your-readiness.html) checklist fits in the overall process.

The tables on this page link to resources where available. Unlinked resources are suggested artifacts. If they fit your jurisdiction's needs, you would need to create them.
{: .note }

<!--
## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}
-->

## Example deployment stages

The stages in this table represent an example rollout scenario based on deployments to date. Your jurisdiction's timeline, activities, and sequence might differ depending on your infrastructure, staffing, and security requirements. For more information, see [Operational considerations](../before-you-deploy/operational-considerations.html).

| Stage | Goal | Minimum duration |
|:---|:---|:---|
| [Planning](#planning) | Establish your project team, [assess your technical readiness](assess-your-readiness.html), and create a customized migration plan | 2-5 months |
| [Install](#install) | Provision cloud environments and deploy NBS 7 in [phases](deployment-phases.html) | 3-6 months |
| [Test](#test) | Validate ingestion, egress, and system technical readiness before go-live | 3-6 months |
| [Go-live](#go-live) | Complete cutover and launch NBS 7 in production | 1-4 months |
| [Steady state](#steady-state) | Monitor live operations and maintain the system | Ongoing |

These are minimum duration estimates based on typical deployments. Actual timelines will vary by jurisdiction. Security approval, procurement, and legal review processes are common causes of delays in the earlier stages.
{: .important }

---

## Planning

The Planning stage covers discovery, environment setup, and project preparation. Security approval for cloud hosting and required technologies including Kubernetes, Terraform, and Docker can be a source of delay across the entire deployment. Early contact with your IT security office, before detailed timeline planning begins, might reduce the risk of delays.

Before planning detailed timelines, confirm that your current NBS 6 version is compatible with your target NBS 7 version in the [NBS 6 and NBS 7 compatibility matrix](../supported-versions.html).

| Activity | Description | Suggested resource or action |
|:---|:---|:---|
| Review readiness and compatibility | Review technical considerations and confirm your NBS 6 version is compatible with your target NBS 7 version. | [Assess your technical readiness](../before-you-deploy/assess-your-readiness.html), [NBS 6 and NBS 7 compatibility matrix](../supported-versions.html), and [Migration Info Sheet](https://nbscentral.cdc.gov/documents/731) (NBS Central login required; see [Additional resources](../../index.html#additional-resources)) |
| Identify project team | Define roles, responsibilities, and key stakeholders. See [Operational considerations](../before-you-deploy/operational-considerations.html) for staffing guidance. | [Migration Info Sheet](https://nbscentral.cdc.gov/documents/731) (NBS Central login required; see [Additional resources](../../index.html#additional-resources)) |
| Assess current environment | Document your existing NBS 6 setup, including ingestion and egress workflows, integrations, and hosting configuration. | Create a current state assessment |
| Orient migration team to NBS 7 | Review NBS 7 components and features with your migration team. | [Component reference](../before-you-deploy/component-reference.html) |
| Create project plan | Draft a migration plan customized for your jurisdiction. | Create a project plan |
| Plan data migration | Agree on an approach, coordinate the data migration solution, and prepare test files. | Create a data migration plan; see [Assess your technical readiness: Data migration](../before-you-deploy/assess-your-readiness.html#data-migration) |
| Plan user support | Identify how end users will report issues after go-live and document the process. | Create a user support plan |
| Plan user training | Identify training needs and develop materials customized for your jurisdiction. | Create a user training plan |
| Plan communications | Develop a communications plan customized to your timeline and needs. | Create a communications plan |
| Plan user acceptance testing (UAT) | Prepare test scenarios that confirm the system is ready for production. | Create a UAT plan |

---

## Install

The Install stage covers provisioning your cloud environment and deploying NBS 7. Most jurisdictions deploy across multiple environments and repeat some or all of these activities in each one, typically starting with a lower environment before moving to production. The number of environments, their names, and the level of testing performed in each will vary by jurisdiction.

If security approval is still in progress when Install begins, it might extend this stage.

| Activity | Description | Suggested resource or action |
|:---|:---|:---|
| Deploy NBS 7 | Provision and deploy NBS 7 in your environment. Repeat for each environment in your jurisdiction's setup. | [Deploy NBS 7](../deploy-nbs7.html) |
| Transfer database | Complete customizations, user file sharing setup, and integration with your user management system. | Use your own database refresh procedure |
| Migrate user roles and permissions | Map user roles and configure permissions in NBS 7. | Create a user migration map |
| Configure SSO | Review SSO and login requirements and integrate Keycloak with your existing login tools. See [Operational considerations](../before-you-deploy/operational-considerations.html) for SSO planning guidance. | [Deploy and configure Keycloak](../deploy-nbs7/full-deploy/kubernetes-setup/deploy-keycloak.html) |

---

## Test

The Test stage validates that your NBS 7 environment is ready for production use. Some Test stage activities might be performed within each environment during Install. This stage might also run concurrently with some Install activities.

| Activity | Description | Suggested resource or action |
|:---|:---|:---|
| Test database restore process | Review and test the database restore process in each environment. | Use your own database refresh procedure |
| Validate ingestion and egress | Integrate and validate data ingestion and notification pathways to confirm pipelines are working. | [API testing for data ingestion](../deploy-nbs7/microservices-deployment/data-ingestion/api-testing.html) |
| Validate real-time reporting (RTR) | Confirm that RTR streaming updates move into datamart tables. | [Validate the RTR pipeline](../deploy-nbs7/microservices-deployment/real-time-reporting/pipeline-validation.html) |
| Test ELR and eCR ingestion | Test ingestion for individual ELRs and eCRs and at scale. | [Data ingestion smoke test](../deploy-nbs7/microservices-deployment/data-ingestion/smoke-test.html) |
| Validate notifications | Validate Case Notifications | Confirm conditions are received successfully |
| Run regression testing | Run test scripts across environments to validate readiness for UAT. | [Validate the deployment](../deploy-nbs7/validate-the-deployment.html) |
| Conduct user acceptance testing (UAT) | Conduct UAT across all environments. | Your UAT test plan |
| Review cutover and rollback plans | Review and approve cutover and rollback plans. | Create a cutover and rollback plan |

---

## Go-live

The Go-live stage covers final preparation, cutover, and launch. This stage is shorter than the others but involves time-sensitive coordination across your team. In many jurisdictions, this cutover follows work in a separate migration environment rather than direct changes on the primary NBS 6 production server.

| Activity | Description | Suggested resource or action |
|:---|:---|:---|
| Conduct NBS 7 training | Perform scheduled training sessions and share materials with end users. | [NBS Visual Reference Guide](https://nbscentral.cdc.gov/documents/863) (NBS Central login required; see [Additional resources](../../index.html#additional-resources)) |
| Make go/no-go decision | Make the final go-live decision and schedule the cutover date. | No resource required |
| Lock and refresh database | Freeze the database backup and finalize the cutover checklist. | Add to your cutover and rollback plan |
| Execute cutover | Complete the cutover checklist and launch NBS 7. | Your cutover and rollback plan |
| Activate user support channel | Open the support channel to end users. | Your user support plan |

---

## Steady state

After go-live, your jurisdiction enters steady state operations. This stage is ongoing and includes monitoring, support, and periodic upgrades as new NBS 7 releases become available.

| Activity | Description | Suggested resource or action |
|:---|:---|:---|
| Monitor live operations | Track system performance and understand your support options. | [Get support](../support.html) |
| Conduct go-live retrospective | Capture lessons learned from the go-live process. | Use a retrospective template |
| Upgrade to new releases | Test and upgrade to new NBS 7 releases periodically. | [Maintain NBS 7](../maintain-nbs7.html) |
