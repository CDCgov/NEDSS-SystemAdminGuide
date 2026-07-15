---
title: Validate API endpoints
layout: page
parent: NND Service (Data Sync)
nav_order: 2
redirect_from:
  - /docs/6_microservices_deployment/8a_nnd_api_tesing.html
  - /docs/6_microservices_deployment/8a_nnd_api_tesing/
---

# Validate API endpoints

Use this check to confirm that your environment can reach the Data Sync API before you sync data. In production, the Data Sync service calls these endpoints. System administrators still need to validate connectivity and credentials during setup. Complete [Deploy Data Sync service API (cloud)](./deploy-data-sync-service-api-cloud.html) before starting this page. After you finish validating, proceed to [Deploy NND Sync](./on-prem-nnd-sync.html) or [Deploy Data Availability (on-premises)](./on-prem-data-sync.html).

> This page is part of the optional [NND Service (Data Sync)](../nnd-service.html) section. CDC is evaluating long-term support for this service. If your STLT has a use case, contact [nbs@cdc.gov](mailto:nbs@cdc.gov).
{: .important }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

Complete [Deploy Data Sync service API (cloud)](./deploy-data-sync-service-api-cloud.html) deployment before you begin. This procedure uses Postman to send API requests. Download and install Postman from the [Postman installation page](https://learning.postman.com/docs/getting-started/installation/installation-and-updates).

You need a Keycloak client ID and client secret for the Data Sync service. Retrieve these from your Keycloak instance. See [Access the Keycloak admin interface](../../full-deploy/kubernetes-setup/deploy-keycloak.html#access-the-keycloak-admin-interface) for port forwarding instructions and steps to access the Keycloak UI. In the **NBS** realm, go to **Clients** > `nnd-keycloak-client` > **Credentials** > **Client Secret**.

## Validate token generation in Postman

The token endpoint returns a JWT token that clients use to access secured Data Sync endpoints. Send a `POST` request to the following endpoint:

`https://data.<your-site>.<your-domain>.com/data-sync/api/auth/token`

Use `NONE` as the authorization type.

1. Open Postman and send a `POST` request to the token endpoint.
1. Add two request headers using the credentials from your Keycloak instance:
   - `clientid`
   - `clientsecret`

   The following screenshot shows the request configured in Postman:

   ![Postman request configured for token generation endpoint with clientid and clientsecret headers](../images/nnd-api-testing-1.png)

1. Select **Send**.
1. Confirm that the response status is `200 OK` and that a JWT token returns.

   The following screenshot shows an example successful response:

   ![Postman response showing HTTP 200 OK and returned JWT token](../images/nnd-api-testing-2.png)

## Validate service endpoints in Swagger

After token generation succeeds, validate the service endpoints in Swagger:

`https://<host>/data-sync/swagger-ui/index.html`
