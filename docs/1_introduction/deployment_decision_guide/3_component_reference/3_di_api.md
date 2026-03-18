---
title: "Add-on: Data Ingestion (DI) API"
layout: page
parent: Component reference
grand_parent: NBS 7 Deployment Decision Guide
nav_order: 3
---

<!-- PAGE TITLE - DON'T INCLUDE HEADER IN TOC -->
## Component reference: Data Ingestion (DI) API add-on
{: .no_toc }

The DI API is a data transit layer built into NBS 7 that accepts incoming public health data and routes it into NBS without requiring third-party middleware. The DI API is added to your NBS Core deployment when you choose NBS Core + DI API or NBS Complete.


--- 

{: .note }
**Health department leaders:** See [Leadership considerations](../leadership_considerations.html) for guidance on evaluating the DI API for your jurisdiction.


### DI API

A modern data ingestion layer that accepts incoming public health data in multiple formats and routes it into NBS.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Accepts Electronic Case Reports (eCR), HL7 v2.x electronic lab reports (ELRs), and Public Health Document Container (PHDC) files. Validates, transforms, and routes incoming data to the appropriate NBS services. The DI API is designed to be more flexible and maintainable than legacy middleware solutions. |
| When you need it | When your jurisdiction receives high volumes of ELRs or eCRs, or when you want to replace or evaluate alternatives to your current middleware (such as Rhapsody). Required for NBS Core + DI API and NBS Complete configurations. |
| Dependencies | Requires NBS Core. Integrates with external data senders (laboratories, EHR systems, health information exchanges). Routes processed data into the NBS database via the Modernization API. |
