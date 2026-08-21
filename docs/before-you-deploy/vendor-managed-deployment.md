---
title: Working with a vendor
layout: page
parent: Before you deploy NBS 7
nav_order: 4
description: Guidance for jurisdictions using a vendor to host or maintain NBS 7, including what to evaluate in a vendor and how to coordinate with CDC.
---

# Vendor-managed NBS 7 deployments

If you plan to use a vendor to host or maintain {% include term-tooltip.html key="nbs-7" term="NBS 7" id="vendor-nbs-7" %}, confirm that they can:

- Deploy {% include term-tooltip.html key="kubernetes" term="Kubernetes" id="vendor-kubernetes" %}-based applications on {% include term-tooltip.html key="aws" term="AWS" id="vendor-aws" %} or {% include term-tooltip.html key="microsoft-azure" term="Azure" id="vendor-azure" %}
- Manage {% include term-tooltip.html key="terraform" term="Terraform" id="vendor-terraform" %}-based infrastructure provisioning
- Support ongoing cloud infrastructure operations, including monitoring and incident response

> NBS 7 is a recent system with limited deployment history. Do not expect vendors to have direct NBS 7 experience. Evaluate vendors on their Kubernetes and cloud infrastructure expertise instead. You can share the [component reference](../before-you-deploy/component-reference.html) section of this guide with vendors to help them scope the work accurately.
{: .important }

Share the following with your vendor before scoping work:

- The [component reference](../before-you-deploy/component-reference.html) section of this guide
- The [NBS 7 Migration Info Sheet](https://nbscentral.cdc.gov/documents/731) from {% include term-tooltip.html key="nbs-central" term="NBS Central" id="vendor-nbs-central" %}
- Your current {% include term-tooltip.html key="classic-nbs" term="NBS 6" id="vendor-nbs-6" %} hosting setup and data volumes

Then:

1. Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) to let CDC know you are planning a vendor-managed deployment and to access vendor coordination resources.
2. Work with your vendor to review the [NBS 7 deployment phases](../before-you-deploy/deployment-phases.html) to plan your timeline.
3. Refer to the [component reference](../before-you-deploy/component-reference.html) for the configuration parameters your vendor will need.

> Vendors with Kubernetes and cloud infrastructure expertise can deploy NBS 7, but they will need detailed technical guidance from CDC and from this guide to do it accurately. Plan for a close working relationship between your vendor and the CDC NBS team, especially during initial deployment. Also plan for the funding needed to sustain vendor support beyond initial deployment. Ongoing maintenance costs are a common planning gap. Use the [NBS 7 Resource Estimator](https://nbscentral.cdc.gov/documents/872) from {% include term-tooltip.html key="nbs-central" term="NBS Central" id="vendor-nbs-central-2" %} to support cloud cost projections.
{: .note }
