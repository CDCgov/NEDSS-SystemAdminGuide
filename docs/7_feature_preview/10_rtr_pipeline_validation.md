---
title: RTR Pipeline Validation
layout: page
parent: Real Time Reporting (Preview)
nav_order: 10
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## RTR Pipeline Validation
1. **Via the UI:** Testing the RTR pipeline through the NBS UI. This example covers the steps required to create a Hepatitis Investigation from the UI and view the investigation details in the datamart tables. The data input for this example is synthetic and randomly generated.
   - a. Access the NBS UI with the username and password provided for the demo and click Data Entry in the top banner.
         ![rtr-validation-via-ui](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-via-ui.png)
   - b. Select “Lab Report“ under the Data Entry section to start a report.
         ![rtr-validation-lab-report](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-lab-report.png)
   - c. Add patient information to the lab report. Entity Id is required to complete the Patient tab for the report. If SSN is selected, the authority should be 'Social Security Administration'.
         ![rtr-validation-lab-report-2](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-lab-report-2.png)
   - d. Select the Lab Report tab and add necessary details to the report. The Program Area selected for this example is HEP. Required section Resulted Test must be filled in before submitting. Click “Submit” when done. If there are any errors in the submission, they will show up in red. Once they are corrected, the report can be submitted again.
         ![rtr-validation-lab-report-3](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-lab-report-3.png)
   - e. Navigate to the patient record via Patient Search or find the lab report in the Documents Requiring Review queue. From the patient record, navigate to the Events tab to view the lab created.
         ![rtr-validation-lab-report-4](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-lab-report-4.png)
   - f. Click on the “Create Investigation“ button in the upper right corner to create an investigation for the lab report.
         ![rtr-validation-lab-report-create-investigation](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-lab-report-create-investigation.png)
   - g. For this test, select a Hepatitis condition.
         ![rtr-validation-lab-report-create-investigation-2](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-lab-report-create-investigation-2.png)
   - h. Add information to complete the Investigation form and click Submit when done.
         ![rtr-validation-lab-report-create-investigation-3](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-lab-report-create-investigation-3.png)
   - i. The data should be available in the PUBLICHEALTHCASEFACT_Modern and Hepatitis datamarts in 1-2 minutes. The form’s Investigation ID can be used in the query below to review the information from the tables.
         ![rtr-validation-lab-report-create-investigation-4](/NEDSS-SystemAdminGuide/docs/7_feature_preview/images/rtr-validation-lab-report-create-investigation-4.png)
        ```sql
        DECLARE @local_id VARCHAR(20) = 'CAS10001017GA01'

        SELECT LASTUPDATE, PHCF.*
        FROM NBS_ODSE.DBO.PUBLICHEALTHCASEFACT_Modern PHCF
        WHERE LOCAL_ID IN (@local_id);
        
        SELECT REFRESH_DATETIME, hd.*
        FROM RDB_MODERN.DBO.HEPATITIS_DATAMART hd 
        WHERE INV_LOCAL_ID IN (@local_id);
        
        SELECT cl.*
        FROM RDB_MODERN.DBO.CASE_LAB_DATAMART cl 
        WHERE INVESTIGATION_LOCAL_ID IN (@local_id);
        
        SELECT isd.*
        FROM RDB_MODERN.DBO.INV_SUMM_DATAMART isd 
        WHERE INVESTIGATION_LOCAL_ID IN (@local_id);
        ``` 
   - j. If there are any errors, please run the query below to see if there are any SQL script errors. If the data fails to make it into the target datamart tables, please reach out to our support team.
        ```sql
        SELECT *
        FROM RDB_MODERN.DBO.JOB_FLOW_LOG
        WHERE Status_Type = 'ERROR'
        ORDER BY batch_id desc;
        ```
2. **Via the ELR ingestion:**
To test the pipeline, you can perform ELR (Electronic Lab Report) ingestion through the Data Ingestion service instead of creating entries via the NBS UI. Please refer to the Data Ingestion related smoke test section in the release documentation for detailed steps and guidance of the ELR ingestion.

If the Workflow Decision Support (WDS) is configured, and a matching algorithm is detected during a HEP ELR ingestion, an investigation will be automatically created and added to the investigation queue. However, configuring the WSD algorithm is not mandatory. If the WSD algorithm is not in place, the ELR will still be successfully ingested and will appear in the Document Requiring Review queue instead. You can then locate and open the HEP lab report from this queue and follow the steps outlined in step 1.e of the NBS UI validation process as listed above.

The data used for this testing example is synthetic and randomly generated. Any HEP-related ELR, such as Hepatitis A, B, or C etc. can be used for the test.

 **Sample Hepatitis A ELR:**
MSH|^~\&|HL7 Generator^^|Family Health Center^42D7444477^CLIA|ALDOH^OID^ISO|AL^OID^ISO|202408261214||ORU^R01^ORU_R01|20240826121475|P|2.5.1
PID|1|239082358^^^Family Health Center&42D7444477&CLIA|239082358^^^Social Security Administration&SSA&CLIA^SS||Sanchez^Andrew^Frank^ESQ^Mrs^JD|Lin|196903240000|F|kavita|2076-8^Native Hawaiian or Other Pacific Islander^CDCREC|35381 Randy Passage Suite 203^unit 7779^Natashahaven^LA^30342^USA||^^^JaredLee75@yahoo.com^^732^9566115^4740|^^^AndrewSanchez75@hotmail.com^^732^1499917^4740|ENG|T^^^^^|||042-80-2420|||2186-5^Not Hispanic or Latino|Wagnerburgh|Y|3|||USA|202408051214|Y
PV1||R
ORC|RE||94884048343^Russell, Chandler and Potts^34D4434343^CLIA||N||||||||||||||||Lowery-Gonzalez|175 Flores Highway Suite 629^unit 2037^Devinburgh^DE^47827^USA|^^^^^^979^7323277^2821|96626 Tamara Ports Apt. 716^unit 31129^Port Heatherstad^NC^24461^USA
OBR|1|75^Test Org 2 AC^1234^|804164994m^Family Health Center^42D7444477^CLIA|40724-7^Hepatitis A virus IgG Ab [Presence] in Serum by Immunoassay^LN^75^TestData^L|S||202408261214|202408311214||||BLD|Back anything crime everything such research.|202408261214||5860083^Mullen^Sarah^II^Mr^BS|2964833605^^^JenniferSalas75@yahoo.com|||||202408311214|||F|||9097261^Mills^Justin^ESQ^Mrs^BA|||69413^Dietary surveillance and counseling^36866|47356&Young&Barbara&&IV&Mrs&DRN^202408261214^202408311214
OBX|1|NM|40724-7^Hepatitis A virus IgG Ab [Presence] in Serum by Immunoassay^LN|1|100^1^:^1|mL|10-100|H|||C||||||||202408261214
SPM|1|8283570&Test Org 2 AC&1234&^3200553&Family Health Center&42D7444477&CLIA||NAIL^Nail^HL70487^UMB^Umbilical blood^SCT^2.5.1^Nail|||UMB^UMB^TG|426364234^carry^SNM||||75^ML||Participant personal you manager.|||202408261214^202408311214|202408261214|||
