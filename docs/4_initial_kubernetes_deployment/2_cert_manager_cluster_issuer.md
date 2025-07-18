---
title: Cert Manager
layout: page
parent: Initial Kubernetes Deployment
nav_order: 2
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Configure Cert manager Cluster Issuer (Optional automatic certificates)
Cert-manager is a tool to manage certificates within the Kubernetes cluster. By default, [LetsEncrypt](https://letsencrypt.org/) will used as a certificate authority/issuer for certificates for NIFI and modernization-api services. 
Note: If you have manual certificates, please skip below steps 1-4 and store your certificates manually in Kubernetes secrets and reference them in your configuration by following this [link](https://kubernetes.io/docs/concepts/configuration/secret/).
Set up cluster issuer for LetsEncrypt production certificate issuer:
- 1. Use the manifests provided as part of `nbs-helm-v7.X.0` zip file. The YAML manifests should be under `k8-manifests/cluster-issuer-prod.yaml`.
- 2. Update the email address in **cluster-issuer-prod.yaml** to be your valid operations email address. This email address will be used to notify any certificate expirations that are due for renewal. This will only occur if the automatic renewal stops working (as in the case of a decommissioned test system).
- 3. In your terminal, change your directory to `k8-manifests/` and run the following command to install the cluster issuer:
   ```bash
   cd <HELM_DIR>/k8-manifests
   kubectl apply -f cluster-issuer-prod.yaml
   ```
   You should see a cluster issuer created as shown below
- 4. Run the following command to make sure the cluster issuer is deployed properly and is in ready state:
   ```bash
   kubectl get clusterissuer
   ```
   You should see a letsencrypt-production true message as shown below
   ![lets-encrypt](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/images/2_lets-encrypt.png)
