# Content Style Guide

Practical reference for writers contributing to the NBS System Administrator Guide. Open this file to answer "how do I format this?"

This guide documents conventions that are actually in use in the repo. It does not enforce every possible Markdown rule — just the ones that matter for consistency and accessibility in this site.

---

## 1. Heading Hierarchy

| Level | Tag | When to use |
|-------|-----|-------------|
| H1 | `# Heading` | **Write this as the first line of body content, matching the front matter `title:`.** JTD does not inject the title automatically — omitting it leaves the page with no H1. Never write more than one H1. |
| H2 | `## Heading` | Major sections. These appear in the in-page table of contents. |
| H3 | `### Heading` | Subsections within an H2. These do **not** appear in the TOC (configured in `_config.yml` — `toc.max_level: 2`). |
| H4+ | `#### Heading` | Use sparingly. If you need H4, the section is probably too deep — consider restructuring. |

**Example front matter + first heading:**

```markdown
---
title: Kubernetes Bootstrapping
layout: page
nav_order: 2
parent: Initial Kubernetes Deployment
---

# Kubernetes Bootstrapping

This is an overview paragraph.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Before you begin
```

The `# Heading` matches the front matter `title:` exactly. Every page needs it — JTD shows the title in the nav and breadcrumbs, but only your H1 creates the visible page heading. The first section heading after the H1 should be `##`.

## 1.1 Page Layout Order

Use this page layout sequence for content pages:

1. H1 that matches the front matter `title:` exactly
2. Brief intro text directly under the H1 (one sentence for reference pages; one to three sentences for concept, task, and landing pages)
3. `On this page` TOC block
4. First H2 section immediately after the TOC block

**Required pattern:**

```markdown
# Page title

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

#### `note` — Yellow

Use for helpful context, clarifications, or background information that readers may find useful but can skip without consequences.

```markdown
> NBS 7 requires Kubernetes 1.24 or later. Earlier versions are not supported.
{: .note }
```

#### `important` — Blue

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

#### `highlight` — Yellow (no label)

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
2. Remove `/_site` from the front of the path.
3. Use the resulting `/docs/.../*.html` path in your Markdown link.

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

**Do this:**

```markdown
See the [Keycloak installation guide](../5_keycloak/1_keycloak_installation.html) for prerequisites.
Refer to the [Just the Docs configuration reference](https://just-the-docs.com/docs/configuration/).
```

**Not this:**

```markdown
Click [here](../5_keycloak/1_keycloak_installation.html) for more information.
See [this page](https://just-the-docs.com/docs/configuration/) for details.
```

External links do not need special treatment in JTD — they render as standard links and open in the same tab by default.

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
| `kubernetes-pod-status-healthy.png` | `image.png` |

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

2. Second step.
```

**Paragraphs between steps** also break the list if unindented. If a note applies to the next step, put it inside that step as a callout rather than between steps as a bare paragraph.
