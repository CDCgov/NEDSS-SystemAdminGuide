---
title: Configure cert-manager
layout: page
parent: Initial Kubernetes Deployment
nav_order: 3
nav_enabled: true
---

# Configure cert-manager (optional)
{: .no_toc }

cert-manager manages TLS certificates within the Kubernetes cluster. By default, cert-manager uses [Let's Encrypt](https://letsencrypt.org/) as the certificate authority for NiFi and modernization-api services.

> If you have manual certificates, skip steps 1–4 and store your certificates in Kubernetes secrets instead. See the [Kubernetes Secrets documentation](https://kubernetes.io/docs/concepts/configuration/secret/) for instructions.
{: .note }

1. Locate the cluster issuer manifest in the `nbs-helm-v7.X.0` zip file at `k8-manifests/cluster-issuer-prod.yaml`.

1. In `cluster-issuer-prod.yaml`, update the email address to a valid operations address. Let's Encrypt uses this address to notify you of upcoming certificate expirations if automatic renewal stops working.

1. From your terminal, apply the manifest:

   ```bash
   cd <HELM_DIR>/k8-manifests
   kubectl apply -f cluster-issuer-prod.yaml
   ```

1. Verify the cluster issuer is deployed and in a ready state:

   ```bash
   kubectl get clusterissuer
   ```

   You should see `letsencrypt-production` with a `READY` status of `True`.

   ![lets-encrypt](/NEDSS-SystemAdminGuide/docs/4_initial_kubernetes_deployment/images/2_lets-encrypt.png)
