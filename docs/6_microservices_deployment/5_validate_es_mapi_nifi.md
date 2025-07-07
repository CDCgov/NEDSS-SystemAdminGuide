---
title: Validate ES, Mapi and Nifi
layout: page
parent: Microservices Deployment
nav_order: 5
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Validate Elasticsearch, Modernization-API and Nifi
When you are able to perform the validation steps and get results back, it validates the following portions of the system are functioning properly:
- Name resolution is working
- Routing requests and traffic between the NBS 6.x portions of the system and NBS 7 is working properly
- Routing from the NBS 7 components to the (shared) database is working
- The search indices have been created and populated, and are available, thereby validating Elasticsearch, NiFi, and the Modernization-API.

> ℹ️ **Please note:** The search indices may take longer time to populate depending on the data. For example, a larger database may take **3–6 hours**.
