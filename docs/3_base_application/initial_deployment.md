---
title: Initial Kubernetes Bootstrapping
layout: page
parent: AWS Infrastructure
nav_order: 2
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
## Initial Kubernetes Bootstrapping

1. Download the Helm configuration package from GitHub. Make sure you go through the release page and see what's included [Latest release of CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/releases).
2. Open bash/mac/cloudshell/powershell and unzip the downloaded nbs-helm-v7.5.0 zip file.
3. **All helm commands should be executed from the charts directory.** Change directory to where you unzipped the helm **charts** folder `<Helm_Dir>/charts`.

---

## Deploy NGINX ingress controller on the Kubernetes cluster

1. NGINX will use the values in `charts/nginx-ingress/values.yaml` as a part of `nbs-helm-v1.1.7.1` zip file. These values have been preconfigured to setup Prometheus to scrape metrics and also to instruct NGINX controller to create AWS network load balancer instead of classic load balancer in front of the k8 NGINX ingress.
  - a. The result of the command below should create NGINX controller within Kubernetes.
      ```bash
      helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx
      ```
      ![ingress-nginx](/just-the-doc/docs/3_base_application/images/ingress-controller.png)
  - b. Monitor the status of the nginx deployment
      ```bash
      kubectl --namespace ingress-nginx get services -o wide -w ingress-nginx-controller
      ```
      NOTE: Use Ctrl+c to exit if the command is still running.
  - c. You may also check that a network load balancer was created in the AWS web console and the target groups are pointing to the EKS cluster [List of load balancers](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#LoadBalancers:)
  - d. Run the following command to confirm at least one NGINX controller pod is running
      ```bash
      kubectl get pods -n=ingress-nginx
      ```
2. You will need to manually create some DNS entries. Ensure that the following DNS entries (A records) point to the new network load balancer in front of your Kubernetes cluster (make sure this is the ACTIVE NLB just provisioned via nginx-ingress). This should be done in your DNS service (For eg: Route 53). Please replace example.com with the appropriate domain_name from the Table-3 below.
  - a. Modernized NBS Application - Eg: app.example.com
  - Data Services -
  - NIFI application - Eg: nifi.example.com [Note: NIFI has reported vulnerabiltiies. Please expose only if you absolutely need it and want to adminsiter it. Otherwise, dont add NIFI].
    These are the 5 required URL’s for NBS
    {: .no_toc }
    
    | **Parameter**                           | **Template Value**                                  | **Example**                          |
    |----------------------------------------|-----------------------------------------------------|--------------------------------------|
    | nbs domain                             | site_name.example_domain.com                        | fts3.nbspreview.com                  |
    | classic sub_domain (NBS 6)             | app-classic.site_name.example_domain.com            | app-classic.fts3.nbspreview.com      |
    | app sub_domain (Modern NBS 7)          | app.site_name.example_domain.com                    | app.fts3.nbspreview.com              |
    | nifi sub_domain (Nifi) [Optional, only if you want to administer NIFI] | nifi.site_name.example_domain.com                   | nifi.fts3.nbspreview.com             |
    | data ingestion sub_domain (DI)         | data.site_name.example_domain.com                   | data.fts3.nbspreview.com             |
