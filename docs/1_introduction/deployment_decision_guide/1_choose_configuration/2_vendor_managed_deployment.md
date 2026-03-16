---
title: Vendor-managed deployment
layout: page
parent: Choose your configuration
grand_parent: About this guide
nav_order: 2
---

If you plan to use a vendor to host or maintain NBS 7, the guidance in this section applies to you.

Before you engage a vendor, confirm that they can:

- Deploy Kubernetes-based applications on AWS or Azure
- Manage Terraform-based infrastructure provisioning
- Support ongoing cloud infrastructure operations, including monitoring and incident response

> NBS 7 is a recent system with limited deployment history. Do not expect vendors to have direct NBS 7 experience. Evaluate vendors on their Kubernetes and cloud infrastructure expertise instead. You can share the [component reference](../../3_component_reference/) section of this guide with vendors to help them scope the work accurately.
{: .note }

Share the following with your vendor before scoping work:

- The [component reference](../../3_component_reference/) section of this guide
- The **NBS 7 Migration Info Sheet** (available from CDC)
- Your current NBS 6 hosting setup and data volumes

Then:

1. Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) to let CDC know you are planning a vendor-managed deployment and to access vendor coordination resources.
2. Work with your vendor to complete steps 4–8 of the [decision tree](../3_decision_tree/) to identify your recommended configuration tier.
3. Return to the [component reference](../../3_component_reference/) for the configuration parameters your vendor will need.

> Vendors with Kubernetes and cloud infrastructure expertise can deploy NBS 7, but they will need detailed technical guidance from CDC and from this guide to do it accurately. Plan for a close working relationship between your vendor and the CDC NBS team, especially during initial deployment. Also plan for the funding needed to sustain vendor support beyond initial deployment. Ongoing maintenance costs are a common planning gap.
{: .highlight }
