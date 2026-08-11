---
title: NBS 7 release history
layout: page
parent: NBS 7 Introduction
nav_order: 4
description: A summary of new features and notable fixes introduced in each NBS 7 release.
---

# History of enhancements in NBS 7 releases
This page summarizes the new features and notable fixes introduced in each NBS 7 release, starting with the most recent release. Use this page to see what capabilities NBS 7 has gained over time and which release introduced them.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## 7.13: Azure support, RTR launch, SAS removed from reporting

NBS 7.13, released in July 2026, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.13 | New feature | Added Microsoft Azure as a supported deployment platform, alongside AWS. | Jurisdictions can choose a cloud provider based on existing contracts rather than being locked to AWS. |
| 7.13 | New feature | Introduced layered Terraform: infrastructure split into independently deployable landing-zone, nbs7, and applications layers, each with its own state file. | Infrastructure changes are isolated and lower-risk. A failure in one layer does not block the others. |
| 7.13 | New feature | Real-Time Reporting (RTR) reaches data and UI parity with MasterETL, with a simplified 3-step installation, down from separate admin accounts, a Liquibase deployment, and manual data-load scripts. | Near-real-time reporting data becomes a realistic option for STLTs, not just a beta. |
| 7.13 | New feature | Reporting module rebuilt on Python, removing the SAS dependency for most reports. Includes a modernized, accessible UI with grouped filters and a guided advanced-filter query builder. | STLTs no longer need to maintain SAS licenses for standard reporting. |
| 7.13 | New feature | Consolidated 6 RTR microservices into 1 (`reporting-pipeline-service`), retired the XML-HL7 parser service, and merged the data extraction service into the case notification service. | Fewer services to install, patch, and monitor lowers ongoing operating cost. |
| 7.13 | Notable fix | Corrected RDB data quality issues found by comparing MasterETL and RTR output, documented in full in the release appendix, so jurisdictions running UAT do not mistake intentional corrections for defects. | Smoother RTR adoption testing. |
| 7.13 | Notable fix | Fixed a risk where back-button navigation could incorrectly auto-approve or auto-reject case notifications. Modernized Patient File is now disabled by default until a jurisdiction opts in. | Prevents an unreviewed case notification from being approved or rejected by mistake. |

## 7.12: Infrastructure currency

NBS 7.12, released in May 2026, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.12 | New feature | Replaced Ingress NGINX with Traefik ahead of the NGINX end-of-life date. | Avoids running an unsupported ingress controller. |
| 7.12 | New feature | Upgraded Elasticsearch 7 to 9. Support for Elasticsearch 7 ended January 2026; Elasticsearch 9 is supported through 2029. | Keeps Patient Search infrastructure on a supported version. |
| 7.12 | New feature | Upgraded the Kubernetes control plane to 1.35. Kubernetes 1.32.5 was set to be discontinued March 31, 2026. | Avoids extended-support licensing costs on EKS and AKS. |
| 7.12 | Notable fix | Stabilized NND Sync at version 1.1.3 after testing found it more reliable than version 1.1.5. | Fewer sync-related issues for jurisdictions running NND Service. |

## 7.11: RTR reporting in RDB, expanded Patient Profile

NBS 7.11.0 and 7.11.1, released in August 2025, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.11.0 | New feature | RTR reporting enabled through SAS reports integrated with the RDB, with least-privilege service accounts and automatic retry for post-processing failures. | RTR data becomes usable in actual reports for the first time, not just populated in the background. |
| 7.11.1 | New feature | Patient Profile expanded: editable demographics, superseded-record indicators, and clinical data access for vaccinations, morbidity reports, investigations, documents, treatments, lab reports, and birth records. | A single, more complete patient record view for case investigators. |
| 7.11.0 | Notable fix | Improved skip links, heading structure, landmark navigation, and ARIA labeling across Patient Search and New Patient. | Accessibility, Section 508-relevant. |
| 7.11.1 | Notable fix | Corrected CDA XML county and country mapping errors, and a missing pregnancy-status display issue, from eCR ingestion. | Data accuracy for ingested case report data. |

## 7.10: Data Availability API, RTR migration completed

NBS 7.10.0 through 7.10.3, released between June and July 2025, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.10.0 | New feature | First release of the Data Availability API. STLTs can register custom SQL queries and sync their local databases with the cloud RDB. | Gives STLTs programmatic, self-service access to reporting data instead of relying on CDC-built reports alone. |
| 7.10.0 | New feature | Completed migration of all identified tables for the first release of RTR. Testing began the following sprint. | RTR reaches full table coverage for the first time. |
| 7.10.1 | New feature | Began migrating the notification and case-notification pipeline from Rhapsody to Java, including a modularized HL7 parser. | Early groundwork for the microservice consolidation completed later, in 7.13. |
| 7.10.1-7.10.2 | Notable fix | Added screen reader announcements for "no results found" and required-field indicators, and full keyboard navigation for combo boxes, dropdowns, date pickers, and charts. | Accessibility, Section 508-relevant. A meaningful jump in keyboard and screen reader coverage. |

