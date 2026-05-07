---
title: Introduction
layout: home
nav_order: 1
description: Overview of the NBS system administration guide, including preparation, deployment, validation, and maintenance content for NBS 7.
---

# Introduction

The National Electronic Disease Surveillance System (NEDSS) Base System (NBS) is a CDC-developed disease surveillance system that health departments use to manage reportable disease data. NBS 7 is the modernized version of the platform, designed for deployment and operation on cloud-based infrastructure. This documentation supports the administration lifecycle for NBS 7, including planning, deployment, validation, and maintenance.
{: .fw-300}

> The content in this guide reflects NBS {{ site.version_latest }}. For procedures from earlier releases, see **Previous Versions** in the sidebar.
{: .note }

---

## Purpose and scope

The NBS 7 System Administration guide helps you prepare for NBS 7, deploy the platform, validate that it is working correctly, and maintain it over time. It brings together operational guidance for system administration tasks across the NBS 7 lifecycle.

The content is centered on system administration. It covers readiness and planning work before deployment, phased deployment guidance for NBS 7 infrastructure and services, and maintenance topics for operating environments after go-live.

## In this guide

- [Before you deploy](docs/before-you-deploy.html) covers readiness checks, configuration decisions, compatibility guidance, and pre-deployment planning.
- [Deploy NBS 7](docs/deploy-nbs7.html) covers infrastructure, microservices, add-ons, and deployment validation steps.
- [Maintain NBS 7](docs/maintain-nbs7.html) covers post-deployment administration and maintenance tasks.

## Runtime environment support

NBS 7 supports AWS and Azure as runtime options. The platform uses a cloud-agnostic approach, and the deployment content includes guidance for both supported providers. NBS 7 runs on [Kubernetes](https://kubernetes.io/) and relies on tools such as [Terraform](https://developer.hashicorp.com/terraform) and [Helm](https://helm.sh/) to provision and manage infrastructure and services.

## Intended audience

The primary audience is system administrators at state, tribal, local, and territorial health departments who install, operate, and maintain NBS 7. The content assumes familiarity with your cloud platform, Kubernetes, Terraform, Helm, and related administration tasks. You need administrator-level access to your runtime environment and a local system with required prerequisites installed.

## Additional resources

For more information on NBS, see the official CDC [National Electronic Disease Surveillance System Base System (NBS)](https://www.cdc.gov/nbs/php/index.html) website and [NBS Central](https://nbscentral.cdc.gov/), the community hub for NBS users where you can download software, access technical resources, and participate in user group calls.

> Access to **NBS Central** requires a login. To register for an NBS Central account, choose **Register** at the top of the [login screen](https://nbscentral.cdc.gov/login).
{: .note }
