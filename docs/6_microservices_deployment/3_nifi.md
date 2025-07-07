---
title: Nifi
layout: page
parent: Microservices Deployment
nav_order: 3
nav_enabled: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Deploy Nifi via helm chart

1. Important Note: The NIFI ingress is intentionally disabled by default to enhance security. Consequently, the NIFI admin UI is not accessible out of the box. To enable access to the NIFI admin interface, it is necessary to activate the ingress feature by setting "ingress:enabled: true" within the values.yaml file before initiating the installation process using the Helm chart. For the sake of heightened security, it is strongly advised to establish a privately accessible domain name instead of a public one, considering the presence of known security vulnerabilities within NIFI.
2. The helm chart for nifi should be available under charts/nifi-efs.
3. In the values.yaml file, replace all occurrences of nifi.EXAMPLE_DOMAIN with your domain name as shown in [Table](/just-the-doc/docs/4_initial_kubernetes_deployment/1_nginx_ingress_deployment.html#deploy-nginx-ingress-controller-on-the-kubernetes-cluster).
4. Ensure the image repository and tags are populated with the following:
  ```yaml
  image:
    repository: quay.io/us-cdcgov/cdc-nbs-modernization/nifi
    tag: <release-version-tag> e.g v1.0.1
  ```
5. Update the efsFileSystemId with the [efs-id](https://us-east-1.console.aws.amazon.com/efs/home?region=us-east-1#/file-systems).
6. Populate jdbc connection string with the same information (refer Table - 5) as before which includes the username and password.
  ```yaml
  jdbcConnectionString: "jdbc:sqlserver://EXAMPLE_DB_ENDPOINT:1433;databaseName=NBS_ODSE;user=DBUser;password=DBpassword;encrypt=true;trustServerCertificate=true;"
  ```
7. Populate singleUserCredentialsUsername to change the default of “admin“ username
8. Populate singleUserCredentialsPassword with the password for the NIFI admin UI. This can be any password of your choice.
9. After updating the values file, run the following command to install nifi.
  ```bash
  helm install nifi -f ./nifi-efs/values.yaml nifi-efs
  ```
10. IMPORTANT: Confirm the pod is running before proceeding with the next deployment using the below command. If the pod is still creating (or in any other state other than running), wait and/or troubleshoot.
  ```bash
  kubectl get pods
  ```
