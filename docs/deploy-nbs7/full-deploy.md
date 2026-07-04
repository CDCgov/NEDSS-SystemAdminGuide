---
title: NBS 7 full deployment
layout: page
parent: Deploy NBS 7
nav_order: 2
has_children: true
description: Complete step-by-step instructions for deploying NBS 7, from prerequisites through post-deployment cleanup.
---

# NBS 7 full deployment

This section walks you through the NBS 7 deployment process in full detail, from prerequisites and infrastructure setup through microservices deployment and cleanup. If you are familiar with deploying NBS 7, or with your cloud provider, Terraform, Kubernetes, and Helm, you can use the [Quick start](quickstart.html) instead. Both paths create the same infrastructure and services.

> Some of the steps in this section depend on previous steps. Complete each page in this section, including any nested subpages, in order.
{: .important }

## In this section

1. **[Prerequisites](full-deploy/prerequisites.html):** Verify your NBS 6 readiness, network access, DNS, security, and management workstation requirements.
1. **[Provision cloud infrastructure](full-deploy/provision-cloud-infrastructure.html):** Verify your cloud requirements, then use Terraform to create the virtual network, Kubernetes cluster, and supporting services in AWS or Azure.
1. **[Set up Kubernetes](full-deploy/kubernetes-setup.html):** Deploy the core Kubernetes services, then deploy and configure Keycloak.
1. **[Deploy NBS 7 microservices](microservices-deployment/deploy-nbs7-microservices.html):** Install and configure the NBS 7 application services with Helm.
1. **[Clean up after deployment](full-deploy/post-deploy-cleanup.html):** Remove temporary deployment artifacts and tighten access after a successful installation.
