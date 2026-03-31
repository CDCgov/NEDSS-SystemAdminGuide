---
title: Validate ES, Mapi and Nifi
layout: page
parent: Deploy NBS 7 microservices
nav_order: 4
has_children: true
nav_enabled: true
redirect_from:
  - /docs/6_microservices_deployment/5_validate_es_mapi_nifi.html
  - /docs/6_microservices_deployment/5_validate_es_mapi_nifi/
---

# Validate ES, Mapi and Nifi
{: .no_toc }

After deploying Elasticsearch, Modernization API, and NiFi, validate all three services together before continuing with the remaining microservices. When you are able to perform the validation steps and get results back, it confirms that:

- Name resolution is working
- Routing requests and traffic between the NBS 6.x portions of the system and NBS 7 is working properly
- Routing from the NBS 7 components to the (shared) database is working
- The search indices have been created and populated, and are available, thereby validating Elasticsearch, NiFi, and the Modernization-API

> The search indices may take longer to populate depending on the data. A larger database may take **3–6 hours**.
{: .note }

## In this section

- [Manual validation](validate-es-mapi-nifi/manual-validation.html) — Test end-to-end functionality by searching patient records in the NBS UI.
- [API smoke test](validate-es-mapi-nifi/api-smoke-test.html) — Run the scripted `nbs-test-api.sh` smoke test against the Modernization API.
- [Web UI smoke test](validate-es-mapi-nifi/web-ui-smoke-test.html) — Run the scripted `nbs-test-webui.sh` smoke test against the NBS web interface.
