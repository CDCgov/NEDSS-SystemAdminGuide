---
title: Glossary
layout: page
nav_order: 5
description: "Definitions for terms and acronyms used in the NBS 7 System Administrator Guide."
last_modified_date: 2026-05-12
---

# Glossary
{: .no_toc }

Definitions for terms and acronyms used in this guide. Terms with NBS-specific meanings are defined in that context. General infrastructure terms are defined as they apply to NBS 7 deployments.

<!--
  CONTRIBUTOR GUIDANCE — this comment block is stripped from the rendered output.

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
-->

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

## A

### AIMS

**APHL Informatics Messaging System.** A platform managed by the Association of Public Health Laboratories (APHL) for public health data exchange and messaging. Some STLTs use AIMS to transmit electronic lab reports (ELRs) or case notification data to CDC.

### AKS

**Azure Kubernetes Service.** Azure's managed Kubernetes service. Hosts NBS 7 containerized services in Azure deployments. The Azure equivalent of [Amazon EKS](#amazon-eks).

### AMG

**Amazon Managed Grafana.** An AWS-managed version of Grafana, an open-source dashboarding platform. Visualizes metrics collected by [Amazon Managed Service for Prometheus](#amp). Used to monitor NBS 7 infrastructure. In Azure deployments, [Azure Monitor](#azure-monitor) covers this function.

### AMP

**Amazon Managed Service for Prometheus.** An AWS-managed version of Prometheus, an open-source monitoring and alerting toolkit. Collects infrastructure metrics from NBS 7 components. Metrics are visualized in [Amazon Managed Grafana](#amg). In Azure deployments, [Azure Monitor](#azure-monitor) covers this function.

### API

**Application Programming Interface.** A defined interface that allows software systems to communicate. NBS 7 exposes APIs for patient data, investigations, and external data integrations.

### ArgoCD

An open-source GitOps tool for deploying and managing Kubernetes applications. ArgoCD implements the [GitOps](#gitops) pattern for NBS 7 deployments by syncing the cluster state to configuration defined in the [NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm) repository.

### AVR

**Analysis, Visualization, and Reporting.** An umbrella term for the reporting and analytics capabilities of NBS and related public health systems. May appear in documentation describing [RTR](#rtr) and reporting service functionality.

### AWS

**Amazon Web Services.** A public cloud platform that STLTs might choose to host their NBS 7 deployment. STLTs that use AWS often engage with services such as [Amazon EKS](#amazon-eks), [Amazon MSK](#amazon-msk), [Amazon EFS](#amazon-efs), [Amazon RDS](#amazon-rds), [Amazon S3](#amazon-s3), [AWS KMS](#kms), [Amazon Managed Service for Prometheus](#amp), and [Amazon Managed Grafana](#amg). See also [Microsoft Azure](#microsoft-azure).

### Azure

See [Microsoft Azure](#microsoft-azure).

### Azure Blob Storage

Azure object storage. Used for Terraform state files and NBS 7 logs in Azure deployments. The Azure equivalent of [Amazon S3](#amazon-s3).

### Azure Key Vault

An Azure service for creating and managing encryption keys, certificates, and application and database secrets. Used to protect sensitive configuration values in Azure NBS 7 deployments. The Azure equivalent of [AWS KMS](#kms).

### Azure Files

An Azure-managed file storage service. In Azure NBS 7 deployments, Azure Files and Azure NetApp Files are common options for the persistent file storage that [Amazon EFS](#amazon-efs) provides in AWS deployments. The appropriate service depends on the STLT's performance requirements and existing infrastructure.

### Azure Monitor

An Azure platform service for monitoring infrastructure health and performance. In Azure NBS 7 deployments, Azure Monitor covers the observability functions that [Amazon Managed Service for Prometheus](#amp) and [Amazon Managed Grafana](#amg) provide in AWS deployments — metrics collection and dashboard visualization. Azure Monitor includes Azure-managed Grafana as an optional dashboarding component. STLTs might use Azure Monitor alone or in combination with other observability tools.

### Azure RBAC

**Azure Role-Based Access Control.** The Azure service for managing access to cloud resources. In Azure NBS 7 deployments, Azure RBAC controls resource-level permissions in the same way that [AWS IAM](#iam) does in AWS deployments. Often used in conjunction with [Microsoft Entra ID](#microsoft-entra-id) for identity management.

### Azure SQL

A family of Azure-managed database services. In Azure NBS 7 deployments, Azure SQL Database or Azure Database for SQL Server are common options for hosting the NBS 6 database. The appropriate service depends on the STLT's existing infrastructure and licensing. The Azure equivalent of [Amazon RDS](#amazon-rds) in this context.

---

## B

### build provenance

Verifiable, tamper-proof metadata documenting how a software artifact was created, including source code location, dependencies, build tools, and process logs. Build provenance supports software supply chain integrity by allowing you to confirm that a given artifact was built from a known, unmodified source.

---

## C

### C-CDA

**Consolidated Clinical Document Architecture.** A broad [HL7](#hl7) standard for structured clinical documents, including discharge summaries and referral notes. The [eICR](#eicr) format is a public health-specific implementation of C-CDA. NBS can ingest general C-CDA documents when they carry clinical data relevant to surveillance.

### case investigation

The primary workflow unit in NBS. A case investigation records one instance of a disease or condition for a specific person, including clinical, epidemiological, and administrative data. Investigations may use the generic form (applicable to most conditions) or a condition-specific [PAM](#pam).

### case notification

A message sent from a STLT to CDC reporting a confirmed or probable case of a nationally notifiable disease. A case notification contains investigation data and associated observations and vaccinations.

### case surveillance

The collection, analysis, and reporting of data on individual disease cases. NBS is a case surveillance system. Case surveillance differs from syndromic surveillance, which uses aggregate or pre-diagnostic data.

### CDA

**Clinical Document Architecture.** An [HL7](#hl7) standard for structuring clinical documents for exchange. Used in the NBS 7 [data ingestion pipeline](#data-ingestion-pipeline): the `phdc-xsd-jaxb` library maps CDA/PHDC XML documents into NBS data structures. [C-CDA](#c-cda) is a US-specific implementation of CDA; [eICR](#eicr) is a public health-specific implementation of C-CDA.

### CDF

**Commonly Defined Fields** (also: Collaboratively Defined Fields). Custom fields in NBS that are defined collaboratively across jurisdictions, as distinct from [locally defined fields (LDFs)](#ldf). CDFs support import versioning.

### CDC

**Centers for Disease Control and Prevention.** The federal agency that develops and maintains NBS. The NBS program is managed within the Office of Public Health Data, Surveillance, and Technology [OPHDST](#ophdst).

### change data capture

A technique for tracking row-level changes in a database and streaming them to downstream systems in near real time. [Debezium](#debezium) performs change data capture in the NBS 7 [RTR](#rtr) pipeline.

### CIDR

**Classless Inter-Domain Routing.** A notation for specifying IP address ranges (for example, `10.0.0.0/16`). Used when configuring [Amazon VPC](#amazon-vpc) network settings and security group rules in NBS 7 infrastructure.

### Classic NBS

Any [NBS](#nbs) versions prior to 7.0.0, including all NBS 6.x releases. Classic NBS is approaching end of support. CDC has ceased active development on NBS 6 so that resources can focus on [NBS 7](#nbs-7). STLTs still running Classic NBS should plan to migrate to [NBS 7](#nbs-7) or evaluate an alternative solution.

### CLI

**Command-Line Interface.** A text-based interface for running commands. NBS 7 sysadmins use several CLI tools, including the AWS CLI, [kubectl](#kubectl), and the Terraform CLI.

### condition

In NBS, a disease or health event that is subject to public health reporting. Conditions may be nationally notifiable (reported to CDC) or only jurisdiction-level reportable. Not all conditions have a [PAM](#pam); some use the generic investigation form.

### container

A lightweight, portable unit of software that packages an application and its dependencies so it runs consistently across environments. NBS 7 services are deployed as containers orchestrated by [Kubernetes](#kubernetes).

### container image

A read-only template used to create containers. NBS 7 container images are hosted on `quay.io` and pulled during deployment.

### control plane

The component of a Kubernetes cluster that manages cluster state, including scheduling workloads and maintaining desired configuration. In [Amazon EKS](#amazon-eks), AWS manages the control plane.

### CRD

**Custom Resource Definition.** A schema that defines validation rules for a new resource type within Kubernetes. NBS 7 uses CRDs to extend the Kubernetes API with custom resource types needed by its services.

---

## D

### [data ingestion pipeline](#data-ingestion-pipeline)

The [NBS 7](#nbs-7) services responsible for receiving, validating, and routing incoming public health data into NBS. Accepts data in [eICR](#eicr), [PHDC](#phdc), and [C-CDA](#c-cda) formats. The pipeline includes the [DI API](#di-api) as the entry point and integrations with [Elasticsearch](#elasticsearch) and the NBS operational database. 

### Debezium

An open-source change data capture tool. Debezium monitors the NBS database for row-level changes and streams them to [Kafka](#kafka) as part of the [RTR](#rtr) pipeline.

### DI API

**Data Integration API.** An NBS 7 service that provides an API for external systems to push data into NBS. Requires separate deployment and configuration.

### DIBBs

**Data Integration Building Blocks.** CDC open-source middleware for public health data integration. <!-- Includes tools such as [Record Linker](#record-linker) for patient matching. -->

### DNS

**Domain Name System.** The system that translates domain names (such as `app.example.com`) to IP addresses. DNS routing must be configured as part of NBS 7 deployment to direct traffic to the Kubernetes ingress controller.

---

## E

### eCR

**Electronic Case Reporting.** Automated reporting of disease cases from healthcare electronic health records (EHRs) to public health agencies. Some STLTs ingest eCR data into NBS.

### Amazon EFS

**Amazon Elastic File System.** AWS-managed file storage. Used by NBS 7 for persistent data, including [Elasticsearch](#elasticsearch) indices. In Azure deployments, [Azure Files](#azure-files) serves the same function.

### EHR

**Electronic Health Record.** A digital system used by clinical providers to record and manage patient health information. EHRs generate [eICR](#eicr) documents automatically when a reportable condition is diagnosed, enabling automated case reporting to public health agencies.

### eICR

**Electronic Initial Case Report.** A structured document automatically generated by an [EHR](#ehr) system when a clinician diagnoses a patient with a reportable condition. eICRs send relevant clinical data directly to public health agencies without manual data entry. eICR is the modern, preferred pathway for case reporting and the primary format the [DI API](#di-api) is designed to receive. After the DI API forwards an eICR to NBS, NBS returns a [Reportability Response](#reportability-response) to the originating EHR.

### Amazon EKS

**Amazon Elastic Kubernetes Service.** AWS's managed Kubernetes service. Hosts NBS 7 containerized services in AWS deployments. In Azure deployments, [AKS](#aks) serves the same function.

### ELR

**Electronic Lab Report.** Lab results transmitted electronically from laboratories to public health departments. NBS ingests ELRs via [HL7](#hl7) messaging. ELRs often trigger the creation of a [case investigation](#case-investigation).

### Elasticsearch

An open-source search and analytics engine. Used in NBS 7 to power fast patient and event search. Elasticsearch indices are populated from the NBS database by [NiFi](#nifi).

> Elasticsearch version upgrades (for example, from version 7 to 8) involve schema changes. See the upgrade documentation before performing a version upgrade.
{: .note }

### ETL

**Extract, Transform, Load.** A batch process that moves and transforms data from one system to another. In NBS, the [MasterETL](#masteretl) batch job uses ETL to populate the [RDB](#rdb) from the NBS operational database. The [RTR](#rtr) pipeline replaces this batch approach with event-driven data movement during the NBS 7 transition.

### ETOR

**Electronic Test Orders and Results.** A public health data exchange standard for transmitting laboratory test orders and results electronically. Related to [ELR](#elr) but covers the ordering side as well as results.

---

## F

### FHIR

**Fast Healthcare Interoperability Resources.** A modern [HL7](#hl7) standard for healthcare data exchange using web APIs.

---

## G

### GitOps

A practice of using Git repositories as the source of truth for infrastructure and application configuration. [ArgoCD](#argocd) implements GitOps for NBS 7 Kubernetes deployments by applying changes defined in the NEDSS-Helm repository to the cluster.

---

## H

### HDInsight

An Azure-managed Kafka service. Used by the NBS 7 [RTR](#rtr) pipeline and [data ingestion](#data-ingestion-pipeline) services for event streaming in Azure deployments. The Azure equivalent of [Amazon MSK](#amazon-msk).

### Helm

A package manager for Kubernetes. NBS 7 uses Helm charts defined in the [NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm) repository to deploy and configure microservices.

### Helm chart

A collection of files that define a Kubernetes application deployment, including configuration templates and default values. Each NBS 7 microservice has a corresponding Helm chart in the NEDSS-Helm repository.

### HIE / HIN

**Health Information Exchange / Health Information Network.** Organizations or networks that facilitate electronic sharing of health information across providers and public health agencies. Some STLTs integrate NBS with a regional HIE.

### HL7

**Health Level Seven.** A set of international standards for exchanging clinical and administrative health data. NBS uses HL7 messaging, including version 2 (v2) and [CDA](#cda), for [ELR](#elr) ingestion and case notifications to CDC.

---

## I

### IaC

**Infrastructure as Code.** The practice of managing infrastructure through code (such as Terraform scripts) rather than manual configuration. NBS 7 uses IaC through [Terraform](#terraform) scripts in the NEDSS-Infrastructure repository.

### IAM

**AWS Identity and Access Management.** The AWS service for controlling access to cloud resources. Used to define roles and permissions for Terraform provisioning and Kubernetes operations in NBS 7 deployments. In Azure deployments, [Microsoft Entra ID](#microsoft-entra-id) and [Azure RBAC](#azure-rbac) serve the same function.

### IdP

**Identity Provider.** A system that manages user authentication and issues identity tokens. [Keycloak](#keycloak) serves as the IdP for NBS 7.

### ingress controller

A Kubernetes component that manages external access to services within a cluster, typically through HTTP/HTTPS routing rules. NBS 7.12 and higher use [Traefik](#traefik) as the ingress controller, with earlier 7.x releases using NGINX.

### investigation

See [case investigation](#case-investigation). In NBS, "investigation" refers specifically to the record of a public health case investigation, not a general inquiry.

### IRD

**Investigate and Respond Division.** The CDC division within [OPHDST](#ophdst) where NBS is housed, within the [PHIT](#phit) branch.

---

## J

### jurisdiction

The geographic or programmatic scope of authority for a health department unit. In NBS, jurisdiction controls which records a user can view and act on. A user's [role](#role-nbs) includes their assigned jurisdiction or jurisdictions.

---

## K

### Kafka

**Apache Kafka.** An open-source distributed event streaming platform. Used by NBS 7's [RTR](#rtr) pipeline and [data ingestion](#data-ingestion-pipeline) services to move data between microservices in near real time. Hosted on AWS as [Amazon MSK](#amazon-msk) or on Azure as [HDInsight](#hdinsight).

### Keycloak

An open-source identity and access management tool. Serves as the primary [IdP](#idp) for NBS 7, managing user authentication, [SSO](#sso), and token issuance.

### KMS

**AWS Key Management Service.** The AWS service for creating and managing encryption keys. Used to encrypt NBS 7 data at rest. In Azure deployments, [Azure Key Vault](#azure-key-vault) serves the same function.

### kubectl

The command-line tool for interacting with Kubernetes clusters. NBS 7 sysadmins use `kubectl` to inspect cluster state, manage pods, and run administrative commands.

### Kubernetes

An open-source container orchestration platform that automates deployment, scaling, and management of containerized applications. NBS 7 runs on Kubernetes, managed through [Amazon EKS](#amazon-eks) on AWS or [AKS](#aks) on Azure.

---

## L

### lab report

In NBS, an observation originating from a laboratory, containing lab orders and results. Lab reports may arrive electronically as an [ELR](#elr) or be entered manually. Lab reports often trigger the creation of a [case investigation](#case-investigation).

### LDF

**Locally Defined Fields.** Custom fields added by an individual STLT within NBS to capture jurisdiction-specific data. LDFs are distinct from [CDFs](#cdf), which are shared across jurisdictions. Sysadmins configure LDFs during NBS setup and customization.

### LIMS / LIS

**Laboratory Information Management System / Laboratory Information System.** Software used by laboratories to manage samples, workflows, and results. STLTs and their reporting labs use LIMS/LIS systems as the source of [ELR](#elr) data transmitted to NBS.

### Linkerd

An open-source service mesh for Kubernetes. Used in NBS 7 to manage encrypted communication between microservices within the cluster.

### load balancer

A component that distributes incoming network traffic across multiple servers or services. NBS 7 uses load balancers to route traffic to the Kubernetes [ingress controller](#ingress-controller).

### LOINC

**Logical Observation Identifiers Names and Codes.** A standard code system that identifies what was measured in a lab test. Used in [ELR](#elr) processing and stored in the NBS [SRTE](#srt--srte) database.

---

## M

### MasterETL

The [Classic NBS](#classic-nbs) batch process that extracts, transforms, and loads data from the NBS operational database ([ODSE](#ods--odse)) into the reporting database ([RDB](#rdb)). MasterETL coexists with the [RTR](#rtr) pipeline during the NBS 7 transition.

### Microsoft Azure

A public cloud platform that STLTs might choose to host their NBS 7 deployment. STLTs that use Azure often engage with services such as [AKS](#aks), [HDInsight](#hdinsight), [Azure Files](#azure-files), [Azure SQL](#azure-sql), [Azure Blob Storage](#azure-blob-storage), [Azure Key Vault](#azure-key-vault), and [Azure Monitor](#azure-monitor). See also [AWS](#aws).

### microservice

A software architecture pattern in which an application is built as a collection of small, independently deployable services. NBS 7 is built as a set of microservices, each responsible for a specific function.

### MMG

**Message Mapping Guide.** A CDC-published guide that defines the HL7 message structure for reporting a specific notifiable condition to CDC. STLTs and NBS use MMGs to ensure case notifications conform to required formats.

### MoU

**Memorandum of Understanding.** A formal agreement between parties. A STLT may be required to establish a MoU with its cloud service provider before deploying NBS 7.

### Microsoft Entra ID

An Azure identity and access management service, formerly known as Azure Active Directory. In Azure NBS 7 deployments, Microsoft Entra ID handles identity and authentication functions similar to [AWS IAM](#iam), including user authentication and role-based access control. Often used in conjunction with [Azure RBAC](#azure-rbac) for resource-level permissions.

### morbidity report

In NBS, an observation originating from a healthcare provider (such as a hospital or clinic), containing basic data about one instance of a disease. Morbidity reports typically arrive by paper or non-electronic means.

### MPR / MPI

**Master Patient Record / Master Patient Index.**

- **MPR:** The authoritative patient record in NBS, derived from all patient revisions (point-in-time demographics).
- **MPI:** A cross-system index used to match and link patient records across sources.

### MS SQL

**Microsoft SQL Server.** The relational database used by [Classic NBS](#classic-nbs) (NBS 6.x). NBS 7 connects to the existing NBS 6 MS SQL database.

### MSGOUT / MSGOUTE

**Messaging Database (Enterprise).** The NBS staging database for inbound and outbound messaging. Stores electronic messages going into and out of NBS. Referenced in [data ingestion pipeline](#data-ingestion-pipeline) configuration.

### Amazon MSK

**Amazon Managed Streaming for Apache Kafka.** An AWS-managed version of [Kafka](#kafka), an open-source event streaming platform. Used by the NBS 7 [RTR](#rtr) pipeline and [data ingestion](#data-ingestion-pipeline) services for event streaming. In Azure deployments, [HDInsight](#hdinsight) serves the same function.

---

## N

### namespace (Kubernetes)

A logical partition within a Kubernetes cluster used to isolate resources. NBS 7 services are deployed into specific namespaces.

### NIST 800-53

**National Institute of Standards and Technology Special Publication 800-53 (Rev. 5).** A risk-based framework providing a catalog of security and privacy controls for federal information systems. STLTs deploying NBS 7 on cloud infrastructure may be required to demonstrate compliance with a NIST 800-53 control baseline as part of their agency's security authorization process.

### NBS

**National Electronic Disease Surveillance System Base System.** A CDC-developed software system for public health surveillance. Helps STLTs collect, manage, and share reportable and notifiable disease data. Available as [Classic NBS](#classic-nbs) (NBS 6.x) and the modernized [NBS 7](#nbs-7) (the subject of this guide).

### NBS 6

See [Classic NBS](#classic-nbs).

### NBS 7

The modernized version of [NBS](#nbs), built as a containerized microservices platform deployed on cloud infrastructure. NBS 7 incrementally replaces [Classic NBS](#classic-nbs) using the [strangler fig pattern](#strangler-fig-pattern), allowing STLTs to transition to the modernized system without disrupting active surveillance operations. NBS 7 is the subject of this guide.

### NBS Central

A web-based portal providing helpdesk ticketing, collaboration forums, documentation, and a wiki for the NBS community. NBS Central is a support resource, not a deployable component. Access to NBS Central requires a login. To register for an account, navigate to [NBS Central](https://nbscentral.cdc.gov) and choose **Register** at the top of the login screen.

### NEDSS

**National Electronic Disease Surveillance System.** The federal initiative that establishes standards for electronic disease surveillance. NBS is the base system implementation of NEDSS.

### NETSS

**National Electronic Telecommunications System for Surveillance.** A legacy data exchange format for transmitting surveillance data to CDC. NETSS is being phased out in favor of more current standards.

### NiFi

<!-- This is true as of May 2026, but is being phased out -->

**Apache NiFi.** An open-source data flow automation tool. Used in NBS 7 to populate [Elasticsearch](#elasticsearch) indices from the NBS database.

### NND

**National Notifiable Disease.** A disease or condition that jurisdictions are required by federal policy to report to CDC. CDC maintains the national list; STLTs may also designate additional jurisdiction-level reportable conditions.

### NNDSS

**National Notifiable Diseases Surveillance System.** The CDC system that receives case notification data from STLTs.

### node

A physical or virtual machine in a Kubernetes cluster that runs containerized workloads ([pods](#pod)).

### notifiable disease

A disease or condition that providers and laboratories are legally required to report to public health authorities. CDC maintains the national list. See also [reportable disease](#reportable-disease).

---

## O

### observation

In NBS, a report received by a health department from an external source (such as a lab or provider). Observations include [lab reports](#lab-report) and [morbidity reports](#morbidity-report). They may trigger [case investigations](#case-investigation) or be associated with existing ones.

### ODS / ODSE

**Operational Data Store (Enterprise).** The NBS primary transactional database. Stores real-time case and investigation data. The "E" suffix reflects the current design iteration of the database schema.

### on-premises

Infrastructure that is hosted and managed at a physical location controlled by the organization, rather than in a cloud environment. [Classic NBS](#classic-nbs) is commonly deployed on-premises. Hyphenated when used as an adjective.

### OPHDST

**Office of Public Health Data, Surveillance, and Technology.** The CDC office that oversees NBS development and houses the [IRD](#ird) division.

---

## P

### Page Builder

An NBS feature that allows administrators to build configurable forms for collecting, analyzing, and sending notifications for disease and condition data.

### PAM

**Program Area Module.** An NBS extension that adds disease-specific data collection fields and workflows beyond the base system. Examples include PAMs for Hepatitis, STD/HIV, and Vaccine-Preventable Diseases.

### peering

A network connection between two VPCs, or between a VPC and an on-premises network, that allows resources in each to communicate as if on the same network. Used in NBS 7 deployments to connect the modern VPC to the [Classic NBS](#classic-nbs) environment.

### permission set

In NBS, a collection of objects and operations a user is authorized to access. A permission set is combined with program area, jurisdiction, and access level to define a user's [role](#role-nbs).

### PHCR

**Public Health Case Report.** An XML format used to import case data into NBS from legacy or external systems.

### PHDC

**Public Health Document Container.** An XML document format used in NBS for structured case data exchange.

### PHI

**Protected Health Information.** Health data protected under HIPAA. NBS databases contain PHI; access and data handling must comply with applicable regulations.

### PHIN

<!-- FYI that PHIN will sunset in November 2026 -->

**Public Health Information Network.** A CDC initiative establishing standards and tools for public health information exchange. The parent initiative for [PHIN VADS](#phin-vads) and historically for [PHINMS](#phinms).

### PHIN VADS

**Public Health Information Network Vocabulary Access and Distribution System.** A CDC-hosted repository of standardized vocabulary and code sets used in public health messaging. STLTs use PHIN VADS to access and validate code sets for NBS configuration.

### PHINMS

**Public Health Information Network Messaging System.** A legacy CDC messaging system for transmitting surveillance data. Being replaced by current standards.

### PHIT

**Public Health Investigation Tools.** The CDC branch within [IRD](#ird) that directly manages NBS.

### PII

**Personally Identifiable Information.** Data that can identify an individual. NBS databases contain PII; access and data handling must comply with applicable regulations.

### pod

The smallest deployable unit in Kubernetes. A pod contains one or more containers that share network and storage resources. Each NBS 7 microservice runs as one or more pods.

### program area

In NBS, a category that groups related diseases or conditions for administrative and security purposes (for example, STD/HIV or Hepatitis). Users are assigned to program areas as part of their [role](#role-nbs).

---

## R

### RBAC

**Role-Based Access Control.** An access management principle that restricts resource access based on a user's job role rather than individual identity. Applied when managing permissions in [AWS IAM](#iam), the Azure portal, and [Kubernetes](#kubernetes) cluster access controls.

### RDB

**Reporting Database.** The NBS database that stores flattened data for reporting and analysis. Populated by [MasterETL](#masteretl) (legacy path) or [RTR](#rtr) (modern path). See also [RDB_Modern](#rdb_modern).

### RDB_Modern

The modernized reporting database in NBS 7, populated by the [RTR](#rtr) pipeline. RDB_Modern runs alongside the legacy [RDB](#rdb) during the migration period.

### Amazon RDS

**Amazon Relational Database Service.** An AWS managed database service. In AWS deployments, RDS is one option for hosting the NBS 6 database. In Azure deployments, [Azure SQL](#azure-sql) services are common options for this purpose.

<!-- **Work on patient matching is unfinished, and unclear when it will be picked up.**
### Record Linker

A CDC open-source tool, part of [DIBBs](#dibbs), for matching and linking patient records across systems. Integrating with NBS 7 for patient deduplication.
-->

### Reportability Response

**Reportability Response (RR).** A structured message returned to an originating [EHR](#ehr) system after an [eICR](#eicr) is received and processed. The RR confirms whether the reported condition is reportable and to which jurisdiction. The RR is part of the eICR two-way exchange workflow and is generated by NBS after the [DI API](#di-api) forwards the eICR.

### reportable disease

A disease or condition that providers are required to report to the local or state health department under jurisdiction law. Distinct from [notifiable disease](#notifiable-disease), which refers to federal reporting requirements to CDC.

### role (NBS)

In NBS, the combination of a [permission set](#permission-set), program area or areas, jurisdiction or jurisdictions, and access level assigned to a user. A user may have multiple roles.

### RR

See [Reportability Response](#reportability-response).

### RTR

**Real-Time Reporting.** An NBS 7 reporting pipeline that replaces the batch [ETL](#etl) approach with event-driven data movement using [Kafka](#kafka). RTR coexists with [MasterETL](#masteretl) during the NBS 7 migration period.

### RxNorm

A standard code system for medications. RxNorm codes are stored in the NBS [SRTE](#srt--srte) database.

---

## S

### Amazon S3

**Amazon Simple Storage Service.** AWS object storage. Used for Terraform state files and NBS 7 logs. In Azure deployments, [Azure Blob Storage](#azure-blob-storage) serves the same function.

### SAML

**Security Assertion Markup Language.** A standard for exchanging authentication and authorization data. Used for [SSO](#sso) integrations with [Keycloak](#keycloak).

### SAS

**Statistical Analysis System.** Analytics software used with [Classic NBS](#classic-nbs) for reporting. Referenced in NBS 6 compatibility documentation.

### SBOM

**Software Bill of Materials.** A formal, machine-readable inventory of the software components, dependencies, and libraries used to build an application. SBOMs identify vulnerable or outdated components in a software supply chain. Security requirements may require CDC to produce SBOMs for NBS 7, which STLTs might reference as part of their own security authorization process.

### service mesh

An infrastructure layer that manages service-to-service communication within a distributed application, providing encryption, observability, and traffic management. [Linkerd](#linkerd) serves as the service mesh for NBS 7.

### SLA

**Service Level Agreement.** A contract defining service performance expectations. A STLT may be required to establish an SLA with its cloud service provider when deploying NBS 7.

### SNOMED CT

**Systematized Nomenclature of Medicine - Clinical Terms.** A standard code system identifying clinical findings and organisms. Used in NBS [ELR](#elr) processing and stored in the [SRTE](#srt--srte) database.

### SQL

**Structured Query Language.** A standard language for managing and querying relational databases. NBS uses SQL-based databases throughout its architecture, including the application database and the [ODS and ODSE](#ods-and-odse), [RDB](#rdb), and [SRT and SRTE](#srt-and-srte) databases.

### SRT / SRTE

**System Reference Tables (Enterprise).** The NBS database that stores standard code sets including [LOINC](#loinc), [SNOMED CT](#snomed-ct), [RxNorm](#rxnorm), and FIPS codes. Used for code mapping during ELR processing and jurisdiction derivation.

### SSO

**Single Sign-On.** An authentication method that allows users to log in once to access multiple systems. NBS 7 supports SSO through [Keycloak](#keycloak).

### STLT

**State, Territorial, Local, and Tribal.** The jurisdictions that operate NBS day-to-day. STLTs are the primary audience for this guide. Pronounced "stilt."

### strangler fig pattern

A software migration strategy in which new functionality is built alongside a legacy system and gradually replaces it, rather than rewriting everything at once. NBS 7 uses this pattern to modernize [Classic NBS](#classic-nbs) incrementally. The NBS Gateway routes requests between the modernized services and the Classic NBS application as migration proceeds.

### subnet

A subdivision of a [VPC's](#amazon-vpc) IP address range. NBS 7 infrastructure uses public and private subnets to isolate internet-facing components from internal services.

---

## T

### Terraform

An open-source infrastructure-as-code tool for provisioning and managing cloud resources. NBS 7 uses Terraform scripts in the [NEDSS-Infrastructure](https://github.com/CDCgov/NEDSS-Infrastructure) repository to provision cloud infrastructure. In AWS deployments, the scripts provision resources including [Amazon EKS](#amazon-eks), [Amazon VPC](#amazon-vpc), [Amazon MSK](#amazon-msk), and [Amazon EFS](#amazon-efs). In Azure deployments, the scripts provision resources including [AKS](#aks), [VNet](#vnet), [HDInsight](#hdinsight), and [Azure Files](#azure-files).

### TLS

**Transport Layer Security.** A cryptographic protocol that secures data in transit. TLS is required for NBS 7 deployments.

### Traefik

An open-source [ingress controller](#ingress-controller) and reverse proxy. Traefik replaced NGINX in NBS 7 deployments as of the 7.12 release.

### transfer of ownership

In NBS, the act of reassigning an observation or investigation from one jurisdiction or program area to another. The receiving owner becomes responsible for investigation and resolution tasks.

---

## V

### values file (Helm)

A YAML configuration file that supplies environment-specific settings to a [Helm chart](#helm-chart) during deployment. NBS 7 sysadmins customize values files to configure services for their environment.

### VNet

**Virtual Network.** An isolated cloud network in Azure. NBS 7 runs inside a VNet in Azure deployments. The Azure equivalent of [Amazon VPC](#amazon-vpc).

### Amazon VPC

**Amazon Virtual Private Cloud.** An isolated cloud network in AWS. NBS 7 runs inside a VPC in AWS deployments. The AWS equivalent of [VNet](#vnet). See also [peering](#peering) and [subnet](#subnet).

---

## W

### WDS

**Workflow Decision Support.** An NBS application feature that automates processing of incoming [ELR](#elr) and [eCR](#ecr) data. For example, automatically creating case investigations or marking documents as reviewed. Sysadmins configure the permission sets and security derivation that WDS depends on; changes to WDS behavior in the `NBS_Configuration` table require a [WildFly](#wildfly) restart.

### WildFly

An open-source Java application server. [Classic NBS](#classic-nbs) (NBS 6.x) runs on WildFly. During NBS 7 deployments, the Classic NBS application continues to run on WildFly alongside the modernized microservices during the [strangler fig](#strangler-fig-pattern) transition.
