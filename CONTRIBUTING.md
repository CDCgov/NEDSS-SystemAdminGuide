# RDC Contributor Guide

If you're new to this project, start here.

## Getting started

**Workflow setup and daily git commands:** See [WORKFLOW.md](WORKFLOW.md). It covers cloning the repo, VS Code setup, branch and commit commands, and the staging-to-production workflow.

**Formatting standards:** See [STYLES.md](STYLES.md). It covers headings, callout types, code blocks, links, images, and tables.

## Branch naming

Prefix your branch name with your initials. Use a short, descriptive name or include the Jira ticket number:

```
js/add-authentication-docs
js/STLT-123-keycloak-setup
```

Full details in [WORKFLOW.md](WORKFLOW.md).

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
- **Style compliance** — verify formatting follows [STYLES.md](STYLES.md)
- **Front matter** — confirm it's present and complete per [FRONT-MATTER.md](FRONT-MATTER.md)
- **No broken links or missing images**

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
3. Fill in all front matter fields. Replace every all-caps placeholder (`TITLE`, `NAV_ORDER`, `PARENT_TITLE`) with real values. See [FRONT-MATTER.md](FRONT-MATTER.md) for field definitions and requirements.
4. Write a `description:` for every new page — even if it is optional, it improves search results for every reader.
5. Write the page content, using the HTML guidance comments as your brief.
6. Remove all HTML guidance comments (`<!-- ... -->`) before committing. Guidance comments are not rendered by Jekyll but they should not be left in as dead weight.

For front matter field reference, see [FRONT-MATTER.md](FRONT-MATTER.md).
For formatting standards (headings, callouts, code blocks, links, images, tables), see [STYLES.md](STYLES.md).

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