## 7.9: Session timeout warning, sortable search columns

NBS 7.9.0 through 7.9.3, released between March and May 2025, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.9.0 | New feature | Users receive an idle-session warning after 28 minutes, with a 2-minute notice before logout. | Reduces unexpected data loss from session timeouts. |
| 7.9.0 | New feature | Patient Search results become sortable and filterable by address, phone, ID, email, sex, and date of birth or age. Results respect user permissions. | More usable search results for high-volume users. |
| 7.9.0-7.9.3 | New feature | Continued RTR table migration: 93 of 163 tables by 7.9.0, reaching 146 of 163 by 7.9.3, covering diseases, vaccinations, antimicrobials, and contact-tracing tables. | Steady progress toward full real-time reporting coverage. |
| 7.9.2 | New feature | Data Ingestion service supports SFTP retrieval with configurable file paths and types, ingestion from multiple folders, and date-range error lookups. | More flexible, more auditable ingestion configuration for admins. |

## 7.8: Flexible date search, more RTR datamarts

NBS 7.8.0 through 7.8.3, released between December 2024 and February 2025, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.8.0 | New feature | Patient Search supports multiple patient IDs and flexible date criteria, including day, month, year, and date ranges. | More precise search for investigators working partial records. |
| 7.8.3 | New feature | Added CRS, Rubella, Morbidity, Measles, Generic Case, and Case Lab datamarts, plus supporting dimensions, to the RTR pipeline. | Continued RTR coverage. Several condition-specific reports move toward real-time data. |
| 7.8.1 | Notable fix | Fixed Patient Search returning no results when searching by last name, and corrected date of birth display in results. | Core search reliability. |
| 7.8.1 | Notable fix | Prevented duplicate patient records from being created when the Save button was selected repeatedly. | Data integrity. |

## 7.7: On-premises Data Sync Service, full patient entry in one page

NBS 7.7.0 through 7.7.2, released between October and December 2024, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.7.0 | New feature | New on-premises Data Sync Service synchronizes cloud NBS data to an S3 bucket, local directory, or local database on a flexible schedule. | Gives STLTs a supported way to keep local systems current with cloud data. |
| 7.7.0 | New feature | Data Ingestion API can now ingest eCR XML in PHDC format, with Rhapsody Route Integration documentation. | Adds electronic case reporting as a supported ingestion type. |
| 7.7.0 | New feature | Users can enter a full patient record, including extended data, from a single new-patient page instead of visiting Patient Profile separately. | Faster case and patient intake workflow. |
| 7.7.1 | New feature | Data Ingestion ELR pipeline gained an optional Near Real-Time Ingestion (NRTI) mode for event-based processing. | Faster lab report availability where NRTI is enabled. |
| 7.7.2 | New feature | Added Lab100 and Lab101 datamarts to the RTR pipeline. | Continued RTR datamart coverage expansion. |

## 7.6: RTR launches, customizable search tables

NBS 7.6.0 through 7.6.2, released between September and October 2024, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.6.0 | New feature | Real-Time Reporting (RTR) introduced, starting with the Hepatitis Datamart, replacing the existing batch ETL process for that datamart. | First working instance of a long-term goal: real-time instead of overnight-batch reporting data. |
| 7.6.0 | New feature | New on-premises API lets systems hosted on-premises retrieve data from a cloud-hosted NBS database, without disrupting existing outbound NNDSS routes. | Supports hybrid cloud and on-premises architectures during migration. |
| 7.6.0 | New feature | Search results for Patients, Lab Reports, and Investigations gained a customizable table view: sortable, filterable, and persisted with a shareable, bookmarkable URL. | Investigators can save and share specific search views. |
| 7.6.2 | New feature | Added a new API for ELR PHDC (eCR) data ingestion, and added the Public Health Case Fact (PHCF) Datamart to the RTR pipeline, for 2 datamarts total. | Broadens both ingestion formats and RTR coverage. |

## 7.5: Keycloak by default, RTR groundwork

