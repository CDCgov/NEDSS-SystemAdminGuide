# Content Style Guide

Practical reference for contributors to the NBS System Administrator Guide. Open this file to answer "how do I format this?" or "what front matter does this page need?"

This guide is the authoritative reference for formatting, front matter, and accessibility requirements. It covers conventions that are actually in use in the repo and documents Section 508 / WCAG 2.1 AA standards that apply to this federally published resource.

---

## Front Matter

### Quick-reference table

| Field | docs/ pages | _guide_preview/ pages | What it does |
|-------|------------|----------------------|--------------|
| `title` | **Required** | **Required** | Sets the page title. JTD renders this as the page's H1 heading and uses it as the left-nav label and browser tab title. |
| `layout` | **Required** — always `page` | **Required** — always `page` | Specifies the JTD page template. Use `page` for all content pages. `home` is used only on the site root `index.md` — do not use it elsewhere. |
| `nav_order` | **Required** | **Omit** | Controls display order among sibling pages in the nav. Must be an integer. See [How nav_order works](#how-nav_order-works). |
| `has_children` | **Required** when this page has child pages | **Omit** | Tells JTD to render an expand arrow in the nav. Without it, child pages exist but the parent page shows no arrow and may not nest visibly. |
| `has_toc` | **Set `false`** on parent pages that provide a manual "In this section" list | **Omit** | JTD auto-renders a table of contents of child pages at the bottom of every `has_children` page. Set `has_toc: false` to suppress it when the page provides its own richer child list. See [Parent landing pages](#parent-landing-pages). |
| `parent` | **Required** for child pages | **Omit** | Sets the parent page. The value must exactly match the `title:` of the intended parent. Case-sensitive. |
| `grand_parent` | **Required** for grandchild pages | **Omit** | Sets the grandparent page. Required when a page's `parent` is itself a child page. Must exactly match the grandparent's `title:`. |
| `description` | **Optional, recommended** | **Optional** | 1–2 sentences describing the page's purpose. JTD uses this for search result snippets and the HTML `<meta name="description">` tag. See [Writing descriptions](#writing-descriptions). |
| `redirect_from` | Optional — plugin feature | **Omit** | From the `jekyll-redirect-from` gem. Redirects one or more old URLs to this page. Use only when a page has been moved or renamed to preserve existing links. See [Redirects](#redirects). |
| `nav_enabled` | **Omit** — remove on sight | **Omit** — remove on sight | **Non-standard. Has no effect.** Not a JTD front matter key. See [Note on nav_enabled](#note-on-nav_enabled). |

### Annotated examples

Use placeholder values as shown. Replace all-caps placeholders before committing.

#### Top-level section page (has children)

```yaml
---
title: TITLE          # Required. Becomes the H1 heading and left-nav label.
                      # Child pages must use this exact string as their parent: value.
layout: page          # Required. Always "page" — do not change.
nav_order: NAV_ORDER  # Required. Integer. Controls position among top-level nav items.
has_children: true    # Required. Enables the expand arrow; without it children won't nest.
has_toc: false        # Set false when the page provides a manual "In this section" list.
description: DESCRIPTION  # Optional. 1–2 sentences, under 160 characters. Describe purpose, not the title.
---
```

#### Child page (has a parent)

```yaml
---
title: TITLE              # Required.
layout: page              # Required.
parent: PARENT_TITLE      # Required. Must exactly match the parent page's title: value.
nav_order: NAV_ORDER      # Required. Controls position among siblings under the same parent.
description: DESCRIPTION  # Optional.
---
```

#### Grandchild page (has a parent and a grandparent)

```yaml
---
title: TITLE                        # Required.
layout: page                        # Required.
parent: PARENT_TITLE                # Required. Must exactly match the direct parent's title:.
grand_parent: GRANDPARENT_TITLE     # Required for grandchild pages. Must exactly match the grandparent's title:.
nav_order: NAV_ORDER                # Required. Controls position among siblings under the same parent.
description: DESCRIPTION            # Optional.
---
```

#### Guide preview page (_guide_preview/ directory)

```yaml
---
title: TITLE              # Required.
layout: page              # Required.
description: DESCRIPTION  # Optional.
---
```

Nav keys (`nav_order`, `parent`, `has_children`, `grand_parent`) are **intentionally omitted** from guide preview pages. The `just_the_docs.collections` setting in `_config.yml` already excludes these pages from the left nav and search index. Nav keys on these pages have no effect and create misleading front matter.

### How nav_order works

JTD sorts sibling pages in ascending order by `nav_order`. Siblings are pages that share the same `parent:` value, or all top-level pages (those with no `parent:`).

- Pages without a `nav_order` value fall to the bottom of their sibling group and sort alphabetically among themselves.
- `nav_order` values only need to be unique within a sibling group. The same value can appear independently in different sections.
- Values do not need to be sequential. Leaving gaps — using 10, 20, 30 rather than 1, 2, 3 — makes it easy to insert a page later without renumbering every sibling.
- The value must be an integer, not a string.

**Example:** Three top-level pages with `nav_order: 10`, `nav_order: 20`, and no `nav_order` will appear in the nav as: page-at-10, page-at-20, then the unnumbered page at the bottom.

### Writing descriptions

JTD uses `description:` in two places:

1. **Search result snippet** — shown below the page title in the site's built-in search overlay
2. **HTML meta description** — read by search engines and accessibility tools

**Guidelines:**

- Write 1–2 sentences, under 160 characters total
- Describe what the reader will find or be able to do — the page's *purpose*
- Do not restate the title word-for-word; add information the title doesn't already convey
- Write in third person (describing the page), not second person ("you will learn...")

| | Example |
|-|---------|
| **Weak** | "This page covers prerequisites." — restates the title, tells the reader nothing new |
| **Strong** | "Lists the AWS environment, tooling, and access requirements you must satisfy before beginning the NBS 7 installation." — specific, describes what the reader gets |

### Note on nav_enabled

`nav_enabled: true` appears in the front matter of most current pages in this repo. **It is not a JTD front matter key and has no functional effect.** JTD does not recognize this key. The correct key to hide a page from navigation is `nav_exclude: true`.

The field is legacy noise carried over before front matter standards were established for this project. It does not need an immediate cleanup pass — remove it opportunistically when editing a page for other reasons. Do not add it to new pages.

---

## Page Layout

Use this structure for content pages:

1. H1 (`#`) that exactly matches `title:` (or is longer and more descriptive)
2. Brief intro text directly under the H1 (one sentence for reference pages; one to three sentences for concept, task, and landing pages)
3. `## On this page` TOC block
4. First H2 section immediately after the TOC

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

**Full example including front matter:**

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

Every page needs an H1. JTD shows `title:` in navigation and breadcrumbs, but only your H1 creates the visible page heading in content. Keep `title:` concise for navigation, and use the H1 to provide full page context.

### Parent landing pages

Pages with `has_children: true` that serve as section landing pages follow an additional pattern:

1. Set `has_toc: false` in front matter. JTD otherwise auto-renders a bare table of contents of child pages at the bottom of the page, which duplicates the manual list below.
1. Provide a manual **In this section** list: each child page as a bold link followed by a one-line description of what the reader does or finds there.
1. Match the list type to the relationship between the children:
   - **Ordered list** (`1.`) when the children are sequential. Use a lead-in that states the sequence, ending with a colon: "Complete the pages in this section in order:"
   - **Bulleted list** when the children are alternatives or independent topics.

Ordered-list semantics announce sequence to assistive technology, so the list type is an accessibility signal, not just a visual one.

**Example (sequential children):**

```markdown
## In this section

Complete the pages in this section in order:

1. **[Cloud prerequisites](provision-cloud-infrastructure/cloud-prerequisites.html)**: Verify your AWS or Azure account, hardware, software, network, and security requirements before provisioning begins.
1. **[Provision cloud environment](provision-cloud-infrastructure/provision-cloud-environment.html)**: Use Terraform to create the virtual network, Kubernetes cluster, and supporting services for NBS 7.
```

### Navigation titles (sidebar)

Use the front matter `title:` as the navigation label, and keep it short enough to scan easily in the sidebar.

- Remove redundancy: if the section context already provides detail, shorten the child title.
- Use actionable language for task pages: use a verb phrase such as "Transfer data".
- Handle acronyms carefully: use common acronyms (for example, API) and avoid uncommon abbreviations.
- Prioritize clarity: prefer plain language over internal shorthand.

Examples:

- Full page H1: Managing OAuth 2.0 credentials → Nav title (`title:`): OAuth credentials
- Full page H1: Retrieving data sets using API → Nav title (`title:`): Data sets
- Full page H1: Getting started with the Core SDK → Nav title (`title:`): Core SDK

---

## Heading Hierarchy

| Level | Tag | When to use |
|-------|-----|-------------|
| H1 | `# Heading` | **Write this as the first line of body content.** JTD does not inject the title automatically, so omitting it leaves the page with no visible page heading. Keep one H1 per page. |
| H2 | `## Heading` | Major sections. These appear in the in-page table of contents. |
| H3 | `### Heading` | Subsections within an H2. These do **not** appear in the TOC (configured in `_config.yml` — `toc.max_level: 2`). |
| H4+ | `#### Heading` | Use sparingly. If you need H4, the section is probably too deep — consider restructuring. |

**Do not skip heading levels.** Skipping (for example, jumping from H2 to H4) fails WCAG 2.1 SC 1.3.1 (Info and Relationships) and breaks assistive technology navigation. Screen reader users navigate by heading list — they cannot rely on surrounding visual context.

**Do not use bold text as a structural substitute for a heading.** Bold text is not exposed to screen readers as a landmark.

**Heading text must be unique and descriptive within the page.** Avoid generic headings like "Details" or "More information" — screen reader users navigate by heading list and cannot rely on surrounding context.

---

## Callouts (Admonitions)

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

**Accessibility note:** The `highlight` callout has no `title:` label configured in `_config.yml`. In JTD's callout implementation, the title field provides a text label (e.g., "Note", "Warning") that supplements the color indicator. Without it, color becomes the sole differentiator — which fails WCAG 2.1 SC 1.4.1 (Use of Color) if the callout type itself conveys meaning. Keep `highlight` usage rare, and ensure the surrounding copy communicates the intent without relying on the purple color alone.

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
| `highlight` | Short tip or emphasis without a formal label; use sparingly |

### Callout color contrast

JTD callouts use a `-000` background tint and `-300` foreground accent. The ratios below apply to the accent-on-tint combination (left border stripe and any title text). Body text inside callouts inherits the standard dark body color at 17.40:1 — these ratios do not affect paragraph readability.

| Callout type | Foreground (`-300`) | Background (`-000`) | Ratio | AA normal | Notes |
|---|---|---|---|---|---|
| Note (blue) | #2474B6 | #E6EFF7 | 4.25 : 1 | ⚠️ Borderline | 0.25 below 4.5:1 AA threshold; body text unaffected. |
| Important (yellow) | #ECB046 | #FBEDD6 | 1.67 : 1 | Fail | Accent color only; body text passes at 17.40:1. |
| Warning (red) | #CB3E6E | #F8E4EB | 3.88 : 1 | Fail | Passes 3.0:1 large-text threshold; body text passes. |
| New (green) | #9ACC54 | #EAF5DC | 1.67 : 1 | Fail | Accent color only; body text passes at 17.40:1. |
| Highlight (purple) | #A1518B | #F1E9EE | 4.14 : 1 | Fail | 0.36 below 4.5:1; body text passes. |

Before treating any callout as non-compliant, verify in a built-site browser using DevTools color picker to confirm which elements actually render in the accent color. These are known theme-level constraints — see [Known accessibility limitations](#known-accessibility-limitations).

---

## Code Formatting

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

## Terminology and Naming

### Acronym first use

Spell out an acronym at its first use on each page, with the acronym in parentheses: "Data Ingestion API (DI API)". Use the bare acronym on subsequent mentions on that page.

**First use means first RENDERED use.** Front matter fields (`description:`, `parent:`) do not render in the page body, so an expansion that appears only in front matter does not count. A reader must encounter the spelled-out form in visible prose before the bare acronym appears.

Every acronym used in the guide should also have an entry in `_data/glossary.yml`.

### Service names are namespace-specific

The same NBS service can be spelled differently in different technical namespaces, and each spelling is correct for its namespace. **Never normalize a service-name spelling across namespaces.** Verify against the namespace being referenced before "correcting" any service name.

Example — the data ingestion service:

| Namespace | Canonical string |
|-----------|-----------------|
| NEDSS-Helm chart directory | `dataingestion-service` |
| quay.io container image path | `data-ingestion-service` |
| NEDSS-DataIngestion source repo module | `data-ingestion-service` |

A values file that references the container image must use the image path spelling; a `helm install` command must use the chart spelling. Changing either to match the other breaks the reference.

### Data ingestion naming standard

Three forms are sanctioned; use the one that matches what the sentence names:

1. **"Data Ingestion API (DI API)"** at first rendered use on a page when naming the API; **"DI API"** on subsequent mentions on that page.
2. **"data ingestion service"** (lowercase) when referring descriptively to the service, capitalized only as normal sentence rules require.
3. **`dataingestion-service`** (code format) only inside commands, code samples, and values-file references, where it is a technical string rather than a prose name.

There is no Title Case "Data Ingestion Service" form.

---

## Links

**Use descriptive link text.** Link text must tell the reader where they are going or what the target document covers. Screen reader users navigate by link text alone — "click here" and "here" provide no context and fail WCAG 2.1 SC 2.4.4 (Link Purpose).

```markdown
<!-- BAD -->
See [here](../path.md) for installation steps.

<!-- GOOD -->
See [Keycloak installation](../path.md) for installation steps.
```

### Internal cross-links (within this doc set)

For links to other pages in this guide, use a relative HTML path from the current file to the target page.

**Internal links must be relative — never root-absolute (no leading `/`).** A root-absolute path such as `/docs/page.html` resolves against the domain root and bypasses the GitHub Pages project baseurl (`/NEDSS-SystemAdminGuide`). The result works under a default local serve (which serves at the domain root) but returns 404 on the published site.

To catch this class of bug locally, run `bundle exec jekyll serve` without a baseurl override and browse the site under `http://localhost:4000/NEDSS-SystemAdminGuide/`. With the baseurl respected, root-absolute links break locally the same way they break in production.

Do not link to `.md` files for internal navigation links.

**Example conversion:**

- Source page link target in repo: `../deploy-nbs7/set-up-cloud-infrastructure.md`
- Link to use from a page in `docs/before-you-deploy/`: `../deploy-nbs7/set-up-cloud-infrastructure.html`

**How to build the link:**

1. Start from the current page's directory.
1. Navigate relatively to the target page.
1. Use the target page's `.html` path in the Markdown link.

Avoid `../../docs/...` or similar "up-and-back" paths in content. Those are harder to maintain and are not needed for internal navigation.

**Anchor links:**

Use standard heading anchors on the HTML target when linking to a section:

```markdown
See [NBS 7 core components](component-reference/nbs-core-components.html#nbs-modernization-api).
```

Anchor-only links (`#section-name`) are valid and excluded from the automated link checker by default. Verify that the target heading exists in the destination file.

External links do not need special treatment in JTD — they render as standard links and open in the same tab by default.

### Redirects

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

### Reference-style links for templated GitHub URLs

GitHub URLs that contain Liquid template values (e.g., `{{ site.version_latest_tag }}`) must use **reference-style links** rather than inline links. Inline links with Liquid values trigger markdownlint rule MD034 (bare URL in text), which is a blocking CI check.

**Use inline links for** static URLs and internal cross-links — those are fine and easier to read when the URL is short.

**Use reference-style links for** any GitHub URL that contains `{{ site.version_latest_tag }}` or another Liquid variable.

**Reference-style syntax:**

```markdown
Locate the chart in the [NEDSS-Helm repository][nedss-helm-traefik-chart].

[nedss-helm-traefik-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/traefik>
```

**Naming convention for reference labels:**

Use lowercase hyphenated labels that identify the repo and target clearly. Keep them stable — a label used in the page body must match its definition exactly.

| Pattern | Example label |
|---------|--------------|
| NEDSS-Helm chart | `nedss-helm-<chart-name>-chart` |
| NEDSS-Helm specific file | `nedss-helm-<chart-name>-<file>` |
| NEDSS-Infrastructure release page | `nedss-infra-release-page` |
| NEDSS-Infrastructure specific file | `nedss-infra-<path-description>` |
| NEDSS-NNDSS release page | `nedss-nndss-release-page` |
| NEDSS-NNDSS specific file | `nedss-nndss-<description>` |

**Placement rule:** Put all link definitions at the very end of the file, after all content. Never place a definition block in the middle of a page — it interrupts prose flow and makes definitions hard to find.

**Full pattern for a page with templated links:**

```markdown
## Deploy the service

1. Locate the Helm chart in the [NEDSS-Helm repository][nedss-helm-myservice-chart].
1. Configure `values.yaml` as described below.

[nedss-helm-myservice-chart]: <https://github.com/CDCgov/NEDSS-Helm/tree/{{ site.version_latest_tag }}/charts/myservice>
```

**When editing existing pages:**

1. If you add a templated GitHub link, write it in reference style and add its definition at the bottom.
2. If a file already has reference definitions at the bottom, add yours to the same block.
3. Run `npm run lint` on the touched file before pushing. If `npm run link-check:github:changed` reports an error on a templated URL, check that the link definition uses angle-bracket syntax (`<https://...>`).

---

## Images

**Always include alt text.** Every image must have descriptive alt text. Empty `alt=""` is only appropriate for purely decorative images with no informational content.

**Standard:** Describe what the image shows AND what the reader should take away from it. Do not use the file name as alt text — it is not a description.

```markdown
<!-- BAD — file name is not a description -->
![screenshot](images/output.png)

<!-- GOOD — describes content and meaning -->
![Terminal output showing all three pods in Running status
 with READY 1/1 after running kubectl get pods -n nbs
](images/pod-status.png)
```

**Images must not be the sole carrier of critical information.** Also provide the information as text. Screen readers and users with images disabled depend on it. This is a Section 508 requirement.

### File naming

Use lowercase-hyphenated filenames: `pod-status.png`, not `PodStatus.PNG` or `pod_status.png`.

| Good | Avoid |
|------|-------|
| `terraform-plan-output.png` | `screenshot1.png` |
| `keycloak-realm-settings.png` | `Keycloak_Settings.PNG` |
| `kubernetes-pod-status-healthy.png` | `k8spodstatushealthy.png` |

### Storage

Place images in an `images/` subfolder within the relevant `docs/` section.

```text
docs/
  5_keycloak/
    images/
      keycloak-realm-settings.png
    1_keycloak_installation.md
```

### Reviewer checklist

- Every `![` in the file has non-empty alt text
- Alt text describes the image content and what the reader should conclude
- Images are not the sole carrier of critical information

---

## Tables

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
- Layout — tables are for data, not positioning content

**Accessibility requirements:**

- Every table must have a header row using Markdown `|---|` separator syntax.
- Column headers must describe the data in that column.
- Do not use tables to arrange non-tabular content.

**Column alignment:** Use the default (left-aligned). Only use `:---:` center alignment for columns that contain short codes or symbols where centering aids scanning.

---

## Numbered Lists

**Use `1.` for every item.** Markdown renderers increment the numbers automatically, so writing `1.` throughout makes it easy to insert or reorder steps without renumbering.

```markdown
1. First step.
1. Second step.
1. Third step.
```

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

---

## Accessibility Compliance Record

The NEDSS System Administration Guide is a federally published resource and must meet **Section 508** and **WCAG 2.1 Level AA** requirements. The site is built with Jekyll and the Just the Docs (JTD) theme; most structural accessibility (landmark regions, skip-navigation, focus management) is provided by the theme. Authoring-time obligations — alt text, heading hierarchy, link text, color contrast, and table markup — are documented throughout this guide.

WCAG 2.1 AA contrast thresholds:

| Text type | Required ratio |
|-----------|----------------|
| Normal text (< 18 pt regular or < 14 pt bold) | 4.5 : 1 |
| Large text (≥ 18 pt regular or ≥ 14 pt bold) | 3.0 : 1 |
| UI components and graphical objects | 3.0 : 1 |

### Brand and body color contrast

The following pairings are used across the site and have been verified against WCAG 2.1 AA.

| Foreground | Background | Ratio | AA normal | AA large |
|------------|-----------|-------|-----------|----------|
| `$cdc-blue` #005DAA | White #FFFFFF | 6.68 : 1 | Pass | Pass |
| `$body-heading-color` #1A1A1A | White #FFFFFF | 17.40 : 1 | Pass | Pass |
| `$cdc-blue` #005DAA | JTD sidebar #F5F6FA | 6.20 : 1 | Pass | Pass |

### Known accessibility limitations

The following issues are documented and tracked. They represent theme or infrastructure constraints, not authoring errors.

| Area | Issue | Status |
|------|-------|--------|
| Callout accent colors | Yellow-on-yellow-tint (1.67:1) and green-on-green-tint (1.67:1) fail WCAG AA for accent elements. Body text contrast is unaffected. | Known; body text passes. Accent-only failure pending upstream theme resolution. |
| Red callout | Red-300 on red-000 (3.88:1) fails AA normal text threshold for accent elements. | Known; body text passes. |
| Blue callout | Blue-300 on blue-000 (4.25:1) is borderline — 0.25 below the 4.5:1 AA normal threshold for accent elements. | Known; body text passes. Verify in built site. |
| Highlight callout | No `title:` text label; color can become the sole type indicator if used incorrectly. | Unused in `docs/`; use sparingly and pair with clear wording. |

### Tooltip usage syntax

Use the `term-tooltip` include for glossary-style terms that need an inline definition.

1. Add or update the term definition in `_data/glossary.yml`.
1. Reference the term inline using the include.
1. Use a page-unique `id` value for each tooltip instance.
1. If a page already defines the term in plain language on first mention, keep that first mention as-is and use the include on later mentions.
1. If the first mention is the only place the term appears or the usage is ambiguous, leave a note for review instead of forcing a tooltip.

**Data-driven definition (preferred):**

```liquid
{% include term-tooltip.html key="kubernetes" term="Kubernetes" id="kubernetes-runtime" %}
```

- `key`: lookup key in `_data/glossary.yml`
- `term`: visible text in the paragraph
- `id`: unique suffix used to build the tooltip element ID

**Inline definition (one-off):**

```liquid
{% include term-tooltip.html term="Helm" id="helm-runtime" definition="A package manager for Kubernetes." %}
```

**In-paragraph example:**

```markdown
NBS 7 runs on {% include term-tooltip.html key="kubernetes" term="Kubernetes" id="kubernetes-home" %} and relies on Terraform.
```

When a page introduces a term plainly first, follow-on uses can use the include:

```markdown
The content assumes familiarity with your cloud platform, {% include term-tooltip.html key="kubernetes" term="Kubernetes" id="kubernetes-audience" %}, Terraform, Helm, and related administration tasks.
```

### Tooltip accessibility verification checklist

When adding or modifying tooltip terms, verify all of the following before merge:

1. **Keyboard open/close:** `Tab` to the term opens the tooltip; `Escape` closes it.
1. **Hover/focus persistence:** Tooltip remains visible while hovered or while trigger has focus.
1. **Dismiss without moving pointer:** `Escape` closes any open tooltip even when opened by mouse hover.
1. **Screen reader announcement:** Trigger has `aria-describedby` that points to a unique tooltip `id`, and the tooltip uses `role="tooltip"`.
1. **State sync:** Tooltip visibility and ARIA state remain synchronized (`hidden` with `aria-hidden`).
1. **Touch behavior:** Tapping the term toggles the tooltip and tapping outside dismisses it.
