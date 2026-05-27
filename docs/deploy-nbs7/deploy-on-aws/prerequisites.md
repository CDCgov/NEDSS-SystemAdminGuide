---
title: Prerequisites for AWS
layout: page
parent: Deploy on AWS
nav_order: 1
redirect_from:
  - /docs/2_prerequisites/prereq.html
  - /docs/2_prerequisites/prereq/
description: Prepare your AWS cloud environment before you provision AWS for NBS 7.
---

# Prerequisites for AWS deployments
{: .no_toc }

Before you deploy NBS 7, confirm that your Amazon Web Services (AWS) environment meets the requirements in each of the following areas.

> Start with the cloud-agnostic [Prerequisites for NBS 7 deployment](../prerequisites.html), then complete the AWS-specific requirements on this page.
{: .important }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## AWS environment requirements

Your AWS environment must meet the following requirements:

- An existing AWS account with a production instance of NBS 6 listed in the NBS 6 and NBS 7 compatibility matrix and related third-party products
- A configured DNS routing infrastructure
- Permissions to create security groups and AWS IAM roles
- Access to NBS 6 databases hosted on a SQL Server instance. Two common hosting options with AWS include Amazon RDS and self-managed Amazon EC2. See [AWS services reference](../deploy-on-aws.html#aws-services-reference) for details.
- Access to an Amazon S3 bucket to store Terraform state

## Hardware requirements

### Higher-volume STLTs

| **Type** | **Resource** | **Size** |
|-----------|--------------|----------|
| Container runtime environment | Amazon EKS | 4 Nodes - Linux (4 cores/32 GB RAM, 100GB block storage) r5.xlarge |
| Relational Database | SQL Server 2017+ Standard or Enterprise (hosted on Amazon RDS or a self-managed Amazon EC2 instance) | New NBS 6.X.X Deployment Recommendations: [Implementation and Support FAQs](https://www.cdc.gov/nbs/php/technical-resources/implementation-and-support-faqs.html) |
| Persistent Store | Amazon EFS | 1 TB |

### Lower-volume STLTs

| **Type** | **Resource** | **Size** |
|-----------|--------------|----------|
| Container runtime environment | Amazon EKS | 4 Nodes - Linux (4 cores/32 GB RAM, 100GB block storage) r5.xlarge |
| Relational Database | SQL Server 2017+ Standard or Enterprise (hosted on Amazon RDS or a self-managed Amazon EC2 instance) | New NBS 6.X.X deployment recommendations: [Implementation and Support FAQs](https://www.cdc.gov/nbs/php/technical-resources/implementation-and-support-faqs.html) |
| Persistent Store | Amazon EFS | 500 GB |

## Software requirements

| **Software** | **Version** | **Comments** |
|---|---|---|
| Kubernetes | 1.25+ | Deployed as Amazon EKS by default |
| Cert Manager | 1.13 | Deployed in Kubernetes |
| Elasticsearch | 7.17 | Deployed by default in Kubernetes |
| Apache NiFi | 1.19 | Deployed in Kubernetes |
| Traefik | 3.x | Deployed in Kubernetes as ingress controller |
| Prometheus | 2.44 | Deployed as Amazon Managed Service for Prometheus (AMP) by default |
| Grafana | 9.5.x | Deployed as Amazon Managed Grafana (AMG) by default |
| Fluent Bit | 1.9.x | Deployed in Kubernetes. Log storage can be configured. |
| NBS Classic | 6.0.18.1 or higher | Reuse current NBS instance |
| SQL Server | 2017+ | Reuse current NBS instance |
| Kafka | 2.8.1 | Deployed as Amazon MSK |
| Keycloak | 22.0.5+ | Deployed in Kubernetes |

## Management machine setup

To configure, deploy, and maintain NBS 7, you need a local or cloud-hosted workstation such as AWS CloudShell with the following tools installed:

- **AWS CLI:** Download and installation instructions are in the [AWS CLI documentation](https://aws.amazon.com/cli/). For credential configuration, see the [AWS CLI credential configuration guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
- **GitHub CLI:** Download and installation instructions are at [cli.github.com](https://cli.github.com/).
- **Terraform CLI:** Download and installation instructions are in the [Terraform CLI installation guide](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli). Version 1.5.5 has been tested with NBS 7. Installing this version is suggested over the latest non-open source version.
- **Helm CLI**: Download and installation instructions are in the [Helm installation guide](https://helm.sh/docs/intro/install/)
- **Kubernetes CLI (kubectl):** Download and installation instructions are in the [kubectl installation guide for Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html).
- **eksctl:** Download and installation instructions are in the [eksctl installation guide](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html).

## Network and database access requirements

NBS 7 infrastructure and microservices are deployed into a new Amazon VPC, provisioned using the Terraform scripts in [Provision the AWS cloud environment](provision-aws.html).

Confirm that network access is available from NBS 7 components to classic NBS 6 components, including the database server. The NBS 6 SQL Server database must allow access from the NBS 7 VPC address space, whether hosted on Amazon RDS or a self-managed EC2 instance. Use a private route for this network access rather than a publicly accessible connection.

The team member who creates this infrastructure should have operational knowledge of Terraform.

## Security requirements

### Encryption management

AWS storage services including Amazon EBS, Amazon EFS, and Amazon RDS use AWS Key Management Service (AWS KMS) for encryption.

### End-user authentication

NBS 7 integrates with standards-based SSO systems and is designed to work with your existing Identity Provider (IdP), such as Okta. Because NBS 7 requires a working NBS 6 instance, an authentication mechanism is assumed to be in place. No additional authentication configuration is needed before deployment.

If you are integrating NBS into a new SSO ecosystem, a proof of concept is available on request.

## What to do now

1. Confirm that you have completed both the AWS-specific requirements from this page and the cloud-agnostic [Prerequisites](../prerequisites.html)
1. Continue with [Provision the AWS cloud environment](provision-aws.html)
