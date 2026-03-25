---
title: Hardware and software requirements
layout: page
parent: Prerequisites
grand_parent: Deploy NBS 7
nav_order: 2
---

## Hardware Requirements (AWS)

<h4 align="center"><b> High Volume STLTs </b></h4>
{: .no_toc }

| **Type** | **Resource** | **Size** |
|-----------|--------------|----------|
| Container runtime environment | EKS | 4 Nodes - Linux (4 cores/32 GB RAM, 100GB block storage) r5.xlarge |
| Relational Database | SQL Server 2017+ Standard or Enterprise | New NBS 6.X.X Deployment Recommendations: [📝 Implementation and Support FAQs](https://www.cdc.gov/nbs/php/technical-resources/implementation-and-support-faqs.html?CDC_AAref_Val=https://www.cdc.gov/nbs/resources/implementation-and-support.html) |
| Persistent Store | EFS | 1 TB |

<h4 align="center"><b> Low Volume STLTs </b></h4>
{: .no_toc }

| **Type** | **Resource** | **Size** |
|-----------|--------------|----------|
| Container runtime environment | EKS | 4 Nodes - Linux (4 cores/32 GB RAM, 100GB block storage) r5.xlarge |
| Relational Database | Cloud Managed MS SQL Server Standard or Enterprise | New NBS 6.X.X Deployment Recommendations: [📝 Implementation and Support FAQs](https://www.cdc.gov/nbs/php/technical-resources/implementation-and-support-faqs.html?CDC_AAref_Val=https://www.cdc.gov/nbs/resources/implementation-and-support.html) |
| Persistent Store | EFS | 500 GB |

## Software requirements
{: .no_toc }

| **Software**        | **Version**                   | **Comments**                                                    |
|---------------------|-------------------------------|-----------------------------------------------------------------|
| Kubernetes          | 1.25+                         | Deployed as EKS by default                                      |
| Cert Manager        | 1.13                          | Deployed in Kubernetes                                          |
| Elasticsearch       | 7.17                          | Deployed by default in Kubernetes                               |
| Apache NiFi         | 1.19                          | Deployed in Kubernetes                                          |
| NGINX Ingress       | 3.0.2                         | Must be deployed in Kubernetes                                  |
| Prometheus          | 2.44                          | Deployed as AMP by default                                      |
| Grafana             | 9.5.x                         | Deployed as AMG by default                                      |
| FluentBit           | 1.9.x                         | Deployed in Kubernetes. Log storage can be configured.          |
| NBS Classic         | NBS 6.0.16 (or newer version) | Reuse current NBS instance                                      |
| SQL Server          | 2017+                         | Reuse current NBS instance                                      |
| Kafka               | 2.8.1                         | Deployed as MSK. Needed only if running Data Ingestion Service. |
| Keycloak            | 22.0.5+                       | Deployed in Kubernetes                                          |
