---
title: Java services
layout: page
parent: Real-time reporting (preview)
nav_order: 4
redirect_from:
  - /docs/7_feature_preview/4_rtr_java_reporting_services.html
  - /docs/7_feature_preview/4_rtr_java_reporting_services/
---

# Deploy real-time reporting (RTR) Java services

This page covers deploying the RTR Java services that process streamed events from Kafka and load domain-specific reporting data.

1. The helm chart for all RTR java services should be available under charts/rtr.
2. Validate the Kubernetes secret for the database credentials:

   ```bash
   kubectl get secret/database-access -o yaml
   ```

   a. Ensure that the secret contains the correct database username and password, kafka cluster, and other necessary configurations.
      If the secret does not exist, create it using the following command or by applying the provided YAML file
      (Make sure to replace the placeholders with actual values):
      Script location: [NEDSS-DataReporting/create-kubernetes-secrets](https://github.com/CDCgov/NEDSS-Helm/blob/main/k8-manifests/nbs-secrets.yaml)

      ```bash
      kubectl apply -f k8-manifests/nbs-secrets.yaml
      ```

3. Validate image repository:

   ```yaml
     global.image.repository: "quay.io/us-cdcgov/cdc-nbs-modernization/data-reporting-service"
   ```

4. Update any feature flag for each of the services:
   - a. Please ensure `PHCMartETL.bat` is turned off before enabling updates to PublicHealthCaseFact datamart via RTR.

      ```yaml
      featureFlag:
        investigation-reporting:
           phcDatamartEnable: '''true'''
      ```

5.Install helm chart for all the RTR java services

   ```bash
   helm install rtr . -f values.yaml
   ```

6.Verify if pods are all running

   ```bash
   kubectl get pods
   ```

   Example Expected output:

   ```text
      NAME                                                READY   STATUS           RESTARTS             AGE
      rtr-java-services-investigation-reporting-<hash>    1/1     Running            0                  2m6s
      rtr-java-services-ldfdata-reporting-<hash>          1/1     Running            0                  2m6s
      rtr-java-services-observation-reporting-<hash>      1/1     Running            0                  2m6s
      rtr-java-services-organization-reporting-<hash>     1/1     Running            0                  2m6s
      rtr-java-services-person-reporting-<hash>           1/1     Running            0                  2m6s
      rtr-java-services-post-processing-reporting-<hash>  1/1     Running            0                  2m6s
      ```

7.Validate services (on browser).
    The following services should be available at the specified URLs. Replace `<exampledomain>` with your actual domain.
   Replace `app.EXAMPLE_DOMAIN` with the URL of your modern app as shown in [Table](../../../docs/deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.html#deploy-nginx-ingress-controller-on-your-cluster)

   a. investigation-svc

   ```text
   https://data.<exampledomain>/reporting/investigation-svc/status
   Expected: Investigation Service Status OK
   ```

   b. person-svc

   ```text
   https://data.<exampledomain>/reporting/person-svc/status
   Expected: Person Service Status OK
   ```

   c. observation-svc

   ```text
   https://data.<exampledomain>/reporting/observation-svc/status
   Expected: Observation Service Status OK
   ```

   d. organization-svc

   ```text
   https://data.<exampledomain>/reporting/organization-svc/status
   Expected: Organization Service Status OK
   ```

   e. ldfdata-svc

  ```text
  https://data.<exampledomain>/reporting/ldfdata-svc/status
  Expected: LDFData Service Status OK
  ```

   f. post-processing-svc

  ```text
  https://data.<exampledomain>/reporting/post-processing-svc/status
  Expected: Post Processing Service Status OK
  ```
