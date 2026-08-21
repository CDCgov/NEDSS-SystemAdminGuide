---
title: NBS 7 Introduction
layout: home
nav_order: 1
has_children: true
has_toc: false
description: Overview of the NBS system administration guide, including preparation, deployment, validation, and maintenance content for NBS 7.
---

# Introduction

The National Electronic Disease Surveillance System ([[nedss]]) Base System ([[nbs]]) is a disease surveillance system developed by the Centers for Disease Control and Prevention ([[cdc]]) that health departments use to manage [[reportable-disease]] data. [[nbs-7]] is the modernized version of the platform, designed for deployment and operation on cloud-based infrastructure. This documentation supports the administration lifecycle for NBS 7, including planning, deployment, validation, and maintenance.
{: .fw-300}

> The content in this guide reflects NBS {{ site.version_latest }}. For procedures from earlier releases, see **Previous Versions** in the sidebar. Each NBS 7 release supports specific [[classic-nbs|NBS 6]] versions. Before you begin any deployment or upgrade, verify that your NBS 6 version is supported for your target NBS 7 version on the [Supported NBS versions](docs/supported-versions.html) page.
{: .important }

---

## Purpose and scope

The NBS 7 System Administration guide helps you prepare for NBS 7, deploy the platform, validate that it is working correctly, and maintain it over time. It brings together operational guidance for system administration tasks across the NBS 7 lifecycle.

## In this guide

This guide covers the full NBS 7 administration lifecycle in three main parts:

- **[Before you deploy NBS 7](docs/before-you-deploy.html)** covers readiness checks and pre-deployment planning.
- **[Deploy NBS 7](docs/deploy-nbs7.html)** covers infrastructure, microservices, and deployment validation steps.
- **[Maintain NBS 7](docs/maintain-nbs7.html)** covers post-deployment administration and maintenance tasks.

The guide also includes supplementary reference materials, such as the glossary and support resources.

## Intended audience

The primary audience is system administrators at state, tribal, local, and territorial ([[stlt]]) health departments who install, operate, and maintain NBS 7. The content assumes familiarity with your cloud platform, [[kubernetes]], [[terraform]], [[helm]], and related administration tasks.

## Runtime environment support

NBS 7 supports Amazon Web Services ([[aws]]) and [[microsoft-azure]] as runtime options. The platform uses a cloud-agnostic approach, and the deployment content includes guidance for both supported providers. NBS 7 runs on Kubernetes and relies on tools such as Terraform, and Helm to provision and manage infrastructure and services. You need administrator-level access to your runtime environment and a local system with required prerequisites installed.

## Additional resources

For more information on NBS, see the official CDC [National Electronic Disease Surveillance System Base System (NBS)](https://www.cdc.gov/nbs/php/index.html) website and [NBS Central](https://nbscentral.cdc.gov/), the community hub for NBS users where you can download software, access technical resources, and participate in user group calls.

Access to [[nbs-central]] requires a login. To register for an NBS Central account, choose **Register** at the top of the [login screen](https://nbscentral.cdc.gov/login).
{: .note }
