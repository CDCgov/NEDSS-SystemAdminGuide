# Front Matter Reference

Practical reference for contributors adding or editing pages in this repo. Answers "what front matter does this page need?"

Two page contexts have different standards: **standard content pages** (docs/) and **guide preview pages** (_guide_preview/). Both are explained below.

---

## Quick-reference table

| Field | docs/ pages | _guide_preview/ pages | What it does |
|-------|------------|----------------------|--------------|
| `title` | **Required** | **Required** | Sets the page title. JTD renders this as the page's H1 heading and uses it as the left-nav label and browser tab title. |
| `layout` | **Required** — always `page` | **Required** — always `page` | Specifies the JTD page template. Use `page` for all content pages. `home` is used only on the site root `index.md` — do not use it elsewhere. |
| `nav_order` | **Required** | **Omit** | Controls display order among sibling pages in the nav. Must be an integer. See [How nav_order works](#how-nav_order-works). |
| `has_children` | **Required** when this page has child pages | **Omit** | Tells JTD to render an expand arrow in the nav. Without it, child pages exist but the parent page shows no arrow and may not nest visibly. |
| `parent` | **Required** for child pages | **Omit** | Sets the parent page. The value must exactly match the `title:` of the intended parent. Case-sensitive. |
| `grand_parent` | **Required** for grandchild pages | **Omit** | Sets the grandparent page. Required when a page's `parent` is itself a child page. Must exactly match the grandparent's `title:`. |
| `description` | **Optional, recommended** | **Optional** | 1–2 sentences describing the page's purpose. JTD uses this for search result snippets and the HTML `<meta name="description">` tag. See [Writing descriptions](#writing-descriptions). |
| `redirect_from` | Optional — plugin feature | **Omit** | From the `jekyll-redirect-from` gem. Redirects one or more old URLs to this page. Use only when a page has been moved or renamed to preserve existing links. |
| `nav_enabled` | **Omit** — remove on sight | **Omit** — remove on sight | **Non-standard. Has no effect.** Not a JTD front matter key. See [Note on nav_enabled](#note-on-nav_enabled). |

---

## Annotated examples

Use placeholder values as shown. Replace all-caps placeholders before committing.

### Top-level section page (has children)

```yaml
---
title: TITLE          # Required. Becomes the H1 heading and left-nav label.
                      # Child pages must use this exact string as their parent: value.
layout: page          # Required. Always "page" — do not change.
nav_order: NAV_ORDER  # Required. Integer. Controls position among top-level nav items.
has_children: true    # Required. Enables the expand arrow; without it children won't nest.
description: DESCRIPTION  # Optional. 1–2 sentences, under 160 characters. Describe purpose, not the title.
---
```

### Child page (has a parent)

```yaml
---
title: TITLE              # Required.
layout: page              # Required.
parent: PARENT_TITLE      # Required. Must exactly match the parent page's title: value.
nav_order: NAV_ORDER      # Required. Controls position among siblings under the same parent.
description: DESCRIPTION  # Optional.
---
```

### Grandchild page (has a parent and a grandparent)

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

### Guide preview page (_guide_preview/ directory)

```yaml
---
title: TITLE              # Required.
layout: page              # Required.
description: DESCRIPTION  # Optional.
---
```

Nav keys (`nav_order`, `parent`, `has_children`, `grand_parent`) are **intentionally omitted** from guide preview pages. The `just_the_docs.collections` setting in `_config.yml` already excludes these pages from the left nav and search index. Nav keys on these pages have no effect and create misleading front matter.

---

## How nav_order works

JTD sorts sibling pages in ascending order by `nav_order`. Siblings are pages that share the same `parent:` value, or all top-level pages (those with no `parent:`).

- Pages without a `nav_order` value fall to the bottom of their sibling group and sort alphabetically among themselves.
- `nav_order` values only need to be unique within a sibling group. The same value can appear independently in different sections.
- Values do not need to be sequential. Leaving gaps — using 10, 20, 30 rather than 1, 2, 3 — makes it easy to insert a page later without renumbering every sibling.
- The value must be an integer, not a string.

**Example:** Three top-level pages with `nav_order: 10`, `nav_order: 20`, and no `nav_order` will appear in the nav as: page-at-10, page-at-20, then the unnumbered page at the bottom.

---

## Writing descriptions

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

---

## Note on nav_enabled

`nav_enabled: true` appears in the front matter of most current pages in this repo. **It is not a JTD front matter key and has no functional effect.** JTD does not recognize this key. The correct key to hide a page from navigation is `nav_exclude: true`.

The field is legacy noise carried over before front matter standards were established for this project. It does not need an immediate cleanup pass — remove it opportunistically when editing a page for other reasons. Do not add it to new pages.
