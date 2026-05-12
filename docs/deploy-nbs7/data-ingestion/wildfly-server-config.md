---
title: Wildfly server
layout: page
parent: Deploy data ingestion service (DI API)
nav_order: 1
description: Configure the Windows Task Scheduler on NBS WildFly server to run the ELR Importer batch process.
redirect_from:
  - /docs/6_microservices_deployment/6a_di_wildfly_Server_config.html
  - /docs/6_microservices_deployment/6a_di_wildfly_Server_config/
  - /docs/3_base_application/wildfly-server-config-di.html
  - /docs/3_base_application/wildfly-server-config-di/
  - /docs/deploy-nbs7/microservices-deployment/data-ingestion/wildfly-server-config.html
  - /docs/deploy-nbs7/microservices-deployment/data-ingestion/wildfly-server-config/
---

# WildFly server configuration

Configure the Windows Task Scheduler on your NBS 6 WildFly server to run the ELR Importer batch process.

1. Connect to the NBS 6 Windows server using a remote desktop client such as Microsoft Remote Desktop. You will need the server's hostname or IP address, username, and password.
2. Follow the [Windows Task Scheduler for ELR Importer](../microservices-deployment/images/NM-Windows%20Task%20scheduler%20for%20ELRImporter.pdf) (PDF) guide to create and configure the scheduled task.
