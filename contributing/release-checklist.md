# Admin Guide release checklist

Use this checklist for each NBS 7 release. At the start of each release cycle,
copy the checklist items into a new Jira ticket and track completion there.

For the broader NBS release process (engineering, testing, beta, CDC approval),
see the [Template] 6 Release Process Checklist in NBS Central.

---

## Before you begin

Identify the following values for the new release before starting any checklist items.

| Value | Example | Notes |
|---|---|---|
| New version number | `7.13` | Used in `version_latest` |
| New version tag | `v7.13.0` | Used in `version_latest_tag`; confirm tag exists in NEDSS-Infrastructure before starting |
| Previous version number | `7.12` | Used in archiving steps |
| Previous version tag | `v7.12.0` | Used in archiving steps |

---

## Checklist

### 1. Update version variables

- [ ] In `_config.yml`, update `version_latest` to the new version number (e.g., `7.13`).
- [ ] In `_config.yml`, update `version_latest_tag` to the new version tag (e.g., `v7.13.0`).
- [ ] Update the `title:` field in `_config.yml` to reflect the new version (e.g., `NBS 7.13 System Administrator Guide`).
- [ ] Confirm the site builds without errors after the update.

### 2. Confirm the guide title

- [ ] Confirm the guide title reflects the new version (e.g., "NBS 7.13 System Administrator Guide").
  The title is set in `_config.yml` and must be updated manually alongside `version_latest`.

### 3. Confirm version-sensitive pages

Every page that links to a GitHub repository at a specific version tag is version-sensitive.
Links using `{{ site.version_latest_tag }}` update automatically when you update the variable
in step 1. This step confirms those links resolve at the new tag and flags pages that also
need manual content review.

- [ ] Search the repo for any remaining hardcoded previous version tag (e.g., `v7.12.0`)
  and update all instances to the new tag.
- [ ] Work through the page list below and confirm each item.

| Page | What to confirm |
|------|----------------|
| `docs/deploy-nbs7/quickstart.md` | NEDSS-Infrastructure and NEDSS-Helm chart README links resolve at the new tag. |
| `docs/deploy-nbs7/deploy-on-aws/provision-aws.md` | NEDSS-Infrastructure Terraform README link resolves at the new tag. |
| `docs/deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.md` | NEDSS-Helm Traefik chart links resolve at the new tag. |
| `docs/deploy-nbs7/real-time-reporting/real-time-reporting.md` | NEDSS-DataReporting script links and NEDSS-Helm secrets link resolve at the new tag. |
| `docs/deploy-nbs7/real-time-reporting/liquibase.md` | NEDSS-Helm Liquibase chart link resolves at the new tag. |
| `docs/deploy-nbs7/real-time-reporting/debezium.md` | NEDSS-Helm Debezium chart link resolves at the new tag. |
| `docs/deploy-nbs7/real-time-reporting/kafka-connector.md` | NEDSS-Helm Kafka chart link resolves at the new tag. |
| `docs/deploy-nbs7/real-time-reporting/rtr-java-services.md` | NEDSS-Helm RTR chart and NEDSS-Helm secrets links resolve at the new tag. Review the consolidation warning callout for accuracy. |
| `docs/deploy-nbs7/real-time-reporting/data-compare-tool.md` | Both NEDSS-Helm links resolve at the new tag. NEDSS-DataCompare link stays at `main` — that repo has no version tags. |
| `docs/deploy-nbs7/microservices-deployment/case-notification.md` | NEDSS-Helm Keycloak profile link resolves at the new tag. |
| `docs/deploy-nbs7/microservices-deployment/data-ingestion.md` | NEDSS-DataIngestion DB scripts link resolves at the new tag. |
| `docs/deploy-nbs7/microservices-deployment/case-notification/api-testing.md` | NEDSS-Helm templates and NEDSS-NNDSS-Case-Notifications links resolve at the new tag. |
| `docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-data-sync.md` | NEDSS-NNDSS scripts links resolve at the new tag. |
| `docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-nnd-sync.md` | NEDSS-NNDSS README link resolves at the new tag. |
| `docs/maintain-nbs7/eks-upgrade.md` | Update the Kubernetes versions table. Confirm the conditional add-ons step (Step 4) still reflects the correct `eks_nbs` module version behavior. *(Page not yet created as of 7.12.)* |

> Add rows to this table as version-sensitive pages are identified.

### 4. Review per-page version callouts

Pages with a per-page version callout (e.g., "This page applies to NBS 7.12")
are updated automatically when `version_latest` is updated in step 1.

- [ ] Search the repo for any hardcoded version callouts and update them.

> Add pages with callouts to this list as they are identified.

### 5. Quality checks

- [ ] Run a link checker or manually spot-check for broken links (historically a
  known problem at release time).
- [ ] Confirm all new or updated content meets Section 508 requirements (heading
  structure, alt text, table formatting, hyperlink text). See [styles.md §10](styles.md#10-accessibility-compliance-record).
- [ ] Confirm all new or updated content follows Global English and Google
  Developer Style Guide conventions. See [styles.md](styles.md).

### 6. Archive the previous release

The site uses branch-based archiving. Any branch named `release-*` is
automatically discovered by the GitHub Actions build workflow, checked out into
`_previous_versions/<branch>/` at build time, and rendered as a Previous
Versions entry in the left nav. **Do not manually copy files into
`_previous_versions/`.** That directory is ephemeral and not committed to `main`.

Because Jekyll builds the entire site — including archived release branches —
using `_config.yml` from `main`, Liquid variables (`{{ site.version_latest }}`,
`{{ site.version_latest_tag }}`) in archived files would resolve to the
**current** release values, not the archived ones. The variables must be
replaced with hardcoded values on the release branch before it is pushed.

- [ ] From the current `main`, create a new branch named `release-7.12` (see [workflow.md](workflow.md) for git command reference):
  ```
  git checkout -b release-7.12
  ```
- [ ] On that branch, do a global find-and-replace of `{{ site.version_latest }}`
  with the previous version number (e.g., `7.12`).
- [ ] Do a global find-and-replace of `{{ site.version_latest_tag }}` with the
  previous version tag (e.g., `v7.12.0`).
- [ ] Commit and push `release-7.12` to the remote. The next push to `main`
  will trigger the build workflow to discover and include this branch.
- [ ] Confirm the archived release renders correctly and all links resolve.
- [ ] Confirm the archived release appears correctly under "Previous Versions"
  in the sidebar.

### 7. Create a per-release Jira ticket

At the start of each release cycle, create a new Jira ticket in the STLT project
under the [Admin Guide: polishing and hardening] epic. Use this checklist as the
source of truth for line items. Copy the checklist items as acceptance criteria
into the new ticket, and track completion there.

Suggested Jira ticket title: `Admin Guide: Update guide for NBS 7.XX release`

### 8. Final review

- [ ] Confirm the live guide title shows the new version.
- [ ] Confirm the site builds and deploys successfully on GitHub Pages.
- [ ] Peer review completed.
