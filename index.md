---
title: Introduction
layout: home
nav_order: 1
description: Introduction to the National Electronic Disease Surveillance System (NEDSS) Base System (NBS) administration and deployment guide.
---

# Introduction

The National Electronic Disease Surveillance System (NEDSS) Base System (NBS) is a CDC-developed disease surveillance system that health departments use to manage reportable disease data. This guide covers deploying and administering NBS 7, the modernized version of the platform built on cloud-native infrastructure. NBS 7 retains NBS 6 feature equivalence while introducing improved interfaces and optional near real-time patient search.
{: .fw-300}

---

## Purpose

This guide helps NBS system administrators plan, deploy, validate, and maintain NBS 7. It provides the information needed to prepare the required environment and complete the initial installation.

## Runtime Environment Support

NBS 7 supports AWS and Azure as runtime options. The platform uses a cloud-agnostic approach, and this guide includes deployment guidance for both supported providers. NBS 7 runs on [Kubernetes](https://kubernetes.io/) and relies on tools such as [Terraform](https://developer.hashicorp.com/terraform) and [Helm](https://helm.sh/) to provision and manage infrastructure and services.

## Intended Audience

This guide is for system administrators who install and maintain NBS 7, a complex cloud-native application. It assumes familiarity with cloud technologies and tools, including your cloud provider, [Kubernetes](https://kubernetes.io/), [Terraform](https://developer.hashicorp.com/terraform), and [Helm](https://helm.sh/). You need administrator-level access to your runtime environment and access to a local system with the required prerequisites installed.

For more information on NBS, see the official CDC [National Electronic Disease Surveillance System Base System (NBS)](https://www.cdc.gov/nbs/php/index.html) website.

## Revision History

| Date         | Description        | Author |
|:-------------|:------------------|:-------|
| April xx, 2026 | Site restructure and before-you-deploy content | Jill Shaheen |
| August 19, 2025 | 7.11.0 Minor Release | Anand Logan, Upasana Pattnaik, Kashyap Ramakur, Aaron Chapman, Duc Nguyen, Chuck Moss, Serban Zamfir |
