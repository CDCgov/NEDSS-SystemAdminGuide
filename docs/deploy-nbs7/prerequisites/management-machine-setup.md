---
title: Management machine setup
layout: page
parent: Prerequisites
grand_parent: Deploy NBS 7
nav_order: 3
---

## Management Machine Setup
{: .no_toc }
You will also need a local or cloud hosted workstation (e.g. CloudShell) with the set of tools required to configure, deploy and maintain the
NBS 7 system. The following tools should be installed on a local or cloud-based management machine to support this work:

- **AWS CLI**: Download and installation instructions can be found [here](https://aws.amazon.com/cli/)
  - Instructions for getting and using AWS credentials for use with the CLI can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

- **GitHub CLI**: Download and installation instructions are here:
  <https://cli.github.com/>

- **Terraform CLI**: Download and installation instructions are [here](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
  *(Tested through 1.5.5 Terraform, suggest install that specific version rather than the latest non-open source version)*

- **Helm CLI**: Download and installation instructions are [here](https://helm.sh/docs/intro/install/)

- **Kubernetes CLI**: Download and installation instructions are [here](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)

- **Optional, but nice to have, eksctl**: Download and installation instructions are [here](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)
