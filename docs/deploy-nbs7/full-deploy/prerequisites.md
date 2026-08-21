---
title: NBS 7 prerequisites
layout: page
parent: NBS 7 full deployment
nav_order: 1
description: Prerequisites for NBS 7 deployment, including NBS 6 readiness, network access, DNS, security, and local management machine setup.
redirect_from:
  - /docs/deploy-nbs7/prerequisites.html
  - /docs/deploy-nbs7/prerequisites/
---

# Prerequisites for NBS 7 deployment

Before you begin deployment, confirm that your {% include term-tooltip.html key="jurisdiction" term="jurisdiction" id="prereq-jurisdiction" %} meets the prerequisites in each of the following areas. Additional prerequisites such as database, server, and workstation details are covered at the point of cloud provisioning in the [Cloud prerequisites for AWS and Azure](./provision-cloud-infrastructure/cloud-prerequisites.html) section.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Knowledge requirements

Your deployment team should include at least one person who has:

- Working knowledge of {% include term-tooltip.html key="terraform" term="Terraform" id="prereq-terraform" %} configuration and the ability to read and modify {% include term-tooltip.html key="hcl" term="HCL" id="prereq-hcl" %} code
- {% include term-tooltip.html key="kubernetes" term="Kubernetes" id="prereq-kubernetes" %} administration experience or the willingness to build this capability with training
- Familiarity with your organization's cloud provider ({% include term-tooltip.html key="aws" term="AWS" id="prereq-aws" %} or {% include term-tooltip.html key="microsoft-azure" term="Azure" id="prereq-azure" %}) and cloud networking concepts
- Understanding of {% include term-tooltip.html key="microsoft-sql-server" term="SQL Server" id="prereq-mssql" %} database administration, including backup and restore procedures

## NBS 6 readiness

Your {% include term-tooltip.html key="classic-nbs" term="NBS 6" id="prereq-nbs-6" %} instance is the foundation for {% include term-tooltip.html key="nbs-7" term="NBS 7" id="prereq-nbs-7" %}. Confirm the following:

- **Supported version:** Your NBS 6 version must be supported for your target NBS 7 version. See the [Supported NBS versions](../../supported-versions.html) page.
- **Database access and refresh:** If your current NBS 6 database is hosted {% include term-tooltip.html key="on-premises" term="on-premises" id="prereq-on-premises" %} and you plan to move it to the cloud, you must complete a database refresh and ensure that the database is accessible from your test environment. This is typically a jurisdiction-managed procedure using your organization's standard database backup and restore process.
- **Database server access:** Your cloud environment must have network access to your NBS 6 database server (either on-premises {% include term-tooltip.html key="amazon-rds" term="RDS" id="prereq-rds" %} or {% include term-tooltip.html key="amazon-ec2" term="EC2" id="prereq-ec2" %} instance, depending on your hosting setup). If the database is on-premises, network connectivity must be established before deployment begins.
- **Related applications:** Any third-party products integrated with NBS 6, such as Rhapsody or {% include term-tooltip.html key="sas" term="SAS" id="prereq-sas" %}, must remain operational during the NBS 7 migration. Confirm that these systems will remain accessible from your NBS 7 environment.

## Network access

Your network must provide connectivity from all NBS 7 components to NBS 6 components, including the database server.

- **Private network route preferred:** Use a private route for this access rather than exposing the database to the public internet.
- **Encryption required:** All virtual network traffic between NBS 6 and NBS 7 must be encrypted.
- **VPC/network setup:** Confirm that your organization can provision and configure virtual private networks ({% include term-tooltip.html key="amazon-vpc" term="VPCs" id="prereq-vpc" %}) or equivalent network isolation and can allow the necessary connectivity.

For provider-specific network setup, see [Prerequisites for AWS](provision-cloud-infrastructure/cloud-prerequisites.html) or [Prerequisites for Azure](provision-cloud-infrastructure/cloud-prerequisites.html).

## Required tools and software

You will need a local or cloud-hosted workstation, such as AWS CloudShell, Azure Cloud Shell, or a local laptop, with specific tools installed to support deployment and ongoing maintenance. These include the cloud provider {% include term-tooltip.html key="cli" term="CLI" id="prereq-cli" %}, Terraform, {% include term-tooltip.html key="helm" term="Helm" id="prereq-helm" %}, {% include term-tooltip.html key="kubectl" term="kubectl" id="prereq-kubectl" %}, and Docker.

For the supported versions and cloud-specific install instructions, see [Management workstation setup](provision-cloud-infrastructure/cloud-prerequisites.html#management-workstation-setup) in Cloud prerequisites.

## DNS and SSL/TLS certificates

Your deployment requires Domain Name System ({% include term-tooltip.html key="dns" term="DNS" id="prereq-dns" %}) resolution and certificate management:

- **DNS infrastructure:** Your organization must have a properly configured DNS system that can create and manage entries for NBS 7 endpoints (for example, `app.yourstlts.com` and `data.yourstlts.com`).
- **{% include term-tooltip.html key="tls" term="TLS" id="prereq-tls" %}/{% include term-tooltip.html key="ssl" term="SSL" id="prereq-ssl" %} certificates:** You must have a process to provision and renew TLS/SSL certificates for encrypted traffic. This can be automatic (certificate manager) or manual (self-signed or CA-provided certificates).

## Security and authentication

Your organization must have or be prepared to establish the following security controls:

- **Encryption at rest:** All cloud infrastructure storage (databases, filesystems, object storage) must support encryption. This is standard on AWS and Azure.
- **Identity and access management:** You must be able to create and manage cloud {% include term-tooltip.html key="iam" term="IAM" id="prereq-iam" %} roles and policies (AWS) or role-based access control (Azure).
- **{% include term-tooltip.html key="sso" term="Single Sign-On" id="prereq-sso" %} (optional but recommended):** NBS 7 uses {% include term-tooltip.html key="keycloak" term="Keycloak" id="prereq-keycloak" %} for identity management. If your organization uses a centralized {% include term-tooltip.html key="idp" term="identity provider" id="prereq-idp" %} such as Okta or Active Directory, Keycloak can integrate with it so users log in with their existing jurisdiction credentials. Coordinate with your identity provider administrators early in the planning process if you plan to integrate.
- **Existing authentication mechanism:** NBS 7 assumes your organization already has a working NBS 6 instance and therefore already has end-user authentication in place. NBS 7 extends this authentication; no new user authentication steps are required.

## Next steps

After completing these prerequisites, [Provision your cloud infrastructure](provision-cloud-infrastructure.html).
