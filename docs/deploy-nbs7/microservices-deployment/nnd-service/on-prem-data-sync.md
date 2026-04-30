---
title: Deploy Data Availability (on-premises)
layout: page
parent: NND Service (Data Sync)
nav_order: 3
redirect_from:
  - /docs/6_microservices_deployment/8c_nnd_stlt_on_prem_configuration_data_sync.html
  - /docs/6_microservices_deployment/8c_nnd_stlt_on_prem_configuration_data_sync/
---

# Deploy Data Availability (on-premises)

This section provides instructions for on-premises deployment of the **Data Availability service**, which extracts data from the modernized NBS cloud implementation so STLTs can keep copies of selected tables from **RDB, ODSE, and SRTE**.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

- **Keycloak client ID and client secret** - CDC provides these values
- **Data service URL** - CDC provides this value
- **Release materials/package** needed for the Data Sync service - CDC provides this package
- **MS SQL Server database**
- **Java 21 or higher**
- **AWS S3** (Optional)

---

## Components for Data Availability service

The Data Availability service includes:

- `data-sync-service.jar`
- `.cmd` files (only for Windows environments)
- `.sql` files (for configuration table)

The service supports multiple options to download the data:

- Direct database sync
- Drop incremental `.JSON` files into an **AWS S3 bucket**
- Drop incremental `.JSON` files into a **local directory**

---

## Set up the Data Availability service

Download the above files (`.jar`, `.cmd`, and `.sql`) from the most recent GitHub release under the **data-sync directory** in the `v7.x.x.NEDSS.NBS.Modernized.Documentation.zip` file.
Save the files to a secure directory with executable permissions to run the services.

Before you proceed, **choose where to send the data**:

- SQL database
- AWS S3 bucket
- Local directory

The SQL database option uses a different setup (see **Appendix**).
For AWS S3 bucket and local directory options, pass the appropriate arguments in the `.cmd` file based on the selected option. Templates are provided in the release documents and **#readme**.

---

### Step 0: Choose the option for Data Availability service

Use one of these three download options:

1. **Direct insert into the database**
   - *Default setup*: Syncs all tables into **one database**
   - *Custom setup*: Syncs tables into **separate databases** as preferred (e.g., target databases match source databases)

2. **Drop JSON files in S3 bucket**

3. **Drop JSON files in a local file system**

---

### Step 1: Create the data config table

This step is important because this config table ensures that tables sync correctly.

#### Default setup for Data Availability

- Use this if downloading data into **S3 bucket** or **File location**, or if having all tables in **one database** is acceptable.
- Use the `.sql` file (`create_data_config.sql`) provided in the release package to create a new database (optional) and the required config table.
- STLTs can name their local database as preferred.
- Ensure the `poll_data_sync_config` table is created.
- Run the script `poll_config_insert.sql` to insert the static/lookup data into the config table.

#### Custom setup for Data Availability

- Use this if you prefer multiple databases and want to redirect table inserts per your preference.
- Create any sync database with your chosen name.
- The service requires the `poll_data_sync_config` table (`create_data_config.sql`).
- For each new database, create this configuration table and update its records as needed (`poll_config_insert.sql`), depending on sync requirements.

**Example:**
By default, Data Availability syncs all tables in the RDB database, without considering their original source.

If a user wants to direct **SRTE table data** into a separate SRTE database:

1. Create the SRTE database in the on-premises environment.
2. Create the `poll_data_sync_config` table in that database.
3. Insert only **SRTE-specific configurations** into the table.
   - These can be identified by the `source_db` field (e.g., `source_db = SRTE`).

---

### Config table scripts

- **Create config table**
  [create_data_config.sql](https://github.com/CDCgov/NEDSS-NNDSS/blob/{{ site.version_latest_tag }}/nnd-data-poll-service/src/main/resources/sql/config_table/create_data_config.sql)

- **Insert config records** (pick only the tables you want to download into that database, for example, only SRTE tables)
  [poll_config_insert.sql](https://github.com/CDCgov/NEDSS-NNDSS/blob/{{ site.version_latest_tag }}/nnd-data-poll-service/src/main/resources/sql/config_table/poll_config_insert.sql)

---

### Step 2: Configure the `.cmd` files

- Find the configurable `.cmd` script file in the release materials.
- Replace the argument values with your own.
- **Important:** No spaces between argument name and value.
  - Example: `arg_name=arg_value`
- For customizations, refer to **#readme**.

Make sure you validate the **provided API endpoints** before running any Data Sync services.

---

## Repo reference

GitHub: <https://github.com/CDCgov/NEDSS-NNDSS>

---

## Appendix: Data Sync service

### Setup for downloading data into SQL database (on-premises)

- Use this setup if the **SQL sync option** is chosen.
- Ensure relevant tables exist in the designated database **before sync**.
- Execute the following `.sql` scripts to create necessary tables required to download the data.

- **Database creation scripts** (includes RDB, SRTE, and RDB Modern)
  [create_test_db SQL scripts](https://github.com/CDCgov/NEDSS-NNDSS/tree/{{ site.version_latest_tag }}/nnd-data-poll-service/src/main/resources/sql/create_test_db)
