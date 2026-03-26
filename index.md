---
title: Introduction
layout: home
nav_order: 1
description: Introduction to the National Electronic Disease Surveillance System (NEDSS) Base System (NBS) administration and deployment guide.
---

# Introduction

The National Electronic Disease Surveillance System (NEDSS) Base System (NBS) is a CDC-developed disease surveillance system that health departments use to manage reportable disease data. This guide covers deploying and administering NBS 7, a modernized version of the platform built on cloud-native infrastructure. NBS 7 retains full NBS 6 feature equivalence while introducing improved interfaces, optional near real-time patient search, and a modular architecture that makes the system easier to maintain and extend over time.
{: .fw-300 }

---

## Purpose

The purpose of this document is to help an NBS system administrator deploy the NBS 7 infrastructure and microservices in an AWS environment. It will provide the information needed to set up the required environment, as well as convey a common understanding of the initial install.

## Runtime Environment Support

NBS 7 supports AWS and Azure as runtime options. The underlying system itself has been developed using a cloud-agnostic approach. This guide targets the AWS runtime. For more information on Azure, please contact [nbs@cdc.gov](mailto:nbs@cdc.gov). Future versions of this guide will cover other cloud runtime environments that support [Kubernetes](https://kubernetes.io/) such as Google Cloud Platform and Azure.

## Intended Audience

This guide is intended to be used to install NBS 7, a complex cloud-native application. It assumes familiarity with cloud technologies and tools: knowledge of your cloud service provider (e.g. AWS), runtime environment (e.g. [Kubernetes](https://kubernetes.io/)), experience running [Terraform](https://www.terraform.io/) and [Helm](https://helm.sh/), and experience debugging routine systems and infrastructure problems. You will need administrator-level access to your runtime environment, and access to a local system with a set of installed prerequisites.

For more information on NBS, see the official CDC [National Electronic Disease Surveillance System Base System (NBS)](https://www.cdc.gov/nbs/php/index.html) website.

## Revision History

| Date         | Description        | Author |
|:-------------|:------------------|:-------|
| April xx, 2026 | Site restructure and before-you-deploy content | Jill Shaheen |
| August 19, 2025 | 7.11.0 Minor Release | Anand Logan, Upasana Pattnaik, Kashyap Ramakur, Aaron Chapman, Duc Nguyen, Chuck Moss, Serban Zamfir |
