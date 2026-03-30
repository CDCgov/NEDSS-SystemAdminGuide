---
title: Prerequisites for AWS
layout: page
parent: Deploy on AWS
nav_order: 1
toc_levels: 1..2
nav_enabled: true
has_children: true
---

# Prerequisites for AWS deployments
{: .no_toc }

Before you deploy NBS 7, make sure your environment meets the requirements in each of the following areas.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## AWS environment requirements

Your AWS environment must:

- Contain a pre-existing AWS account that contains a production instance of NBS 6 that is listed in the [NBS 6 and NBS 7 compatibility matrix](../../../docs/before-you-deploy/compatibility.html), plus related third-party products such as Rhapsody and SAS
- Have a properly configured DNS routing infrastructure
- Be configured to enable you to create security groups and IAM roles
- Provide access to NBS 6 databases that are located on an MS SQL Server instance (RDS or EC2)
- Have access to an S3 bucket to store Terraform (TF) state

## Hardware requirements

### High-volume STLTs

| **Type** | **Resource** | **Size** |
|-----------|--------------|----------|
| Container runtime environment | EKS | 4 Nodes - Linux (4 cores/32 GB RAM, 100GB block storage) r5.xlarge |
| Relational Database | SQL Server 2017+ Standard or Enterprise | New NBS 6.X.X Deployment Recommendations: [📝 Implementation and Support FAQs](https://www.cdc.gov/nbs/php/technical-resources/implementation-and-support-faqs.html) |
| Persistent Store | EFS | 1 TB |

### Low-volume STLTs

| **Type** | **Resource** | **Size** |
|-----------|--------------|----------|
| Container runtime environment | EKS | 4 Nodes - Linux (4 cores/32 GB RAM, 100GB block storage) r5.xlarge |
| Relational Database | Cloud Managed MS SQL Server Standard or Enterprise | New NBS 6.X.X Deployment Recommendations: [📝 Implementation and Support FAQs](https://www.cdc.gov/nbs/php/technical-resources/implementation-and-support-faqs.html) |
| Persistent Store | EFS | 500 GB |

## Software requirements

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

## Management machine setup

You will need a local or cloud hosted workstation (e.g. CloudShell) with the set of tools required to configure, deploy and maintain the NBS 7 system. The following tools should be installed on a local or cloud-based management machine to support this work:

- **AWS CLI**: Download and installation instructions can be found [here](https://aws.amazon.com/cli/)
  - Instructions for getting and using AWS credentials for use with the CLI can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- **GitHub CLI**: Download and installation instructions are here:
  <https://cli.github.com/>
- **Terraform CLI**: Download and installation instructions are [here](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
  *(Tested through 1.5.5 Terraform, suggest install that specific version rather than the latest non-open source version)*
- **Helm CLI**: Download and installation instructions are [here](https://helm.sh/docs/intro/install/)
- **Kubernetes CLI**: Download and installation instructions are [here](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)
- **Optional, but nice to have, eksctl**: Download and installation instructions are [here](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)

## Network and database access requirements

Installation of the NBS 7 infrastructure and microservices uses a new VPC, which is provisioned using the Terraform scripts included in [the provisioning steps](../../../docs/deploy-nbs7/aws-infrastructure/aws-infrastructure.html).

You must ensure that there is network access available from the location of modern NBS 7 components to the classic NBS 6 components, including the database server. The database server or RDS should allow access to the NBS 7 VPC address space. As a best practice, use a private route for this network access, rather than making it publicly accessible.

A team member who has operational knowledge of and is familiar with using Terraform is most suited to create this infrastructure.

## Security requirements

### Encryption management

AWS infrastructure storage services like AWS EBS, EFS, and RDS utilize AWS Key Management Store (KMS) for encryption, ensuring a
robust layer of security.

### End-user authentication

The NBS 7 system will support end user authentication by integrating with a standards-based SSO system. It is designed to be deployed as a protected endpoint within your preexisting SSO ecosystem, and can be configured to work with a wide variety of standards compliant Identity Providers (e.g. Okta, AD).

This is similar to NBS 6. As documented in ["NEDSS Base System Release 4.4.1 Hardening NBS Perimeter Security"](https://nbscentral.cdc.gov/attachments/1995) (requires access on NBS central), NBS 6 does not authenticate users. Instead, it delegates authentication to a security proxy, which each State, Tribal, Local, and Territorial (STLT) must provide in order to deploy NBS.

The NBS 7 release requires that prospective users already have a working NBS 6 instance, and therefore assumes that a user authentication mechanism is already in place.

NBS 7 extends functionality that is available to the authenticated user. NBS 7 therefore works alongside the existing authentication mechanism. No additional steps are needed to authenticate users for NBS 7.

To assist those who are integrating NBS into their SSO ecosystem, a proof of concept in which authentication is performed using an Identity Provider (IdP) and a proxy is available on request. To request it, [please create a ticket here](https://nbscentral.cdc.gov/projects/nbs700/issues/new).
