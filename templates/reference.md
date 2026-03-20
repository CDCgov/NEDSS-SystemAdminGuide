---
title: TITLE              # Required. Use a noun phrase that names what this page documents.
                          # Good: "NBS Gateway Helm values" or "Terraform input variables"
                          # Weak: "Reference" (not specific enough for the nav label)
layout: page              # Required. Always "page" — do not change.
nav_order: NAV_ORDER      # Required. Integer. Controls position among siblings in the nav.
parent: PARENT_TITLE      # Include if this reference page lives under a section parent.
                          # Must exactly match the parent page's title:. Remove if top-level.
description: DESCRIPTION  # Optional but recommended. 1–2 sentences, under 160 characters.
                          # State what is documented here — parameter set, version matrix, etc.
                          # Example: "Complete list of Helm values for the NBS Gateway chart,
                          #           including defaults and accepted value ranges."
---

<!--
  ================================================================
  VOICE AND TONE — remove this comment block before committing.

  - Reference pages are scanned, not read linearly. Keep prose
    minimal. Let the tables carry the information.
  - Use present tense for descriptions: "Controls the number of
    replicas" — not "will control."
  - Write for Global English: no idioms, no colloquialisms.
    Define acronyms on first use — readers may land here directly
    from search without reading a parent concept page.
  ================================================================
-->

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

<!--
  Write exactly one sentence identifying what this page documents.
  This is not an introduction paragraph — it is a single statement
  of scope that helps the reader confirm they are on the right page.

  Examples:
  - "This page documents all Helm values for the NBS Gateway chart."
  - "Lists the IAM permissions required to run the Terraform
    provisioning scripts."
  - "Reference for all environment variables read by the
    Modernization API service at startup."

  Keep it to one sentence. If you need more context, that content
  belongs on a concept page, not here.
-->

ONE_SENTENCE_SCOPE_STATEMENT

## [PARAMETER/VALUES/REQUIREMENTS TABLE HEADING]

<!--
  Use a table for all structured data: parameters, configuration
  values, version requirements, command flags, environment
  variables, error codes, etc.

  Tables are the primary structure of a reference page. Prose
  should appear only when context cannot be expressed in a table —
  for example, a constraint that applies to multiple rows, or a
  prerequisite that applies to the entire table.

  Standard column patterns:
  - Parameters/config: | Parameter | Type | Required | Default | Description |
  - Command flags:     | Flag | Shorthand | Description |
  - Version matrix:    | Component | Minimum version | Notes |
  - Requirements:      | Requirement | Details |

  Choose columns based on what information the reader actually
  needs to look up. Do not add columns for information you don't
  have.

  ================================================================
  ACCESSIBILITY — tables (remove this comment before committing)
  - Always include a header row. Never use the first data row as
    an implicit header.
  - Do not use tables for layout or for sequential steps that
    belong in a numbered list.
  - If a "Description" cell would need more than 2–3 sentences
    to explain, that content belongs on a concept or task page,
    not in this table.
  ================================================================
-->

<!--
  ================================================================
  ACCESSIBILITY — links (remove this comment before committing)
  - Link text must describe the destination.
  - Never use "click here," "here," or "learn more" as the full
    link text.
  ================================================================
-->

| COLUMN_HEADER | COLUMN_HEADER | COLUMN_HEADER | COLUMN_HEADER |
|---------------|---------------|---------------|---------------|
| `VALUE` | TYPE | DEFAULT | DESCRIPTION |
| `VALUE` | TYPE | DEFAULT | DESCRIPTION |

<!--
  Include a note callout only when there is a constraint,
  exception, or clarification that applies to the table above
  and cannot fit in a cell. Replace NOTE_TEXT with a factual,
  specific statement.

  Example:
  - "All timeout values are in seconds. Values below 5 are
    ignored; the service enforces a minimum of 5 seconds."

  Remove this callout if there is nothing to add.
-->

> NOTE_TEXT
{: .note }

## [ADDITIONAL TABLE HEADING — add sections as needed]

<!--
  Add additional table sections for logically distinct groups of
  reference data. For example, a Helm values page might have
  separate sections for "Database configuration," "Ingress
  configuration," and "Resource limits."

  Keep each section focused. If a section would only have one or
  two rows, consider consolidating with an adjacent section.

  If your table requires a "Notes" column with long prose for most
  rows, that's a signal the content should move to a concept or
  task page. Reference pages should be scannable in under a minute.
-->
