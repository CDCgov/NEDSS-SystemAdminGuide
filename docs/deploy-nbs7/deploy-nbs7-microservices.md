---
title: Deploy NBS 7 microservices
layout: page
parent: Deploy NBS 7
nav_order: 5
has_children: true
description: Install and configure NBS 7 application services using Helm, including Elasticsearch, NiFi, the Modernization API, and optional add-ons such as Real-Time Reporting.
---

# Deploy NBS 7 microservices
{: .no_toc }

This phase deploys the NBS 7 application services into your Kubernetes cluster using Helm. Deploy services in the order listed — each service has dependencies on the ones before it.

After completing this phase, proceed to [Validate the deployment](validate-the-deployment.html).
