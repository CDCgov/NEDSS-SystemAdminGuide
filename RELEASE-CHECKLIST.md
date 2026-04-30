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

### 3. Update version-sensitive pages

The following pages contain hardcoded version references or version-specific
content that requires manual review at each release.

- [ ] `docs/deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.md` — confirm
  Traefik Helm chart links resolve correctly at the new tag.
- [ ] `docs/deploy-nbs7/real-time-reporting/real-time-reporting.md` — confirm
  NEDSS-DataReporting script links resolve correctly at the new tag.
- [ ] `docs/deploy-nbs7/real-time-reporting/debezium.md` — confirm Helm chart link.
- [ ] `docs/deploy-nbs7/real-time-reporting/kafka-connector.md` — confirm Helm chart link.
- [ ] `docs/deploy-nbs7/real-time-reporting/rtr-java-services.md` — confirm Helm chart link;
  review the consolidation warning callout for accuracy.
- [ ] `docs/deploy-nbs7/real-time-reporting/data-compare-tool.md` — confirm both Helm chart links.
- [ ] `docs/maintain-nbs7/eks-upgrade.md` — update the Kubernetes versions table;
  confirm the conditional add-ons step (Step 4) still reflects the correct
  `eks_nbs` module version behavior. *(Page not yet created as of 7.12.)*

> Add pages to this list as version-sensitive content is identified.

### 4. Update pinned repository links

Pages that link to GitHub repositories at a specific version tag are updated
automatically via `{{ site.version_latest_tag }}`. Confirm updated links resolve correctly.

- [ ] Search the repo for any remaining hardcoded previous version tag (e.g., `v7.12.0`) and
  update all instances to the new tag.
- [ ] Confirm updated links resolve correctly.

Known pages with pinned repo links as of 7.12 (managed via `{{ site.version_latest_tag }}`):

- `docs/deploy-nbs7/quickstart.md` (NEDSS-Infrastructure, NEDSS-Helm chart READMEs)
- `docs/deploy-nbs7/deploy-on-aws/provision-aws.md` (NEDSS-Infrastructure Terraform README)
- `docs/deploy-nbs7/initial-kubernetes-deployment/initial-kubernetes-deployment.md` (NEDSS-Helm Traefik charts)
- `docs/deploy-nbs7/real-time-reporting/real-time-reporting.md` (NEDSS-DataReporting scripts, NEDSS-Helm secrets)
- `docs/deploy-nbs7/real-time-reporting/liquibase.md` (NEDSS-Helm Liquibase chart)
- `docs/deploy-nbs7/real-time-reporting/debezium.md` (NEDSS-Helm Debezium chart)
- `docs/deploy-nbs7/real-time-reporting/kafka-connector.md` (NEDSS-Helm Kafka chart)
- `docs/deploy-nbs7/real-time-reporting/rtr-java-services.md` (NEDSS-Helm RTR chart, NEDSS-Helm secrets)
- `docs/deploy-nbs7/real-time-reporting/data-compare-tool.md` (NEDSS-Helm; NEDSS-DataCompare link stays at `main` — repo has no version tags)
- `docs/deploy-nbs7/microservices-deployment/case-notification.md` (NEDSS-Helm Keycloak profile)
- `docs/deploy-nbs7/microservices-deployment/data-ingestion.md` (NEDSS-DataIngestion DB scripts)
- `docs/deploy-nbs7/microservices-deployment/case-notification/api-testing.md` (NEDSS-Helm templates, NEDSS-NNDSS-Case-Notifications)
- `docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-data-sync.md` (NEDSS-NNDSS scripts)
- `docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-nnd-sync.md` (NEDSS-NNDSS README)

> Add pages to this list as pinned links are identified.

### 5. Review per-page version callouts

Pages with a per-page version callout (e.g., "This page applies to NBS 7.12")
are updated automatically when `version_latest` is updated in step 1.

- [ ] Search the repo for any hardcoded version callouts and update them.

> Add pages with callouts to this list as they are identified.

### 6. Quality checks

- [ ] Run a link checker or manually spot-check for broken links (historically a
  known problem at release time).
- [ ] Confirm all new or updated content meets Section 508 requirements (heading
  structure, alt text, table formatting, hyperlink text).
- [ ] Confirm all new or updated content follows Global English and Google
  Developer Style Guide conventions.

### 7. Archive the previous release

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

- [ ] From the current `main`, create a new branch named `release-7.12`:
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

### 8. Create a per-release Jira ticket

At the start of each release cycle, create a new Jira ticket in the STLT project
under the [Admin Guide: polishing and hardening] epic. Use this checklist as the
source of truth for line items. Copy the checklist items as acceptance criteria
into the new ticket, and track completion there.

Suggested Jira ticket title: `Admin Guide: Update guide for NBS 7.XX release`

### 9. Final review

- [ ] Confirm the live guide title shows the new version.
- [ ] Confirm the site builds and deploys successfully on GitHub Pages.
- [ ] Peer review completed.
