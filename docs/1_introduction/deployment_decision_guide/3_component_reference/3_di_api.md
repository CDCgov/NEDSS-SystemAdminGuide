---
title: "Add-on: Data Ingestion (DI) API"
layout: page
parent: Component reference
grand_parent: NBS 7 Deployment Decision Guide
nav_order: 3
description: Details the Data Ingestion (DI) API add-on component, which accepts ELRs, eCRs, and PHDC files without requiring third-party middleware.
---

## Component reference: Data Ingestion (DI) API add-on
{: .no_toc }

For information on migration planning, staffing, and budget, see [Operational considerations](leadership_considerations.html).
{: .note }

<!--
## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}
-->

The DI API is a data transit layer built into NBS 7 that accepts incoming public health data and routes it into NBS without requiring third-party middleware. The DI API is added to your NBS 7 deployment when you choose to deploy the DI API add-on.

## DI API

A modern data ingestion layer that accepts incoming public health data in multiple formats and routes it into NBS.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Accepts Electronic Case Reports (eCR), HL7 v2.x electronic lab reports (ELRs), and Public Health Document Container (PHDC) files. Validates, transforms, and routes incoming data to the appropriate NBS services. The DI API is designed to be more flexible and maintainable than legacy middleware solutions. |
| When you need it | When your jurisdiction receives high volumes of ELRs or eCRs, or when you want to replace or evaluate alternatives to your current middleware (such as Rhapsody). Required for NBS Core + DI API and NBS Complete configurations. |
| Dependencies | Requires NBS Core. Integrates with external data senders (laboratories, EHR systems, health information exchanges). Routes processed data into the NBS database via the Modernization API. |
