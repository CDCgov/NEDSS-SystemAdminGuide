---
title: Verbose truncation warnings
layout: page
parent: Maintain NBS 7
redirect_from:
  - /docs/maintain-nbs7/sql-server-configuration.html
  - /docs/maintain-nbs7/sql-server-configuration/
---

# Enable SQL Server verbose truncation warnings

SQL Server Trace Flag 460 provides detailed error messages when string or binary data truncation occurs. This is particularly useful for diagnosing data truncation errors when saving investigations in NBS, as it includes column names and data types in error messages rather than generic truncation warnings.

For more information, see the [Microsoft SQL Server documentation on VERBOSE_TRUNCATION_WARNINGS](https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-scoped-configuration-transact-sql?view=sql-server-ver15#verbose_truncation_warnings---on--off-).

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Benefits for NBS Operations

When Trace Flag 460 is enabled, truncation errors will provide detailed information such as:

- The specific column name where truncation occurred
- The data type and size of the column
- The actual length of the data being inserted

This detailed information significantly reduces troubleshooting time when diagnosing data integrity issues during investigation saves or other database operations in NBS.

## Method 1: Enable at SQL Server Startup (Persistent)

To enable Trace Flag 460 permanently across SQL Server restarts:

1. Open **SQL Server Configuration Manager**
2. Navigate to **SQL Server Services**
3. Right-click on your **SQL Server instance** and select **Properties**
4. Go to the **Startup Parameters** tab
5. Add the parameter: `-T460`
6. Click **Add** then **Apply**
7. **Restart the SQL Server service** for the change to take effect

## Method 2: Enable on Running Instance (No Restart Required)

To enable Trace Flag 460 on a live SQL Server instance without restarting:

```sql
-- Enable trace flag 460 globally for all connections
DBCC TRACEON(460, -1);
```

**Note:** This method enables the trace flag immediately but it will be disabled when SQL Server restarts. For persistent configuration across restarts, use Method 1.

## Verifying Trace Flag Status

To verify that Trace Flag 460 is enabled:

```sql
-- Check if trace flag 460 is enabled
DBCC TRACESTATUS(460);
```

Expected output when enabled:

```text
TraceFlag  Status  Global  Session
460        1       1       0
```
