---
title: API Testing and Integration
layout: page
parent: Data Processing
nav_order: 1
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Data Processing API Testing and Integration
Test will be exactly similar to Data Ingestion ELR ingestion endpoint test, user will have to utilize DI ELR Ingestion to trigger RTI service. Please follow the DI ingestion API testing guide

- The only change a user will have to specify on ELR Ingestion API is the on specific header
- Request Header (Additional)
  -  version: value is either 1 or 2, 1 is default
  -  If value is set to 1 the DI process will use the legacy batch importer process
  -  If value is set to 2, then DI will ignore legacy process and trigger the RTI
    - For RTI testing, this is the only change required on the Data Ingestion ELR endpoint

  ![data-processing-api-testing-1](/just-the-doc/docs/6_microservices_deployment/images/data-processing-api-testing-1.jpg)
 
To validate whether the data ingestion is successful, the user can also use DI status endpoint to verify the status.

- With the legacy flow, data status in NBS_Interface can be one of these three statuses: QUEUED, FAILED, and SUCESS
- Similarly with RTI, data status in NBS_Interface can be one of these three statuses: RTI_QUEUED, RTI_FAILURE, and RTI_SUCESS_STEP_N
  - There are 3 steps in RTI that can end up in the above statuses
    - RTI_SUCESS_STEP_1
      - Meaning data has passed through the core data process, and the specified data should be available in ODSE database
    - RTI_SUCESS_STEP_2
      - This will happen when WDS algorithm is specified, data will be running the algorithm and service will perform WDS comparison
    - RTI_SUCESS_STEP_3
      - Triggered once WDS is complete, the service will use the WDS result and assign the appropriate action for the ingested payload

    ![data-processing-flow-diagram](/just-the-doc/docs/6_microservices_deployment/images/data-processing-api-testing-2.jpg)

    ![data-processing-flow-diagram](/just-the-doc/docs/6_microservices_deployment/images/data-processing-api-testing-3.jpg)

    
