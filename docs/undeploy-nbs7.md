---
title: Undeploy NBS 7
layout: page
nav_order: 5
description: Steps to remove DNS entries, Helm ingress resources, and Terraform-managed infrastructure when decommissioning an NBS 7 environment.
redirect_from:
  - /docs/removal_and_cleanup.html
  - /docs/removal_and_cleanup/
  - /docs/deploy-nbs7/removal-and-cleanup.html
  - /docs/deploy-nbs7/removal-and-cleanup/
---

# Remove an NBS 7 environment

Use this procedure to decommission an NBS 7 environment that was deployed using Terraform and Helm. This applies to development, staging, and production environments. Complete the steps in the order shown. Helm resources must be removed before you run `terraform destroy`.

> These steps are irreversible. Removing ingress resources immediately interrupts access to NBS 7 endpoints in this environment. Running `terraform destroy` permanently deletes all infrastructure managed by this Terraform workspace.
{: .warning }

## Before you begin

- Confirm that this is the correct environment and that you have approval to decommission it
- Verify that any data you need to retain has been exported or backed up
- Confirm that no active users or dependent systems are connected to this environment

## Remove DNS entries

Remove the DNS records for this environment from your DNS provider:

- `app.<site_name>.<domain>.com`
- `data.<site_name>.<domain>.com`

## Remove Helm ingress resources

List the current Helm releases in the `ingress-nginx` namespace and verify the release name before uninstalling:

```bash
helm list --namespace ingress-nginx
helm uninstall --namespace ingress-nginx ingress-nginx
```

## Empty the FluentBit S3 bucket

Empty the S3 bucket used by FluentBit for log storage before running `terraform destroy`. Terraform cannot delete a non-empty S3 bucket and the destroy will fail if this step is skipped. Complete this step manually in the AWS Console or using the AWS CLI.

## Destroy Terraform-managed infrastructure

```bash
terraform destroy
```

Review the plan output carefully before confirming. Terraform will display a summary of all resources it will delete.
