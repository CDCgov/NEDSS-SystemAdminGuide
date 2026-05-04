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

## Release workflow overview

Each release has two phases that must happen in this order (follow the explicit steps in the [Checklist](#checklist) section):

**Phase 1 — Archive the previous release (see [step 1](#1-archive-the-previous-release))**

Cut a `release-X.XX` branch from `main` *before* any new-release content is merged. This preserves the current release docs as a snapshot. On that branch, replace Liquid variables with hardcoded version values and push. The build workflow discovers the branch automatically and adds it to Previous Versions.

**Phase 2 — Update main for the new release (see [steps 2–7](#2-update-version-variables))**

With the archive in place, update `main`: bump the version variables, confirm the guide reflects the new version, review version-sensitive pages, and run quality checks.

> Always complete phase 1 before merging new-release content to `main`. If the archive branch is cut after the version variables are updated, it will capture new-release content instead of the release being archived.
{: .warning }

---

## Checklist

### 1. Archive the previous release

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

> The version banner reads the archived version from the URL automatically and
> does not require find-and-replace.
{: .note }

- [ ] From the current `main` — before any new-release content is merged — create a release branch named for the version being archived (e.g., `release-7.12`). See [workflow.md](workflow.md) for git command reference:
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
- [ ] Confirm the archived version banner shows the correct version (e.g., "Archived: NBS 7.12.0").

### 2. Update version variables

- [ ] In `_config.yml`, update `version_latest` to the new version number (e.g., `7.13`).
- [ ] In `_config.yml`, update `version_latest_tag` to the new version tag (e.g., `v7.13.0`).
- [ ] Update the `title:` field in `_config.yml` to reflect the new version (e.g., `NBS 7.13 System Administrator Guide`).
- [ ] Update the `title:` field in `docs/deploy-nbs7.md` to the new version (e.g., `Deploy NBS 7.13`).
- [ ] Confirm the site builds without errors after the update.

> Updating `version_latest` also updates the version banner (shown on every page), the version callouts on the Introduction, Deploy, and Maintain section landing pages, and all pinned GitHub links that use `version_latest_tag`. The `docs/deploy-nbs7.md` title must be updated manually because Jekyll does not process Liquid variables in front matter.
{: .note }

### 3. Confirm the guide title

- [ ] Confirm the live guide title shows the new version (e.g., "NBS 7.13 System Administrator Guide").
- [ ] Confirm the Deploy section landing page title shows the new version (e.g., "Deploy NBS 7.13").

### 4. Confirm version-sensitive pages

Pages that link to a GitHub repository at a specific version tag use `{{ site.version_latest_tag }}`, which updates automatically when you update the variable in step 2.

- [ ] Search the repo for any remaining hardcoded previous version tag (e.g., `v7.12.0`) and update all instances.
- [ ] Run a link checker to confirm all `version_latest_tag`-pinned links resolve at the new tag (see step 5).

The following pages require manual content review beyond link verification:

| Page | What to review |
|------|----------------|
| `docs/deploy-nbs7/real-time-reporting/rtr-java-services.md` | Review the consolidation warning callout for accuracy. |
| `docs/deploy-nbs7/real-time-reporting/data-compare-tool.md` | The NEDSS-DataCompare link is pinned to `main` — that repo has no version tags. Confirm this is still correct. |
| `docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-data-sync.md` | Confirm the NEDSS-NNDSS release at the new tag includes a `vX.Y.Z.NEDSS.NBS.Modernized.Documentation.zip` asset. If missing, coordinate with the dev team before publishing. |
| `docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-nnd-sync.md` | Same documentation zip caveat as `on-prem-data-sync.md`. |
| `docs/maintain-nbs7/eks-upgrade.md` | Update the Kubernetes versions table. Confirm the conditional add-ons step still reflects correct module version behavior. *(Page not yet created as of 7.12.)* |

> Add rows to this table as pages requiring manual review are identified.

### 5. Quality checks

- [ ] Run a link checker or manually spot-check for broken links (historically a
  known problem at release time).
- [ ] Confirm all new or updated content meets Section 508 requirements (heading
  structure, alt text, table formatting, hyperlink text). See [styles.md §10](styles.md#10-accessibility-compliance-record).
- [ ] Confirm all new or updated content follows Global English and Google
  Developer Style Guide conventions. See [styles.md](styles.md).

### 6. Create a per-release Jira ticket

At the start of each release cycle, create a new Jira ticket in the STLT project
under the [Admin Guide: polishing and hardening] epic. Use this checklist as the
source of truth for line items. Copy the checklist items as acceptance criteria
into the new ticket, and track completion there.

Suggested Jira ticket title: `Admin Guide: Update guide for NBS 7.XX release`

### 7. Final review

- [ ] Confirm the live guide title shows the new version.
- [ ] Confirm the site builds and deploys successfully on GitHub Pages.
- [ ] Peer review completed.
