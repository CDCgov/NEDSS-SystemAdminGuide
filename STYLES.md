# Content Style Guide

Practical reference for writers contributing to the NBS System Administrator Guide. Open this file to answer "how do I format this?"

This guide documents conventions that are actually in use in the repo. It does not enforce every possible Markdown rule — just the ones that matter for consistency and accessibility in this site.

---

## 1. Heading Hierarchy

| Level | Tag | When to use |
|-------|-----|-------------|
| H1 | `# Heading` | **Write this as the first line of body content.** JTD does not inject the title automatically, so omitting it leaves the page with no visible page heading. Keep one H1 per page. The H1 can be longer and more descriptive than the front matter `title:` used in navigation. |
| H2 | `## Heading` | Major sections. These appear in the in-page table of contents. |
| H3 | `### Heading` | Subsections within an H2. These do **not** appear in the TOC (configured in `_config.yml` — `toc.max_level: 2`). |
| H4+ | `#### Heading` | Use sparingly. If you need H4, the section is probably too deep — consider restructuring. |

**Example front matter + first heading:**

```markdown
---
title: Kubernetes setup
layout: page
nav_order: 2
parent: Initial Kubernetes Deployment
---

# Kubernetes setup for NBS 7

This is an overview paragraph.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Before you begin
```

Every page needs an H1. JTD shows `title:` in navigation and breadcrumbs, but only your H1 creates the visible page heading in content. Keep `title:` concise for navigation, and use the H1 to provide full page context. The first section heading after the H1 should be `##`.

### 1.0.1 Navigation Titles (Sidebar)

Use the front matter `title:` as the navigation label, and keep it short enough to scan easily in the sidebar.

- Remove redundancy: if the section context already provides detail, shorten the child title.
- Use actionable language for task pages: use a verb phrase such as "Transfer data".
- Handle acronyms carefully: use common acronyms (for example, API) and avoid uncommon abbreviations.
- Prioritize clarity: prefer plain language over internal shorthand.

Examples:

- Full page H1: Managing OAuth 2.0 credentials
  Nav title (`title:`): OAuth credentials
- Full page H1: Retrieving data sets using API
  Nav title (`title:`): Data sets
- Full page H1: Getting started with the Core SDK
  Nav title (`title:`): Core SDK

## 1.1 Page Layout Order

Use this page layout sequence for content pages:

1. H1 as the first heading in the body (descriptive page heading)
1. Brief intro text directly under the H1 (one sentence for reference pages; one to three sentences for concept, task, and landing pages)
1. `On this page` TOC block
1. First H2 section immediately after the TOC block

**Required pattern:**

```markdown
# Descriptive page title

Brief intro text.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## First section heading
```

---

## 2. Callouts (Admonitions)

Callouts are styled block quotes. JTD applies the callout style based on a CSS class applied to the paragraph after the block quote.

**Syntax:**

```markdown
> Your callout text here. Can span multiple sentences.
{: .note }
```

### Available types

#### `note` — Blue

Use for helpful context, clarifications, or background information that readers may find useful but can skip without consequences.

```markdown
> NBS 7 requires Kubernetes 1.24 or later. Earlier versions are not supported.
{: .note }
```

#### `important` — Yellow

Use for requirements, prerequisites, or steps that must be completed before proceeding. The reader cannot skip this.

```markdown
> You must complete the Keycloak installation before enabling Keycloak authentication.
{: .important }
```

#### `warning` — Red

Use when an action is irreversible, could cause data loss, or could break a running system.

```markdown
> Running `terraform destroy` will permanently delete all infrastructure in the target environment.
{: .warning }
```

#### `new` — Green

Use to flag content that documents a recently added feature or a significant change in the current release.

```markdown
> The Liquibase schema migration workflow was added in NBS 7.9.0 and replaces the manual SQL process.
{: .new }
```

#### `highlight` — Purple (no label)

Use for inline callouts where you want visual emphasis without a title label. Useful for tips or one-liners that don't need a formal label.

```markdown
> Use `--dry-run` to preview Terraform changes before applying them.
{: .highlight }
```

### Custom titles (`-title` variants)

Each type except `highlight` supports a `-title` variant that lets you replace the default label ("Note", "Important", etc.) with your own title. Use this when the default label is too generic for the context.

**Syntax:** append `-title` to the class name. The first line of the blockquote becomes the title; leave a blank line before the body.

```markdown
> Best for
>
> Jurisdictions with smaller IT teams or limited cloud experience.
{: .note-title }
```

The `-title` variants follow the same usage rules as their base types — the variant only changes the label, not when to use the callout.

`highlight` has no default label and does not have a `-title` variant.

### When to use which type

| Type | Use when... |
|------|-------------|
| `note` | Readers benefit from knowing, but skipping won't break anything |
| `important` | Must-read before continuing — a required step or dependency |
| `warning` | Irreversible action, data loss risk, or system breakage risk |
| `new` | Documenting a feature added in the current or recent release |
| `highlight` | Short tip or emphasis without a formal label |

---

## 3. Code Formatting

### Inline code

Use backticks for:

- File names and paths: `_config.yml`, `/etc/nginx/nginx.conf`
- Command names: `kubectl`, `helm`, `terraform`
- Parameter names and flags: `--namespace`, `max_level`
- Values: `true`, `quiet`, `main`
- Environment variable names: `KUBECONFIG`, `DB_PASSWORD`

```markdown
Run `kubectl get pods` to verify the deployment.
Set `nav_exclude: true` to hide a page from the left nav.
```

### Fenced code blocks

Always use fenced code blocks (triple backticks) for multi-line content. **Always include a language tag** — this enables syntax highlighting and signals to readers what they're reading.

