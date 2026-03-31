---
title: Get support
layout: page
nav_order: 5
description: Explains when to contact CDC for NBS 7 planning, deployment, and maintenance support and what information to include in a support request.
redirect_from:
  - /docs/support.html
  - /docs/support/
---

# Get support for NBS 7

Use this page to understand when to contact CDC for help with NBS 7 planning, deployment, validation, and ongoing maintenance. Start with the guidance in this admin guide when it covers your issue, then contact CDC if you need clarification, encounter a blocker, or cannot find the procedure you need.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## When to contact CDC

CDC provides deployment support at no cost. Reach out if your jurisdiction needs help with any of the following:

- evaluating whether NBS 7 is the right next step for your jurisdiction
- choosing a starting configuration or optional add-ons
- resolving a deployment blocker during cloud, cluster, or microservices setup
- troubleshooting validation failures before go-live
- identifying the right maintenance procedure after go-live
- locating documentation that is not yet covered in this guide

## Start with the right resource

Use the resource that best matches where you are in the process.

| If you need help with... | Start here |
|:---|:---|
| Readiness, staffing, cloud prerequisites, or go or no-go planning | [Before you deploy NBS 7](../before-you-deploy.html) |
| Deployment steps for infrastructure, microservices, identity, or validation | [Deploy NBS 7](../deploy-nbs7.html) |
| Post-go-live operations, upgrades, or runtime configuration | [Maintain NBS 7](../maintain-nbs7.html) |

If the guide does not answer your question, contact [nbs@cdc.gov](mailto:nbs@cdc.gov).

## Before you contact CDC

Include enough context for the support team to understand where you are in the process and what has already been tried. When possible, include:

- your jurisdiction name
- your NBS 6 version and target NBS 7 version
- your cloud provider and deployment configuration
- the deployment phase you are in, such as planning, install, test, or steady state
- the page or procedure you were following when the issue occurred
- the exact error message, affected component, and time of failure
- relevant logs, screenshots, or command output with sensitive information removed
- a short summary of what changed immediately before the issue started

## Common support scenarios

The most common questions usually fall into one of these areas:

- **Planning and readiness**: questions about staffing, cloud prerequisites, security review, or whether a vendor-managed deployment is the better fit
- **Configuration decisions**: questions about optional add-ons such as Real-time reporting or the Data Ingestion API
- **Deployment troubleshooting**: issues during Terraform, Kubernetes, Keycloak, or microservices setup
- **Validation and cutover**: help interpreting smoke test results, validating data flow, or confirming readiness for go-live
- **Ongoing maintenance**: questions about upgrades, operational procedures, or newly documented maintenance tasks

## Release and documentation updates

This guide reflects the currently documented deployment and maintenance procedures, but NBS 7 is under active development. For the latest documented procedures:

- review the relevant sections in this guide before starting work
- check the repository for newly published guidance and release-related updates
- contact [nbs@cdc.gov](mailto:nbs@cdc.gov) if you need a procedure that is not yet documented
