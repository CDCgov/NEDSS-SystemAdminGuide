---
title: Get support
layout: page
nav_order: 5
description: Explains when to contact CDC for NBS 7 planning, deployment, and maintenance support and what information to include in a support request.

---

# Get support for NBS 7

Use this page to understand when to contact CDC for help with NBS 7 planning, deployment, validation, and ongoing maintenance. Start with the guidance in this admin guide when it covers your issue, then contact CDC if you need clarification, encounter a blocker, or cannot find the procedure you need.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## When to contact CDC

CDC provides deployment support at no cost. Reach out if your jurisdiction needs help with any of the following:

- Evaluating whether NBS 7 is the right next step for your jurisdiction
- Choosing a starting configuration or optional add-ons
- Resolving a deployment blocker during cloud, cluster, or microservices setup
- Troubleshooting validation failures before go-live
- Identifying the right maintenance procedure after go-live
- Locating documentation that is not yet covered in this guide

## Support scenarios and where to start

Use this table to match your scenario to the most relevant section of the guide.

| Scenario | Typical questions | Start here |
|:---|:---|:---|
| Planning and readiness | Staffing, cloud prerequisites, security review, or whether a vendor-managed deployment is the better fit | [Before you deploy NBS 7](../before-you-deploy.html) |
| Configuration decisions | Optional add-ons such as Real-time reporting or the Data Ingestion API | [Before you deploy NBS 7](../before-you-deploy.html) |
| Deployment troubleshooting | Issues during Terraform, Kubernetes, Keycloak, or microservices setup | [Deploy NBS 7](../deploy-nbs7.html) |
| Validation and cutover | Interpreting smoke test results, validating data flow, or confirming readiness for go-live | [Deploy NBS 7](../deploy-nbs7.html) |
| Ongoing maintenance | Upgrades, operational procedures, or newly documented maintenance tasks | [Maintain NBS 7](../maintain-nbs7.html) |

If the guide does not answer your question, contact [nbs@cdc.gov](mailto:nbs@cdc.gov).

## What to include in your support request

Include enough context for the support team to understand where you are in the process and what has already been tried. When possible, include:

- Your jurisdiction name
- Your NBS 6 version and target NBS 7 version
- Your cloud provider and deployment configuration
- The deployment phase you are in, such as planning, install, test, or steady state
- The page or procedure you were following when the issue occurred
- The exact error message, affected component, and time of failure
- Relevant logs, screenshots, or command output with sensitive information removed
- A short summary of what changed immediately before the issue started

## Release and documentation updates

This guide reflects the currently documented deployment and maintenance procedures, but NBS 7 is under active development. For the latest documented procedures:

- Review the relevant sections in this guide before starting work
- Check the repository for newly published guidance and release-related updates
- Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) if you need a procedure that is not yet documented
