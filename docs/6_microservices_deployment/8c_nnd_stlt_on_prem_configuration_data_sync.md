---
title: On-Prem Deployment for Data Sync
layout: page
parent: NND Service (Data Sync)
nav_order: 3
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Data Availability On-Prem Deployment

## Overview
This section of the documentation provides instructions for On-Prem deployment of the **Data Availability service** necessary to extract the data from the modernized NBS cloud implementation to facilitate the request for STLTs to have a copy of the data from specific tables from **RDB, ODSE, SRTE**.

---

## Pre-requisites
- **Keycloak client ID and client secret** – Will be provided by CDC  
- **Data service URL** – Will be provided by CDC  
- **Release materials/package** needed for Data Sync service – Will be provided by CDC  
- **MS SQL Server database**  
- **Java 21 or higher**  
- **AWS S3** (Optional)

---

## Components for Data Availability Service
The Data Availability service comprises of:
- `data-sync-service.jar`  
- `.cmd` files (only for Windows environments)  
- `.sql` files (for configuration table)  

The service supports multiple options to download the data:
- Direct Database Sync  
- Dropping incremental `.JSON` files into **AWS S3 Bucket**  
- Dropping incremental `.JSON` files into **Local Directory**  

---

## Setting up the Data Availability Service
Download the above files (`.jar`, `.cmd`, and `.sql`) from the most recent GitHub release under the **data-sync directory** in the `v7.x.x.NEDSS.NBS.Modernized.Documentation.zip` file.  
Save the files to a secure directory with executable permissions to run the services.  

Before you proceed, **choose the option** where the data should be sent to:
- SQL database  
- AWS S3 Bucket  
- Local Directory  

There is a different setup recommended for synchronizing the data into SQL database (see **Appendix**).  
For AWS S3 Bucket and Local Directory, pass the appropriate arguments in the `.cmd` file according to the option selected. Templates are provided in the release documents and **#readme**.

---

### Step 0: Choose the Option for Data Availability Service
We have 3 options for downloading data:

1. **Direct Insert into the Database**  
   - *Default setup*: Syncs all tables into **one database**  
   - *Custom setup*: Syncs tables into **separate databases** as preferred (e.g., target databases match source databases)

2. **Drop JSON files in S3 bucket**

3. **Drop JSON files in a local file system**

---

### Step 1: Creating the Data Config Table
This is an important step as this config table ensures that tables are synced properly.

#### Default Setup for Data Availability
- Use this if downloading data into **S3 bucket** or **File location**, or if having all tables in **one database** is acceptable.  
- Use the `.sql` file (`create_data_config.sql`) provided in the release package to create a new database (optional) and the required config table.  
- STLTs can name their local database as preferred.  
- Ensure the `poll_data_sync_config` table is created.  
- Run the script `poll_config_insert.sql` to insert the static/lookup data into the config table.  

#### Custom Setup for Data Availability
- Use this if you prefer multiple databases and want to redirect table inserts per your preference.  
- Create any sync database with your chosen name.  
- The service requires the `poll_data_sync_config` table (`create_data_config.sql`).  
- For each new database, create this configuration table and update its records as needed (`poll_config_insert.sql`), depending on sync requirements.  

**Example:**  
By default, Data Availability syncs all tables in the RDB database, without considering their original source.  

If a user wants to direct **SRTE table data** into a separate SRTE database:
1. Create the SRTE database in the on-prem environment.  
2. Create the `poll_data_sync_config` table in that database.  
3. Insert only **SRTE-specific configurations** into the table.  
   - These can be identified by the `source_db` field (e.g., `source_db = SRTE`).  

---

### Config Table Scripts
- **Create Config Table**  
  [create_data_config.sql](https://github.com/CDCgov/NEDSS-NNDSS/blob/main/nnd-data-poll-service/src/main/resources/sql/rdb/create_data_config.sql)  

- **Insert Config Records** (pick only the tables you want to download into that database, e.g., only SRTE tables)  
  [poll_config_insert.sql](https://github.com/CDCgov/NEDSS-NNDSS/blob/main/nnd-data-poll-service/src/main/resources/sql/rdb/poll_config_insert.sql)  

---

### Step 2: Configuring the `.cmd` Files
- Find the configurable `.cmd` script file in the release materials.  
- Replace the argument values with your own.  
- **Important:** No spaces between argument name and value.  
  - Example: `arg_name=arg_value`  
- For customizations, refer to **#readme**.  

✅ Make sure to validate the **provided API endpoints** before running any of the Data Services.  

---

## Repo Reference
GitHub: [https://github.com/CDCgov/NEDSS-NNDSS](https://github.com/CDCgov/NEDSS-NNDSS)

---

## Appendix: Data Sync Service

### Setup for Downloading Data into SQL Database (On-Prem)
- Use this setup if the **SQL sync option** is chosen.  
- Ensure relevant tables exist in the designated database **before sync**.  
- Execute the following `.sql` scripts to create necessary tables required to download the data.

- **RDB tables**  
  [RDB SQL scripts](https://github.com/CDCgov/NEDSS-NNDSS/tree/main/nnd-data-poll-service/src/main/resources/sql/rdb)  

- **SRTE tables** (populate under the same RDB database)  
  [SRTE SQL scripts](https://github.com/CDCgov/NEDSS-NNDSS/tree/main/nnd-data-poll-service/src/main/resources/sql/srte)  

- **RDB Modern tables** (populate under the same RDB database)  
  [RDB Modern SQL scripts](https://github.com/CDCgov/NEDSS-NNDSS/tree/main/nnd-data-poll-service/src/main/resources/sql/rdb_modern)  
