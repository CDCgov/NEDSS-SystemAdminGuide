---
title: Validate RTR installation
layout: page
parent: Real-time reporting
nav_order: 4
description: Lightweight checks to confirm that RTR services started, database migration is accounted for, and connectors registered before full pipeline validation.
---

# Validate the RTR installation

Use this page for lightweight checks that confirm real-time reporting (RTR) is running before you run full end-to-end pipeline validation. These checks confirm that the RTR services started successfully, that database migration configuration is accounted for, and that the reporting-pipeline-service registered the Debezium and Kafka Connect connectors.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Scope

These checks validate the RTR deployment, application startup, database migration configuration, and connector registration. They do not replace full data-flow validation.

Validate external dependencies separately, according to your organization's infrastructure and change-management process. These include the managed Kafka cluster, SQL Server connectivity, Change Data Capture enablement, and database change-approval procedures.

## Check service status

List the RTR pods in your namespace. Replace `<namespace>` with your namespace, or omit the flag to use your current namespace:

```bash
kubectl get pods -n <namespace>
```

The RTR services are:

- `debezium`
- `kafka-connect-sink`
- `reporting-pipeline-service`

All RTR pods should be in the `Running` state, and the `READY` column should show that all containers are ready, for example `1/1` or `2/2`. No pods should be in `Pending`, `CrashLoopBackOff`, `Error`, or another unexpected state.

## Check reporting-pipeline-service health

Confirm that the reporting-pipeline-service pod is healthy and that its Kubernetes readiness and liveness probes are passing:

```bash
kubectl describe pod -l app=reporting-pipeline-service -n <namespace>
```

<!-- [SME REVIEW] Confirm the pod label selector app=reporting-pipeline-service matches the deployed chart's labels. -->

Then check the application health endpoint from inside the pod:

```bash
kubectl exec -n <namespace> deploy/reporting-pipeline-service -- \
  curl -s http://localhost:8095/actuator/health
```

The pod should be `Running`, its containers should be `Ready`, and there should be no recent failed readiness or liveness probe events.

The health endpoint should return status `UP`. Because the reporting-pipeline-service handles connector setup, connector health should also be `UP`. If the service reports `DOWN`, check the reporting-pipeline-service logs before continuing.

The following example shows a healthy response:

```json
{
    "status": "UP",
    "groups": ["liveness", "readiness"],
    "components": {
        "connectors": {
            "status": "UP",
            "details": {
                "debezium": {
                    "odse-main-connector": "RUNNING",
                    "odse-schema-only-connector": "RUNNING",
                    "odse-meta-connector": "RUNNING",
                    "srte-connector": "RUNNING"
                },
                "kafkaConnect": { "Kafka-Connect-SqlServer-Sink": "RUNNING" }
            }
        },
        "db": {
            "status": "UP",
            "details": {
                "database": "Microsoft SQL Server",
                "validationQuery": "isValid()"
            }
        },
        "livenessState": { "status": "UP" },
        "readinessState": { "status": "UP" }
    }
}
```

## Check database migration status

Automatic Liquibase migration is enabled by default. The `LIQUIBASE_AUTOMIGRATION_ENABLE` environment variable controls it:

- Unset: automatic migration is enabled.
- `true`: automatic migration is enabled.
- `false`: migrations must be applied separately through your approved database change process.

Review the Liquibase actuator output:

```bash
kubectl exec -n <namespace> deploy/reporting-pipeline-service -- \
  curl -s http://localhost:8095/actuator/liquibase
```

If needed, check the application logs:

```bash
kubectl logs -n <namespace> deploy/reporting-pipeline-service --tail=300
```

If automatic migration is enabled, the service starts without Liquibase errors and the actuator output shows the executed changelogs. If automatic migration is disabled, confirm that the approved migration SQL was applied before continuing. In either case, there should be no changelog, database connection, permission, or migration errors.

## Check connector registration

The health check confirms connector health. This check confirms that the expected connector definitions were registered. Debezium and Kafka Connect run as services, but the reporting-pipeline-service registers the connectors during startup.

Confirm that the connector service URLs are available to the reporting-pipeline-service:

```bash
kubectl exec -n <namespace> deploy/reporting-pipeline-service -- \
  printenv | grep -E 'DEBEZIUM_CONNECT_URL|KAFKA_CONNECT_URL'
```

List the registered Debezium connectors:

```bash
kubectl exec -n <namespace> deploy/reporting-pipeline-service -- sh -c \
  'curl -sf "$DEBEZIUM_CONNECT_URL/connectors"'
```

The expected Debezium connectors are:

- `odse-main-connector`
- `odse-schema-only-connector`
- `odse-meta-connector`
- `srte-connector`

List the registered Kafka Connect connectors:

```bash
kubectl exec -n <namespace> deploy/reporting-pipeline-service -- sh -c \
  'curl -sf "$KAFKA_CONNECT_URL/connectors"'
```

The expected Kafka Connect connector is:

- `Kafka-Connect-SqlServer-Sink`

The connector lists should include the expected Debezium source connectors and the Kafka Connect SQL Server sink connector. If a list is empty, is missing connectors, or the command fails, check the reporting-pipeline-service logs first, because that service registers the connectors.

<!-- [SME REVIEW] Confirm this connector name is stable across deployments rather than environment-specific. -->

## Next steps

When all checks pass, run full end-to-end validation to confirm data movement across the pipeline. Then continue to [Validate the NBS 7 deployment](../../full-deploy/validate-the-deployment.html).
