---
title: Decision tree
layout: page
parent: Choose your configuration
grand_parent: Before you deploy
nav_order: 1
description: A step-by-step decision tree that guides jurisdictions to a recommended NBS 7 starting configuration based on hosting model, capacity, and case volume.
---

# NBS 7 configuration decision tree
{: .no_toc }

Use the decision tree to identify your recommended starting configuration. Answer each question in order, then validate your recommendation with the CDC NBS team before you begin deployment.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

{: .important }
The decision tree identifies a recommended starting point, not a final answer. CDC provides free pre-deployment consultation to help jurisdictions validate their configuration choice. Connect with the CDC NBS team at [nbs@cdc.gov](mailto:nbs@cdc.gov) before you begin deployment.

## Step 1: Hosting model

Is your jurisdiction planning to self-host and self-maintain NBS 7, or will you use a vendor to host or maintain it?

- **Self-hosted, self-maintained** → Go to [Step 2](#step-2-state-it-security-approval).
- **Vendor-hosted or vendor-maintained** → Go to [Vendor-managed deployment](vendor-managed-deployment.html).

## Step 2: State IT security approval

Has your jurisdiction obtained state IT security approval for cloud hosting and the required software technologies (Kubernetes, Terraform, Docker)?

- **Yes, or approval is not required** → Go to [Step 3](#step-3-internal-technical-capacity).
- **No, or unknown** → Begin the approval process now, then continue planning. Approval is required before deployment. Go to [Step 3](#step-3-internal-technical-capacity).

Because NBS handles PII and PHI, state IT might still need to review and approve the deployment, even in vendor-managed models. See [State IT security approval takes time](../operational_considerations.html#state-it-security-approval-takes-time).
{: .note }

## Step 3: Internal technical capacity

Does your jurisdiction have IT staff with skills in Kubernetes, Terraform, and cloud infrastructure management, roughly half or more of the required skill set?

- **Yes** → Go to [Step 4](#step-4-current-nbs-6-hosting).
- **No** → Go to [Step 3a](#step-3a-external-assistance).

## Step 3a: External assistance

Will your jurisdiction obtain external assistance from a contractor, vendor, or consultant for deployment and ongoing maintenance?

- **Yes** → Go to [Step 4](#step-4-current-nbs-6-hosting). Note that your vendor or contractor must be capable of Kubernetes-based deployments on AWS or Azure. See [Vendor-managed deployment](vendor-managed-deployment.html) for what to look for.
- **No** → **Stop.** Build internal capacity or identify a vendor before proceeding. Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) for support resources.

## Step 4: Current NBS 6 hosting

Where does your NBS 6 currently run?

- **Already on AWS or Azure** → Staying on the same provider avoids additional procurement and approval steps. Go to [Step 5](#step-5-case-volume).
- **On-premises** → Your migration includes a cloud migration as well as an NBS 7 deployment. Plan for additional time and resources. Go to [Step 5](#step-5-case-volume).

## Step 5: Case volume

What is the approximate annual reportable disease case volume in your jurisdiction?

- **Lower volume** (fewer than approximately 50,000 cases per year) → Go to [Step 6](#step-6-data-intake-needs-lower-volume-jurisdictions).
- **Higher volume** (50,000+ cases per year), or significant growth expected → Go to [Step 7](#step-7-reporting-needs-higher-volume-jurisdictions).

{: .note }
The 50,000 case threshold is a planning guideline, not a hard rule. Validate your volume assessment with CDC before making a final configuration decision.

## Step 6: Data intake needs (lower-volume jurisdictions)

Does your jurisdiction currently receive high volumes of electronic lab reports (ELRs) or electronic case reports (eCRs)?

- **No** → Recommended starting point: **NBS 7**. Validate with CDC before deploying.
- **Yes** → Recommended starting point: **NBS 7 + DI API add-on**. Validate with CDC before deploying.

## Step 7: Reporting needs (higher-volume jurisdictions)

Does your jurisdiction need near-real-time reporting → data available within minutes to hours, rather than 24 hours?

- **No** → Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) to discuss your specific needs. **NBS 7** or **NBS 7 + DI API add-on** might be appropriate starting points.
- **Yes** → Go to [Step 8](#step-8-data-intake-needs-higher-volume-jurisdictions).

## Step 8: Data intake needs (higher-volume jurisdictions)

Does your jurisdiction currently receive high volumes of ELRs or eCRs?

- **No** → Recommended starting point: **NBS 7 + RTR add-on**. Validate with CDC before deploying.
- **Yes** → Recommended starting point: **NBS 7 + RTR + DI API add-ons**. Validate with CDC before deploying.
