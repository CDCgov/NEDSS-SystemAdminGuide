---
title: Case Notification
layout: page
parent: Microservices Deployment
nav_order: 9
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Case Notification Overview
This guide sets out the detailed steps to installing NBS 7 Case Notification, end to end.
- Case Notification consist of 4 services and should be deployed in this top down order
  - Debezium Case Notification
  - XML HL7 Parser Service
  - Data Extraction Service
  -  Notification Service
