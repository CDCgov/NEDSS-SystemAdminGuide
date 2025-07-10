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

## Check List before Deployment
- Case Notification Services are alternative option for the STLT, we need to determine whether the STLT would want to use Case Notification Service or the STLT want to stick with Rhapsody Case Notification Route
    - If STLT sticks with Rhapsody, then we can ignore Case Notification Service and not deploying it
    - If STLT choose modernize, then we can proceed with the following steps
- If choose NOT to deploy Case Notification Service, these following services should not be turned on in Kubernetes
    - Debezium Case Notification
    - XML HL7 Parser Service
    - Data Extraction Service
    - Case Notification Service

## Case Notification Dependency
Case notification need NND data sync for the full pipeline to functional with STLT
- Please following this step to setup Data Sync for any STLT who require to have Case Notification Service
- Case Notification only require STLT to run NND Sync, not the RDB Data Sync

## Case Notification Overview
This guide sets out the detailed steps to installing NBS 7 Case Notification, end to end.
- Case Notification consist of 4 services and should be deployed in this top down order
  - Debezium Case Notification
  - XML HL7 Parser Service
  - Data Extraction Service
  -  Notification Service
