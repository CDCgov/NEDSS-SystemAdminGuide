---
title: On-Prem Deployment for  NND Sync
layout: page
parent: NND Service (Data Sync)
nav_order: 2
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## NNDSS On-Prem Data Sync Deployment (NND Sync)

Instructions for On-Prem deployment of the Data Sync service required to extract the data from the Modernized NBS cloud implementation to support the ongoing Notifiable Disease message transmission to CDC.

![data-sync-on-prem-1](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/images/data-sync-on-prem-1.png)

---

## Pre-requisites

To sync data for NNDSS through NBS 7 Data Sync service, you will need the following:

- **Keycloak client ID and client secret** – Will be provided by CDC  
- **Data service URL** – Will be provided by CDC  
- **Release materials/package for Data Sync service** – Will be provided by CDC  
- **Rhapsody engine and IDE** is installed  
- **MS SQL Server database** is installed  
  - Can be on a different machine, or  
  - Repurpose an already existing SQL Server database (Rhapsody should have access to it)  
- **Java 21 or higher**

---

## Components for NND Data Sync Service

NNDSS Data Sync service comprises of:

- `data-sync-service.jar`  
- `netss-message-processor.jar`  
- `.cmd` files (only for Windows environments)  
- `.sql` files (to create NND Database and required objects)

---

## Setting up the Data Sync Service for NNDSS

Download the above files (`.jar`, `.cmd`, and `.sql`) from the most recent GitHub release under the **data-sync directory** in the `v7.x.x.NEDSS.NBS.Modernized.Documentation.zip` file.  
Save the files to a secure directory with executable permissions to run the services.

---

### Step 1: Configure command/execute script (`.cmd` file)

- A configurable `.cmd` script file is included in the release materials, used to run the Data Sync service.  
- Replace the values for arguments in the file with your own.  
- **Important:** Do not allow any space between the argument name and value.  
  - Example: `arg_name=arg_value`  

Reference for arguments: **#readme** [link](https://github.com/CDCgov/NEDSS-NNDSS/tree/main/nnd-data-poll-service#readme)

---

### Step 2: Build/Reuse the Database and Database Objects

- It is recommended to create a separate database and tables for the new service.  
- Use the provided `.sql` scripts to create the required database and tables.  

**Tables required in the new database:**

- `TransportQ_out`  
- `CN_transportQ_out`  
- `NETSS_transportQ_out`  

Ensure the database is accessible from Rhapsody.

---

### Step 3: Update Connection Details on Rhapsody Routes

- Only variables in the **database components** of the route need to be updated.  
- They should point to the new database and tables created in the previous step.  

**Steps:**

1. Login to Rhapsody console  
2. Open **Variables Manager** and confirm the route has the correct hostname and new database name  
3. Open all database components in the route and verify they refer to the right database variable  
   1. ![data-sync-on-prem-rhapsody-1](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/images/data-sync-on-prem-rhapsody-1.png)

**List of database components to be updated in Rhapsody route** (highlighted in red boxes in provided documentation).

![data-sync-on-prem-rhapsody-2](/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/images/data-sync-on-prem-rhapsody-2.png)

---

### Step 4: Configuring/Verifying PHINMS and SAMS

#### PHINMS
- Verify and update the database connections for the existing PHINMS setup.

#### SAMS
- Verify that the file drop-off location used in NETSS service parameters matches the one SAMS is picking up from.

---

## Repo Reference

- GitHub: [https://github.com/CDCgov/NEDSS-NNDSS](https://github.com/CDCgov/NEDSS-NNDSS)

---

## Final Note

Make sure to validate the **API endpoints** provided before running the Data Sync services.


