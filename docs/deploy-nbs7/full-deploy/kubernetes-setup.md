---
title: 3. Kubernetes setup
layout: page
parent: NBS 7 full deployment
nav_order: 3
has_children: true
description: Deploy core Kubernetes services and Keycloak before deploying NBS 7 application services.
redirect_from:
  - /docs/deploy-nbs7/cluster-infrastructure.html
  - /docs/deploy-nbs7/cluster-infrastructure/
---

# Deploy cluster infrastructure
{: .no_toc }

This phase installs the core infrastructure services that NBS 7 application components depend on. This includes the Kubernetes networking and certificate management stack, as well as Keycloak for identity and access management.

Complete the steps in this phase in order before proceeding to [Deploy NBS 7 microservices](../microservices-deployment/deploy-nbs7-microservices.html).
