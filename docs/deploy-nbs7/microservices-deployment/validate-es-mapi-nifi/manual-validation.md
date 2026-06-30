---
title: Manual validation
layout: page
parent: Validate Elasticsearch, Modernization API, NiFi
nav_order: 1
redirect_from:
  - /docs/6_microservices_deployment/5a_manual_validation_es_mapi_nifi.html
  - /docs/6_microservices_deployment/5a_manual_validation_es_mapi_nifi/
  - /docs/3_base_application/manual-validation-es-mapi-nifi.html
  - /docs/3_base_application/manual-validation-es-mapi-nifi/
---

# Manual validation for Elasticsearch, Modernization API, and NiFi

Use these steps to validate end-to-end behavior in the NBS UI after deploying Elasticsearch, Modernization API, and NiFi.

1. Log in to NBS using your configured URL, for example: `https://app.<your-site>.<your-domain>.com/nbs/login`.
1. Select **Advanced Search**:

   ![Advanced Search button in the NBS UI](../images/manual-validation-1.png)
1. Run a search. For example, select **Male** from the **Sex** drop-down and select **Search**:

   ![Patient search form with Sex drop-down set to Male](../images/manual-validation-2.png)
1. Confirm that results appear in the results pane:

   ![Search results pane showing patient records](../images/manual-validation-3.png)
