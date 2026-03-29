---
title: Deploy NND Sync
layout: page
parent: NND Service (Data Sync)
nav_order: 2
---

# Deploy NND Sync

Use these instructions to deploy the on-premises Data Sync service that extracts data from the Modernized NBS cloud implementation and supports ongoing Notifiable Disease message transmission to CDC.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

![Architecture diagram for on-premises NNDSS data sync deployment](../images/data-sync-on-prem-1.png)

## Prerequisites

To sync data for NNDSS through the NBS 7 Data Sync service, you need the following:

- **Keycloak client ID and client secret** - CDC provides these values
- **Data service URL** - CDC provides this value
- **Release materials/package for Data Sync service** - CDC provides this package
- Install the **Rhapsody engine and IDE**
- Install an **MS SQL Server database**
  - Can be on a different machine, or
  - Repurpose an already existing SQL Server database (Rhapsody should have access to it)
- **Java 21 or higher**

---

## Components for NND Sync

NNDSS Data Sync service includes:

- `data-sync-service.jar`
- `netss-message-processor.jar`
- `.cmd` files (only for Windows environments)
- `.sql` files (to create NND Database and required objects)

---

## Set up the Data Sync service for NNDSS

Download the above files (`.jar`, `.cmd`, and `.sql`) from the most recent GitHub release under the **data-sync directory** in the `v7.x.x.NEDSS.NBS.Modernized.Documentation.zip` file.
Save the files to a secure directory with executable permissions to run the services.

---

### Step 1: Configure command or execute script (`.cmd` file)

- The release materials include a configurable `.cmd` script file that runs the Data Sync service.
- Replace the values for arguments in the file with your own.
- **Important:** Do not allow any space between the argument name and value.
  - Example: `arg_name=arg_value`

Reference for arguments: [README](https://github.com/CDCgov/NEDSS-NNDSS/tree/main/nnd-data-poll-service#readme)

---

### Step 2: Build or reuse the database and database objects

- Create a separate database and tables for the new service.
- Use the provided `.sql` scripts to create the required database and tables.

**Tables required in the new database:**

- `TransportQ_out`
- `CN_transportQ_out`
- `NETSS_transportQ_out`

Ensure the database is accessible from Rhapsody.

---

### Step 3: Update connection details on Rhapsody routes

- Update only variables in the route's **database components**.
- Point them to the new database and tables from the previous step.

**Steps:**

1. Log in to the Rhapsody console
2. Open **Variables Manager** and confirm the route has the correct hostname and new database name
3. Open all database components in the route and verify they refer to the right database variable

![Rhapsody route view showing database component variables](../images/data-sync-on-prem-rhapsody-1.png)

**List of database components to update in the Rhapsody route** (highlighted in red boxes in provided documentation).

![Rhapsody route with database components highlighted in red](../images/data-sync-on-prem-rhapsody-2.png)

---

### Step 4: Configure and verify PHINMS and SAMS

#### PHINMS

- Verify and update database connections for the existing PHINMS setup.

#### SAMS

- Verify that the file drop-off location in NETSS service parameters matches the location that SAMS reads.

---

## Repo reference

- GitHub: <https://github.com/CDCgov/NEDSS-NNDSS>

---

## Final note

Make sure you validate the provided **API endpoints** before you run the Data Sync services.
