---
title: Case notifications
layout: page
parent: Deploy NBS 7 microservices
nav_order: 9
has_children: true
nav_enabled: true
redirect_from:
  - /docs/6_microservices_deployment/9_case_notification.html
  - /docs/6_microservices_deployment/9_case_notification/
  - /docs/6_microservices_deployment/9b_keycloak_configuration.html
---

# Deploy case notifications
This section sets out the detailed steps to installing NBS 7 Case Notification, end to end.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Overview

Case notifications comprise three services and should be deployed in the following order:

  1. [Debezium](../../deploy-nbs7/microservices-deployment/case-notification/debezium.html)
  1. [Data extraction service](../../deploy-nbs7/microservices-deployment/case-notification/data-extraction.html)
  1. [Notification service](../../deploy-nbs7/microservices-deployment/case-notification/case-notification-service.html)

Services 2 and 3 require you to first set up [Keycloak configuration](#keycloak-configuration). After you deploy all required services for case notifications, validate with [API testing](../../deploy-nbs7/microservices-deployment/case-notification/api-testing.html).

## Considerations

Case notifications are optional. Your jurisdiction can use either the NBS 7 case notification services or continue to route case notifications through Rhapsody.

- **If you are continuing with Rhapsody**, skip this section. Do not deploy any of the four services listed above, and do not enable them in Kubernetes.
- **If you are moving to NBS 7 case notifications**, complete all four services in the order listed.

## Dependencies

Case notifications require [NND Sync](../../deploy-nbs7/microservices-deployment/nnd-service.html) for the full pipeline to function. Set up NND Sync before deploying case notification services. NND Sync is the only dependency. RDB Data Sync is not required.

## Keycloak configuration

The data extraction and notification services require Keycloak. Complete this configuration before deploying them.

1. In each service's `values.yaml`, confirm the Keycloak auth URI. In the default configuration this value should not need to change unless the name or namespace of the Keycloak pod is modified.

   ```yaml
   authUri: "http://keycloak.default.svc.cluster.local/auth/realms/NBS"
   ```

1. For each of the three services, import the corresponding Keycloak profile from [`NEDSS-Helm/charts/keycloak/extra`][nedss-helm-keycloak-extra].

{: .note }

[nedss-helm-keycloak-extra]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/keycloak/extra>
