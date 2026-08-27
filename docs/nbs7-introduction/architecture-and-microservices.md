---
title: Architecture overview
layout: page
parent: NBS 7 Introduction
nav_order: 1
description: How NBS 7 components fit together, including the strangler fig coexistence model, the request path, and the real-time reporting data flow.
redirect_from:
  - /docs/1_introduction/architecture_and_microservices.html
  - /docs/1_introduction/architecture_and_microservices/
  - /docs/deploy-nbs7/architecture-and-microservices.html
  - /docs/deploy-nbs7/architecture-and-microservices/
---

# NBS 7 architecture

This page explains how the [[nbs-7]] components fit together and how data flows between them. Understanding this architecture helps you plan your deployment and interpret the steps in the deployment guide. For cloud-provider and tooling details, see [Cloud prerequisites for AWS and Azure](../deploy-nbs7/full-deploy/provision-cloud-infrastructure/cloud-prerequisites.html).

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## How NBS 7 relates to NBS 6

NBS 7 does not replace NBS 6 all at once. It runs alongside your existing [[classic-nbs|NBS 6]] system and takes over functionality incrementally, an approach known as the [strangler fig pattern](https://martinfowler.com/bliki/StranglerFigApplication.html). Users move between modern NBS 7 features and classic NBS 6 features during the transition. As the modern system gains functionality, they rely on it for more of their work.

NBS 7 uses the same underlying NBS 6 databases rather than migrating the data to a new store. As a result, NBS 7 requires network access to the NBS 6 application and database server. In a typical deployment, NBS 7 runs in its own virtual network, [[peering|peered]] with the network that hosts NBS 6 to provide this access. Establishing this connectivity is part of your chosen network configuration.

## Architecture diagram

The following diagram shows the NBS 7 components, the request path that serves users, and the reporting path that streams data changes to the reporting database. Cloud-specific service names, such as the [[load-balancer]] and managed services, are described generically here. See [Provision cloud infrastructure](../deploy-nbs7/full-deploy/provision-cloud-infrastructure.html) for the [[aws]] and [[microsoft-azure|Azure]] implementation of each.

![Architecture diagram of NBS 7. On the left, external actors: a container registry and source control supply images and Helm charts, an admin user deploys charts and has cloud admin access, and a jurisdiction user reaches the system through a DNS service. In the center, the Modern NBS environment contains a load balancer feeding a Kubernetes cluster. Inside the cluster, a Traefik ingress routes to the NBS microservice containers (Modernization API, Data Ingestion API, additional NBS 7 services, and the NBS Gateway), a shared services and tools tier (cert-manager, Elasticsearch, Apache NiFi, OTEL collector, and Keycloak), and a real-time reporting tier (Debezium, Kafka connector, and reporting pipeline service). A message streaming service using Kafka sits outside the cluster and exchanges events with the reporting tier. Cloud-managed services for metrics and dashboards sit outside the cluster. On the right, the Classic NBS environment contains NBS 6, SAS, and the NBS 6 database, peered with the modern environment. The NBS 6 database change log flows to Debezium, which publishes to Kafka, and the reporting pipeline service writes to a separate reporting database.](./images/713-architecture.png)

## The request path

When a user opens NBS 7, their request follows this path:

1. The user's browser resolves the NBS 7 address through your Domain Name System ([[dns]]) service.
1. DNS directs the request to the load balancer, the entry point into the virtual network.
1. The load balancer forwards the request to the [[traefik]] [[ingress-controller]] inside the [[kubernetes]] cluster.
1. Traefik routes the request to the correct service based on the address. The NBS Gateway applies the strangler routing rules that decide whether a request is served by NBS 7 or passed through to NBS 6.

## The reporting path

Real-time reporting ([[rtr]]) streams changes from the NBS databases to a reporting database in near real time, which reduces reporting latency from as long as 24 hours to between 5 minutes and 1 hour. The data flows through these stages:

1. [[debezium]] monitors the change log of the `NBS_ODSE` and `NBS_SRTE` databases and captures row-level changes.
1. Debezium publishes those changes as events to [[kafka]] topics. Kafka runs as a managed message-streaming service outside the Kubernetes cluster.
1. The Kafka connector and the reporting pipeline service consume the events from Kafka.
1. The reporting pipeline service transforms the events and writes them to the reporting database (`RDB` or `RDB_MODERN`).

During the transition, RTR runs alongside the legacy [[masteretl]] batch process rather than replacing it, so you can compare results before relying on RTR. For deployment steps, see [Deploy real-time reporting](../deploy-nbs7/microservices-deployment/real-time-reporting/real-time-reporting.html).

## Components

NBS 7 groups its components into tiers by role. The following sections describe each tier shown in the [architecture diagram](#architecture-diagram): the microservices that provide NBS 7 features, the shared services that support them, the real-time reporting services, and the cloud-managed services for observability.

### NBS microservice containers

These services provide the modernized NBS 7 features:

- **Modernization API:** Provides modernized versions of core NBS features. As NBS 7 development progresses, additional NBS 6 features will migrate into this API layer.
- **Data Ingestion API ([[di-api]]):** Accepts electronic [[lab-report|lab reports]] and other electronic data, validates it, and routes it into NBS.
- **NBS Gateway:** Applies the strangler routing rules between NBS 7 and NBS 6, using Spring Cloud Gateway.
- **Additional NBS 7 services:** Supporting services deployed as the modernized system grows.

### Shared services and tools

These services support the NBS 7 microservices:

- **cert-manager:** Automates Transport Layer Security ([[tls]]) certificate management, using Let's Encrypt as the default certificate authority.
- **[[elasticsearch]]:** Provides fast search across NBS data.
- **[[apache-nifi]]:** Populates Elasticsearch indices from the NBS database.
- **[[otel]] collector:** Collects logs and metrics from the microservices and Kubernetes components.
- **[[keycloak]]:** Provides authentication, token management, and single sign-on ([[sso]]) integration with external identity providers such as Okta, using OpenID Connect ([[oidc]]).

### Real-time reporting

These services make up the reporting path described in [the reporting path](#the-reporting-path):

- **Debezium:** Captures row-level changes from the `NBS_ODSE` and `NBS_SRTE` databases and publishes them to Kafka.
- **Kafka connector:** Consumes reporting events from Kafka topics.
- **Reporting pipeline service:** Transforms the events and writes them to the reporting database.

### Cloud-managed services

NBS 7 uses managed services from your cloud provider for observability, provisioned by [[terraform]]:

- **Managed Prometheus:** Collects infrastructure and application metrics.
- **Managed Grafana:** Visualizes those metrics in dashboards.

## How NBS 7 is deployed

NBS 7 uses an [[infrastructure-as-code]] approach, so the environment is defined in version-controlled files rather than configured by hand:

- Terraform provisions the cloud environment: the virtual network, the Kubernetes cluster, storage, the managed services, and the message-streaming service.
- [[helm]] deploys and configures the workloads that run inside the Kubernetes cluster.
- Both are distributed from [GitHub](https://github.com/CDCgov).

For the full deployment procedure, see [Deploy NBS {{ site.version_latest }}](../deploy-nbs7.html).
