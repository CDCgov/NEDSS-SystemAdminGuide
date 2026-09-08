---
title: Revert to MasterETL
layout: page
parent: Real-time reporting
nav_order: 5
description: Returns reporting to the classic MasterETL batch jobs after installing RTR, for both reporting-database options.
---

# Revert from real-time reporting (RTR) to MasterETL

> This feature is in Beta preview and not production ready.
{: .important }

A jurisdiction that installs [[rtr]] may decide to return to the classic [[masteretl|MasterETL]] batch
jobs — during a pilot, after a failed seeding run, or later. This page covers both of the
reporting-database options offered at [Prerequisites](real-time-reporting.html#prerequisites).

Reverting does **not** require undeploying [[nbs-7]]. If you want to remove RTR and keep NBS 7 running,
this page is the whole procedure.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

> Verify that you are connected to the correct [[kubernetes]] cluster before proceeding. To confirm, run `kubectl config current-context`.
{: .note }

SQL on this page is written for a client such as SQL Server Management Studio or `sqlcmd`, connected as
an account with `sysadmin` rights. Several steps **generate** SQL for you to review before running it;
those are marked.

> This page describes RTR 7.13, where the Java services are deployed from a single
> `reporting-pipeline-service` [[helm-chart|Helm chart]]. Releases before 7.13 used an `rtr` umbrella
> chart that produced six `rtr-java-services-*` deployments and installed the schema from a separate
> Liquibase chart. If that is what you have, the Kubernetes resource names below will not match — see
> [Installs from before 7.13](#installs-from-before-713).
{: .important }

---

## Before you begin: which revert applies to you

| You installed RTR against | Your revert | Requires |
| :--- | :--- | :--- |
| **`RDB_MODERN`** (a duplicate of `RDB`) | Stop RTR, resume MasterETL on `RDB`, decommission `RDB_MODERN` | Nothing extra |
| **`RDB`** (the existing reporting database) | Stop RTR, **restore the pre-RTR `RDB` backup**, resume MasterETL | The backup taken when you chose a reporting database |

> On the RDB path, the backup taken at [Prerequisites, step 3](real-time-reporting.html#prerequisites)
> is the revert mechanism, not a precaution. Reverting in place — leaving RTR's objects and rows in
> `RDB` — does not work, and neither does removing them first. There is currently no supported way to
> return `RDB` to a correct state without that backup. See
> [Why the RDB path requires a restore](#why-the-rdb-path-requires-a-restore).
{: .warning }

---

## Step 1. Stop the RTR pipeline

The order matters. Removing the sink before the queue drains strands whatever is still in flight.

### 1a. Find your releases and their resource names

Two of the three RTR charts name their Kubernetes resources from the **release name chosen at install**,
so the names below are not fixed. Start by listing what is actually deployed:

```bash
helm list
kubectl get deployments -o wide
kubectl get services
```

An install that followed this guide produces:

```text
NAME                        CHART                             APP VERSION
cp-kafka-connect-server     cp-kafka-connect-1.3.0            7.13.0
debezium-connect            debezium-rtr-1.3.0                7.13.0
reporting-pipeline-service  reporting-pipeline-service-1.3.0  7.13.0
```

```text
NAME                                    READY   AGE
cp-kafka-connect-server                 1/1     35m
debezium-connect-debezium-rtr-connect   1/1     35m
reporting-pipeline-service              1/1     34m
```

> **Do not assume these names.** [[helm]] derives them from the release name:
>
> | Chart | Resource name |
> | :--- | :--- |
> | `debezium-rtr` | `<release>-debezium-rtr-connect`, or `<release>-connect` if the release name already contains `debezium-rtr` |
> | `cp-kafka-connect` | exactly `<release>` if the release name contains `cp-kafka-connect`, otherwise `<release>-cp-kafka-connect` |
> | `reporting-pipeline-service` | always `reporting-pipeline-service`, whatever the release is called |
>
> A cluster where the sink was installed as `cp-kafka-connect-sqlserver` rather than
> `cp-kafka-connect-server` names its Service and Deployment `cp-kafka-connect-sqlserver`, and every
> command below that hardcodes the other name fails. Take the names from `kubectl get services`.
{: .warning }

Set them once and use the variables for the rest of this step:

```bash
DBZ=debezium-connect-debezium-rtr-connect      # from kubectl get services
SINK=cp-kafka-connect-server                   # from kubectl get services
RPS=reporting-pipeline-service
```

### 1b. Record what is running before you change anything

Run the checks on [Validate RTR installation](rtr-validation.html) and keep the output. At minimum,
capture connector state, which one call reports alongside the database connection:

```bash
kubectl port-forward svc/$RPS 8095:8095
curl -s http://localhost:8095/actuator/health
```

```json
{ "status": "UP",
  "components": {
    "connectors": { "status": "UP", "details": {
      "debezium": { "odse-main-connector": "RUNNING", "odse-schema-only-connector": "RUNNING",
                    "odse-meta-connector": "RUNNING", "srte-connector": "RUNNING" },
      "kafkaConnect": { "Kafka-Connect-SqlServer-Sink": "RUNNING" } } },
    "db": { "status": "UP", "details": { "database": "Microsoft SQL Server" } } } }
```

If a connector is already `FAILED` or missing here, investigate before reverting — you want to know that
now, not halfway through.

### 1c. Delete the Debezium source connectors

Open a connection to the [[debezium|Debezium]] Connect REST API and leave it running in its own
terminal:

```bash
kubectl port-forward svc/$DBZ 8083:8083
```

In a second terminal, list the registered connectors to confirm the names before deleting them:

```bash
curl -s http://localhost:8083/connectors
```

Expected — the same four names, in any order:

```json
["odse-meta-connector","odse-schema-only-connector","odse-main-connector","srte-connector"]
```

Delete all four, so no new change events are produced. Each returns HTTP 204 with an empty body:

```bash
for c in odse-main-connector odse-schema-only-connector odse-meta-connector srte-connector; do
  curl -s -X DELETE "http://localhost:8083/connectors/$c"
done
sleep 5
curl -s http://localhost:8083/connectors
```

The final command should return `[]`.

### 1d. Wait for the pipeline to drain

In a third terminal:

```bash
kubectl port-forward svc/$RPS 8095:8095
curl -s http://localhost:8095/actuator/lag
```

Repeat the `curl` until both queues report zero:

```json
{ "status": "READY",
  "details": { "caughtUp": true,
    "pipeline": { "messagesQueued": 0, "byTopic": {} },
    "sink":     { "messagesQueued": 0, "byTopic": {} } } }
```

`byTopic` names the specific topics still holding messages, which is where to look if the count does not
fall.

> Do not continue until `messagesQueued` is 0 for both. The ingress URL for this endpoint requires
> Traefik, so the port-forward above is the reliable route.
{: .important }

### 1e. Delete the sink connector

```bash
kubectl port-forward svc/$SINK 8084:8083
curl -s -X DELETE http://localhost:8084/connectors/Kafka-Connect-SqlServer-Sink
sleep 5
curl -s http://localhost:8084/connectors
```

### 1f. Scale down, then uninstall

Scale to zero first — it is reversible, and it stops the services without discarding their
configuration:

```bash
kubectl scale deployment $RPS  --replicas=0
kubectl scale deployment $SINK --replicas=0
kubectl scale deployment $DBZ  --replicas=0
kubectl get deployments
```

All three should report `0/0`.

> Scale `reporting-pipeline-service` down **first**. It reads its Connect URLs from the two ConfigMaps
> the Debezium and [[kafka|Kafka]] Connect charts own (`debezium-rtr-connect` and
> `cp-kafka-connect-sqlserver-connect`) through `configMapKeyRef`. Removing those charts while the
> deployment still exists leaves its pods in `CreateContainerConfigError` rather than stopped cleanly.
{: .note }

Give the pods a few seconds to finish terminating, then uninstall the releases:

```bash
kubectl get pods
helm uninstall <your reporting-pipeline-service release>
helm uninstall cp-kafka-connect-server
helm uninstall debezium-connect
```

Uninstalling while pods are still terminating leaves them orphaned in `Error` state — harmless, and
Kubernetes collects them, but it makes the next check confusing.

### 1g. Confirm nothing is left

```bash
helm list
kubectl get all,configmap
```

`helm list` should be empty, and the only remaining ConfigMap should be `kube-root-ca.crt`.
`helm uninstall` removes the RTR ConfigMaps along with everything else — you should not need to delete
`cp-kafka-connect-sqlserver-connect` or `debezium-rtr-connect` by hand, and their absence here is the
check that the uninstall was complete.

### Prevent the pipeline restarting itself

> Starting `reporting-pipeline-service` does two things, and the second is the dangerous one.
>
> 1. It **re-creates all five connectors**. `DEBEZIUM_AUTOCONFIG_ENABLE` and
>    `KAFKA_CONNECT_AUTOCONFIG_ENABLE` both default to `true`.
> 2. It also **runs Liquibase and re-applies the entire RTR schema** to whatever database
>    `DB_CONNECTION_URL` points at. As
>    [Validate RTR installation](rtr-validation.html#check-database-migration-status) notes,
>    `LIQUIBASE_AUTOMIGRATION_ENABLE` is enabled unless it is explicitly set to `false`. From 7.13 the
>    service performs the migration itself on boot; there is no separate Liquibase chart.
>
> So a pod brought up for any unrelated reason will restart the pipeline *and* reinstall RTR's tables
> into the reporting database. On the RDB path, after a restore, that means reinstalling RTR into the
> database you just recovered.
{: .warning }

Keep the deployment scaled to zero or uninstalled until the revert is finished. Do not scale it back up
to check something, and make sure nothing else — a [[gitops|GitOps]] sync, a saved Helm release, a
deployment pipeline — will reinstall the chart on its own.

If your environment sets those variables, confirm they took effect from the service log rather than the
REST API:

```bash
kubectl logs deployment/$RPS | grep -i "auto-configuration"
kubectl logs deployment/$RPS | grep -c "Registered connector"
```

Expected:

```text
KafkaConnectConfig : Kafka Connect connector auto-configuration is disabled
DebeziumConfig     : Debezium connector auto-configuration is disabled
```

and a count of `0`.

> Check the log, not the Connect REST endpoints. During a revert those services are down, so a REST
> query is refused whether the flags took effect or not — the refusal tells you nothing.
{: .important }

### Installs from before 7.13

Releases before 7.13 deployed the Java services from an `rtr` umbrella chart, typically installed as
`helm install rtr . -f values.yaml`, producing six deployments:

```text
rtr-java-services-investigation-reporting
rtr-java-services-ldfdata-reporting
rtr-java-services-observation-reporting
rtr-java-services-organization-reporting
rtr-java-services-person-reporting
rtr-java-services-post-processing-reporting
```

Those releases also installed the schema from a separate Liquibase chart rather than from the service.
On such an install, substitute `helm uninstall rtr` for the release above, scale down all six
deployments rather than one, and expect the health and drain endpoints to live on the individual
services. Everything from [Step 2](#step-2-change-data-capture) onward is unaffected.

---

## Step 2. Change Data Capture

> In this section, the terms `cdc` and `CDC` appear as part of SQL Server column and parameter names and refer to Change Data Capture, not the Centers for Disease Control and Prevention.
{: .note }

> Never run `sp_cdc_disable_db` on `NBS_ODSE`. It drops every capture instance in the database,
> including the one Case Notification depends on.
{: .warning }

As [Enable Change Data Capture](real-time-reporting.html#enable-change-data-capture) notes,
[[change-data-capture|CDC]] was already enabled on `NBS_ODSE` by the Case Notification service
deployment; the RTR bootstrap script adds `NBS_SRTE` and the RTR source tables. Case Notification
consumes a Kafka topic produced by a Debezium connector on **`NBS_ODSE.dbo.CN_transportq_out`**, which
appears in neither the RTR bootstrap script's table list nor any RTR connector — so the two table sets
do not overlap, but the database-level setting is shared and must stay on.

### 2a. List the capture instances and their creation times

```sql
USE NBS_ODSE;

SELECT s.name                                        AS source_schema,
       t.name                                        AS source_table,
       ct.capture_instance,
       CONVERT(VARCHAR(23), ct.create_date, 121)     AS create_date
  FROM cdc.change_tables ct
  JOIN sys.tables  t ON t.object_id = ct.source_object_id
  JOIN sys.schemas s ON s.schema_id = t.schema_id
 ORDER BY ct.create_date;
```

The bootstrap script enables 20 tables in `NBS_ODSE` in a single pass — on a reference install all 20
were created within a 13-second window.

> Any capture instance that pre-dates your RTR install belongs to something else. Leave it.
>
> The bootstrap script enables CDC with `EXCEPT SELECT NAME FROM SYS.TABLES WHERE IS_TRACKED_BY_CDC = 1`
> — it skips tables that are already tracked. So where another component enabled CDC on one of those
> tables first, RTR reused that instance rather than creating its own, and nothing in the instance
> records which component asked for it. Creation time is the only available signal.
{: .warning }

### 2b. Confirm Case Notification's capture instance

```sql
USE NBS_ODSE;

SELECT t.name                                    AS source_table,
       ct.capture_instance,
       CONVERT(VARCHAR(23), ct.create_date, 121) AS create_date
  FROM cdc.change_tables ct
  JOIN sys.tables t ON t.object_id = ct.source_object_id
 WHERE t.name LIKE '%transportq%'
    OR t.name LIKE '%transport[_]q%';
```

If this returns a row, Case Notification is wired up on this environment. **Do not disable that
instance,** and do not include it in the next step. If it returns no rows, Case Notification is not
using CDC here and the next step covers everything.

### 2c. Generate the disable statements for the RTR tables

This produces SQL for you to review. It does not disable anything.

```sql
USE NBS_ODSE;

SELECT 'EXEC sys.sp_cdc_disable_table @source_schema = N''' + s.name +
       ''', @source_name = N''' + t.name +
       ''', @capture_instance = N''' + ct.capture_instance + ''';' AS statement_to_run,
       CONVERT(VARCHAR(23), ct.create_date, 121) AS create_date
  FROM cdc.change_tables ct
  JOIN sys.tables  t ON t.object_id = ct.source_object_id
  JOIN sys.schemas s ON s.schema_id = t.schema_id
 WHERE t.name IN ('Act_relationship','Auth_user','CT_contact','Intervention','Interview',
                  'NBS_page','NBS_rdb_metadata','NBS_ui_metadata','Notification','Observation',
                  'Organization','Page_cond_mapping','Person','Place','Public_health_case',
                  'state_defined_field_data','State_Defined_Field_Metadata','Treatment',
                  'NBS_configuration','LOOKUP_QUESTION')
   AND t.name NOT LIKE '%transportq%'
   AND t.name NOT LIKE '%transport[_]q%'
 ORDER BY t.name;
```

Review the `create_date` on every row. Run only the statements whose instances were created by your RTR
install.

### 2d. Disable CDC on NBS_SRTE

`NBS_SRTE` is reference data and RTR is its only known CDC consumer. Confirm that for your environment,
then disable the capture instances and the database-level flag:

```sql
USE NBS_SRTE;

-- Generate the per-table statements
SELECT 'EXEC sys.sp_cdc_disable_table @source_schema = N''' + s.name +
       ''', @source_name = N''' + t.name +
       ''', @capture_instance = N''' + ct.capture_instance + ''';' AS statement_to_run
  FROM cdc.change_tables ct
  JOIN sys.tables  t ON t.object_id = ct.source_object_id
  JOIN sys.schemas s ON s.schema_id = t.schema_id
 ORDER BY t.name;
```

After running the generated statements:

```sql
USE NBS_SRTE;
EXEC sys.sp_cdc_disable_db;
```

### 2e. Leave these alone

| Setting | Why |
| :--- | :--- |
| Database-level CDC on `NBS_ODSE` | Case Notification depends on it |
| `ALLOW_SNAPSHOT_ISOLATION` on `NBS_ODSE` | Set ON by the RTR bootstrap; other readers may now rely on it |
| `max text repl size (B)` | Instance-wide, affects every database on the server |

### 2f. Verify

```sql
SELECT name, is_cdc_enabled
  FROM sys.databases
 WHERE name IN ('NBS_ODSE','NBS_SRTE');

USE NBS_ODSE;
SELECT COUNT(*) AS remaining_capture_instances FROM cdc.change_tables;

SELECT name, enabled FROM msdb.dbo.sysjobs WHERE name LIKE 'cdc.%' ORDER BY name;
```

Expected: `NBS_ODSE` still `is_cdc_enabled = 1`; `NBS_SRTE` now `0`; remaining ODSE instances 0, or 1 if
Case Notification's instance is present.

The last query will still list `cdc.NBS_ODSE_capture` and `cdc.NBS_ODSE_cleanup`, both enabled. The
`NBS_SRTE` pair disappears on its own once database-level CDC is disabled there.

> The two `NBS_ODSE` jobs are expected to remain, running against zero capture instances. Do not tidy
> them up by disabling database-level CDC — that is the action this page warns against above.
{: .important }

---

## Step 3. Kafka topics

RTR creates substantially more topics than the `nbs_*` and `nrt_*` names suggest. On a reference 7.13
install, 140 of 141 topics were RTR-owned:

| Count | Class | Pattern |
| :--- | :--- | :--- |
| 62 | retry tier | `*_retry-0`, `*_retry-1` |
| 33 | pipeline data | `nbs_*` (14), `nrt_*` (19) |
| 31 | dead letter | `*_dlt` |
| 6 | Connect worker state | derived from each chart's `topics_basename` — see below |
| 4 | Debezium schema history | `*-schema-history` |
| 3 | Debezium raw CDC | `cdc_*` |
| 1 | sink dead-letter queue | `nrt-nbs-dlq-1` |

> Do not treat those counts as a checksum. They vary with how much data has flowed and which connectors
> have produced anything — `cdc_odse_act_rel` never appears on a fresh install, because the schema-only
> connector emits no data topic, and not every base topic has `_dlt` and `_retry` siblings. Rely on the
> filter and on the leftover check below, not on a total.
{: .note }

Everything except the two worker-state groups is named by `reporting-pipeline-service` itself and is the
same on every install. The six worker-state topics are named from Helm values.

### 3a. Read the two topic base names from your values files

```bash
grep topics_basename charts/debezium/values.yaml
grep topics_basename charts/kafka-connect-sink/values.yaml
```

The chart defaults are `rtr-debezium` and `rtr-kafka-connect-sink`, which produce:

| Chart | Topics |
| :--- | :--- |
| `debezium` | `rtr-debezium_config`, `rtr-debezium_offset`, `rtr-debezium_status` |
| `kafka-connect-sink` | `rtr-kafka-connect-sink-config`, `rtr-kafka-connect-sink-offset`, `rtr-kafka-connect-sink-status` |

> Note the separators differ — the Debezium chart joins with an underscore, the sink chart with a
> hyphen — and neither matches Kafka Connect's stock `connect-configs` / `connect-offsets` /
> `connect-status`. A filter written against the stock names silently matches nothing, and the offset
> topics are exactly the ones that must not be left behind.
{: .warning }

These six topics are created by the Connect **workers**, not by the connectors, so they exist even when
no connector is registered — including part-way through a revert.

### 3b. List and filter

Substitute your own bootstrap servers — for [[amazon-msk|Amazon MSK]], see
[Getting the bootstrap brokers](https://docs.aws.amazon.com/msk/latest/developerguide/msk-get-bootstrap-brokers.html).

```bash
export BOOTSTRAP=<your-bootstrap-servers>
export DBZ_BASE=rtr-debezium              # from step 3a
export SINK_BASE=rtr-kafka-connect-sink   # from step 3a

kafka-topics --bootstrap-server $BOOTSTRAP --list | sort > /tmp/all-topics.txt
wc -l < /tmp/all-topics.txt
```

**Select the RTR-owned topics and review the list before deleting anything.**

```bash
grep -E "^(nbs_|nrt_|cdc_)|-schema-history$|_dlt$|_retry-[0-9]+$|^nrt-nbs-dlq|^${DBZ_BASE}_(config|offset|status)$|^${SINK_BASE}-(config|offset|status)$" \
  /tmp/all-topics.txt > /tmp/rtr-topics.txt
wc -l < /tmp/rtr-topics.txt

# Anything the filter did not match — inspect before proceeding
grep -vxF -f /tmp/rtr-topics.txt /tmp/all-topics.txt
```

On a cluster running only RTR, the last command prints `__consumer_offsets` and nothing else. **Keep
`__consumer_offsets`** — it is a Kafka internal topic. Anything else it prints belongs to another NBS
component; check before you continue.

Confirm the six worker-state topics are in the delete list:

```bash
grep -E "_(config|offset|status)$|-(config|offset|status)$" /tmp/rtr-topics.txt
```

### 3c. Delete them

```bash
while read -r t; do
  kafka-topics --bootstrap-server $BOOTSTRAP --delete --topic "$t"
done < /tmp/rtr-topics.txt

kafka-topics --bootstrap-server $BOOTSTRAP --list
```

> This cleanup is load-bearing, not tidiness. If the source database is ever restored or rebuilt while
> Kafka retains the Debezium offset topic and the `*-schema-history` topics, Debezium resumes from a log
> position that database has never reached. Every connector reports `RUNNING`, health reports `UP`, lag
> reports `caughtUp`, no error appears in any log — and no data moves. The same trap catches anyone
> restoring `NBS_ODSE` from backup with RTR still installed.
{: .warning }

If you reach that state, the recovery is this same step: stop the pipeline, delete the RTR-owned topics,
restart. The connectors then find no prior offsets and take fresh snapshots. Changes captured while the
pipeline was dead are not lost — they remain in the `cdc.*_CT` change tables and replay on recovery,
bounded by your CDC retention window.

---

## Step 4. Service accounts

Enumerate rather than assume. The account holds `db_owner` on **both** reporting databases, not only the
one RTR targeted — confirmed on a reference install that used `RDB_MODERN`, where the service user was
`db_owner` on `RDB` as well.

**Find the login and every database user:**

```sql
SELECT name, type_desc, is_disabled,
       CONVERT(VARCHAR(23), create_date, 121) AS create_date
  FROM sys.server_principals
 WHERE name LIKE '%rtr%';
```

Run this in each of `NBS_ODSE`, `NBS_SRTE`, `RDB` and `RDB_MODERN`:

```sql
SELECT DB_NAME() AS database_name,
       dp.name   AS database_user,
       r.name    AS role_name,
       (SELECT COUNT(*) FROM sys.schemas s WHERE s.principal_id = dp.principal_id) AS owned_schemas
  FROM sys.database_principals dp
  LEFT JOIN sys.database_role_members rm ON rm.member_principal_id = dp.principal_id
  LEFT JOIN sys.database_principals  r   ON r.principal_id = rm.role_principal_id
 WHERE dp.name LIKE '%rtr%';
```

Expected, matching the permissions set at [Create service user](real-time-reporting.html#create-service-user):
`db_datareader` in `NBS_ODSE` and `NBS_SRTE`, `db_owner` in both reporting databases, `owned_schemas` 0
everywhere.

> If `owned_schemas` is greater than zero, transfer ownership before dropping the user, or `DROP USER`
> will fail.
{: .note }

**Drop the database users first, then the login:**

```sql
USE NBS_ODSE;    DROP USER [rtr-service-user];
USE NBS_SRTE;    DROP USER [rtr-service-user];
USE RDB;         DROP USER [rtr-service-user];
USE RDB_MODERN;  DROP USER [rtr-service-user];

USE master;
DROP LOGIN [rtr-service-user];
```

Substitute the account name your install used, and omit any database where the previous query returned
no user.

---

## Step 5. Remove the reporting-database setting, if your install has one

Some RTR installs carry an `ENV` row in `NBS_ODSE.dbo.NBS_Configuration` — `PROD` where RTR targeted
`RDB`, `UAT` where it targeted a duplicate — used by earlier onboarding scripts to decide which
reporting database to write to. Current guidance does not create this row, so a recent install will not
have one.

```sql
SELECT config_key, config_value, add_release,
       CONVERT(VARCHAR(23), add_time, 121) AS add_time
  FROM NBS_ODSE.dbo.NBS_Configuration
 WHERE config_key = 'ENV';
```

If the query returns nothing, skip this step. If it returns a row, that row no longer describes anything
once RTR is removed. Remove it, or return it to its previous value if your jurisdiction used the key for
something else before RTR:

```sql
DELETE FROM NBS_ODSE.dbo.NBS_Configuration WHERE config_key = 'ENV';

SELECT COUNT(*) AS env_rows_remaining
  FROM NBS_ODSE.dbo.NBS_Configuration WHERE config_key = 'ENV';
```

---

## Step 6. Resume MasterETL

### 6a. RDB path only — restore the pre-RTR backup

Do this **before** running MasterETL. Nothing should be connected to `RDB`: RTR is stopped and MasterETL
is not yet running.

```sql
USE master;

ALTER DATABASE [RDB] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

RESTORE DATABASE [RDB]
    FROM DISK = N'<path to your pre-RTR RDB backup>'
    WITH REPLACE, RECOVERY, STATS = 10;

ALTER DATABASE [RDB] SET MULTI_USER;
```

Confirm the restore removed RTR and returned the bookmark:

```sql
SELECT COUNT(*) AS rtr_objects_remaining
  FROM RDB.sys.objects
 WHERE is_ms_shipped = 0
   AND (name LIKE 'nrt[_]%' OR name LIKE 'sp[_]nrt[_]%' OR name LIKE 'sp[_]%[_]event'
        OR name LIKE 'v[_]nrt[_]%' OR name IN ('DATABASECHANGELOG','DATABASECHANGELOGLOCK'));

SELECT TOP (1) *
  FROM RDB.dbo.job_batch_log
 WHERE type_code = 'MasterETL' AND Status_Type = 'complete'
 ORDER BY update_dttm DESC;
```

Expected: `rtr_objects_remaining` is 0, and the batch row is the last MasterETL run before RTR was
installed. That row is where MasterETL will resume.

> Do not restore `RDB` while `reporting-pipeline-service` can still start. That service runs Liquibase
> on boot and will reinstall RTR's schema into the freshly restored database. Confirm Step 1 is complete
> first.
{: .warning }

### 6b. Re-enable the batch jobs

> "Running MasterETL" colloquially covers several jobs. Name them explicitly when re-enabling —
> `MasterETL.bat`, `covid19ETL.bat`, `PHCMartETL.bat`, and any others your jurisdiction schedules —
> rather than relying on the shorthand.
{: .note }

On the **RDB_MODERN path**, MasterETL was writing `RDB` throughout, so it resumes from its own last
successful run and the data gap is small or zero. Confirm the jobs are still scheduled and completing;
if they were quietly disabled during the RTR pilot, re-enable them.

Point reporting consumers back at the original reporting execution server.

### 6c. Run MasterETL and check it properly

Trigger a run through your scheduler, then verify:

```sql
SELECT TOP (5) record_id, batch_id, type_code, Status_Type,
       CONVERT(VARCHAR(23), batch_start_dttm, 121) AS batch_start_dttm,
       CONVERT(VARCHAR(23), batch_end_dttm, 121)   AS batch_end_dttm
  FROM RDB.dbo.job_batch_log
 ORDER BY record_id DESC;
```

Then check the [[sas|SAS]] logs, which is the only place some failures appear — see
[check 10](#check-10-is-not-optional) below.

If a run fails and leaves a stalled batch, clear it before retrying:

```sql
DELETE FROM RDB.dbo.job_batch_log
 WHERE type_code = 'MasterETL' AND Status_Type != 'complete';
```

On the RDB path, MasterETL reprocesses the period RTR was running, deriving it from `NBS_ODSE`, which is
the source of truth. Nothing needs migrating out of the RTR database, and reprocessing a period that was
already loaded does not create duplicate rows.

> A long catch-up may need `RDB_log` enlarged with unlimited growth before it will complete. Check and,
> if needed, enlarge it first:
>
> ```sql
> SELECT name, type_desc, size * 8 / 1024 AS current_MB, max_size, growth
>   FROM RDB.sys.database_files;
>
> ALTER DATABASE RDB MODIFY FILE (NAME = 'RDB_log', SIZE = 4096MB);
> ALTER DATABASE RDB MODIFY FILE (NAME = 'RDB_log', MAXSIZE = UNLIMITED, FILEGROWTH = 256MB);
> ```
>
> To estimate the run, read your own `job_batch_log` history: take recent `batch_start_dttm` to
> `batch_end_dttm` spans and scale by the length of the gap you are closing. Run time varies with
> database size, available resources, and accumulated data, so no published figure will match your
> environment.
{: .warning }

---

## Why the RDB path requires a restore

RTR and MasterETL allocate surrogate keys into the same tables, independently.

MasterETL's dimension keys — `INVESTIGATION_KEY`, `PATIENT_KEY` and the rest — are not database identity
columns. The [[etl|ETL]] assigns them. When RTR is installed against `RDB`, it creates its own key
tables as `IDENTITY` columns and seeds each from MasterETL's current maximum:

```sql
CREATE TABLE dbo.nrt_patient_key (d_patient_key bigint IDENTITY(1,1) NOT NULL, ...);
select @max = max(patient_key)+1 from dbo.d_patient;
DBCC CHECKIDENT ('dbo.nrt_patient_key', RESEED, @max);
```

From that point two independent allocators write into one key space from the same starting value. When
MasterETL next runs it derives the same key RTR has already used:

```text
ERROR: Violation of PRIMARY KEY 'PK__INVESTIG__...'.
       Cannot insert duplicate key in object 'dbo.INVESTIGATION'. The duplicate key value is (4).
```

This is structural rather than a race condition, and it is **not** visible at install time — RTR's
schema migration applies to a live, MasterETL-owned `RDB` without error. The failure appears at the
first MasterETL run afterwards.

### Removing RTR's rows first does not fix it

In testing, deleting the rows RTR had written into MasterETL's tables let MasterETL run without any
error — and produced an **incomplete** reporting database. An investigation present in `NBS_ODSE` never
reached `RDB` across two subsequent runs, because MasterETL's incremental processing had already passed
it. Every signal reported success: exit code 0, no `ERROR:` lines in the SAS logs, `job_batch_log`
marked `complete`.

> A revert that fails loudly gets investigated. A revert that reports success while silently omitting
> records does not. Do not attempt an in-place revert on the RDB path.
{: .warning }

The contamination is also wider than the errors suggest. In a reference test, keys RTR had allocated for
**four patients, one investigation and one LDF record** appeared across **15 tables** — dimensions, link
tables, datamarts and MasterETL's own staging tables. Only two of those tables carried primary-key
constraints on the affected columns; the other thirteen accepted the values silently.

Restoring the pre-RTR backup avoids all of this: RTR's objects and rows were never in it, and the
surrogate key space returns to exactly where MasterETL left it.

---

## Step 7. Decommission the RTR reporting database

**RDB_MODERN path only.** Back up `RDB_MODERN` first if you want to retain it, and decide your retention
period:

```sql
BACKUP DATABASE [RDB_MODERN]
    TO DISK = N'<path>/rdb_modern_final.bak'
    WITH COMPRESSION, INIT, STATS = 10;

RESTORE VERIFYONLY FROM DISK = N'<path>/rdb_modern_final.bak';
```

**Check that nothing references it by name.** Run in each of `NBS_ODSE`, `NBS_SRTE`, `RDB` and
`NBS_MSGOUTE`:

```sql
SELECT DB_NAME()   AS database_name,
       s.name      AS schema_name,
       o.name      AS object_name,
       o.type_desc
  FROM sys.sql_modules m
  JOIN sys.objects o ON o.object_id = m.object_id
  JOIN sys.schemas s ON s.schema_id = o.schema_id
 WHERE o.is_ms_shipped = 0
   AND (m.definition LIKE '%rdb_modern.%' OR m.definition LIKE '%[[]rdb_modern].%');
```

Anything returned here will break when the database is dropped. Expect no rows.

**Drop it:**

```sql
USE master;
ALTER DATABASE [RDB_MODERN] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
DROP DATABASE [RDB_MODERN];

SELECT name, state_desc FROM sys.databases WHERE database_id > 4 ORDER BY name;
```

> `RDB` cannot simply be dropped after a full cutover to RTR — the mirror image of this case. Running
> the same scan with `RDB` substituted returns two objects in `NBS_ODSE` that reference it by name:
> `dbo.sp_PublicHealthCaseFact_DATAMART` and `dbo.uvw_treatment_patient_keys`. Run that scan before
> removing any reporting database.
{: .warning }

---

## Post-revert validation checklist

| # | Check | Expected |
| :--- | :--- | :--- |
| 1 | RTR pods | None running |
| 2 | Helm releases | `helm list` empty |
| 3 | ConfigMaps | Only `kube-root-ca.crt` remains |
| 4 | Connect REST endpoints | Unreachable — the services are gone |
| 5 | Capture instance on `dbo.CN_transportq_out` | Unchanged from before the revert |
| 6 | `cdc.NBS_ODSE_capture` and `cdc.NBS_ODSE_cleanup` | Still present and enabled |
| 7 | The RTR service user | Removed from all databases and the server |
| 8 | RTR-owned Kafka topics, worker-state topics included | Removed; only `__consumer_offsets` remains |
| 9 | MasterETL scheduled and green in `job_batch_log` | `Status_Type = complete` |
| 10 | SAS logs | **Zero lines beginning `ERROR:`** |
| 11 | A record created after the revert | Reaches `RDB` (see below) |
| 12 | Reports | Served from `RDB`, returning expected data |

Checks 1 to 4, and 8:

```bash
kubectl get pods
helm list
kubectl get configmap
kafka-topics --bootstrap-server $BOOTSTRAP --list
```

Checks 5, 6 and 7:

```sql
USE NBS_ODSE;
SELECT t.name AS source_table, ct.capture_instance
  FROM cdc.change_tables ct
  JOIN sys.tables t ON t.object_id = ct.source_object_id;

SELECT name, enabled FROM msdb.dbo.sysjobs WHERE name LIKE 'cdc.%';

SELECT name FROM sys.server_principals WHERE name LIKE '%rtr%';
```

And confirm the reporting database is intact and untouched by RTR:

```sql
SELECT COUNT(*) AS rtr_objects_in_RDB FROM RDB.sys.objects
 WHERE is_ms_shipped = 0
   AND (name LIKE 'nrt[_]%' OR name IN ('DATABASECHANGELOG','DATABASECHANGELOGLOCK'));

SELECT COUNT(*) AS user_tables FROM RDB.sys.tables WHERE is_ms_shipped = 0;

SELECT TOP (5) record_id, type_code, Status_Type,
       CONVERT(VARCHAR(23), batch_end_dttm, 121) AS batch_end_dttm
  FROM RDB.dbo.job_batch_log ORDER BY record_id DESC;
```

### Check 10 is not optional

> MasterETL can exit 0, write `complete` to `job_batch_log`, and log `BATCH_COMPLETE` while a third of
> its database connections are dead. In testing, two of three SAS ODBC librefs failed to connect and
> every conventional success signal still reported success. The failure appeared only in the SAS log.
{: .warning }

On the SAS host, from the report log directory (typically
`.../nedssdomain/Nedss/report/log/`):

```bash
grep -c '^ERROR' MasterETL1.log MasterEtl2.log DynamicDatamart.log SSIS.log
grep -n '^ERROR' MasterETL1.log MasterEtl2.log | head -20
```

Expected: `0` for every file. Confirm all expected library references were assigned:

```bash
grep -E 'Libref [A-Z_]+ was successfully assigned' MasterETL1.log
```

Expected: `NBS_ODS`, `NBS_RDB` and `NBS_SRT`. If only one appears, MasterETL ran with dead connections
and its output is incomplete regardless of what `job_batch_log` says.

### What check 11 must not assert

Do not verify a revert by asserting that every patient in the RTR reporting database reappears in `RDB`.
That assertion fails on a *correct* revert.

MasterETL's `sp_D_PATIENT` inner-joins `PERSON` to `PARTICIPATION`: a patient is invisible to `RDB`
until they participate in a clinical act. RTR's equivalent is entity-centric and captures the Master
Patient Record regardless. So the RTR database legitimately holds patients MasterETL will never create,
and their absence after a revert is correct behaviour rather than data loss.

Enter a new patient **with an investigation** through the NBS UI, run MasterETL, then trace it:

```sql
SELECT TOP (5) p.person_uid, p.last_nm, p.first_nm,
       (SELECT COUNT(*) FROM NBS_ODSE.dbo.Participation pt
         WHERE pt.subject_entity_uid = p.person_uid)  AS participation_rows,
       (SELECT COUNT(*) FROM RDB.dbo.D_PATIENT d
         WHERE d.PATIENT_UID = p.person_uid)          AS in_RDB
  FROM NBS_ODSE.dbo.Person p
 WHERE p.cd = 'PAT'
 ORDER BY p.person_uid DESC;
```

Expected: the new patient has `participation_rows` greater than 0 and `in_RDB = 1`. A patient with
`participation_rows = 0` and `in_RDB = 0` is correct, not a fault.

And confirm the investigation arrived:

```sql
SELECT TOP (5) phc.public_health_case_uid, phc.cd_desc_txt,
       (SELECT COUNT(*) FROM RDB.dbo.INVESTIGATION i
         WHERE i.CASE_UID = phc.public_health_case_uid) AS in_RDB
  FROM NBS_ODSE.dbo.Public_health_case phc
 ORDER BY phc.public_health_case_uid DESC;
```

Two further readings that look like faults but are not:

- `S_INVESTIGATION` is a staging table, holding rows only for investigations processed in the most
  recent run. An empty `S_INVESTIGATION` is normal.
- Records that pre-date CDC being enabled have no rows in the `cdc.*_CT` change tables. That means
  "older than capture", not a broken pipeline.

---

## What this procedure does not cover

- **Automating the revert.** No supporting code exists today.
- **Migrating records that exist only in the RTR reporting database.** They do not need migrating —
  MasterETL re-derives from `NBS_ODSE`, the source of truth. Reprocessing time is the only cost.
- **Reverting the RDB path without a pre-RTR backup.** There is currently no supported path. If this
  applies to you, contact support at [nbs@cdc.gov](mailto:nbs@cdc.gov) before making changes.
