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
- `nifi.<site_name>.<domain>.com` (if you created a NiFi record during deployment)

## Remove Helm ingress resources

List the current Helm releases in the `traefik` namespace and verify the release name before uninstalling:

```bash
helm list --namespace traefik
helm uninstall --namespace traefik traefik
```

## Empty the OTEL collector storage bucket (AWS only)

<!-- [SME REVIEW] Does Azure use Azure Monitor natively (no OTEL collector bucket to empty), making this step AWS-only as documented here? The Azure observability Terraform module provisions Azure Monitor resources only. -->

On AWS, empty the S3 bucket that the OpenTelemetry (OTEL) collector uses for log storage before you run `terraform destroy`. Terraform cannot delete a non-empty S3 bucket, so the destroy fails if you skip this step. Complete this step manually in the AWS console or with the AWS CLI.

On Azure, observability uses Azure Monitor, which Terraform removes as part of `terraform destroy`. No manual storage cleanup is required.

## Destroy Terraform-managed infrastructure

```bash
terraform destroy
```

Review the plan output carefully before confirming. Terraform will display a summary of all resources it will delete.
