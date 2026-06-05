---
title: NBS 7 core components
layout: page
parent: Component reference
grand_parent: Before you deploy
nav_order: 1
description: Details each component in NBS 7 — the application, infrastructure, and networking layers required for all NBS 7 deployments.
---

# Component reference: NBS 7 core components
{: .no_toc }

For information on migration planning, staffing, and budget, see [Operational considerations](../../before-you-deploy/operational-considerations.html).
{: .note }

NBS 7 core components are organized into three layers: the application layer, the infrastructure layer, and the networking layer. The application layer components are documented individually below. [Infrastructure and networking layer components](#infrastructure-and-networking-layer-components) are summarized as a group.

\[architecture diagram\]

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Legacy NBS 6

The existing NBS 6 application. A WildFly-based UI and backend that most STLTs currently run.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | NBS Core does not replace NBS 6 immediately. Instead, it runs alongside it. During migration, the NBS Gateway routes requests between the legacy NBS 6 application and new NBS 7 services. NBS 6 continues to handle all functionality that has not yet been replaced by a modern NBS 7 equivalent. |
| When you need it | Always. An operational NBS 6 instance is a prerequisite for any NBS 7 deployment. You must be running a [compatible NBS 6 version](../../compatibility.html) before you can install NBS 7. |
| Dependencies | Required by NBS Gateway, Elasticsearch (via Nifi), and the NBS Modernization API. Must maintain network connectivity to your NBS 7 environment throughout the migration period. |

## NBS Modernization API

The modern backend API layer for NBS 7, built to replace NBS 6 functionality incrementally.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Provides modernized versions of core NBS features including patient search, event search, patient profile, and investigation management. As NBS 7 development progresses, additional NBS 6 features will migrate into this API layer. |
| When you need it | Always. The Modernization API is a core component of NBS 7 and is required for all configurations. |
| Dependencies | Requires Legacy NBS 6 and NBS Gateway. Exposes functionality to the NBS Web UI. |

## NBS Web UI

The modern React/TypeScript frontend for NBS 7 features.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Provides the user interface for modernized NBS 7 functionality. STLT users see a composite interface. Some screens are served by the new NBS Web UI, while others continue to be served by the legacy NBS 6 UI. The NBS Gateway manages which interface handles each request. |
| When you need it | Always. The NBS Web UI is a core component of NBS 7 and is required for all configurations. |
| Dependencies | Requires NBS Gateway and the NBS Modernization API. |

## NBS Gateway

A routing service (built on Spring Cloud Gateway) that manages traffic between the legacy NBS 6 application and modern NBS 7 services.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Implements the strangler fig pattern by routing requests based on path. Requests for modernized features (such as patient search) go to NBS 7 services. All other requests go to Legacy NBS 6. This routing layer is what allows NBS 6 and NBS 7 to run simultaneously during migration without users needing to switch between systems. |
| When you need it | Always. NBS Gateway is a core component of NBS 7 and is required for all configurations. |
| Dependencies | Requires Legacy NBS 6, the NBS Modernization API, and the NBS Web UI. Sits behind the infrastructure layer ingress controller. |

<!-- COMMENTING OUT PER EMMA/MAGGIE UNTIL 7.13
## Report Execution API

A Python FastAPI service intended to replace SAS-based report execution in NBS 7. SAS 9.4 is currently required for report execution and must be carried forward into NBS 7 deployments until this component is production-ready. Jurisdictions with significant SAS infrastructure or licensing costs should monitor this component as NBS 7 matures.

> This component is not yet confirmed for production. Check with your CDC NBS point of contact to find out whether it affects your deployment plan.
{: .note }

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | \[Pending SME verification\] |
| Dependencies | \[Pending SME verification\] |
-->

## Elasticsearch

An open-source search and analytics engine optimized for speed and scalability.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Powers real-time patient and event search in NBS 7. NBS 6 requires batch processing before search results can reflect recent data, so this is a key improvement. [Nifi](#nifi) populates Elasticsearch indices from the NBS database. |
| When you need it | Always. Elasticsearch is a core component of NBS 7 and is required for all configurations. |
| Dependencies | Requires Nifi to populate its indices from the NBS database. Search functionality in the NBS Web UI and Modernization API depends on Elasticsearch. |

## Nifi

An open-source data flow automation tool for moving and transforming data between systems.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Continuously moves data from the NBS database into Elasticsearch, keeping search indices current. Without Nifi, Elasticsearch indices would not reflect recent changes to patient and investigation records. |
| When you need it | Always. Nifi is a core component of NBS 7 and is required for all configurations. |
| Dependencies | Requires the NBS database (NBS\_ODSE) as its data source and Elasticsearch as its destination. |

## Keycloak

An open-source identity and access management platform.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | Handles authentication for NBS 7, including token management and single sign-on (SSO) integration. Keycloak supports OAuth and SAML, which means your jurisdiction can integrate NBS 7 with an existing identity provider such as Okta or Active Directory Federation Services (ADFS) rather than managing a separate set of NBS credentials. |
| When you need it | Always. Keycloak is a core component of NBS 7 and is required for all configurations. |
| Dependencies | Requires network access to your identity provider if you are integrating with an existing SSO system. All NBS 7 services that require authentication depend on Keycloak. |

> Health department leaders
>
> For guidance on Single Sign-On planning and early coordination requirements, see [Operational considerations](../../before-you-deploy/operational-considerations.html).
{: .note-title }

## Database (NBS\_ODSE, NBS\_SRTE)

The core SQL Server databases that store operational and reference data for NBS.

| Attribute | Description |
|:---|:---|
| What it does in NBS 7 | NBS\_ODSE (Operational Data Store) is the primary transactional database where case, patient, investigation, and event records are stored. NBS\_SRTE (System Reference Tables) stores reference and metadata used across NBS, including LOINC, SNOMED CT, and other code sets used for data validation and mapping. |
| When you need it | Always. Both databases are required for all NBS 7 configurations. |
| Dependencies | Required by Legacy NBS 6, the Modernization API, Nifi, Debezium (for RTR), and the DI API. |

## Infrastructure and networking layer components

The following components make up the infrastructure and networking layers of NBS 7. They are provisioned and managed primarily through Terraform and Helm, and most do not require configuration decisions from IT admins during the [planning stage](../../before-you-deploy/planning.html#planning). They are documented here for awareness.

Full configuration guidance is in the [Deploy NBS 7](../../deploy-nbs7.html) section of this guide.

| Component | What it does in NBS 7 |
|:---|:---|
| Kubernetes (EKS/AKS) | Container orchestration platform that hosts and manages all NBS 7 services. EKS is used on AWS; AKS is used on Azure. |
| Traefik Ingress Controller | Manages inbound traffic routing into the Kubernetes cluster. Traefik replaced NGINX as of the NBS 7.12 release. |
| Terraform modules | Infrastructure-as-code tooling that provisions your cloud environment, including VPC, Kubernetes cluster, storage, and managed services. Four modules cover network/VPC, NBS 6 database layer, NBS 7 cluster, and application services. |
| Cert Manager | Automates provisioning and renewal of TLS/SSL certificates for encrypted traffic within and into the NBS 7 environment. |
| FluentBit | Lightweight log forwarding agent that collects and routes logs from NBS 7 services for monitoring and troubleshooting. |
| Linkerd | Service mesh (provisioned via Terraform) that manages encrypted communication between NBS 7 services inside the Kubernetes cluster. |
| DNS (Route 53 or equivalent) | Routes user traffic to your NBS 7 environment. On AWS, Route 53 is the standard option; Azure and on-premises DNS services are also supported. |
