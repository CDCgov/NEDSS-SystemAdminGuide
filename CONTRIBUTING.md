# RDC Contributor Guide

If you're new to this project, start here.

## Getting started

**Workflow setup and daily git commands:** See [workflow.md](contributing/workflow.md). It covers cloning the repo, VS Code setup, branch and commit commands, and the staging-to-production workflow.

**Formatting standards:** See [styles.md](contributing/styles.md). It covers front matter, headings, callout types, code blocks, links, images, tables, and accessibility requirements.

## Branch naming

Prefix your branch name with your initials. Use a short, descriptive name or include the Jira ticket number:

```
js/add-authentication-docs
js/STLT-123-keycloak-setup
```

Full details in [workflow.md](contributing/workflow.md).

## Commit messages

- Use present tense, imperative mood: **"Add overview section"** — not "Added" or "Adds"
- Keep the subject line under 72 characters
- Reference the Jira ticket when relevant: `Add keycloak installation section (STLT-123)`
- No period at the end of the subject line

## Pull requests

One logical change per PR — one page, one section, one fix. Not a batch of unrelated edits.

A good PR description explains **what changed and why**, not just which files were touched. Link the Jira ticket in the PR description.

PRs should be reviewed within 2 business days. If yours sits longer, it's fine to ping the reviewer.

## Code review

Reviewers should check:

