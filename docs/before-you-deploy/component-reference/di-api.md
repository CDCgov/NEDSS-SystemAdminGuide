---
title: "Add-on: Data Ingestion (DI) API"
layout: page
parent: Component reference
grand_parent: Before you deploy
nav_order: 3
description: Details the Data Ingestion (DI) API add-on component, which provides a REST API layer for routing incoming data into NBS through middleware.
---

# Component reference: Data Ingestion (DI) API add-on

The DI API is a REST API layer built into NBS 7 that accepts incoming public health data and routes it into NBS. Middleware such as Rhapsody or an equivalent integration engine preprocesses and formats the data, then sends it to the DI API instead of writing directly to the NBS database.

For information on the relationship between the DI API and your existing middleware, see [Operational considerations](../../before-you-deploy/operational_considerations.html).
{: .note }

<!--
## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}
-->

## DI API

A REST API layer that accepts incoming public health data in multiple formats and routes it into NBS.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Accepts Electronic Case Reports (eCR), HL7 v2.x electronic lab reports (ELRs), and Public Health Document Container (PHDC) files through a standard API interface. Middleware preprocesses, enriches, and formats the data, then sends it to the DI API for ingestion into NBS. This supports near-real-time ingestion and gives jurisdictions an option when they do not want middleware or other third-party tools writing directly to the NBS database. |
| When you need it | Use the DI API add-on when your jurisdiction needs an API-based ingestion path instead of direct database access. This is especially useful for jurisdictions with security constraints that prevent middleware from connecting directly to the NBS database. |
| Dependencies | Requires middleware such as Rhapsody or an equivalent integration engine. External senders such as laboratories, EHR systems, and health information exchanges continue to send data through middleware, which then sends the processed payload to the DI API. |
