# Content Style Guide

Practical reference for writers contributing to the NBS System Administrator Guide. Open this file to answer "how do I format this?"

This guide documents conventions that are actually in use in the repo. It does not enforce every possible Markdown rule — just the ones that matter for consistency and accessibility in this site.

---

## 1. Heading Hierarchy

| Level | Tag | When to use |
|-------|-----|-------------|
| H1 | `# Heading` | **Never write this in body content.** JTD renders the page `title:` from front matter as the H1 automatically. Writing a second `# Heading` creates two H1s on the page. |
| H2 | `## Heading` | Major sections. These appear in the in-page table of contents. |
| H3 | `### Heading` | Subsections within an H2. These do **not** appear in the TOC (configured in `_config.yml` — `toc.max_level: 2`). |
| H4+ | `#### Heading` | Use sparingly. If you need H4, the section is probably too deep — consider restructuring. |

**Example front matter + first heading:**

```yaml
---
title: Kubernetes Bootstrapping
layout: page
nav_order: 2
parent: Initial Kubernetes Deployment
---
```

The page renders "Kubernetes Bootstrapping" as the H1 automatically. The first heading you write in the body should be `##`.

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

**Do this:**

```markdown
See the [Keycloak installation guide](../5_keycloak/1_keycloak_installation.md) for prerequisites.
Refer to the [Just the Docs configuration reference](https://just-the-docs.com/docs/configuration/).
```

**Not this:**

```markdown
Click [here](../5_keycloak/1_keycloak_installation.md) for more information.
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

```
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
