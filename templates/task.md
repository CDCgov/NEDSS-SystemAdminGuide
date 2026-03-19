---
title: TITLE              # Required. Use an action phrase that names the task.
                          # Good: "Deploy the NBS Gateway service"
                          # Weak: "NBS Gateway" (a label, not a task)
layout: page              # Required. Always "page" — do not change.
nav_order: NAV_ORDER      # Required. Integer. Controls position among siblings in the nav.
parent: PARENT_TITLE      # Include if this task page lives under a section parent.
                          # Must exactly match the parent page's title:. Remove if top-level.
description: DESCRIPTION  # Optional but recommended. 1–2 sentences, under 160 characters.
                          # State what the reader will accomplish — do not restate the title.
                          # Example: "Walks through deploying the NBS Gateway Helm chart and
                          #           verifying the service is reachable after deployment."
---

<!--
  ================================================================
  VOICE AND TONE — remove this comment block before committing.

  - Address the reader directly as "you": "Run the following
    command" not "The user should run..."
  - Use active voice and imperative mood in steps: "Run,"
    "Open," "Copy," "Replace" — not "The file should be opened."
  - Use present tense for expected results: "The command outputs
    a JSON object" — not "The command will output..."
  - Write for Global English: short sentences, no idioms, no humor.
    Define every acronym on first use.
  ================================================================
-->

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Before you begin

<!--
  List what the reader must have done or have available before
  starting this procedure. Think of this as an explicit dependency
  check — if any of these aren't true, the reader will fail
  partway through.

  Write each prerequisite as a complete sentence or noun phrase.
  Examples:
  - "You have completed [Keycloak installation](../5_keycloak/1_keycloak_installation.md)."
  - "You have `kubectl` configured with cluster access."
  - "You have the `nbs-helm-vX.Y.Z.zip` package from the release page."

  If there are genuinely no prerequisites, remove this section
  entirely. Do not write "None."

  ================================================================
  ACCESSIBILITY — links (remove this comment before committing)
  Link text must describe the destination — not "this page,"
  "here," or "click here."
  - BAD:  "See [here](../path.md) first."
  - GOOD: "Complete [Keycloak installation](../5_keycloak/1_keycloak_installation.md) first."
  ================================================================
-->

- PREREQUISITE
- PREREQUISITE

## PROCEDURE_TITLE

<!--
  Write a stem sentence introducing the steps. The stem sentence
  is a short, grammatically incomplete phrase ending with a colon
  that sets up the numbered list.

  The stem sentence tells the reader what they are about to do —
  not just "Steps:" or "Procedure:".

  Examples of good stem sentences:
  - "To deploy the NBS Gateway service:"
  - "To create the Kubernetes secrets manifest:"
  - "To configure Keycloak for NBS 7 authentication:"

  Replace "PROCEDURE_TITLE" above with the task's action phrase,
  e.g., "Deploy the NBS Gateway service" or "Configure Keycloak."

  Replace STEM_SENTENCE below with your stem sentence.
-->

STEM_SENTENCE

<!--
  Write one numbered step per action. Each step = one thing to do.
  Do not nest steps as a/b/c — split them into separate numbers
  or use a note callout for supplementary detail.

  Step format:
  1. Start with an imperative verb: "Run," "Open," "Copy," "Set."
  2. Include the complete command or value — never refer readers
     to "the command above" or "the previous step."
  3. After steps that produce visible output, show the expected
     result as a code block or a short descriptive sentence.
     This helps readers confirm the step succeeded.

  Example of a well-formed step with expected output:
    5. Run the Helm install command:
       ```bash
       helm upgrade --install nbs-gateway ./charts/nbs-gateway \
         --namespace nbs --create-namespace \
         --values values.yaml
       ```
       Helm outputs `Release "nbs-gateway" has been upgraded.`
       If you see an error instead, verify your kubeconfig is
       pointing at the correct cluster.
-->

<!--
  ================================================================
  ACCESSIBILITY — headings (remove this comment before committing)
  - Do not skip heading levels.
  - Do not use bold text as a structural substitute for a heading.
  ================================================================
-->

<!--
  Include a warning callout when a step involves an irreversible
  action, data loss risk, or a change that could break a running
  system. Replace WARNING_TEXT with a specific, factual statement.

  Examples:
  - "Running `terraform destroy` permanently deletes all resources
    in the target environment. This action cannot be undone."
  - "This step removes the existing Kubernetes namespace and all
    resources in it. Ensure you have a backup before proceeding."

  Remove this callout if there is no destructive step.
-->

> WARNING_TEXT
{: .warning }

1. STEP
1. STEP
1. STEP

<!--
  After steps that produce visible terminal output, format the
  expected output as a code block using the "text" language tag.
  This confirms to the reader that the step completed successfully.

  Example:
  ```text
  Release "nbs-gateway" has been upgraded. Happy Helming!
  LAST DEPLOYED: Mon Jan  1 12:00:00 2025
  NAMESPACE: nbs
  STATUS: deployed
  ```

  Also note common failure modes inline, where they are most
  useful — not in a separate troubleshooting section at the end.
-->

## After you finish

<!--
  Tell the reader what to do next or how to verify success.
  This section is optional — include it when there is a natural
  next step or when verification is non-obvious.

  Examples:
  - "Verify the deployment: run `kubectl get pods -n nbs` and
    confirm all pods show STATUS Running."
  - "Proceed to [Configure Keycloak authentication](../path.md)."
  - "The service is now available at https://app.YOURDOMAIN/."

  Remove this section if there is no meaningful follow-up.
-->
