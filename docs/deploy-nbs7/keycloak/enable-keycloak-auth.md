---
title: Enable Keycloak auth
layout: page
parent: Deploy cluster infrastructure
nav_order: 3
nav_enabled: true
redirect_from:
  - /docs/5_keycloak/2_enable_keycloak_auth.html
  - /docs/5_keycloak/2_enable_keycloak_auth/
---

# Enable Keycloak Auth
{: .no_toc }

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Verify Keycloak is running

1. Confirm the Keycloak pod is running:

   ```bash
   kubectl get pods
   ```

1. Set up port forwarding:

   ```bash
   kubectl --namespace default port-forward "<pod_name>" 8080
   ```

1. Log in to the Keycloak web UI as an admin.

## Create the NBS users realm

1. In the top-left menu, select **Create realm**.

   ![nbs-users-realm](images/nbs-users-realm.png)

1. Upload or paste `charts/keycloak/extra/02-nbs-users-realm.json` and click **Create**.

   ![nbs-users-2-realm](images/nbs-users-realm-2.png)

1. Verify the new realm exists.

   ![nbs-users-3-realm](images/nbs-users-realm-3.png)

## Import base users and clients

1. Select the **nbs-users** realm, then go to **Realm settings** → **Action** → **Partial Import**.

   ![nbs-users-base-users](images/nbs-realm-base-users.png)

1. Upload or paste `charts/keycloak/extra/03-nbs-users-base-users.json`, select the 3 users, and click **Import**.

   ![nbs-users-base-users-2](images/nbs-users-base-users-2.png)
   ![nbs-users-base-users-3](images/nbs-users-base-users-3.png)

1. Upload or paste `charts/keycloak/extra/04-nbs-users-development-clients.json`, select the 1 client, and click **Import**.

   ![nbs-users-development](images/nbs-users-development.png)
   ![nbs-users-development-2](images/nbs-users-development-2.png)

## Configure the NBS gateway

> OIDC must be enabled when deploying `modernization-api` and `nbs-gateway`. This is configured during Microservices Deployment, not here.
{: .note }

1. In the **nbs-users** realm, go to **Clients** → **nbs-modernization** → **Credentials** → **Client Secret**.

   ![nbs-modernization](images/nbs-modernization.png)

1. Copy the client secret and update `charts/nbs-gateway/values.yaml` under the `oidc` settings.

## Set the login theme

You may use the pre-populated NBS login theme, keep the default, or create your own. The Keycloak Helm chart loads a sample theme in a persistent volume mounted at `/opt/keycloak/themes/nbs`.

1. Select the **nbs-users** realm.
1. Go to **Realm settings** → **Themes** → **Login** and select your preferred theme.

   ![nbs-login-theme](images/nbs-login-theme.png)
