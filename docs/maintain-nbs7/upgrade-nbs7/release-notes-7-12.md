---
title: NBS 7.12 release notes
layout: page
parent: Upgrade NBS 7
grand_parent: Maintain NBS 7
nav_order: 7120
description: Summarizes release-specific prerequisites, infrastructure changes, and required actions for upgrading to NBS 7.12.
---

# NBS 7.12 release notes

This page summarizes the release-specific prerequisites and required actions for NBS 7.12. Use it with [Upgrade NBS 7](../upgrade-nbs7.html) before you begin the upgrade.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Release summary

- Release date: March 2026
- Release type: Patch
- Scope: Infrastructure updates for core dependencies that affect security, search functionality, and Kubernetes support

## Prerequisites

Before you install NBS 7.12, confirm the following:

- Your NBS 6 deployment is running version 6.0.18.1 or later. See [Compatibility matrix](../../before-you-deploy/compatibility.html).
- Required NBS 6 dependencies remain in place, including Rhapsody routes, SAS 9.4 reporting, and authentication configured with a standards-based identity protocol such as OpenID Connect (OIDC), SAML, OAuth 2.0, or Active Directory.

## What changed in 7.12

| Component | Change | Action required |
|---|---|---|
| Elasticsearch | Upgraded from 7.17.1 to 9 | Yes. See [Elasticsearch upgrade](#elasticsearch-upgrade). |
| Ingress controller | Replaced Ingress NGINX with Traefik | Yes. See [Ingress controller migration: NGINX to Traefik](#ingress-controller-migration-nginx-to-traefik). |
| Kubernetes | Control plane updated to version 1.35 | Yes if your cluster is running 1.32 or earlier. See [Kubernetes control plane update](#kubernetes-control-plane-update). |

## Infrastructure changes

### Elasticsearch upgrade

NBS 7.11 included Elasticsearch 7.17.1, which reached end-of-life in January 2026. NBS 7.12 upgrades Elasticsearch to version 9, which is supported through 2029.

You cannot upgrade directly from version 7 to version 9. Depending on your current version, you might need to upgrade from 7 to 8 first, then from 8 to 9.

> Step-by-step Elasticsearch upgrade instructions for NBS 7.12 are in the 7.12 collaboration space on NBS Central. Retrieve those instructions before you begin because this version transition includes index migration steps that are not part of the standard upgrade procedure.
{: .important }

To access those instructions:

1. Sign in to [NBS Central](https://nbscentral.cdc.gov).
1. Open the 7.12 collaboration space.
1. Download the Elasticsearch upgrade instructions from the release artifacts.

### Ingress controller migration: NGINX to Traefik

NBS 7.12 replaces Ingress NGINX with [Traefik](https://traefik.io/traefik) as the required ingress controller.

> Migration instructions for this change are in the 7.12 collaboration space on NBS Central. This release replaces a core infrastructure component and requires steps beyond the standard Terraform and Helm upgrade procedure.
{: .important }

To access those instructions:

1. Sign in to [NBS Central](https://nbscentral.cdc.gov).
1. Open the 7.12 collaboration space.
1. Download the NGINX to Traefik migration guide from the release artifacts.

If you encounter issues during the migration, open a ticket on [NBS Central](https://nbscentral.cdc.gov/issues/new) with the subject line "Traefik migration issues."

### Kubernetes control plane update

NBS 7.12 updates the Kubernetes control plane to version 1.35. Clusters running version 1.32 reached end-of-support on March 31, 2026.

For Amazon Elastic Kubernetes Service (EKS) environments, follow [Update EKS control plane](../eks-upgrade.html). That procedure covers version-by-version upgrades using Terraform and applies to this release.

## Standard upgrade steps

After you complete any release-specific steps in this page, follow [Upgrade NBS 7](../upgrade-nbs7.html) to apply the 7.12 Terraform scripts and Helm charts.

## Known issues

No new known issues were introduced in NBS 7.12.

For a full list of active known issues, see the [NBS Central defects log](https://nbscentral.cdc.gov/projects/def/issues).

## Get help

- [Open a ticket on NBS Central](https://nbscentral.cdc.gov/issues/new)
- Email [nbs@cdc.gov](mailto:nbs@cdc.gov)