NBS 7.5.0 and 7.5.3, released in August 2024, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.5.0 | New feature | NBS now ships with an integrated Keycloak identity provider by default, securing access and database connections even without a jurisdiction-provided identity provider or single sign-on. | Removes a dependency on STLTs standing up their own identity provider. |
| 7.5.0 | New feature | New login and home page with installation guides, feature overviews, and CDC links. Updated to support NBS 6.0.16. | Easier onboarding for new NBS 7 users and admins. |
| 7.5.3 | New feature | Completed foundational infrastructure and testing for RTR in the cloud, ahead of the first Hepatitis Datamart release in 7.6.0. | First concrete step toward replacing overnight batch reporting. |

## 7.4: Page Builder completed, high-volume ingestion fixes

NBS 7.4.0 through 7.4.4, released between April and July 2024, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.4.0 | New feature | Completed Page Builder delivery: preview pages before publishing, manage sections, tabs, and questions, and reorder and group elements. | Investigation page configuration becomes fully self-service. |
| 7.4.0 | New feature | Data Ingestion API now accepts HL7 ELR text files through SFTP. | Additional intake path for jurisdictions using file-based transfer. |
| 7.4.0 | Notable fix | Resolved an out-of-memory error that limited how many ELRs could be posted during high-volume ingestion, and corrected mandatory-field validation timing. | Reliability during surge periods, such as outbreak reporting volume. |
| 7.4.0 | Notable fix | Upgraded to the latest Spring Boot version to close known security vulnerabilities. | Security patching with no user-facing change. |
| 7.4.4 | Notable fix | Fixed the timestamp for patient address changes not being recorded. | Data audit accuracy. |

## 7.3: Page Builder 2.0

NBS 7.3.0 through 7.3.3, released between February and April 2024, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.3.0 | New feature | Page Builder 2.0: create condition-specific investigation pages, manage conditions and value sets, import templates, and browse, search, and export the page library. | First step toward configurable investigation pages instead of hardcoded classic NBS forms. |
| 7.3.2 | New feature | Edited or deleted demographic data now writes to patient history tables, matching NBS 6 audit behavior. | Preserves a change history for patient records, supporting data governance. |
| 7.3.0 | Notable fix | Improved screen reader heading structure and keyboard navigation on Patient Search and Patient Profile. | Accessibility, Section 508-relevant. |
| 7.3.1 | Notable fix | Corrected event search results for notification status, and added autocomplete for ordering and reporting facility and provider search. | Search accuracy for event investigators. |
| 7.3.3 | Notable fix | Fixed "Clear All" not resetting search filters, and corrected screen reader interaction issues on the new patient form. | Accessibility and search reliability. |

## 7.2: ReportStream integration, Keycloak identity provider

NBS 7.2.0 through 7.2.2, released between January and February 2024, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.2.0 | New feature | Added ReportStream setup so HL7 ELR can be sent directly to NBS from ReportStream, plus CLI onboarding commands for status checks and error review. | Expands lab report intake options beyond direct Rhapsody routes. |
| 7.2.1 | New feature | Added secure service-to-service authentication to the Data Ingestion Pipeline using Keycloak, and extended CLI support from Mac-only to Windows and Linux. | Secures data ingestion traffic and removes an operating system restriction on admin tooling. |
| 7.2.0 | Notable fix | Lab reports were not appearing on Patient Profile. Replaced the Elasticsearch-based lookup with a direct database call. | Fixes a core clinical data visibility gap. |
| 7.2.2 | Notable fix | Fixed lab report dates defaulting to 01/01/1970, prevented duplicate race entries, and removed the ability to delete, rather than edit, administrative comments. | Data integrity on patient records. |

## 7.1: Data Ingestion Service launch

NBS 7.1.0 and 7.1.1, released between November and December 2023, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.1.0 | New feature | First release of the Data Ingestion Service: accepts HL7 v2.3.1 and v2.5.1 ELR, audits all incoming messages, validates against standard rules, and checks for duplicates. | Lays the foundation for automated, auditable lab report ingestion instead of manual entry. |
| 7.1.0 | Notable fix | Fixed a page crash when entering text beyond a field's character limit during patient data entry. | Prevents data entry from failing outright on long input. |
| 7.1.1 | Notable fix | Corrected patient search failures for "Other" gender, partial phone number matching, and event search by processing status. | Core search reliability. |

## 7.0: Initial modernized release

NBS 7.0.0 and 7.0.1, released between September and November 2023, added the following enhancements and fixes:

| Patch | Type | Enhancement | STLT benefit |
|---|---|---|---|
| 7.0.0 | New feature | First modernized release: Patient Search, Patient Profile with Summary, Events, and Demographics tabs, Patient Data Entry, and Patient Delete, running alongside classic NBS 6. | Established the modernized UI foundation that all later releases build on. |
| 7.0.1 | Notable fix | Corrected session logout routing, SSN, hyphenated-name, and phone number search failures, and patient profile fields not reflecting new names or multiple races. | Search and login reliability for early adopters. |