- **Content accuracy** — reviewers are subject matter owners, not just proofreaders
- **Style compliance** — verify formatting follows [styles.md](contributing/styles.md)
- **Front matter** — confirm it's present and complete per [styles.md §1](contributing/styles.md#1-front-matter)
- **No broken links or missing images**
- **Accessibility** — confirm all images have descriptive alt text and no heading levels are skipped; see [styles.md §10](contributing/styles.md#10-accessibility-compliance-record) for standards

## Merging

Use **squash merge** to keep history clean. The PR author merges after approval.

Never merge `preview` directly to `main` — `preview` accumulates work from multiple authors and is not a clean source for production.

## Using templates

The `/templates` directory at the repo root contains starter files for the four content types used in this guide. Use them when creating a new page.

| Template | Content type | Use when... |
|----------|-------------|-------------|
| `templates/concept.md` | Concept | The page explains what something is, how it works, or why it exists — not how to do it |
| `templates/task.md` | Task / Procedure | The page walks the reader through a sequence of steps to accomplish something |
| `templates/reference.md` | Reference | The page is a lookup resource: parameter tables, version requirements, command flags, specs |
| `templates/landing.md` | Landing / Section index | The page is a section parent that orients the reader and links to child pages |

**How to use a template:**

1. Copy the template file to the appropriate `docs/` subdirectory.
2. Rename it using lowercase-hyphenated convention: `deploy-nbs-gateway.md`, not `DeployNBSGateway.md`.
3. Fill in all front matter fields. Replace every all-caps placeholder (`TITLE`, `NAV_ORDER`, `PARENT_TITLE`) with real values. See [styles.md §1](contributing/styles.md#1-front-matter) for field definitions and requirements.
4. Write a `description:` for every new page — even if it is optional, it improves search results for every reader.
5. Write the page content, using the HTML guidance comments as your brief.
6. Remove all HTML guidance comments (`<!-- ... -->`) before committing. Guidance comments are not rendered by Jekyll but they should not be left in as dead weight.

For front matter, formatting, and accessibility standards, see [styles.md](contributing/styles.md).

### Page layout convention

Use this structure on content pages:

1. H1 (`#`) that exactly matches `title:`
2. Brief intro text directly under the H1
3. `## On this page` TOC block
4. First H2 section immediately after the TOC

See [styles.md](contributing/styles.md) for the canonical pattern and examples.

## Scripts and commands

### Running locally

| Command | What it does | Prerequisites |
|---------|-------------|--------------|
| `bundle exec jekyll serve --livereload` | Starts a local Jekyll server with live reload at `http://localhost:4000`. The browser refreshes automatically when you save a file. | Ruby + Bundler (see README Option 2) |
| `docker compose up` | Same as above, using Docker instead of a local Ruby install. | Docker Desktop (see README Option 3) |
| `npm run lint` | Runs markdownlint against all `docs/**/*.md` and root `*.md` files. Reports formatting violations. | `npm install` from repo root |
| `npm run link-check` | Full local link validation for day-to-day use. Runs internal links + external links + GitHub links for changed files. | `npm install` from repo root |
| `npm run link-check:internal` | Checks internal doc links and anchors using repo-aware logic for the `/docs/...html` convention. | `npm install` from repo root |
| `npm run link-check:external` | Runs `markdown-link-check` across docs and top-level markdown files, then prints a broken-link summary. | `npm install` from repo root |
| `npm run link-check:github:changed` | Checks GitHub URLs in changed markdown files only. Fast and suitable for regular editing workflow. | `npm install` from repo root |
| `npm run link-check:github` | Checks all GitHub URLs across docs and top-level markdown files. Use before large link cleanup PRs or periodic audits. | `npm install` from repo root |

Run `npm install` once from the repo root to install the lint and link-check tools before using those commands.

Link-check implementation scripts live in `scripts/`:

- `scripts/check-internal-links.mjs`
- `scripts/check-external-links.mjs`
- `scripts/check-github-links.mjs`

### What runs automatically

**On push to `main`:** `bundle exec jekyll build` runs via `jekyll.yml`, then deploys to GitHub Pages. Two additional steps run before the build:

- **Cleanup `_guide_preview`:** Strips nav-related front matter keys (`parent`, `grand_parent`, `nav_order`, `has_children`) from `_guide_preview/` files before Jekyll builds. These keys have no effect on the nav-excluded collection, but stripping them prevents JTD from misinterpreting them during the build.
- **Release versioning:** Discovers all branches matching `release-*`, checks them out into `_previous_versions/`, and generates a nav-accessible index page for each. This is how the **Previous Versions** section of the site is populated automatically. See [release-checklist.md](contributing/release-checklist.md) for the full release process.

**On push to `preview`:** `bundle exec jekyll build` runs via `jekyll-preview.yml` and deploys to the staging site.

**On PRs to `main`:** The PR check pipeline runs (see [CI checks](#ci-checks) below).

**Daily:** Dependabot opens PRs to update Bundler gems and GitHub Actions versions. These are routine maintenance PRs — review and merge them as they arrive.

## CI checks

Three checks run automatically on every pull request to `main`. You do not need to run them manually — push your branch and GitHub runs them.

| Check | Blocking? | What it checks |
|-------|-----------|---------------|
| **Jekyll build** | Yes — PR cannot merge if build fails | Confirms the full site builds without errors |
| **Markdown lint** | Yes — PR cannot merge if violations are found | Checks formatting against rules in `.markdownlint-cli2.yaml` |
| **Link check** | No — failure shows as a warning, not a blocker | Checks links for broken URLs; external URLs may return false positives |

**If a check fails:** Fix the issue and push to the same branch. GitHub reruns all checks automatically — you don't need to close and reopen the PR.

**Lint failures:** Either fix the violation or add the narrowest inline disable comment needed, with a reason:
```markdown
<!-- markdownlint-disable MD033 -->
Content with inline HTML that is intentionally used here.
<!-- markdownlint-enable MD033 -->
```

For a single line (for example, Liquid-generated fragment links that trigger `MD051` in source files), use a next-line disable:

```markdown
<!-- markdownlint-disable-next-line MD051 -->
[A](#a) · [B](#b)
```

**Link check failures:** Investigate whether the link is genuinely broken. If it's a false positive (e.g., a GitHub URL that returns 429 due to rate limiting), add the URL pattern to `.markdown-link-check.json` with a comment explaining why it's ignored.

Links inside HTML comments (`<!-- ... -->`) are ignored by the repository's link-check scripts. This allows authors to park draft or coming-soon links in commented sections without failing CI.

The production deploy runs only after merge to `main`, not on PRs.

---

# Welcome!
Thank you for contributing to CDC's Open Source projects! If you have any
questions or doubts, don't be afraid to send them our way. We appreciate all
contributions, and we are looking forward to fostering an open, transparent, and
collaborative environment.

Before contributing, we encourage you to also read our [LICENSE](LICENSE),
[README](README.md), and
[code-of-conduct](code-of-conduct.md)
files, also found in this repository. If you have any inquiries or questions not
answered by the content of this repository, feel free to [contact us](mailto:surveillanceplatform@cdc.gov).

## Public Domain
This project is in the public domain within the United States, and copyright and
related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
All contributions to this project will be released under the CC0 dedication. By
submitting a pull request you are agreeing to comply with this waiver of
copyright interest.

## Requesting Changes
Our pull request/merging process is designed to give the CDC Surveillance Team
and other in our space an opportunity to consider and discuss any suggested
changes. This policy affects all CDC spaces, both on-line and off, and all users
are expected to abide by it.

### Open an issue in the repository
If you don't have specific language to submit but would like to suggest a change
or have something addressed, you can open an issue in this repository. Team
members will respond to the issue as soon as possible.

### Submit a pull request
If you would like to contribute, please submit a pull request. In order for us
to merge a pull request, it must:
   * Be at least seven days old. Pull requests may be held longer if necessary
     to give people the opportunity to assess it.
   * Receive a +1 from a majority of team members associated with the request.
     If there is significant dissent between the team, a meeting will be held to
     discuss a plan of action for the pull request.
