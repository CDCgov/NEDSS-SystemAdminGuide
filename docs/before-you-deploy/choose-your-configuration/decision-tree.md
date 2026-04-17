---
title: Decision tree
layout: page
parent: Choose your configuration
grand_parent: Before you deploy
nav_order: 1
description: A step-by-step decision tree that guides jurisdictions to a suggested NBS 7 starting configuration based on hosting model, capacity, and case volume.
---

# NBS 7 configuration decision tree

Use this decision tree to determine a baseline deployment model for your jurisdiction. Answer the questions in sequence to identify the suggested architecture for your infrastructure and integration needs.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

{: .important }
The decision tree identifies a potential starting point, not a final answer. CDC provides free pre-deployment consultation to help jurisdictions validate their configuration choice. Connect with the CDC NBS team at [nbs@cdc.gov](mailto:nbs@cdc.gov) before you begin deployment.

## Step 1: State IT security approval

Has your jurisdiction obtained state IT security approval for cloud hosting and the required software technologies (Kubernetes, Terraform, Docker)?

- **Yes, or approval is not required** → Go to [Step 2](#step-2-internal-technical-capacity).
- **No, or unknown** → It's a good idea to begin the approval process now, then continue planning. Approval is typically required before deployment. Go to [Step 2](#step-2-internal-technical-capacity).

Because NBS handles PII and PHI, state IT might still need to review and approve the deployment, even in vendor-managed models. For more information, see [State IT security approval takes time](../operational-considerations.html#state-it-security-approval-takes-time) on the Operational Considerations page.
{: .note }

## Step 2: Internal technical capacity

Does your jurisdiction have IT staff with skills in Kubernetes, Terraform, and cloud infrastructure management, roughly half or more of the required skill set?

- **Yes** → Go to [Step 3](#step-3-current-nbs-6-hosting).
- **No** → Go to [Step 2a](#step-2a-external-assistance).

For more information on technical capacity, see [Technical staffing requirements differ from NBS 6](../operational-considerations.html#technical-staffing-requirements-differ-from-nbs-6) on the Operational Considerations page.
{: .note }

## Step 2a: External assistance

Will your jurisdiction obtain external assistance from a contractor, vendor, or consultant for deployment and ongoing maintenance?

- **Yes** → Go to [Step 3](#step-3-current-nbs-6-hosting). Note that your vendor or contractor must be capable of Kubernetes-based deployments on AWS or Azure. See [Vendor-managed deployment](vendor-managed-deployment.html) for what to look for.
- **No** → **Stop.** Build internal capacity or identify a vendor before proceeding. Contact [nbs@cdc.gov](mailto:nbs@cdc.gov) for support resources.

## Step 3: Current NBS 6 hosting

Where does your NBS 6 currently run?

- **Already on AWS or Azure** → Staying on the same provider avoids additional procurement and approval steps. Go to [Step 4](#step-4-reporting-needs).
- **On-premises** → Your migration includes a cloud migration as well as an NBS 7 deployment. Plan for additional time and resources. Go to [Step 4](#step-4-reporting-needs).

This step is informational and does not impact your suggested deployment configuration. For more information, see [Align cloud provider with jurisdictional strategy](../operational-considerations.html#align-cloud-provider-with-jurisdictional-strategy) on the Operational Considerations page.
{: .note }

## Step 4: Reporting needs

Does your jurisdiction need near-real-time reporting (data available within minutes to hours, rather than 24 hours)?

- **Yes** → Go to [Step 5a](#step-5a-database-access-requirements-real-time-reporting-path).
- **No** → Go to [Step 5b](#step-5b-database-access-requirements-legacy-batch-reporting-path).

Real-time reporting adds infrastructure complexity and requires additional cloud resources. For more information, see [Real-Time Reporting adds capability and cost](../operational-considerations.html#real-time-reporting-adds-capability-and-cost) on the Operational Considerations page.
{: .note }

## Step 5a: Database access requirements (real-time reporting path)

Some jurisdictions have security policies that prohibit third-party tools from writing directly to the database or require an intermediary layer when middleware and the database cannot be co-located.

**Does your jurisdiction require an API layer to abstract database access?**

- **Yes** → Suggested starting point: **NBS 7 + RTR + DI API add-ons**.
- **No** → Suggested starting point: **NBS 7 + RTR add-on**.

## Step 5b: Database access requirements (legacy batch reporting path)

Some jurisdictions have security policies that prohibit third-party tools from writing directly to the database or require an intermediary layer when middleware and the database cannot be co-located.

**Does your jurisdiction require an API layer to abstract database access?**

- **Yes** → Suggested starting point: **NBS 7 + DI API add-on**.
- **No** → Suggested starting point: **NBS 7 (no add-ons)**.

For more information, see [The Data Ingestion API adds a secure integration option](../operational-considerations.html#the-data-ingestion-api-adds-a-secure-integration-option) on the Operational Considerations page.
{: .note }

---

## Next steps: Estimate infrastructure costs

After you determine your deployment model, you can use the jurisdictional sizing criteria provided in this section to identify which resource profile to use in the **NBS 7 Resource Estimator**. The estimator is an Excel-based tool available on NBS Central. It provides baseline values for provisioned resources, including compute (vCPU and Memory), SQL storage, and Kafka brokers. 

The following thresholds help you identify your profile for the estimator:

| If your jurisdiction has... | And an estimated case volume of... | Use this profile |
| :--- | :--- | :--- |
| **Fewer than 5 million** person records | **Fewer than 200,000** cases | Small STLT |
| **5 million to 15 million** person records | **200,000 to 700,000** cases | Medium STLT |
| **More than 15 million** person records | **More than 700,000** cases | Large STLT |

>Handling discrepancies
>
>If your metrics fall into different tiers (for example, your person records are "Small" but your case volume is "Medium"), select the **higher tier**. Scaling for the larger metric ensures your infrastructure can handle both the total data volume and the active processing load.
{: .important-title }

If you don't know number of person records in your system, run the following SQL query against the `NBS_ODSE` database to provide the total:

```sql
select count(*) from NBS_ODSE.dbo.Person
```

To generate a monthly cost estimate for your deployment scenario:

1. Log in to [NBS Central](https://nbscentral.cdc.gov/) and download the latest **[NBS 7 Resource Estimator](https://nbscentral.cdc.gov/documents/872)**.
1. Identify the tab that matches your jurisdictional size.
1. Input the quantities and suggested SKUs from that tab into the AWS Pricing Calculator or Azure Pricing Calculator.

{: .note }
Actual resource requirements vary based on data patterns, integration complexity, user activity, and reporting load. Monitoring actual utilization allows for configuration adjustments based on performance metrics.
