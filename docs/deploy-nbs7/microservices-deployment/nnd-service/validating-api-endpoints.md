---
title: Validate API endpoints
layout: page
parent: NND Service (Data Sync)
nav_order: 1
redirect_from:
  - /docs/6_microservices_deployment/8a_nnd_api_tesing.html
  - /docs/6_microservices_deployment/8a_nnd_api_tesing/
---

# Validate API endpoints

Use this check to confirm that your environment can reach the Data Sync API before you sync data.

In production, the Data Sync service calls these endpoints. System administrators still need to validate connectivity and credentials during setup.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Validate token generation in Postman

The token endpoint returns a JWT token that clients use to access secured Data Sync endpoints.

**Endpoint:** `https://data.<your-site>.<your-domain>.com/data-sync/api/auth/token`

**Prerequisite:** The STLT administrator must create values for `clientid` and `clientsecret`.

**HTTP method:** `POST`

**Authorization type:** `NONE`

1. Open Postman and send a `POST` request to the token endpoint.
1. Add two request headers:
   - `clientid`
   - `clientsecret`

![Postman request configured for token generation endpoint with clientid and clientsecret headers](../images/nnd-api-testing-1.png)

1. Select **Send**.
1. Confirm that the response status is `200 OK` and that a JWT token returns.

![Postman response showing HTTP 200 OK and returned JWT token](../images/nnd-api-testing-2.png)

## Validate service endpoints in Swagger

After token generation succeeds, validate the service endpoints in Swagger:

`https://<host>/data-sync/swagger-ui/index.html`

> Use Postman for endpoint validation. You can also use Swagger to inspect and test endpoints.
{: .note }
