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

Before you begin deployment on any cloud provider, confirm that your jurisdiction meets the prerequisites in each of the following areas. Some prerequisites are cloud-agnostic; others are specific to AWS or Azure. Refer to the provider-specific pages for additional requirements.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Knowledge requirements

Your deployment team should include at least one person who has:

- Working knowledge of Terraform configuration and the ability to read and modify HCL code
- Kubernetes administration experience or the willingness to build this capability with training
- Familiarity with your organization's cloud provider (AWS or Azure) and cloud networking concepts
- Understanding of SQL Server database administration, including backup and restore procedures

## NBS 6 readiness

Your NBS 6 instance is the foundation for NBS 7. Confirm the following:

- **Supported version:** Your NBS 6 version must be supported for your target NBS 7 version. See the [Supported NBS versions](../../supported-versions.html) page.
- **Database access and refresh:** If your current NBS 6 database is hosted on-premises and you plan to move it to the cloud, you must complete a database refresh and ensure that the database is accessible from your test environment. This is typically a jurisdiction-managed procedure using your organization's standard database backup and restore process.
- **Database server access:** Your cloud environment must have network access to your NBS 6 database server (either on-premises RDS or EC2 instance, depending on your hosting setup). If the database is on-premises, network connectivity must be established before deployment begins.
- **Related applications:** Any third-party products integrated with NBS 6, such as Rhapsody or SAS, must remain operational during the NBS 7 migration. Confirm that these systems will remain accessible from your NBS 7 environment.

## Network access

Your network must provide connectivity from all NBS 7 components to NBS 6 components, including the database server.

- **Private network route preferred:** Use a private route for this access rather than exposing the database to the public internet.
- **Encryption required:** All virtual network traffic between NBS 6 and NBS 7 must be encrypted.
- **VPC/network setup:** Confirm that your organization can provision and configure virtual private networks (VPCs) or equivalent network isolation and can allow the necessary connectivity.

For provider-specific network setup, see [Prerequisites for AWS](provision-cloud-infrastructure/cloud-prerequisites.html) or [Prerequisites for Azure](provision-cloud-infrastructure/cloud-prerequisites.html).

## Required tools and software

You will need a local or cloud-hosted workstation (for example, AWS CloudShell, Azure Cloud Shell, or a local laptop) with specific tools installed to support deployment and ongoing maintenance.

The following table lists the minimum supported versions of the required software. The [Cloud prerequisites](provision-cloud-infrastructure/cloud-prerequisites.html) page lists additional tools and the specific versions used in testing.

| **Software**        | **Minimum version**             |
|:---|:---|
| Kubernetes CLI      | kubectl 1.25                    |
| Helm CLI            | 3.0                             |
| Terraform CLI       | 1.15.6                          |
| GitHub CLI          | Latest                          |
| Cloud provider CLI  | Latest AWS or Azure CLI version |
| Docker              | 20.x                            |

For installation instructions specific to your cloud provider, see [Cloud prerequisites](provision-cloud-infrastructure/cloud-prerequisites.html).

## DNS and SSL/TLS certificates

Your deployment requires DNS resolution and certificate management:

- **DNS infrastructure:** Your organization must have a properly configured DNS system that can create and manage entries for NBS 7 endpoints (for example, `app.yourstlts.com` and `data.yourstlts.com`).
- **TLS/SSL certificates:** You must have a process to provision and renew TLS/SSL certificates for encrypted traffic. This can be automatic (certificate manager) or manual (self-signed or CA-provided certificates).

## Security and authentication

Your organization must have or be prepared to establish the following security controls:

- **Encryption at rest:** All cloud infrastructure storage (databases, filesystems, object storage) must support encryption. This is standard on AWS and Azure.
- **Identity and access management:** You must be able to create and manage cloud IAM roles and policies (AWS) or role-based access control (Azure).
- **Single Sign-On (optional but recommended):** NBS 7 uses Keycloak for identity management. If your organization uses a centralized identity provider such as Okta or Active Directory, Keycloak can integrate with it so users log in with their existing jurisdiction credentials. Coordinate with your identity provider administrators early in the planning process if you plan to integrate.
- **Existing authentication mechanism:** NBS 7 assumes your organization already has a working NBS 6 instance and therefore already has end-user authentication in place. NBS 7 extends this authentication; no new user authentication steps are required.

## Next steps

After completing these prerequisites, [Provision your cloud infrastructure](provision-cloud-infrastructure.html).
