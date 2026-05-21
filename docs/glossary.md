---
title: Glossary
layout: page
nav_order: 5
description: "Definitions for terms and acronyms used in the NBS 7 System Administrator Guide."
last_modified_date: 2026-05-18
---

# Glossary
{: .no_toc }

Definitions for acronyms and technical terms used in this guide. For context on how a term applies to your specific deployment or configuration, see the relevant section of the guide.

<!--
  ******** CONTRIBUTOR GUIDANCE ********

  SCOPE AND PURPOSE
  - This glossary is an acronym reference for eClearance. Its primary
    function is to let technical documentation use terms like HL7, API,
    and ELR without spelling them out on every page.
  - Definitions must be general and durable. Write them to remain
    accurate as the system evolves — not to describe current NBS behavior
    or implementation details.
  - NBS-specific context (how a term is used in NBS, which component
    handles it, what it triggers) belongs in the admin guide at the point
    of need, not here.
  - Avoid version-specific references (for example, "NBS 7.12"). If a
    version reference is unavoidable, use the major version ("NBS 7").
  - Non-acronym terms are currently included but are under stakeholder
    review and may be removed. Add non-acronym terms sparingly; prefer
    placing NBS-domain context in the relevant guide page instead.

  ADDING NEW ENTRIES
  - Add each term as a ### heading under the correct letter section.
  - Keep definitions present-tense and active voice.
  - Define acronyms in bold at the start of the definition:
    **Full Name.** Definition text here.
  - Cross-link related terms using [term](#anchor) syntax.
    Anchors are auto-generated from heading text: lowercase,
    spaces become hyphens, punctuation dropped.
    Examples: ### HIE / HIN → #hie--hin , ### namespace (Kubernetes) → #namespace-kubernetes
  - Use official AWS service names on first mention in a definition.
    Source of truth: https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.html
    Examples: Amazon EKS, Amazon EFS, Amazon MSK, Amazon S3,
    Amazon RDS, AWS KMS, AWS IAM, Amazon Managed Service for Prometheus,
    Amazon Managed Grafana.

  REDIRECT ENTRIES
  - Add a redirect entry (### ACRONYM / See [Full Term](#anchor)).
    for any initialism that is commonly spoken or used in prose
    rather than spelled out. Example: RR → Reportability Response.

  CLOUD PROVIDER SCOPING PATTERN
  - Terms that are AWS-only or Azure-only services should include
    a cross-reference to their equivalent on the other platform,
    using "In [provider] deployments, [equivalent term] serves the
    same function." If no direct equivalent exists, name the
    closest common option(s) with "such as" framing.
    Examples: Amazon EKS → AKS, Amazon MSK → HDInsight,
    Amazon S3 → Azure Blob Storage.
  - Terms that represent a concept with provider-specific
    implementations (VPC/VNet, peering, subnet, load balancer)
    use inline scoping:
      "In AWS deployments, [AWS Product](#) covers this function.
       In Azure deployments, [Azure Product](#) covers this function."
  - Terms that apply equally to all providers need no scoping.
    Examples: Kubernetes, Terraform, TLS, Helm.
  - If a future deployment path is added (for example, GCP),
    extend the inline scoping sentence rather than changing the
    pattern.

  GLOSSARY LINKING
  - Link the first occurrence of a glossary term on each page.
  - Skip the link if the term is already defined inline in the
    same sentence.
  - Skip the link if the first occurrence is in a heading.
    Link the next occurrence in prose instead.
  - Skip the link if the first occurrence is in a code block.
    Consider adding a linked mention of the term in the prose
    immediately before the code block so it is defined before
    it is used, then treat that mention as the linked occurrence.
-->

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

## A

### AIMS

**APHL Informatics Messaging System.** A platform managed by the Association of Public Health Laboratories (APHL) for public health data exchange and messaging.

### AKS

See [Azure Kubernetes Service](#azure-kubernetes-service).

### AMG

**Amazon Managed Grafana.** An AWS-managed version of Grafana, an open-source dashboarding platform.

### AMP

**Amazon Managed Service for Prometheus.** An AWS-managed version of Prometheus, an open-source monitoring and alerting toolkit.

### API

**Application Programming Interface.** A defined interface that allows software systems to communicate.

### ArgoCD

An open-source GitOps tool for deploying and managing [Kubernetes](#kubernetes) applications.

### AVR

**Analysis, Visualization, and Reporting.** An umbrella term for the reporting and analytics capabilities of NBS and related public health systems.

### AWS

**Amazon Web Services.** A public cloud platform. Often used with services such as [Amazon EKS](#amazon-eks), [Amazon MSK](#amazon-msk), [Amazon EFS](#amazon-efs), [Amazon RDS](#amazon-rds), [Amazon S3](#amazon-s3), [AWS KMS](#kms), [Amazon Managed Service for Prometheus](#amp), and [Amazon Managed Grafana](#amg). See also [Microsoft Azure](#microsoft-azure).

### Azure

See [Microsoft Azure](#microsoft-azure).

### Azure Blob Storage

An [Azure](#microsoft-azure) service for object storage. Used for Terraform state files and logs in Azure deployments. The AWS equivalent is [Amazon S3](#amazon-s3).

### Azure Files

An [Azure](#microsoft-azure) service for file storage. In Azure deployments, Azure Files and Azure NetApp Files are common options for the persistent file storage that [Amazon EFS](#amazon-efs) provides in AWS deployments.

### Azure Key Vault

An [Azure](#microsoft-azure) service for creating and managing encryption keys, certificates, and application and database secrets. Used to protect sensitive configuration values in Azure deployments. The Azure equivalent of [AWS KMS](#kms).

### Azure Kubernetes Service

An [Azure](#microsoft-azure)-managed service for [Kubernetes](#kubernetes), commonly known as **AKS**. Hosts containerized services in Azure deployments. The AWS equivalent of AKS is [Amazon EKS](#amazon-eks).

### Azure Monitor

An [Azure](#microsoft-azure) service for monitoring infrastructure health and performance. In Azure deployments, Azure Monitor covers the observability functions that [Amazon Managed Service for Prometheus](#amp) and [Amazon Managed Grafana](#amg) provide in AWS deployments (metrics collection and dashboard visualization). Azure Monitor includes Azure-managed Grafana as an optional dashboarding component.

### Azure RBAC

**Azure Role-Based Access Control.** An [Azure](#microsoft-azure) service for managing access to cloud resources. In Azure deployments, Azure RBAC controls resource-level permissions in the same way that [AWS IAM](#iam) does in AWS deployments. Often used in conjunction with [Microsoft Entra ID](#microsoft-entra-id) for identity management.

### Azure SQL

A family of [Azure](#microsoft-azure)-managed database services. In Azure deployments, Azure SQL Database or Azure Database for SQL Server are common hosting options. The Azure equivalent of [Amazon RDS](#amazon-rds) in this context.

## B

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### build provenance

Verifiable, tamper-proof metadata documenting how a software artifact was created, including source code location, dependencies, build tools, and process logs. Build provenance supports software supply chain integrity by allowing you to confirm that a given artifact was built from a known, unmodified source.

## C

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### C-CDA

**Consolidated Clinical Document Architecture.** A broad [HL7](#hl7) standard for structured clinical documents, including discharge summaries and referral notes. The [eICR](#eicr) format is a public health-specific implementation of C-CDA.

### case investigation

A case investigation records one instance of a disease or [condition](#condition) for a specific person, including clinical, epidemiological, and administrative data. Investigations may use the generic form (applicable to most conditions) or a condition-specific [PAM](#pam).

### case notification

A message sent from a [STLT](#stlt) to [CDC](#cdc) reporting a confirmed or probable case of a nationally [notifiable disease](#notifiable-disease). A case notification contains [case investigation](#case-investigation) data and associated [observations](#observation) and vaccinations.

### case surveillance

The collection, analysis, and reporting of data on individual disease cases. [NBS](#nbs) is a case surveillance system. Case surveillance differs from syndromic surveillance, which uses aggregate or pre-diagnostic data.

### CDA

**Clinical Document Architecture.** An [HL7](#hl7) standard for structuring clinical documents for exchange. [C-CDA](#c-cda) is a US-specific implementation of CDA; [eICR](#eicr) is a public health-specific implementation of C-CDA.

### CDC

**Centers for Disease Control and Prevention.** The federal agency that develops and maintains [NBS](#nbs). The NBS program is managed within the Office of Public Health Data, Surveillance, and Technology ([OPHDST](#ophdst)).

### CDF

**Commonly Defined Fields** (also: Collaboratively Defined Fields). Custom fields in NBS that are defined collaboratively across [jurisdictions](#jurisdiction), as distinct from [locally defined fields (LDFs)](#ldf). CDFs support import versioning.

### change data capture

A technique for tracking row-level changes in a database and streaming them to downstream systems in near real time.

### CIDR

**Classless Inter-Domain Routing.** A notation for specifying IP address ranges (for example, `10.0.0.0/16`).

### Classic NBS

Any [NBS](#nbs) versions prior to 7.0.0, including all NBS 6.x releases. Classic NBS is approaching end of support. [CDC](#cdc) is phasing out active development on NBS 6 so that resources can focus on [NBS 7](#nbs-7). STLTs still running Classic NBS should plan to migrate to [NBS 7](#nbs-7) or evaluate an alternative solution.

### CLI

**Command-Line Interface.** A text-based interface for running commands. System admins might use several CLI tools, such as the [AWS](#aws) CLI, [kubectl](#kubectl), and the [Terraform](#terraform) CLI.

### condition

A disease or health event that is subject to public health reporting. Conditions may be nationally [notifiable](#notifiable-disease) (reported to [CDC](#cdc)) or only jurisdiction-level [reportable](#reportable-disease).

### container

A lightweight, portable unit of software that packages an application and its dependencies so it runs consistently across environments.

### container image

A read-only template used to create containers.

### control plane

The component of a [Kubernetes](#kubernetes) cluster that manages cluster state, including scheduling workloads and maintaining desired configuration.

### CRD

**Custom Resource Definition.** A schema that defines validation rules for a new resource type within [Kubernetes](#kubernetes). You can use CRDs to extend the Kubernetes [API](#api) with custom resource types needed by its services.

## D

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### data ingestion pipeline

The [NBS 7](#nbs-7) services responsible for receiving, validating, and routing incoming public health data into NBS. Accepts data in [eICR](#eicr), [PHDC](#phdc), and [C-CDA](#c-cda) formats. The pipeline includes the [DI API](#di-api) as the entry point and integrations with [Elasticsearch](#elasticsearch) and the NBS operational database.

### Debezium

An open-source change data capture tool.

### DI API

**Data Integration API.** An NBS 7 service that provides an [API](#api) for external systems to push data into NBS.

### DIBBs

**Data Integration Building Blocks.** CDC open-source middleware for public health data integration.

### DNS

**Domain Name System.** The system that translates domain names (such as `app.example.com`) to IP addresses.

## E

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### eCR

**Electronic Case Reporting.** Automated reporting of disease cases from healthcare electronic health records ([EHRs](#ehr)) to public health agencies.

### Amazon EFS

**Amazon Elastic File System.** AWS-managed file storage. The [Azure](#azure) equivalent to EFS is [Azure Files](#azure-files).

### EHR

**Electronic Health Record.** A digital system used by clinical providers to record and manage patient health information. EHRs generate [eICR](#eicr) documents automatically when a reportable condition is diagnosed, enabling automated case reporting to public health agencies.

### eICR

**Electronic Initial Case Report.** A structured document automatically generated by an [EHR](#ehr) system when a clinician diagnoses a patient with a reportable condition. eICRs send relevant clinical data directly to public health agencies without manual data entry. eICR is the modern, preferred pathway for case reporting.

### Amazon EKS

**Amazon Elastic Kubernetes Service.** A managed Kubernetes service from AWS. Hosts containerized services in AWS deployments. In Azure deployments, [AKS](#azure-kubernetes-service) serves the same function.

### Elasticsearch

An open-source search and analytics engine.

### ELR

**Electronic Lab Report.** Lab results transmitted electronically from laboratories to public health departments.

### ETL

**Extract, Transform, Load.** A batch process that moves and transforms data from one system to another.

### ETOR

**Electronic Test Orders and Results.** A public health data exchange standard for transmitting laboratory test orders and results electronically. Related to [ELR](#elr) but covers the ordering side as well as results.

## F

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### FHIR

**Fast Healthcare Interoperability Resources.** A modern [HL7](#hl7) standard for healthcare data exchange using web APIs.

## G

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### GitOps

A practice of using Git repositories as the source of truth for infrastructure and application configuration.

## H

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### HDInsight

An Azure-managed Kafka service. Used for event streaming in Azure deployments. The AWS equivalent of HDInsight is [Amazon MSK](#amazon-msk).

### Helm

A package manager for [Kubernetes](#kubernetes).

### Helm chart

A collection of files that define a [Kubernetes](#kubernetes) application deployment, including configuration templates and default values.

### HIE / HIN

**Health Information Exchange / Health Information Network.** Organizations or networks that facilitate electronic sharing of health information across providers and public health agencies.

### HL7

**Health Level Seven.** A set of international standards for exchanging clinical and administrative health data.

## I

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### IaC

**Infrastructure as Code.** The practice of managing infrastructure through code (such as Terraform scripts) rather than manual configuration.

### IAM

**AWS Identity and Access Management.** The AWS service for controlling access to cloud resources. In Azure deployments, [Microsoft Entra ID](#microsoft-entra-id) and [Azure RBAC](#azure-rbac) serve the same function.

### IdP

**Identity Provider.** A system that manages user authentication and issues identity tokens.

### ingress controller

A [Kubernetes](#kubernetes) component that manages external access to services within a cluster, typically through HTTP/HTTPS routing rules.

### investigation

See [case investigation](#case-investigation). In NBS, "investigation" refers specifically to the record of a public health case investigation, not a general inquiry.

### IRD

**Investigate and Respond Division.** The CDC division within [OPHDST](#ophdst) where NBS is housed, within the [PHIT](#phit) branch.

## J

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### jurisdiction

The geographic or programmatic scope of authority for a health department unit.

## K

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### Kafka

**Apache Kafka.** An open-source distributed event streaming platform. Hosted on AWS as [Amazon MSK](#amazon-msk) or on Azure as [HDInsight](#hdinsight).

### Keycloak

An open-source identity and access management tool used for managing user authentication, [SSO](#sso), and token issuance.

### KMS

**AWS Key Management Service.** The AWS service for creating and managing encryption keys. Used to encrypt data at rest. In Azure deployments, [Azure Key Vault](#azure-key-vault) serves the same function.

### kubectl

The command-line tool for interacting with [Kubernetes](#kubernetes) clusters.

### Kubernetes

An open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.

## L

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### lab report

An observation originating from a laboratory, containing lab orders and results. Lab reports may arrive electronically as an [ELR](#elr) or be entered manually. In NBS, lab reports often trigger the creation of a [case investigation](#case-investigation).

### LDF

**Locally Defined Fields.** Custom fields added by an individual STLT within NBS to capture jurisdiction-specific data. LDFs are distinct from [CDFs](#cdf), which are shared across jurisdictions. Sysadmins configure LDFs during NBS setup and customization.

### LIMS / LIS

**Laboratory Information Management System / Laboratory Information System.** Software used by laboratories to manage samples, workflows, and results. STLTs and their reporting labs use LIMS/LIS systems as the source of [ELR](#elr) data.

### Linkerd

An open-source service mesh for [Kubernetes](#kubernetes).

### load balancer

A component that distributes incoming network traffic across multiple servers or services.

### LOINC

**Logical Observation Identifiers Names and Codes.** A standard code system that identifies what was measured in a lab test. Used in [ELR](#elr) processing and stored in the [SRTE](#srt--srte) database.

## M

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### managed node group

A group of [worker nodes](#worker-node) in AWS that share the same configuration, such as EC2 instance type and scaling settings. The equivalent concept in [AKS](#azure-kubernetes-service) is a [node pool](#node-pool).

### MasterETL

The [Classic NBS](#classic-nbs) batch process that extracts, transforms, and loads data from the NBS operational database ([ODSE](#ods--odse)) into the reporting database ([RDB](#rdb)). MasterETL coexists with the [RTR](#rtr) pipeline during the NBS 7 transition.

### microservice

A software architecture pattern in which an application is built as a collection of small, independently deployable services.

### Microsoft Azure

A public cloud platform. Often used with services such as [AKS](#azure-kubernetes-service), [HDInsight](#hdinsight), [Azure Files](#azure-files), [Azure SQL](#azure-sql), [Azure Blob Storage](#azure-blob-storage), [Azure Key Vault](#azure-key-vault), and [Azure Monitor](#azure-monitor). See also [AWS](#aws).

### Microsoft Entra ID

An Azure identity and access management service, formerly known as Azure Active Directory. In Azure deployments, Microsoft Entra ID handles identity and authentication functions similar to [AWS IAM](#iam), including user authentication and [RBAC](#rbac). Often used in conjunction with [Azure RBAC](#azure-rbac) for resource-level permissions.

### MMG

**Message Mapping Guide.** A CDC-published guide that defines the [HL7](#hl7) message structure for reporting a specific notifiable condition to CDC.

### morbidity report

An observation originating from a healthcare provider (such as a hospital or clinic), containing basic data about one instance of a disease. Morbidity reports typically arrive by paper or non-electronic means.

### MoU

**Memorandum of Understanding.** A formal agreement between parties. A STLT may be required to establish a MoU with new service providers.

### MPR / MPI

**Master Patient Record / Master Patient Index.**

- **MPR:** The authoritative patient record in NBS, derived from all patient revisions (point-in-time demographics).
- **MPI:** A cross-system index used to match and link patient records across sources.

### MS SQL

**Microsoft SQL Server.** The relational database used by [Classic NBS](#classic-nbs) (NBS 6.x). NBS 7 connects to the existing NBS 6 MS SQL database.

### MSGOUT / MSGOUTE

**Messaging Database (Enterprise).** The NBS staging database for inbound and outbound messaging. Stores electronic messages going into and out of NBS. Referenced in [data ingestion pipeline](#data-ingestion-pipeline) configuration.

### Amazon MSK

**Amazon Managed Streaming for Apache Kafka.** An AWS-managed version of [Kafka](#kafka), an open-source event streaming platform. In Azure deployments, [HDInsight](#hdinsight) serves the same function.

## N

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### namespace (Kubernetes)

A logical partition within a [Kubernetes](#kubernetes) cluster used to isolate resources. NBS 7 services are deployed into specific namespaces.

### NBS

**National Electronic Disease Surveillance System Base System.** A CDC-developed software system for public health surveillance. Helps STLTs collect, manage, and share reportable and notifiable disease data. Available as [Classic NBS](#classic-nbs) (NBS 6.x) and the modernized [NBS 7](#nbs-7) (the subject of this guide).

### NBS 6

See [Classic NBS](#classic-nbs).

### NBS 7

The modernized version of [NBS](#nbs), built as a containerized [microservices](#microservice) platform deployed on cloud infrastructure. NBS 7 incrementally replaces [Classic NBS](#classic-nbs) using the [strangler fig pattern](#strangler-fig-pattern), allowing STLTs to transition to the modernized system without disrupting active surveillance operations. NBS 7 is the subject of this guide.

### NBS Central

A web-based portal providing helpdesk ticketing, collaboration forums, documentation, and a wiki for the NBS community. NBS Central is a support resource, not a deployable component. Access to NBS Central requires a login. To register for an account, navigate to [NBS Central](https://nbscentral.cdc.gov) and choose **Register** at the top of the login screen.

### NEDSS

**National Electronic Disease Surveillance System.** The federal initiative that establishes standards for electronic disease surveillance. [NBS](#nbs) is the base system implementation of NEDSS.

### NETSS

**National Electronic Telecommunications System for Surveillance.** A legacy data exchange format for transmitting surveillance data to [CDC](#cdc). NETSS is being phased out in favor of more current standards.

### NiFi

<!-- This is true as of May 2026, but is being phased out -->

**Apache NiFi.** An open-source data flow automation tool.

### NIST 800-53

**National Institute of Standards and Technology Special Publication 800-53 (Rev. 5).** A risk-based framework providing a catalog of security and privacy controls for federal information systems.

### NND

**National Notifiable Disease.** A disease or condition that jurisdictions are required by federal policy to report to CDC. CDC maintains the national list; STLTs may also designate additional jurisdiction-level reportable conditions.

### NNDSS

**National Notifiable Diseases Surveillance System.** The CDC system that receives [case notification](#case-notification) data from STLTs.

### node

See [worker node](#worker-node).

### node pool

A group of [worker nodes](#worker-node) in Azure that share the same configuration, such as virtual machine size and operating system. The equivalent concept in [Amazon EKS](#amazon-eks) is a [managed node group](#managed-node-group).

### notifiable disease

A disease or condition that providers and laboratories are legally required to report to public health authorities. CDC maintains the national list. See also [reportable disease](#reportable-disease).

## O

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### observation

In NBS, a report received by a health department from an external source (such as a lab or provider). Observations include [lab reports](#lab-report) and [morbidity reports](#morbidity-report). They may trigger [case investigations](#case-investigation) or be associated with existing ones.

### ODS / ODSE

**Operational Data Store (Enterprise).** The NBS primary transactional database. Stores real-time case and investigation data. The "E" suffix reflects the current design iteration of the database schema.

### on-premises

Infrastructure that is hosted and managed at a physical location controlled by the organization, rather than in a cloud environment. Hyphenated when used as an adjective.

### OPHDST

**Office of Public Health Data, Surveillance, and Technology.** The CDC office that oversees NBS development and houses the [IRD](#ird) division.

## P

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### Page Builder

An NBS feature that allows administrators to build configurable forms for collecting, analyzing, and sending notifications for disease and condition data.

### PAM

**Program Area Module.** An NBS extension that adds disease-specific data collection fields and workflows beyond the base system. Examples include PAMs for Hepatitis, STD/HIV, and Vaccine-Preventable Diseases.

### peering

A network connection between two [Amazon VPCs](#amazon-vpc) or [VNets](#azure-vnet), or between one and an on-premises network, that allows resources in each to communicate as if on the same network. In [Amazon VPC](#amazon-vpc), this is called VPC peering. In [Azure](#azure), the equivalent is [VNet](#azure-vnet) peering.

### permission set

In NBS, a collection of objects and operations a user is authorized to access. A permission set is combined with [program area](#program-area), [jurisdiction](#jurisdiction), and access level to define a user's [role](#role-nbs).

### PHCR

**Public Health Case Report.** An XML format used to import case data into NBS from legacy or external systems.

### PHDC

**Public Health Document Container.** An XML document format used for structured case data exchange.

### PHI

**Protected Health Information.** Health data protected under HIPAA.

### PHIN

<!-- FYI that PHIN will sunset in November 2026 -->

**Public Health Information Network.** A CDC initiative establishing standards and tools for public health information exchange. The parent initiative for [PHIN VADS](#phin-vads) and historically for [PHINMS](#phinms).

### PHIN VADS

**Public Health Information Network Vocabulary Access and Distribution System.** A CDC-hosted repository of standardized vocabulary and code sets used in public health messaging.

### PHINMS

**Public Health Information Network Messaging System.** A legacy [CDC](#cdc) messaging system for transmitting surveillance data. Being replaced by current standards.

### PHIT

**Public Health Investigation Tools.** The CDC branch within [IRD](#ird) that directly manages [NBS](#nbs).

### PII

**Personally Identifiable Information.** Data that can be used to identify, locate, or contact an individual.

### pod

The smallest deployable unit in [Kubernetes](#kubernetes). A pod contains one or more containers that share network and storage resources.

### program area

At CDC, a category that groups related diseases or conditions for administrative and security purposes (for example, STD/HIV or Hepatitis). Users are assigned to program areas as part of their [role](#role-nbs).

## R

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### RBAC

**Role-Based Access Control.** An access management principle that restricts resource access based on a user's job role rather than individual identity.

### RDB

**Reporting Database.** The NBS database that stores flattened data for reporting and analysis. Populated by [MasterETL](#masteretl) (legacy path) or [RTR](#rtr) (modern path). See also [RDB_Modern](#rdb_modern).

### RDB_Modern

The modernized reporting database in NBS 7, populated by the [RTR](#rtr) pipeline. RDB_Modern runs alongside the legacy [RDB](#rdb) during the migration period.

### Amazon RDS

**Amazon Relational Database Service.** An AWS managed database service. [Azure SQL](#azure-sql) services are the Azure equivalent of Amazon RDS.

<!-- **Work on patient matching is unfinished, and unclear when it will be picked up.**
### Record Linker

A CDC open-source tool, part of [DIBBs](#dibbs), for matching and linking patient records across systems.
-->

### Reportability Response

**Reportability Response (RR).** A structured message returned to an originating [EHR](#ehr) system after an [eICR](#eicr) is received and processed. The RR confirms whether the reported condition is reportable and to which jurisdiction. The RR is part of the eICR two-way exchange workflow and is generated by NBS after the [DI API](#di-api) forwards the eICR.

### reportable disease

A disease or condition that providers are required to report to the local or state health department under jurisdiction law. Distinct from [notifiable disease](#notifiable-disease), which refers to federal reporting requirements to CDC.

### role (NBS)

In NBS, the combination of a [permission set](#permission-set), [program area](#program-area) or areas, [jurisdiction](#jurisdiction) or jurisdictions, and access level assigned to a user. A user may have multiple roles.

### RR

See [Reportability Response](#reportability-response).

### RTR

**Real-Time Reporting.** An NBS 7 reporting pipeline that replaces the batch [ETL](#etl) approach with event-driven data movement using [Kafka](#kafka). RTR coexists with [MasterETL](#masteretl) during the NBS 7 migration period.

### RxNorm

A standard code system for medications.

## S

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### Amazon S3

**Amazon Simple Storage Service.** AWS object storage. In Azure deployments, [Azure Blob Storage](#azure-blob-storage) serves the same function.

### SAML

**Security Assertion Markup Language.** A standard for exchanging authentication and authorization data. Used for [SSO](#sso) integrations with [Keycloak](#keycloak).

### SAS

**Statistical Analysis System.** Analytics software used with [Classic NBS](#classic-nbs) for reporting. Referenced in NBS 6 compatibility documentation.

### SBOM

**Software Bill of Materials.** A formal, machine-readable inventory of the software components, dependencies, and libraries used to build an application. SBOMs identify vulnerable or outdated components in a software supply chain.

### service mesh

An infrastructure layer that manages service-to-service communication within a distributed application, providing encryption, observability, and traffic management.

### SLA

**Service Level Agreement.** A contract defining service performance expectations. A STLT may be required to establish an SLA with a new service provider (for example, a cloud service provider).

### SNOMED CT

**Systematized Nomenclature of Medicine - Clinical Terms.** A standard code system identifying clinical findings and organisms.

### SQL

**Structured Query Language.** A standard language for managing and querying relational databases.

### SRT / SRTE

**System Reference Tables (Enterprise).** The NBS database that stores standard code sets including [LOINC](#loinc), [SNOMED CT](#snomed-ct), [RxNorm](#rxnorm), and FIPS codes. Used for code mapping during [ELR](#elr) processing and [jurisdiction](#jurisdiction) derivation.

### SSO

**Single Sign-On.** An authentication method that allows users to log in once to access multiple systems.

### STLT

**State, Territorial, Local, and Tribal.** The jurisdictions that operate NBS day-to-day. STLTs are the primary audience for this guide. Pronounced "stilt."

### strangler fig pattern

A software migration strategy in which new functionality is built alongside a legacy system and gradually replaces it, rather than rewriting everything at once.

### subnet

A subdivision of a [VPC's](#amazon-vpc) IP address range. Subnets are used to isolate internet-facing components from internal services.

## T

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### Terraform

An open-source infrastructure-as-code tool for provisioning and managing cloud resources. In AWS deployments, the scripts provision resources including [Amazon EKS](#amazon-eks), [Amazon VPC](#amazon-vpc), [Amazon MSK](#amazon-msk), and [Amazon EFS](#amazon-efs). In Azure deployments, the scripts provision resources including [AKS](#azure-kubernetes-service), [VNet](#azure-vnet), [HDInsight](#hdinsight), and [Azure Files](#azure-files).

### TLS

**Transport Layer Security.** A cryptographic protocol that secures data in transit.

### Traefik

An open-source [ingress controller](#ingress-controller) and reverse proxy.

### transfer of ownership

The act of reassigning an [observation](#observation) or [case investigation](#case-investigation) from one [jurisdiction](#jurisdiction) or [program area](#program-area) to another. The receiving owner becomes responsible for investigation and resolution tasks.

## V

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### values file (Helm)

A YAML configuration file that supplies environment-specific settings to a [Helm chart](#helm-chart) during deployment.

### Azure VNet

**Azsure Virtual Network.** An isolated cloud network in [Azure](#azure). The AWS equivalent of VNet is [Amazon VPC](#amazon-vpc).

### Amazon VPC

**Amazon Virtual Private Cloud.** An isolated cloud network in AWS. The AWS equivalent of [VNet](#azure-vnet). See also [peering](#peering) and [subnet](#subnet).

## W

---

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

### WDS

**Workflow Decision Support.** An NBS application feature that automates processing of incoming [ELR](#elr) and [eCR](#ecr) data. For example, automatically creating [case investigations](#case-investigation) or marking documents as reviewed. System administrators configure the [permission sets](#permission-set) and security derivation that WDS depends on; changes to WDS behavior in the `NBS_Configuration` table require a [WildFly](#wildfly) restart.

### WildFly

An open-source Java application server used as a runtime environment.

### worker node

A physical or virtual machine in a [Kubernetes](#kubernetes) cluster that runs containerized workloads ([pods](#pod)). Worker nodes are managed by you; the [control plane](#control-plane) schedules work onto them and monitors their health. In [Amazon EKS](#amazon-eks) deployments, worker nodes run as EC2 instances provisioned through [managed node groups](#managed-node-group). In [AKS](#azure-kubernetes-service) deployments, they are provisioned as [node pools](#node-pool).
