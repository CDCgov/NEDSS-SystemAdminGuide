---
title: 3. Set up Kubernetes
layout: page
parent: NBS 7 full deployment
nav_order: 3
has_children: true
has_toc: false
description: Configure your Kubernetes cluster and deploy the core services and Keycloak that the NBS 7 microservices depend on.
redirect_from:
  - /docs/deploy-nbs7/cluster-infrastructure.html
  - /docs/deploy-nbs7/cluster-infrastructure/
---

# Set up Kubernetes for NBS 7

This phase performs the deployments and configuration in your Kubernetes cluster that the NBS 7 microservices depend on. You first enable Linkerd for the namespace that the microservices deploy into, then deploy the core Kubernetes services, and then deploy and configure Keycloak.

> The `kubectl` commands in this phase require the cluster connection you configured in [Connect to Kubernetes cluster](provision-cloud-infrastructure/provision-cloud-environment.html#connect-to-kubernetes-cluster).
{: .note }

## Enable Linkerd for the default namespace

Linkerd provides mutual TLS (mTLS) between the NBS 7 microservices, all of which are deployed to the default Kubernetes namespace. Complete these steps to enable Linkerd for that namespace:

1. Annotate the default namespace:

   ```bash
   kubectl annotate namespace default "linkerd.io/inject=enabled"
   ```

   The output should be `namespace/default annotated`.

1. Verify that the annotation is in place:

   ```bash
   kubectl get namespace default -o=jsonpath='{.metadata.annotations}'
   ```

   The output should include `"linkerd.io/inject":"enabled"`.

1. If this is an update rather than a new installation, that is, if you already completed steps in the [Deploy NBS 7 microservices](../microservices-deployment/deploy-nbs7-microservices.html) section for this environment, restart the pods in the default namespace so that each pod gets a Linkerd sidecar container:

   ```bash
   kubectl get pods -n default -o custom-columns=":metadata.name" | xargs kubectl delete pod -n default
   ```

   Restarted pods show `2/2` in the `READY` column of `kubectl get pods` output.

<!-- The "Create Kubernetes secrets" section was deleted per Josh Olson's confirmation (2026-07-06): nbs-secrets.yaml was removed from NEDSS-Helm, and the reporting-pipeline-service chart takes configuration through its values file. Credential configuration for that service is tracked under STLT-538 with Eric Buckley and the Dragon team. -->

## In this section

Complete the pages in this section in order:

1. **[Deploy core services](kubernetes-setup/deploy-core-services.html)**: Get the NEDSS-Helm charts and install the core Kubernetes services that NBS 7 depends on, including the Traefik ingress controller and cert-manager.
1. **[Deploy and configure Keycloak](kubernetes-setup/deploy-keycloak.html)**: Install Keycloak, configure the NBS realms and service clients, and complete the final validation of Traefik and Keycloak.