````markdown
```bash
kubectl apply -f manifests/
helm upgrade --install nbs-gateway ./charts/nbs-gateway \
  --namespace nbs \
  --values values.prod.yaml
```
````

````markdown
```yaml
collections:
  previous_versions:
    output: true
```
````

````markdown
```sql
SELECT * FROM nbs_case WHERE jurisdiction_code = 'GA';
```
````

**Common language tags used in this guide:**

| Content type | Tag |
|--------------|-----|
| Shell commands | `bash` |
| YAML config | `yaml` |
| Terraform HCL | `hcl` |
| JSON | `json` |
| SQL | `sql` |
| Plain output / logs | `text` |

---

## 4. Links

Use descriptive link text. The link text should tell the reader where they are going or what the target document covers.

### 4.1 Internal cross-links (within this doc set)

For links to other pages in this guide, use the built-site HTML path convention:

1. Find the page location under `_site/docs/...`.
1. Remove `/_site` from the front of the path.
1. Use the resulting `/docs/.../*.html` path in your Markdown link.

Do not link to `.md` files for internal navigation links.

**Example conversion:**

- Source page link target in repo: `../deploy-nbs7/set-up-cloud-infrastructure.md`
- Built page path: `_site/docs/deploy-nbs7/set-up-cloud-infrastructure.html`
- Link to use in docs page: `../../docs/deploy-nbs7/set-up-cloud-infrastructure.html`

**Anchor links:**

Use standard heading anchors on the HTML target when linking to a section:

```markdown
See [NBS 7 core components](../../docs/before-you-deploy/component-reference/nbs-core-components.html#nbs-modernization-api).
```

External links do not need special treatment in JTD — they render as standard links and open in the same tab by default.

### 4.2 Redirects

Use redirects when a page has moved and you need old URLs to continue working.

**Implement redirects:**

1. Add `redirect_from:` on the destination page, meaning the page that should receive traffic from the old URL.
1. List only old built-site URLs under `redirect_from:`.
1. Indent each redirect URL with 2 spaces.
1. Include both forms when relevant: the `.html` path and the trailing-slash path.

**Front matter example:**

```yaml
---
title: Prerequisites for AWS
layout: page
parent: Deploy on AWS
nav_order: 1
redirect_from:
  - /docs/2_prerequisites/prereq.html
  - /docs/2_prerequisites/prereq/
description: Prepare your AWS cloud environment before you provision AWS for NBS 7.
---
```

**Test redirects:**

After changing `redirect_from` or `_config.yml`:

1. Use `bundle exec jekyll serve --livereload` (or restart your Docker preview process) to restart local preview.
1. Then `bundle exec jekyll build` to verify redirect artifacts are generated.
1. Confirm that Jekyll generated a redirect file for the old URL under `_site/docs`.
1. Test the old URL in browser.

---

## 5. Images

**Always include alt text.** Alt text should describe what the image shows, not what it is called. Screen readers and users with images disabled depend on it.

```markdown
![Terraform plan output showing 3 resources to add and 0 to destroy](images/terraform-plan-output.png)
```

**File naming:**

- Lowercase only
- Words separated by hyphens (no underscores, no spaces)
- Descriptive — the name should hint at the content
- Include the version or context if the image is version-specific

| Good | Avoid |
|------|-------|
| `terraform-plan-output.png` | `screenshot1.png` |
| `keycloak-realm-settings.png` | `Keycloak_Settings.PNG` |
| `kubernetes-pod-status-healthy.png` | `k8spodstatushealthy.png` |

**Storage:** Place images in an `images/` subfolder within the relevant `docs/` section. For example, images for Keycloak docs go in `docs/5_keycloak/images/`.

```text
docs/
  5_keycloak/
    images/
      keycloak-realm-settings.png
    1_keycloak_installation.md
```

---

## 6. Tables

Use tables for **reference data and comparisons** where the reader will scan across rows to find a specific value.

```markdown
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `namespace` | string | Yes | Kubernetes namespace for the deployment |
| `replicas` | integer | No | Number of pod replicas (default: 1) |
| `image.tag` | string | Yes | Docker image tag to deploy |
```

**Do not use tables for:**

- Sequential steps — use a numbered list instead
- Prose that reads naturally as paragraphs or bullets
- Content with cells that require lengthy explanation (the table becomes unreadable)

**Column alignment:** Use the default (left-aligned). Only use `:---:` center alignment for columns that contain short codes or symbols where centering aids scanning.

---

## 7. Numbered Lists

**Use `1.` for every item.** Markdown renderers increment the numbers automatically, so writing `1.` throughout makes it easy to insert or reorder steps without renumbering.

```markdown
1. First step.
1. Second step.
1. Third step.
```

---

### Numbered lists with code blocks

Kramdown ends a numbered list whenever it encounters an unindented block — a code block, callout, image, or paragraph sitting at the left margin. The list then restarts at 1.

**To keep a numbered list unbroken**, indent all continuation content 3 spaces so kramdown treats it as part of the current list item:

````markdown
1. First step — intro text.

   ```bash
   some command
   ```

1. Second step — the list continues correctly.
````

This applies to everything that belongs inside a list item: code blocks, callouts, images, and paragraphs.

**Do not do this** — the unindented code block ends the list, and step 2 restarts at 1:

````markdown
1. First step.

```bash
some command
```

1. Second step.
````

**Callouts and notes inside list items** follow the same rule — indent 3 spaces:

```markdown
1. First step.

   > Run this only after verifying your credentials.
   {: .warning }

1. Second step.
```

**Paragraphs between steps** also break the list if unindented. If a note applies to the next step, put it inside that step as a callout rather than between steps as a bare paragraph.
