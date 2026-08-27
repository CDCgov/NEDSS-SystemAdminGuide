---
title: Cloud prerequisites
layout: page
parent: Provision cloud infrastructure
nav_order: 1
description: Verify your AWS or Azure account, hardware, software, and network requirements before you provision the cloud environment for NBS 7.
redirect_from:
  - /docs/2_prerequisites/prereq.html
  - /docs/2_prerequisites/prereq/
  - /docs/deploy-nbs7/deploy-on-aws/prerequisites.html
  - /docs/deploy-nbs7/deploy-on-aws/prerequisites/
  - /docs/deploy-nbs7/deploy-on-azure/prerequisites.html
  - /docs/deploy-nbs7/deploy-on-azure/prerequisites/
---

# Cloud prerequisites for AWS and Azure

Before you provision cloud infrastructure for [[nbs-7]], verify that your cloud environment, workstation tools, and network access meet the requirements on this page. These requirements apply to both [[aws]] and [[microsoft-azure|Azure]] deployments. Where the two providers differ, each requirement lists the AWS and Azure equivalents.

> Start with the [Prerequisites for NBS 7 deployment](../prerequisites.html), then verify the cloud requirements on this page.
{: .important }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Cloud environment requirements

Your cloud environment must meet the following requirements:

- An existing AWS account or Azure subscription that contains your [[classic-nbs|NBS 6]] instance.
- A configured Domain Name System ([[dns]]) routing infrastructure.
- Permissions to create the following resources:
  - **AWS:** security groups and AWS Identity and Access Management ([[iam]]) roles
  - **Azure:** Network Security Groups ([[nsg|NSGs]]) and Azure Role-Based Access Control ([[azure-rbac|RBAC]]) role assignments
- Access to store [[terraform]] state files in an [[amazon-s3|S3]] bucket (AWS) or a storage account (Azure).

## Database and Windows Server requirements

Your existing NBS 6 environment provides the database server that NBS 7 reuses. Confirm that your existing server meets the following requirements. The compute, storage, and container resources for NBS 7 do not exist yet. Terraform creates them in [Provision cloud environment](provision-cloud-environment.html).

| Software | Supported versions |
|----------|---------|
| NBS Classic | See [Supported NBS versions](../../../supported-versions.html) |
| Microsoft Windows Server | **Windows Server 2022** - *preferred* <br>Windows Server 2025 |
| [[microsoft-sql-server]] | **SQL Server 2022 (16.x)** - *preferred* <br>SQL Server 2025 (17.x) |

## Management workstation setup

To configure, deploy, and maintain NBS 7, you need a local workstation or a cloud-hosted shell such as AWS CloudShell or Azure Cloud Shell. Install the following tools on that workstation. The table lists the minimum supported version and the install instructions for each tool:

| Tool | Minimum version | Install |
|----|----|----|
| Cloud provider [[cli]] | Latest AWS CLI or Azure CLI | **AWS:** [AWS CLI](https://aws.amazon.com/cli/); set up credentials with the [AWS CLI credential configuration guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html). **Azure:** [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli), plus [kubelogin](https://github.com/Azure/kubelogin), which `kubectl` requires for Azure authentication. |
| Terraform CLI | 1.15.6 | [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) |
| Helm CLI | 3.0 | [Helm CLI](https://helm.sh/docs/intro/install/) |
| kubectl | 1.25  | [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) |
| Docker | Latest | [Docker](https://docs.docker.com/get-started/get-docker/) |

## Network access requirements

NBS 7 infrastructure and microservices are deployed into a new [[amazon-vpc|VPC]] (AWS) or [[azure-vnet|VNet]] (Azure). The Terraform code in [Provision cloud environment](provision-cloud-environment.html) creates this network.

Confirm that network access is available from the NBS 7 components to the classic NBS 6 components, including the database server. The NBS 6 database must allow access from the NBS 7 VPC or VNet address space. Use a private route for this network access rather than a publicly accessible connection.

## Security requirements

### End-user authentication

NBS 7 supports end-user authentication by integrating with a standards-based Single Sign-On ([[sso]]) system. It is designed to be deployed as a protected endpoint within your existing SSO ecosystem, and it can be configured to work with standards-compliant [[idp|identity providers]] such as Okta and Active Directory.

This approach is similar to NBS 6, which does not authenticate users. Instead, NBS 6 delegates authentication to a security proxy that each [[stlt]] provides.

NBS 7 requires a working NBS 6 instance, so it assumes that a user authentication mechanism is already in place. NBS 7 works alongside the existing authentication mechanism. No additional steps are needed to authenticate users for NBS 7.

## Next steps

1. Complete the general [Prerequisites](../prerequisites.html) if you have not already.
1. Continue with [Provision cloud environment](provision-cloud-environment.html).
1. Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) if you have questions about AWS or Azure planning.
