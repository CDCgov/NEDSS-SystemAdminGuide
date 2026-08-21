---
title: Data Ingestion (DI API)
layout: page
parent: Component reference
nav_order: 3
description: Details the Data Ingestion (DI) API component, which provides a REST API layer for routing incoming data into NBS through middleware.
---

# Component reference: Data Ingestion (DI) API

The DI API is a Representational State Transfer ({% include term-tooltip.html key="rest" term="REST" id="diapi-rest" %}) API layer built into {% include term-tooltip.html key="nbs-7" term="NBS 7" id="diapi-nbs-7" %} that accepts incoming public health data and routes it into NBS. Middleware such as Rhapsody or an equivalent integration engine preprocesses and formats the data, then sends it to the DI API instead of writing directly to the NBS database.

For information on the relationship between the DI API and your existing middleware, see [Operational considerations](../../before-you-deploy/operational-considerations.html).
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
| What it does in NBS 7 | Accepts Electronic Case Reports ({% include term-tooltip.html key="ecr" term="eCR" id="diapi-ecr" %}), {% include term-tooltip.html key="hl7" term="HL7" id="diapi-hl7" %} v2.x electronic lab reports ({% include term-tooltip.html key="elr" term="ELRs" id="diapi-elr" %}), and Public Health Document Container ({% include term-tooltip.html key="phdc" term="PHDC" id="diapi-phdc" %}) files through a standard API interface. Middleware preprocesses, enriches, and formats the data, then sends it to the DI API for ingestion into NBS. This supports near-real-time ingestion and gives {% include term-tooltip.html key="jurisdiction" term="jurisdictions" id="diapi-jurisdiction" %} an option when they do not want middleware or other third-party tools writing directly to the NBS database. |
| When you need it | Use DI API for an API-based ingestion path instead of direct database access. This is especially useful for jurisdictions with security constraints that prevent middleware from connecting directly to the NBS database. |
| Dependencies | Requires middleware such as Rhapsody or an equivalent integration engine. External senders such as laboratories, {% include term-tooltip.html key="ehr" term="EHR" id="diapi-ehr" %} systems, and health information exchanges continue to send data through middleware, which then sends the processed payload to the DI API. |
