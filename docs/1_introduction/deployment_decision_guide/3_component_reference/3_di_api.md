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

{: .important-title }
> What leadership needs to know
> 
> The DI API is relevant if your jurisdiction uses middleware like Rhapsody to route incoming lab reports and case reports into NBS. While the DI API has the potential to reduce middleware licensing costs and simplify your data intake architecture, it is not yet a full replacement for existing middleware solutions. Jurisdictions with Rhapsody or Mirth Connect in place should continue using them for now. If your jurisdiction does not have existing middleware, the DI API is worth evaluating. Consider revisiting its viability as the product matures and new features are released.


### DI API

A modern data ingestion layer that accepts incoming public health data in multiple formats and routes it into NBS.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Accepts Electronic Case Reports (eCR), HL7 v2.x electronic lab reports (ELRs), and Public Health Document Container (PHDC) files. Validates, transforms, and routes incoming data to the appropriate NBS services. The DI API is designed to be more flexible and maintainable than legacy middleware solutions. |
| When you need it | When your jurisdiction receives high volumes of ELRs or eCRs, or when you want to replace or evaluate alternatives to your current middleware (such as Rhapsody). Required for NBS Core + DI API and NBS Complete configurations. |
| Dependencies | Requires NBS Core. Integrates with external data senders (laboratories, EHR systems, health information exchanges). Routes processed data into the NBS database via the Modernization API. |
