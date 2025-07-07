---
title: Validating API endpoints
layout: page
parent: NND Service (Data Sync)
nav_order: 1
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Validating API endpoints
STLT must ensure they have a proper connection to the Data APIs, and that the API endpoint is correctly provided and detailed in the accompanying Swagger documentation. Typically, these API endpoints are not accessed directly by human users; instead, they are invoked by the Data Sync service. 

But, users should verify that the connection is successfully established before proceeding with any operations. Please follow the below steps to validate the provided endpoints availability.

Call the token generation endpoint through the Postman API client to ensure the data sync API is up and running.

The Token Generation endpoint is designed to provide a token for authorized access to secured endpoints.

**Endpoint:** https://<<host>>/data-sync/api/auth/token
Ex: https://data.dts1.nbspreview.com/data-sync/api/auth/token

**Pre-Requisite:** The clientid and clientsecret has been created by the STLT Administrator

**HTTP Method:** POST

**Authorization Type:** NONE

**Custom Headers:** Enter 2 new headers called `clientid` and `clientsecret` along with their values.

![nnd-api-endpoint-testing-1](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/images/nnd-api-testing-1.png)

Click 'Send,' and the response should be below. Ensure the response code is 200 OK, and the JWT token is generated.

![nnd-api-endpoint-testing-2](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/images/nnd-api-testing-2.png)

- Once you receive the Token, you can validate the actual API endpoint for the service using Swagger:
  - [https://<<HOST>>/data-sync/swagger-ui/index.html](https://<<HOST>>/data-sync/swagger-ui/index.html)

> ℹ️ **We recommend Postman for endpoint validation although you can use Swagger**
