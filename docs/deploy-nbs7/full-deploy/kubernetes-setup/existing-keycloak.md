---
title: Use an existing Keycloak
layout: page
parent: Deploy cluster services
nav_order: 3
description: Configure an existing Keycloak realm to authenticate NBS 7 users, including the OIDC client, the preferred_username claim mapping, NBS 6 user alignment, and the issuer and client secret that the microservices require.
---

# Integrate NBS 7 with an existing Keycloak

Use this path if your organization already runs [[keycloak]] and you want [[nbs-7]] to authenticate users against an existing realm, instead of deploying the NBS-provided Keycloak described in [Deploy and configure Keycloak](deploy-keycloak.html). On this path, you configure your existing realm with the client, claim mapping, and users that NBS 7 requires, and then supply the realm issuer and client secret to the NBS 7 microservices.

This page covers user authentication (browser login) against your existing realm. The NBS 7 backend service clients for data ingestion, NND, SRTE, and case notification are configured separately. See [Import service clients and retrieve secrets](deploy-keycloak.html#import-service-clients-and-retrieve-secrets).
{: .note }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

Before you begin the procedures on this page, confirm that you have the following:

- Administrator access to your existing Keycloak admin console.
- The target realm for NBS 7 users. Use an existing realm or create one before you begin.
- The public hostname or hostnames for your NBS 7 application, in the form `app.<DOMAIN_NAME.TLD>`. You need one entry for each deployed application host.
- Access to the [[classic-nbs|NBS 6]] database, to confirm that users exist in the `Auth_user` table.
- A secrets manager, such as [[aws-secrets-manager]] or [[azure-key-vault]], to store the client secret.

## Create or verify the NBS 7 client

NBS 7 uses an OpenID Connect ([[oidc]]) client for browser login. Create this client in the realm that authenticates NBS 7 users, or verify its configuration if it already exists.

1. Open the Keycloak admin console and select the target realm for NBS 7 users.
1. Navigate to **Clients** and create or open the client `nbs-modernization`.
1. Set the following values:

   | Setting | Value |
   |----|----|
   | Client type or protocol | OpenID Connect |
   | Client authentication | On (confidential) |
   | Standard flow | On |
   | Valid redirect URIs | `https://app.<DOMAIN_NAME.TLD>/login/oauth2/code/nbs-users` |
   | Valid post logout redirect URIs | `https://app.<DOMAIN_NAME.TLD>/nbs/logged-out` |
   | Web origins | `https://app.<DOMAIN_NAME.TLD>` |

1. Save the client.

Note the following when you configure the client:

- The **Root URL** can be left blank.
- Prefer full URLs for the redirect and post-logout values. Relative paths work in some setups, but full URLs are more reliable.
- Add one redirect URI and one web origin entry for each deployed application host. For example, add a second set of entries for `https://nbs.<DOMAIN_NAME.TLD>`.
- The `nbs-users` segment in the redirect URI is the application registration ID, not the realm name. Keep it as `nbs-users` unless the application registration is renamed everywhere.
- If you use a different client ID, such as `nbs-development`, all NBS 7 configuration must use that same client ID and secret.

## Map the preferred_username claim

NBS 7 expects the username in the `preferred_username` claim. Confirm that the realm's `profile` client scope includes a mapper that produces this claim, and create one if it is missing.

1. Navigate to **Client scopes** > **profile** > **Mappers**.
1. If a `username` mapper exists, open it and verify the following:
   - **Mapper type:** User Attribute
   - **User attribute:** `username`
   - **Token claim name:** `preferred_username`
1. If a `username` mapper does not exist, check pagination or search before you create one. To create it, select **Add mapper** > **By configuration** > **User Attribute**, and set the following:
   - **Name:** `username`
   - **User attribute:** `username`
   - **Token claim name:** `preferred_username`
   - **Add to ID token:** On
   - **Add to access token:** On
   - **Add to userinfo:** On
1. Save the mapper.

## Align Keycloak users with NBS 6 accounts

NBS 7 hands the logged-in username off to NBS 6. Each user who signs in to NBS 7 must exist as an ACTIVE `user_id` in the NBS 6 `Auth_user` table, or NBS 6 page access fails after a successful Keycloak login.

Confirm the user in Keycloak:

1. In the admin console, select the realm that NBS 7 uses.
1. Navigate to **Users** and search for the username, for example `superuser`.

If the user does not exist, create it:

1. Navigate to **Users** > **Add user**.
1. Enter the required fields:
   - **Username:** the NBS username, which must match the NBS 6 `Auth_user.user_id` value.
   - **Email verified:** On.
   - **Enabled:** On.
1. Select **Create**.
1. Open the new user, go to **Credentials**, and set a password. Set **Temporary** to Off so the user is not forced to reset the password on first login.
1. Select **Set password** and confirm.
1. Sign out of any active Keycloak session, then test that the new user can sign in.

Confirm the matching NBS 6 account exists and is active, as described in [NBS 6 user requirement](deploy-keycloak.html#nbs-6-user-requirement). For example, when `superuser` signs in to NBS 7, NBS 6 receives `UserName=superuser`, which must resolve to one ACTIVE row for that user.

## Provide OIDC values to the NBS 7 microservices

The NBS gateway and Modernization API authenticate users through your realm. When you deploy those services in [Deploy NBS 7 microservices](../../microservices-deployment/deploy-nbs7-microservices.html), set the client secret, and set the issuer URI only if your Keycloak is served at a different host than the NBS 7 application.

- **Client secret (required):** In **Clients** > **nbs-modernization** > **Credentials**, copy the client secret and store it in your secrets manager. Set it as the OIDC client secret (`oidc.client.secret`) for both `nbs-gateway` and `modernization-api`. This is the value described as `EXAMPLE_OIDC_SECRET` in the [Helm values reference](../../microservices-deployment/deploy-nbs7-microservices.html#helm-values-reference-for-nbs-7-microservices); use your existing realm's client secret in place of the NBS realm value.
- **Issuer URI (`oidc.uri`, usually blank):** Leave the issuer URI (`oidc.uri`) blank when your Keycloak is reached at the same application host, which is defined by the `ingressHost` parameter. NBS 7 derives the issuer from that host. Set `oidc.uri` explicitly only when your Keycloak is served at a different URL than the NBS 7 application. In that case, copy the `issuer` value from **Realm settings** > **OpenID Endpoint Configuration** (in the form `https://<keycloak-host>/realms/<realm-name>`, exactly as Keycloak returns it) and set it for both `nbs-gateway` and `modernization-api`.

After you set these values and run the Helm upgrade for those services, the `nbs-gateway` and `modernization-api` pods usually roll automatically because the pod specification changed. If they do not restart, trigger a rollout restart for both workloads.

## Troubleshooting

| Symptom | Likely cause |
|----|----|
| `/login?error` with Keycloak `CODE_TO_TOKEN_ERROR` and `invalid_client_credentials` | The client secret configured for `nbs-gateway` does not match the Keycloak client secret. |
| Keycloak `LOGIN_ERROR` with `invalid_user_credentials` | Wrong Keycloak username or password. |
| Login succeeds, but NBS 6 page access fails | The Keycloak username does not exist as an ACTIVE `user_id` in the NBS 6 `Auth_user` table. See [Align Keycloak users with NBS 6 accounts](#align-keycloak-users-with-nbs-6-accounts). |

## Next steps

Continue to [Deploy NBS 7 microservices](../../microservices-deployment/deploy-nbs7-microservices.html).
