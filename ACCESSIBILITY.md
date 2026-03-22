# Accessibility Standards

This document is the authoritative accessibility reference for the NEDSS System Administration Guide. It records Section 508 / WCAG 2.1 AA findings, authoring standards, and known limitations. Future contributors and reviewers should consult it alongside [STYLES.md](STYLES.md).

## Overview

The NEDSS System Administration Guide is a federally published resource and must meet **Section 508** and **WCAG 2.1 Level AA** requirements. The site is built with Jekyll and the Just the Docs (JTD) theme; most structural accessibility (landmark regions, skip-navigation, focus management) is provided by the theme. Authoring-time obligations — color contrast, alt text, heading hierarchy, link text, and table markup — fall to contributors.

WCAG 2.1 AA thresholds used in this document:

| Text type | Required contrast ratio |
|-----------|------------------------|
| Normal text (< 18 pt regular or < 14 pt bold) | 4.5 : 1 |
| Large text (≥ 18 pt regular or ≥ 14 pt bold) | 3.0 : 1 |
| UI components and graphical objects | 3.0 : 1 |

## Color contrast

### Brand and body colors

The following pairings are used across the site and have been verified against WCAG 2.1 AA.

| Foreground | Background | Ratio | AA normal | AA large |
|------------|-----------|-------|-----------|----------|
| `$cdc-blue` #005DAA | White #FFFFFF | 6.68 : 1 | Pass | Pass |
| `$body-heading-color` #1A1A1A | White #FFFFFF | 17.40 : 1 | Pass | Pass |
| `$cdc-blue` #005DAA | JTD sidebar #F5F6FA | 6.20 : 1 | Pass | Pass |

### Callout accent colors

JTD callouts use a `-000` background tint and `-300` foreground accent from a shared color scale. The pairings below reflect the accent-on-tint combination rendered in the built site.

| Callout type | Foreground (`-300`) | Background (`-000`) | Ratio | AA normal | Notes |
|---|---|---|---|---|---|
| Note (blue) | #2474B6 | #E6EFF7 | 4.25 : 1 | ⚠️ Borderline | Slightly below 4.5:1. Body text inside callouts inherits `$body-heading-color` (#1A1A1A) at 17.40:1 — this pairing applies only to the accent border/title element. |
| Warning (yellow) | #ECB046 | #FBEDD6 | 1.67 : 1 | Fail | Body text contrast is still high; the accent color alone fails. |
| Important (red) | #CB3E6E | #F8E4EB | 3.88 : 1 | Fail | Falls short of 4.5:1 for normal text; passes 3.0:1 large-text threshold. |
| New (green) | #9ACC54 | #EAF5DC | 1.67 : 1 | Fail | Body text contrast is still high; the accent color alone fails. |
| Highlight (purple) | (see [Callouts](#callouts) section) | — | — | See below | |

**Important caveat:** The failing ratios above apply to the `-300` accent color against the `-000` tint — most visibly in the left border stripe and any title text rendered in that color. Paragraph body text inside all callouts inherits the standard dark body color and maintains high contrast. Before treating any callout as non-compliant, verify in a built-site browser using DevTools color picker to confirm which elements actually render in the accent color.

## Callouts

### Usage and markup

Five callout types are configured in `_config.yml`. Each maps to a color scale:

| Type | CSS class | Color scale | Use for |
|------|-----------|-------------|---------|
| Note | `.note` | Blue | Supplementary information; tips |
| Warning | `.warning` | Yellow | Irreversible actions; potential data loss |
| Important | `.important` | Red | Critical requirements; hard blockers |
| New | `.new` | Green | Feature availability; version requirements |
| Highlight | `.highlight` | Purple | (see below) |

Callout syntax:

```markdown
> Callout text here.
{: .note }
```

### Highlight callout — color-only concern

The `highlight` callout type (`{: .highlight }`) is **defined in `_config.yml` but has no `title:` field configured**. In JTD's callout implementation, the title field provides a text label (e.g., "Note", "Warning") that supplements the color indicator. Without it, color is the sole differentiator for this callout type.

Using color as the only means of conveying information fails WCAG 2.1 Success Criterion 1.4.1 (Use of Color).

**Current status:** Zero uses of `{: .highlight }` exist in `docs/`. The callout is defined but unused.

**Recommendation:** Remove the `highlight` entry from `_config.yml` and the corresponding purple color scale from `colors.scss`. If a purple callout is needed in the future, add a `title:` field to the `_config.yml` entry before use.

## Images

### Alt text is required

Every image must have descriptive alt text. Empty `alt=""` is only appropriate for purely decorative images with no informational content.

**Standard:** Describe what the image shows AND what the reader should take away from it.

```markdown
<!-- BAD — file name is not a description -->
![screenshot](images/output.png)

<!-- GOOD — describes content and meaning -->
![Terminal output showing all three pods in Running status
 with READY 1/1 after running kubectl get pods -n nbs
](images/pod-status.png)
```

### File naming

Use lowercase-hyphenated filenames: `pod-status.png`, not `PodStatus.PNG` or `pod_status.png`.

### Reviewer checklist

- Every `![` in the file has non-empty alt text
- Alt text describes the image content and what the reader should conclude
- Images are not the sole carrier of critical information (also provide the information as text)

## Headings

### Hierarchy rules

Do not skip heading levels. The page `title:` front matter key renders as the H1 — do not add a duplicate `# H1` in the body.

| Level | Tag | Use for |
|-------|-----|---------|
| H1 | Rendered from `title:` front matter | Page title — one per page, never in body |
| H2 | `##` | Major sections |
| H3 | `###` | Subsections within an H2 |
| H4 | `####` | Subsections within an H3 — use sparingly |

**Do not use bold text as a structural substitute for a heading.** Bold text is not navigable by assistive technology.

### Heading content

Heading text must be unique and descriptive within the page. Avoid generic headings like "Details" or "More information."

## Links

### Descriptive link text

Link text must describe the destination. Screen reader users navigate by link text alone; "click here" and "here" provide no context.

```markdown
<!-- BAD -->
See [here](../path.md) for installation steps.

<!-- GOOD -->
See [Keycloak installation](../path.md) for installation steps.
```

### Anchor links

Anchor-only links (`#section-name`) are valid and excluded from the automated link checker by default. Verify that the target heading exists in the destination file.

## Tables

### When to use tables

Use tables for structured reference data with clear row/column relationships. Do not use tables for layout or for simple two-column key/value lists that read naturally as prose.

### Accessibility requirements

- Every table must have a header row using Markdown `|---|` separator syntax.
- Column headers must describe the data in that column.
- Do not use tables to arrange non-tabular content.

```markdown
<!-- Well-formed table -->
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name`    | string | Yes   | Display name of the resource |
```

## Known limitations

The following issues are documented and tracked. They represent theme or infrastructure constraints, not authoring errors.

| Area | Issue | Status |
|------|-------|--------|
| Callout accent colors | Yellow-on-yellow-tint (1.67:1) and green-on-green-tint (1.67:1) fail WCAG AA for accent elements. Body text contrast is unaffected. | Known; body text passes. Accent-only failure pending upstream theme resolution. |
| Red callout | Red-300 on red-000 (3.88:1) fails AA normal text threshold for accent elements. | Known; body text passes. |
| Blue callout | Blue-300 on blue-000 (4.25:1) is borderline — 0.25 below the 4.5:1 AA normal threshold for accent elements. | Known; body text passes. Verify in built site. |
| Highlight callout | No `title:` text label; color is the sole type indicator. | Unused in `docs/`; recommend removing from `_config.yml`. |
