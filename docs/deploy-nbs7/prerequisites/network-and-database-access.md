---
title: Network and DB access
layout: page
parent: AWS prerequisites
nav_order: 4
---

# Network and database access requirements for AWS deployments

Installation of the NBS 7 infrastructure and microservices uses a new VPC, which is provisioned using the Terraform scripts included in [the provisioning steps](../../../docs/deploy-nbs7/aws-infrastructure/aws-infrastructure.html).

You must ensure that there is network access available from the location of modern NBS 7 components to the classic NBS 6 components, including the database server. The database server or RDS should allow access to the NBS 7 VPC address space. As a best practice, use a private route for this network access, rather than making it publicly accessible.

A team member who has operational knowledge of and is familiar with using Terraform is most suited to create this infrastructure.
