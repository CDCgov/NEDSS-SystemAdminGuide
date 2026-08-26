# Admin Guide release checklist

Use this checklist for each NBS 7 release.

For the broader NBS release process (engineering, testing, beta, CDC approval), see the [Template] 6 Release Process Checklist in NBS Central.

---

## Before you begin

Identify the following values and complete the setup steps before starting the checklist.

| Value | Example | Notes |
|---|---|---|
| New version number | `7.13` | Used in `version_latest` |
| New version tag | `v7.13.0` | Used in `version_latest_tag`; see the note below before choosing the tag |
| Previous version number | `7.12` | Used in archiving steps |
| Previous version tag | `v7.12.0` | Used in archiving steps |

> Point `version_latest_tag` at the tag that has a GitHub **Release** attached, not just a matching git tag. A tag without a release still loads a page, but it has no release notes and none of the download assets the guide sends readers to. Confirm the release's asset filenames match what the guide references — they do not always follow the tag.
{: .note }

- [ ] Create a new Jira ticket in the STLT project under the **SysAdmin Guide: New release checklists** epic. Suggested title: `Admin Guide: Update guide for NBS X.XX release`. Copy the checklist items below as acceptance criteria and track completion there.

---

## Release workflow overview

Each release has two phases that must happen in this order (follow the explicit steps in the [Checklist](#checklist) section):

**Phase 1 — Archive the previous release (see [step 1](#1-archive-the-previous-release))**

Cut a `release-X.XX.X` branch from `main` *before* any new-release content is merged. This preserves the current release docs as a snapshot. On that branch, replace Liquid variables with hardcoded version values and push. The build workflow discovers the branch automatically and adds it to Previous Versions.

**Phase 2 — Update the guide for the new release (see [steps 2–6](#2-update-version-variables))**

Perform these steps on the **next-version branch** (e.g., `7.13`) — the long-lived branch where this release's content has been developed over the cycle. It is not cut from `main` at this point: `main` still holds the release you archived in phase 1, and is not updated until GA, when the next-version branch replaces it. Bump the version variables, confirm the guide reflects the new version, review version-sensitive pages, and run quality checks.

> Always complete phase 1 before merging new-release content to `main`. If the archive branch is cut after the version variables are updated, it will capture new-release content instead of the release being archived.
{: .warning }

---

## Checklist

### 1. Archive the previous release

The site uses branch-based archiving. Any branch named `release-*` is automatically discovered by the GitHub Actions build workflow, checked out into `_previous_versions/<branch>/` at build time, and rendered as a Previous Versions entry in the left nav. **Do not manually copy files into `_previous_versions/`.** That directory is ephemeral and not committed to `main`.

Because Jekyll builds the entire site — including archived release branches — using `_config.yml` from `main`, Liquid variables (`{{ site.version_latest }}`, `{{ site.version_latest_tag }}`) in archived files would resolve to the **current** release values, not the archived ones. The variables must be replaced with hardcoded values on the release branch before it is pushed.

> The version banner reads the archived version from the URL automatically and does not require find-and-replace.
{: .note }

- [ ] From the current `main` — before any new-release content is merged — create a release branch named for the version being archived (e.g., `release-7.12.0`). See [workflow.md](workflow.md) for git command reference:

  ```bash
  git checkout -b release-7.12.0
  ```

- [ ] On that branch, hardcode the version number in all `.md` files in the `/docs/` directory:

  ```bash
  git grep -z -F -l '{{ site.version_latest }}' -- docs \
  | xargs -0 sed -i '' -e 's/{{ site\.version_latest }}/7.12/g'
  ```

- [ ] Hardcode the version tag (used in URLs) in all `.md` files in the `/docs/` directory:

  ```bash
  git grep -z -F -l '{{ site.version_latest_tag }}' -- docs \
  | xargs -0 sed -i '' -e 's/{{ site\.version_latest_tag }}/v7.12.0/g'
  ```

- [ ] Update the remaining occurrences manually:
  - `index.md`
  - `_includes/head_custom.html`
- [ ] Check for straggler mentions of either variable and confirm they are expected:

  ```bash
  git grep -F -l '{{ site.version_latest'
  ```

- [ ] Rebuild the site:

  ```bash
  bundle exec jekyll build
  ```

- [ ] Check your local build.
- [ ] Run lint checks:

  ```bash
  npm run lint
  npm run link-check
  ```

- [ ] Commit and push `release-7.12.0` to the remote. The next push to `main` will trigger the build workflow to discover and include this branch, or you can manually trigger it in **GitHub Actions > Deploy Jekyll site to Pages** (against branch `main`).
- [ ] Confirm the archived release renders correctly and all links resolve.
- [ ] Confirm the archived release appears correctly under "Previous Versions" in the sidebar.
- [ ] Confirm the archived version banner shows the correct version (e.g., "Archived: NBS 7.12.0").

### 2. Update version variables

Steps 2–6 are performed on the next-version branch (e.g., `7.13`) — not on `main`, and not on the `release-X.XX.X` archive branch from [step 1](#1-archive-the-previous-release). The archive branch must keep the previous release's hardcoded values, and `main` still holds the previous release until GA, when the next-version branch replaces it.

- [ ] In `_config.yml`, update `version_latest` to the new version number (e.g., `7.13`).
- [ ] In `_config.yml`, update `version_latest_tag` to the new version tag (e.g., `v7.13.0`).
- [ ] Update the `title:` field in `_config.yml` to reflect the new version (e.g., `NBS 7.13 System Administrator Guide`).
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
| `docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-data-sync.md` | Confirm the NEDSS-NNDSS release at the new tag includes a `vX.Y.Z.NEDSS.NBS.Modernized.Documentation.zip` asset. If missing, coordinate with the dev team before publishing. |
| `docs/deploy-nbs7/microservices-deployment/nnd-service/on-prem-nnd-sync.md` | Same documentation zip caveat as `on-prem-data-sync.md`. |
| `docs/maintain-nbs7/kubernetes-upgrade.md` | Confirm `version_k8s` in `_config.yml` matches the Kubernetes version this release was tested against. Update the minor-version upgrade example, which is hardcoded. Confirm the conditional add-ons step still reflects correct module version behavior. |
| `docs/supported-versions.md` | Update as needed. If this release is a patch (7.x.y), decide patch inheritance for the Supported NBS versions page. |
| `docs/nbs7-introduction/release-history.md` | Confirm the latest, supported, and unsupported NBS 7 version badges are accurate. |
| `docs/deploy-nbs7/full-deploy/kubernetes-setup/deploy-core-services.md` | Reverify the UI screenshots against the versions shipped with this release. |

> Add rows to this table as pages requiring manual review are identified. Some pages also carry an in-page `<!-- RELEASE CHECKLIST: ... -->` comment describing what to check. Run `git grep 'RELEASE CHECKLIST' -- docs` each cycle to catch pages that carry a marker but are not yet listed here.

### 5. Quality checks

- [ ] Run the markdown linter `npm run lint` and resolve any reported issues.
- [ ] Run the link checker `npm run link-check` for broken links (historically a known problem at release time).
- [ ] Confirm all new or updated content meets Section 508 requirements (heading structure, alt text, table formatting, hyperlink text). See [styles.md §10](styles.md#10-accessibility-compliance-record).
- [ ] Confirm all new or updated content follows Global English and Google Developer Style Guide conventions. See [styles.md](styles.md).

### 6. Final review

- [ ] Confirm the live guide title shows the new version.
- [ ] Confirm the site builds and deploys successfully on GitHub Pages.
- [ ] Peer review completed.
- [ ] For content requiring CDC eclearance, generate the review document(s) for the changed chapters and submit them. See [Generate an eclearance review document](workflow.md#generate-an-eclearance-review-document).
