---
title: Deploy NGINX ingress controller
layout: page
parent: Initial Kubernetes Deployment
nav_order: 2
nav_enabled: true
---

# Deploy NGINX ingress controller on the Kubernetes cluster
{: .no_toc }

<!--
## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}
-->

After you create and deploy your Kubernetes secrets, set up the NGINX ingress controller. This page explains how to use the preconfigured Helm values to install the controller, verify that the AWS network load balancer is active, and create the DNS records your cluster needs to route traffic. After you complete these steps, configure Cert Manager to manage TLS certificates for your cluster.

## Install the NGINX ingress controller

The values in `charts/nginx-ingress/values.yaml` (part of the `nbs-helm-vX.Y.Z` zip file) are preconfigured to set up Prometheus metrics scraping and to instruct the NGINX controller to create an AWS network load balancer instead of a classic load balancer.

1. Install the NGINX ingress controller:

   ```bash
   helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx -f ./nginx-ingress/values.yaml --namespace ingress-nginx --create-namespace --version 4.11.5
   ```

   ![ingress-nginx](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/images/1_ingress-controller.png)

1. Monitor the deployment status:

   ```bash
   kubectl --namespace ingress-nginx get services -o wide -w ingress-nginx-controller
   ```

   > Use `Ctrl+C` to exit if the command is still running.
   {: .note }

1. In the [AWS load balancers console](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#LoadBalancers:), confirm a network load balancer was created and its target groups point to the EKS cluster.

1. Confirm at least one NGINX controller pod is running:

   ```bash
   kubectl get pods -n=ingress-nginx
   ```

## Create DNS records

Create A records in your DNS service (for example, Route 53) pointing the following subdomains to the active network load balancer provisioned above. Replace `example_domain.com` with your domain name.

> NiFi has known security vulnerabilities. Only add a NiFi DNS entry if you need to administer it directly. Omit it otherwise.
{: .warning }

| Subdomain | Template | Example |
|---|---|---|
| NBS (main domain) | `site_name.example_domain.com` | `fts3.nbspreview.com` |
| NBS 6 (classic) | `app-classic.site_name.example_domain.com` | `app-classic.fts3.nbspreview.com` |
| NBS 7 (modern) | `app.site_name.example_domain.com` | `app.fts3.nbspreview.com` |
| NiFi (optional) | `nifi.site_name.example_domain.com` | `nifi.fts3.nbspreview.com` |
| Data Ingestion | `data.site_name.example_domain.com` | `data.fts3.nbspreview.com` |
