---
title: 5. Post-deploy cleanup
layout: page
parent: NBS 7 full deployment
nav_order: 5
description: Steps to remove temporary deployment artifacts and tighten access after a successful NBS 7 installation.
redirect_from:
  - /docs/deploy-nbs7/post-install-cleanup.html
  - /docs/deploy-nbs7/post-install-cleanup/
---

# Post-install cleanup for NBS 7 deployments

After go-live is confirmed stable, complete the following cleanup tasks to remove temporary artifacts from the deployment process and tighten your security posture.

> Complete these steps only after go-live has been validated and your team confirms that the production environment is stable.
{: .important }

## Cleanup checklist

The following table contains common cleanup tasks that might not apply to your deployment scenario. Confirm which apply to your  configuration before proceeding.

| Task | Notes |
|:---|:---|
| Remove or rotate temporary deployment credentials | Revoke any service account tokens, API keys, or database passwords created specifically for the installation process |
| Remove installer or bootstrap Kubernetes jobs | Delete one-time Jobs or Pods that ran during cluster setup and are no longer needed |
| Remove migration environment resources | Decommission dev or staging environments used during the cutover if they are no longer needed |
| Archive NBS 6 resources | Once production NBS 7 is confirmed stable, follow your jurisdiction's data retention policy for NBS 6 application and configuration artifacts |
| Review IAM roles and permissions | Remove any over-permissioned roles granted during deployment; confirm only operations-level access remains |
| Confirm monitoring and alerting coverage | Verify that observability tooling is capturing production-level baselines and that alert thresholds are set appropriately |
