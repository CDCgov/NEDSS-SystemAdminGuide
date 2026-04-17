---
title: Upgrade NBS 7
layout: page
parent: Maintain NBS 7
nav_order: 1
has_children: true
description: Walks through the standard NBS 7 upgrade process and links to version-specific release notes for additional required steps.
---

# Upgrade NBS 7

Use this page for the standard procedure to upgrade an existing NBS 7 deployment. Before you begin, review the release notes for the version you are installing. Some releases include additional steps that fall outside the standard procedure.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> Review the release notes for the version you are installing before you start the upgrade. Version-specific release notes identify prerequisite changes, dependency updates, and extra steps that are not part of the standard procedure.
{: .important }

## Before you upgrade

Confirm the following before you begin:

- You have reviewed the release notes for your target version.
- Your current NBS 6 version is compatible with the NBS 7 version you plan to install. See [Compatibility matrix](../before-you-deploy/compatibility.html).
- You have a tested backup or recovery point for the environment you are upgrading.
- You have scheduled a maintenance window and notified affected stakeholders.
- You have upgraded a non-production environment first and verified expected behavior before scheduling production.

## Upgrade NBS 7

To apply a standard NBS 7 upgrade:

1. Download the release artifacts for the version you are installing.

   Release artifacts can include updated Terraform infrastructure code, Helm charts, release notes, and other release-specific materials. Depending on the release, some artifacts might be distributed through the release-specific collaboration space on [NBS Central](https://nbscentral.cdc.gov) and some through GitHub release pages such as [CDCgov/NEDSS-Helm releases](https://github.com/CDCgov/NEDSS-Helm/releases).

1. Sign in to the cloud environment, Kubernetes cluster, and tooling used to administer your NBS 7 deployment.

1. Review the release notes and compare your existing configuration files with the versions supplied in the release artifacts.

   Not every release changes the same values. Update only the parameters that apply to your environment and target version.

1. Run Terraform to preview and apply infrastructure changes that are part of the release.

   ```bash
   terraform plan
   terraform apply
   ```

   Review the plan output before you apply it. Confirm that the changes match the release notes and your target environment.

1. Merge any local Helm chart customizations into the chart values supplied with the release before deploying updated services.

1. Run Helm to deploy the updated containers.

   ```bash
   helm upgrade --install <release-name> <chart-path>
   ```

1. Validate the upgraded environment.

   Confirm that:

   - The application is accessible.
   - Core workflows are functioning as expected.
   - Data ingestion and downstream processing are functioning as expected for your deployment.

## Release-specific steps

Some NBS 7 releases include infrastructure or dependency changes that require additional work beyond the standard procedure. Use the release notes for your target version to identify those steps.

| Component or change area | Where to find instructions |
|---|---|
| EKS control plane updates | [Update EKS control plane](eks-upgrade.html) |
| Elasticsearch version changes | Release notes for the applicable version |
| Ingress controller changes | Release notes for the applicable version |

> Component-level instructions in release notes are version-specific. Use this page for the repeatable baseline procedure and use the release notes for steps that apply only to a specific release.
{: .note }

## Release notes

Use the child pages in this section for version-specific upgrade guidance.

- [NBS 7.12 release notes](upgrade-nbs7/release-notes-7-12.html) describe the release-specific prerequisites and infrastructure changes for NBS 7.12.

## Get help

If you encounter issues during an upgrade:

- [Open a ticket on NBS Central](https://nbscentral.cdc.gov/issues/new)
- Email [nbs@cdc.gov](mailto:nbs@cdc.gov)
