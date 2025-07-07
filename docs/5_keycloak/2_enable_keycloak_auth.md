---
title: Enable Keycloak Auth
layout: page
parent: Keycloak Installation
nav_order: 1
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Enable Keycloak Auth
- a. Confirm the keycloak is running
  ```bash
  kubectl get pods
  ```
- b. Make sure you are authenticated to Keycloak
  ```bash
  kubectl --namespace default port-forward "<pod_name>" 8080
  ```
- c. Make sure you are logged in Keycloak webui as an admin
- d. Run json for nbs-users realm from charts/keycloak/extra/02-nbs-users-realm.json
  - a. Create realm menu top left option
     ![nbs-users-realm](/just-the-doc/docs/5_keycloak/images/nbs-users-realm.png)
  - b. Upload or paste the 02-nbs-users-realm.json file and click on create
    ![nbs-users-2-realm](/just-the-doc/docs/5_keycloak/images/nbs-users-realm-2.png)
  - c. Verify new realm exists
    ![nbs-users-3-realm](/just-the-doc/docs/5_keycloak/images/nbs-users-realm-3.png)
- e. Run partial import for following files from charts/keycloak/extra/ 
  - a. 03-nbs-users-base-users.json
  - b. 04-nbs-users-development-clients.json
- f. Make sure you select the nbs-users realm
  - a. Realm settings → Action → Partial import
    ![nbs-users-base-users](/just-the-doc/docs/5_keycloak/images/nbs-users-base-users.png)
  - b. Paste or upload 03-nbs-users-base-users.json and select the 3 users and click on Import
    ![nbs-users-base-users-2](/just-the-doc/docs/5_keycloak/images/nbs-users-base-users-2.png)
    ![nbs-users-base-users-3](/just-the-doc/docs/5_keycloak/images/nbs-users-base-users-3.png)
  - c. Repeat above steps to paste or upload 04-nbs-users-development-clients.json and select the 1 client and click on Import
    ![nbs-users-development](/just-the-doc/docs/5_keycloak/images/nbs-users-development.png)
    ![nbs-users-development-2](/just-the-doc/docs/5_keycloak/images/nbs-users-development-2.png)
- g. Make sure oidc is enabled when deploying page-builder-api, modernization-api and nbs-gateway services below. This will be done in the Microservices Deployment section.
- h. When deploying nbs-gateway service, also make sure to update the client secret (from Keycloak webui) under oidc in values.yaml. This will be done in the Microservices Deployment section.
  - a. Select nbs-users realm
  - b. Clients → nbs-modernization → Credentials → Client Secret
    ![nbs-modernization](/just-the-doc/docs/5_keycloak/images/nbs-modernization.png)
  - c. Copy the above secret and update in charts/nbs-gateway/values.yaml under oidc settings
- i. You may select the pre-populated NBS login theme, keep the default, or create your own.  The keycloak helm chart loads a sample theme in a persistent volume that is mounted on /opt/keycloak/themes/nbs.
  - a. Select nbs-users realm
  - b. Realm settings → Themes → Login
    ![nbs-login-theme](/just-the-doc/docs/5_keycloak/images/nbs-login-theme.png)
