---
title: TITLE              # Required. The section name. Becomes the left-nav parent label.
                          # Child pages that reference this section must use this exact
                          # string as their parent: value. Case-sensitive.
layout: page              # Required. Always "page" — do not change.
nav_order: NAV_ORDER      # Required. Integer. Controls position among top-level nav items.
has_children: true        # Required. Tells JTD to render the expand arrow in the nav.
                          # Without this, child pages won't appear nested under this section.
description: DESCRIPTION  # Optional but recommended. 1–2 sentences, under 160 characters.
                          # Describe what this section covers and who it is for.
                          # Example: "Covers deployment of all NBS 7 microservices using Helm,
                          #           including Elasticsearch, the Modernization API, and NiFi."
---

<!--
  ================================================================
  VOICE AND TONE — remove this comment block before committing.

  - Address the reader as "you" when describing what they will do.
  - Use active voice. Avoid "this section will cover" — prefer
    "this section covers."
  - Use present tense throughout.
  - Write for Global English: short sentences, no idioms.
    Define acronyms on first use.
  ================================================================
-->

<!--
  Opening paragraph — write 2–3 sentences that orient the reader:
    1. What does this section cover?
    2. Who is it for, or what role or goal does it serve?
    3. Where does it fit in the larger workflow?
       (e.g., "Complete AWS infrastructure setup before starting
       this section.")

  Do not use bullet points here. This is a prose paragraph.

  Example:
    "This section covers deploying and validating all NBS 7
    microservices using Helm. It is intended for administrators
    who have completed Kubernetes bootstrapping and have the
    nbs-helm package available. Work through the pages in order
    — each service depends on the ones deployed before it."

  Weak opening (do not write this):
    "This section covers microservices. There are many microservices.
    They are deployed using Helm." [Too short, adds no guidance]
-->

OPENING_PARAGRAPH

## In this section

<!--
  List each child page with its title as a link and one sentence
  describing what it covers.

  Guidelines:
  - One sentence per child page — do not summarize the child page's
    full content. Give the reader enough to know whether to click.
  - List pages in the order a reader should work through them,
    which should match their nav_order values.
  - Do not repeat information from the child pages — this list
    orients the reader, it does not replace the content.
  - Use descriptive link text (the page title) — never "click here."

  ================================================================
  ACCESSIBILITY — links (remove this comment before committing)
  - Link text must describe the destination.
  - The page title is almost always the right link text here.
  ================================================================
-->

- [CHILD PAGE TITLE](FILENAME.md) — ONE_SENTENCE_DESCRIPTION
- [CHILD PAGE TITLE](FILENAME.md) — ONE_SENTENCE_DESCRIPTION
- [CHILD PAGE TITLE](FILENAME.md) — ONE_SENTENCE_DESCRIPTION

<!--
  Include an important callout when there is a prerequisite,
  ordering constraint, or critical context the reader must know
  before entering this section.

  Examples:
  - "Complete [Initial Kubernetes Deployment](../4_initial_kubernetes_deployment/0_kubernetes_bootstrapping.md)
     before working through this section."
  - "You must have cluster-admin access to deploy these services."

  Use important (blue) for must-read requirements — things the
  reader cannot skip without breaking the workflow.
  Remove this callout if there is no genuine prerequisite.
-->

> IMPORTANT_TEXT
{: .important }

<!--
  ================================================================
  ACCESSIBILITY — headings (remove this comment before committing)
  - Do not skip heading levels.
  - Do not use bold text as a structural substitute for a heading.
  ================================================================

  Landing pages typically do not need a TOC. The child page list
  above serves as the navigation aid for this section. Do not add
  a TOC block unless this page also contains substantial content
  sections below the child list.
-->
