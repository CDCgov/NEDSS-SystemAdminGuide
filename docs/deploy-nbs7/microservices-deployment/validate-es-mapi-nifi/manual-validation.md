---
title: Manual validation
layout: page
parent: Validate ES, MAPI, and NiFi
grand_parent: Deploy NBS 7 microservices
nav_order: 1
redirect_from:
  - /docs/6_microservices_deployment/5a_manual_validation_es_mapi_nifi.html
  - /docs/6_microservices_deployment/5a_manual_validation_es_mapi_nifi/
  - /docs/3_base_application/manual-validation-es-mapi-nifi.html
  - /docs/3_base_application/manual-validation-es-mapi-nifi/
---

# Manual validation for Elasticsearch, Modernization API, and NiFi

Use these steps to validate end-to-end behavior in the NBS UI after deploying Elasticsearch, Modernization API, and NiFi.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Manual steps

Test end-to-end functionality using the following steps:

1. Log in to the new NBS system using the URL you configured: `https://app.<your-site>.<your-domain>.com/nbs/login` (for example, `https://app.<your-site>.<your-domain>.com/nbs/login`).
1. Select **Advanced Search**:

   ![advanced-search-manual-validation](../images/manual-validation-1.png)
1. View patient records. One way to do this is to select "Male" from the "Sex" drop-down and then select **Search**:

   ![patient-search-manual-validation](../images/manual-validation-2.png)
1. Confirm results appear in the pane on the right:

   ![search-results-manual-validation](../images/manual-validation-3.png)
