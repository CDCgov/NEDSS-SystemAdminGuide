---
title: Supported NBS versions
layout: page
parent: NBS 7 Introduction
nav_order: 2
description: Verify that your NBS 6 version is supported and compatible with your target NBS 7 version.
---

<!-- RELEASE CHECKLIST: Review this page each release cycle. Confirm the supported NBS 7 and NBS 6 version lists and the version combination table are current before publishing. -->

# Supported NBS versions

[[cdc]] supports the most recently released versions of [[nbs]]. A **supported version** continues to receive security patches, defect fixes, and compatibility updates. An **unsupported version** no longer receives updates, though every feature and fix it introduced remains present in later supported versions.

Migrating from the latest supported NBS 6 version to the latest NBS 7 version provides the smoothest path to NBS 7.
{: .important }

For the supported Microsoft Windows Server and Microsoft SQL Server versions for your database, and the workstation tool versions needed to deploy, see [Cloud prerequisites](./deploy-nbs7/full-deploy/provision-cloud-infrastructure/cloud-prerequisites.html).

## Supported NBS 7 versions

The following [[nbs-7]] versions are supported:

- 7.13.0
- 7.12.0

To see what changed in each of these releases, see the [History of changes in NBS 7 releases](./nbs7-introduction/release-history.html).

## Supported NBS 6 versions

The following [[classic-nbs]] versions are supported:

- 6.0.19.1 (requires NBS 7.13.0)
- 6.0.18.1

## Supported NBS 6 and NBS 7 version combinations

NBS 7 integrates with and is tested against specific versions of NBS 6. Use the following table to verify that your NBS 6 version is compatible with your target NBS 7 version before you begin deployment.

| Supported NBS 6 version | Works with 7.13.0 | Works with 7.12.0 |
|---|---|---|
| 6.0.19.1 | <span class="text-green">✓ Yes</span> | No |
| 6.0.18.1 | <span class="text-green">✓ Yes</span> | <span class="text-green">✓ Yes</span> |

This table lists the supported NBS version combinations as of the latest NBS 7 release. Versions not listed are not supported, even if a combination appears to work in your environment.
{: .note }
