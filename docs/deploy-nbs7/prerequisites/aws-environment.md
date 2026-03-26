---
title: AWS environment
layout: page
parent: AWS prerequisites
nav_order: 1
---

# AWS environment requirements
{: .no_toc }

Your AWS environment must:

- Contain a pre-existing AWS account that contains a [supported production instance of NBS 6](../../../docs/before-you-deploy/compatibility.html) and related 3rd party products such as Rhapsody and SAS
- Have a properly configured DNS routing infrastructure
- Be configured to enable you to create security groups and IAM roles
- Provide access to NBS 6 databases that are located on an MS SQL Server instance (RDS or EC2)
- Have access to an S3 bucket to store Terraform (TF) state
