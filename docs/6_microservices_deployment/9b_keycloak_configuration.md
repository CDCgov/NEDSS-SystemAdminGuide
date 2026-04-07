---
title: Keycloak Configuration
layout: page
parent: Case Notification
grand_parent: Microservices Deployment
nav_order: 2
nav_enabled: true
---

# Keycloak Configuration
{: .no_toc }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

1. Keycloak Auth URI. Provide keycloak auth uri in the values.yaml file as shown below. In the default configuration this value should not need to change unless the name or namespace of the keycloak pod is modified.

   ```yaml
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   ```

2. The 3 Case notification service except for Debezium will also need keycloak profile
   [NEDSS-Helm/charts/keycloak/extra at main · CDCgov/NEDSS-Helm](https://github.com/CDCgov/NEDSS-Helm/tree/main/charts/keycloak/extra)
