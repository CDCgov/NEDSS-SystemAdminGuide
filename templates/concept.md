---
title: TITLE              # Required. The concept name. Becomes the page's H1 and left-nav label.
                          # Child pages that reference this page must use this exact string as parent:.
layout: page              # Required. Always "page" — do not change.
nav_order: NAV_ORDER      # Required. Integer. Controls position among siblings in the nav.
                          # Remove this line only if this is a guide preview page.
parent: PARENT_TITLE      # Include if this concept page lives under a section parent.
                          # Must exactly match the parent page's title:. Remove if top-level.
description: DESCRIPTION  # Optional but recommended. 1–2 sentences, under 160 characters.
                          # Describe what this concept explains — do not restate the title.
                          # Example: "Explains how NBS 7's microservices communicate across VPC boundaries
                          #           and where each service fits in the deployment sequence."
---

<!--
  ================================================================
  VOICE AND TONE — remove this comment block before committing.

  - Address the reader as "you" when giving direct instruction.
  - Use active voice. Avoid "it is recommended," "it should be
    noted that," and passive constructions.
  - Use present tense for system behavior: "the gateway routes
    requests" — not "the gateway will route requests."
  - Write for Global English: short sentences, no idioms, no humor.
    Define every acronym on first use, e.g., "Virtual Private Cloud
    (VPC)."
  ================================================================
-->

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

<!--
  Opening paragraph — write 1–3 sentences that answer:
    1. What is this concept, in plain language?
    2. Why does it matter to the reader?
  Do not start with a bullet list or a component diagram. Ground
  the reader in simple language before introducing technical detail.

  Example of a strong opening:
    "NBS 7 uses a microservices architecture to separate application
    functions into independently deployable services. Each service
    owns a specific domain — such as data ingestion or case
    notification — and communicates with other services through
    defined APIs. This design allows a single service to be updated
    or replaced without affecting the rest of the system."

  Example of a weak opening (do not write this):
    "This document describes the architecture. The components are:
    Elasticsearch, NiFi, Modernization API..." [starts with the list]
-->

## Overview

<!--
  Expand on the opening paragraph. Explain:
  - What this concept includes and what it does not include
  - Where it fits in the larger system or workflow

  2–4 sentences. Replace this heading with something more specific
  if a better label applies (e.g., "What is the NBS 7 gateway?").
-->

## [Architecture / Components / Structure]

<!--
  Use this section to describe components, services, or structural
  elements and how they relate to each other.

  If the subject has spatial or systemic relationships — for example,
  service dependencies, data flow, or network topology — include a
  diagram. A diagram is not required if prose is sufficient.

  Replace the section heading with a specific label, e.g.:
  "NBS 7 service components" or "VPC architecture."
-->

<!--
  ================================================================
  ACCESSIBILITY — images (remove this comment before committing)

  Alt text is required on every image.
  - Describe the content AND purpose of the image: what it shows,
    and what the reader should understand from it.
  - BAD:  ![architecture diagram](images/arch.png)
  - GOOD: ![Diagram showing the NBS 7 EKS cluster connected to RDS,
           S3, and Keycloak via VPC peering. Arrows indicate data
           flow from ingestion through processing to notification.
           ](images/arch.png)
  - Use empty alt="" only for purely decorative images that convey
    no information to the reader.

  ACCESSIBILITY — headings (remove this comment before committing)
  - Do not skip levels. An H3 requires an H2 parent; H4 requires H3.
  - Do not use bold text as a visual substitute for a heading.
    If content needs a label that should appear in structure, use
    a heading.
  ================================================================
-->

<!--
  If including a diagram, replace the placeholder below.
  Write alt text that describes what the diagram shows and what
  the reader should take away from it.
-->
<!-- ![DESCRIBE THE IMAGE CONTENT AND WHAT IT COMMUNICATES](images/FILENAME.png) -->

## How it works

<!--
  Explain how this concept behaves: the relationships between
  components, the sequence of events, or the rules that govern
  its operation.

  Guidelines:
  - Use present tense: "the service routes requests to..."
  - Use "you" when describing what the administrator can do:
    "you can configure the retry limit by..."
  - Keep paragraphs short: 3–4 sentences maximum.
  - Use H3 subsections if the content spans multiple sub-topics,
    e.g., "### Request routing" and "### Health checks."
  - Do not nest steps as a/b/c. If the reader needs to take
    action, link to the relevant task page instead.
-->

<!--
  Include a callout when there is genuinely useful context the
  reader might otherwise miss. Use note for supplementary
  information that isn't critical — readers can skip a note
  without consequence.

  Replace NOTE_TEXT with a one- or two-sentence note relevant to
  this concept. Remove this block if you have nothing useful to add.
-->

> NOTE_TEXT
{: .note }

## Related topics

<!--
  List 2–5 links to related pages: task pages that put this
  concept into practice, reference pages for related parameters,
  or concept pages for closely related topics.

  Use descriptive link text — never "click here," "here," or
  "learn more" as the full link text.
  - BAD:  See [here](../path.md) for deployment steps.
  - GOOD: See [Terraform deployment procedure](../3_base_application/1_terraform-deployment.md).

  Remove this section if there are no meaningful related pages yet.
-->

<!--
  ================================================================
  ACCESSIBILITY — links (remove this comment before committing)
  - Link text must describe the destination.
  - Never use "click here," "here," "this page," or "learn more"
    as the complete link text.
  ================================================================
-->

- [RELATED PAGE TITLE](../PATH/FILENAME.md)
- [RELATED PAGE TITLE](../PATH/FILENAME.md)
