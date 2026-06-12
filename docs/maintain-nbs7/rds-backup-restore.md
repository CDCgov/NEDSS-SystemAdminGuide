---
title: Back up and restore on Amazon RDS
layout: page
nav_order: 2
parent: Maintain NBS 7
description: 
---

# Back up and restore a SQL Server database on Amazon RDS

If you host your database on Amazon RDS, use the RDS backup and restore stored procedures to back up and restore SQL Server databases within an existing instance.

A common use of this procedure is creating `rdb_modern` for real-time reporting (RTR) deployment. You restore `RDB` under a new name within the same instance with the Amazon RDS backup and restore stored procedures. If you want to create an entirely new DB instance instead, you can use the Amazon RDS snapshot restore functionality in the AWS Management Console. For more information on snapshot restore, see [Creating a DB snapshot for Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateSnapshot.html) and [Restore an Amazon RDS DB instance from a DB snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.RestoringFromSnapshot.html) in the Amazon RDS User Guide.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Enable Backup and Restore on Amazon RDS

Complete the following steps to verify that the **Backup and Restore** option is enabled and enable the configuration if needed.

1. Sign in to the AWS Management Console and navigate to the **Aurora and RDS** service console.
1. Navigate to **Databases**, choose your SQL Server instance, and view the **Summary** and **Configuration** sections to find the **Engine** and **Engine version** values that you need in the next steps.
1. Select **Option groups** from the navigation sidebar and choose the option group attached to your DB instance.
1. Review the **Options** section and confirm that **SQLSERVER_BACKUP_RESTORE** is listed.
   - If it is listed, no action is needed. Proceed to [Enable ad hoc distributed queries](#enable-ad-hoc-distributed-queries).
   - If it is not listed, continue with the next steps to create a custom option group.
1. Navigate to **Option groups** and select **Create group**. Configure the following:
   - **Name:** Enter a descriptive name for your custom option group such as `sqlserver-backup-restore-se-15-00`.
   - **Engine:** Select the SQL Server engine edition that matches your DB instance.
   - **Major engine version:** Select the version that matches your DB instance.
1. Select **Create** to save the empty group.
1. Select your new option group from the list, choose **Add option**, and configure the following:
   - **Option name:** Select **SQLSERVER_BACKUP_RESTORE**.
   - **S3 bucket:** Select the S3 bucket where backups will be stored.
   - **IAM role:** Select or create an Amazon IAM role that has permission to access the S3 bucket you use for backups.
1. Select **Add option** to finish configuring the option group.
1. Navigate to **Databases** and select your SQL Server DB instance.
1. Select **Modify**.
1. In the **Additional configuration** section, locate the **Option group** field and select your new custom option group.
1. Select **Continue** and choose whether to apply the change immediately or during the next scheduled maintenance window. If your NBS 6 instance is running, applying immediately might cause a brief outage. Schedule the change during a maintenance window and notify users before proceeding.
1. Select **Modify DB instance** to confirm your changes.

## Enable ad hoc distributed queries

Complete the following steps to verify your current setting and enable the ad hoc distributed queries parameter if needed. This parameter is required to enable Change Data Capture.

1. Sign in to the AWS Management Console and navigate to the **Aurora and RDS** service console.
1. Navigate to **Databases**, choose your SQL Server instance, and view the **Summary** and **Configuration** sections to find the **Engine**, **Engine version**, and **DB instance parameter group** values that you need in the next steps.
1. Select **Parameter groups** from the navigation sidebar and choose the parameter group attached to your DB instance.
1. Search for the `ad hoc distributed queries` parameter and confirm it is set to `1`.
   - If the parameter is set to `1`, no action is needed. Proceed to [Back up and restore RDB on Amazon RDS](#back-up-and-restore-rdb-on-amazon-rds).
   - If the parameter is set to `0` and your instance uses a custom parameter group, update the value to `1`, select **Save changes**, and proceed to [Back up and restore RDB on Amazon RDS](#back-up-and-restore-rdb-on-amazon-rds).
   - If your instance uses the default parameter group, you cannot edit it directly. Continue with the next steps to create a custom parameter group.
1. Select **Create parameter group** and configure the following:
   - **Name:** Enter a descriptive name such as `enable-ad-hoc-distributed-queries`.
   - **Engine type:** Select the SQL Server engine edition that matches your DB instance.
   - **Parameter group family:** Select the engine and version that matches your DB instance.
1. Select **Create** to save the parameter group.
1. Open the new parameter group and select **Edit**.
1. Search for `ad hoc distributed queries` and set the value to `1`.
1. Navigate to **Databases** and select your SQL Server DB instance.
1. Select **Modify**.
1. In the **Additional configuration** section, locate the **Parameter group** field and select your new custom parameter group.
1. Select **Continue** and choose whether to apply the change immediately or during the next scheduled maintenance window. If your NBS 6 instance is running, applying immediately might cause a brief outage. Schedule the change during a maintenance window and notify users before proceeding.
1. Select **Modify DB instance** to confirm your changes.

## Back up and restore RDB on Amazon RDS

The following steps use backup and restore to create a new database within an existing Amazon RDS database instance.

1. Open a SQL client and connect to your SQL Server instance.
1. Run the following procedure to back up `RDB` to Amazon S3:

   ```sql
   exec msdb.dbo.rds_backup_database
   @source_db_name='RDB',
   @s3_arn_to_backup_to='arn:aws:s3:::<s3-bucket-name>/<s3-path-prefix>/<rdb_backup_filename.bak>',
   @type='FULL'
   ```

   > Use the same filename for `<rdb_backup_filename.bak>` in both the backup and restore procedures. The restore procedure retrieves the file that the backup procedure wrote to Amazon S3.
   {: .note }

1. Run the following procedure to check the status:

   ```sql
   exec msdb.dbo.rds_task_status;
   ```

1. Run the following procedure to restore `RDB` as `rdb_modern`:

   ```sql
   exec msdb.dbo.rds_restore_database
   @restore_db_name='rdb_modern',
   @s3_arn_to_restore_from='arn:aws:s3:::<s3-bucket-name>/<s3-path-prefix>/<rdb_backup_filename.bak>',
   @type='FULL';
   ```

1. Run the following procedure to check the status:

   ```sql
   exec msdb.dbo.rds_task_status;
   ```
