---
title: Network and database access
layout: page
parent: Prerequisites
grand_parent: Deploy NBS 7
nav_order: 4
---

## Network and Database Access
{: .no_toc }
Installation of the NBS 7 Modern infrastructure and microservices will occur using a new VPC, which is provisioned using the Terraform scripts included in the steps below.

You must ensure that there is network access available from the location of modern NBS 7 components to the classic NBS 6 components, including the database server. The database server or RDS should allow access to the nbs7 vpc address space. As a best practice, it is recommended to use a private route for this network access, rather than making it publicly accessible.

Furthermore, you should have a team member who is familiar with Terraform and has experience using it to create infrastructure. This individual should have operational knowledge of Terraform, even if they are not a dedicated Terraform developer.
