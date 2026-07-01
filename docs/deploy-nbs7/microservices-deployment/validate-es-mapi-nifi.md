---
title: Validate Elasticsearch, Modernization API, NiFi
layout: page
parent: Deploy NBS 7 microservices
nav_order: 4
has_children: true
redirect_from:
  - /docs/6_microservices_deployment/5_validate_es_mapi_nifi.html
  - /docs/6_microservices_deployment/5_validate_es_mapi_nifi/
---

# Validate Elasticsearch, Modernization API, and NiFi

After deploying Elasticsearch, Modernization API, and NiFi, validate all three services before continuing with the remaining microservices. Successful validation confirms that:

- Name resolution is working
- Traffic routing between NBS 6 and NBS 7 is working
- Routing from NBS 7 components to the database is working
- Search indices have been created, populated, and are available

> Search indices may take longer to populate depending on the size of your database. A larger database could take 3-6 hours.
{: .note }

## In this section

This mid-point validation covers the following:

1. **[Manual validation for Elasticsearch, Modernization API, and NiFi](validate-es-mapi-nifi/manual-validation.html)**: Test end-to-end functionality by searching patient records in the NBS UI.
1. **[API smoke test for Modernization API](validate-es-mapi-nifi/api-smoke-test.html)**: Run the `nbs-test-api.sh` smoke test against the Modernization API.
1. **[Web UI smoke test for NBS interface and search](validate-es-mapi-nifi/web-ui-smoke-test.html)**: Run the `nbs-test-webui.sh` smoke test against the NBS web interface.
