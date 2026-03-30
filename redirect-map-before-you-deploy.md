# Redirect Map Review: Before You Deploy

This file is a review map for redirects related to the Before You Deploy workstream.

## Scope and source

- Scope: URLs from the live `main` branch that should map into the restructured IA.
- Source inventory method: `git ls-tree -r --name-only main docs/1_introduction/deployment_decision_guide docs/2_prerequisites docs/deploy-nbs7/prerequisites`.
- Result: only `docs/2_prerequisites/prereq.md` exists in `main` for this scope.

## Proposed mapping

| Old URL | New URL | Status | Confidence | Notes |
|---|---|---|---|---|
| `/docs/2_prerequisites/prereq.html` | `/docs/deploy-nbs7/aws-infrastructure/prerequisites.html` | Implemented | High | Legacy page content aligns with current AWS prerequisites content. |
| `/docs/2_prerequisites/prereq/` | `/docs/deploy-nbs7/aws-infrastructure/prerequisites.html` | Implemented | High | Directory-style variant of same legacy page. |

## Out of scope for this phase

- Decision Guide URLs under `docs/1_introduction/deployment_decision_guide/*` are not present in live `main` and are treated as branch-era URLs, not production URLs.
- Anchor-level remaps from old fragments are tracked separately because fragments are not sent to the server during redirect handling.
