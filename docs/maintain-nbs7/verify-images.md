---
title: Verify container image authenticity
layout: page
nav_order: 1
parent: Maintain NBS 7
published: false
description: Inspect the build provenance attestation for an NBS container image to confirm it was built by CDC and has not been altered.
---

# Verify NBS container image authenticity

[[cdc]] publishes [[nbs]] container images through [Quay.io](https://quay.io/search?q=cdc-nbs&page=1). Because images travel across the public internet before reaching your infrastructure, you should verify that the image you pulled matches what CDC built before you deploy it.

Every NBS container image includes a [[build-provenance]] attestation, a cryptographically verifiable record of how the image was built. This article explains how to verify the authenticity of NBS container images.

## On this page
{: .no_toc .text-delta }

1. TOC
{:toc}

## Before you begin

Confirm the following before you begin:

- You have Docker installed with the `buildx` plugin. Docker Desktop 4.x and later include `buildx` by default. Docker Engine 23.0 and later include it as standard.
- You know the image name and version tag you want to verify (for example, `quay.io/us-cdcgov/cdc-nbs-modernization/elasticsearch:9.4.2`).

Public NBS repositories on Quay.io allow anonymous read access. You do not need to log in to inspect an image.

## Inspect the provenance attestation

To verify the authenticity of an NBS container image:

1. Run the `imagetools inspect` command against the image. Replace `<image-name>` and `<version-tag>` with the image that you want to verify:

   ```bash
   docker buildx imagetools inspect \
     quay.io/us-cdcgov/cdc-nbs-modernization/<image-name>:<version-tag> \
     --format "{% raw %}{{ json .Provenance }}{% endraw %}"
   ```

   Docker outputs a JSON object describing how the image was built. If the command returns `{}` or an error, see [Determine whether to trust the image](#determine-whether-to-trust-the-image).

2. Confirm the following fields in the response match your expectations:

   <!-- markdownlint-disable MD055 MD056 -->

   | Field | Description | How to verify |
   | :---- | :---- | :---- |
   | `predicate.buildDefinition.externalParameters.workflow` | References a workflow file within a CDC-owned public repository, typically under `github.com/CDCgov/`. | Open that URL in a browser to confirm the workflow file exists and is public. |
   | `predicate.buildDefinition.externalParameters.workflow.ref` | The git branch or tag the workflow ran on. | For official releases, this value is `refs/heads/main` or a release tag. |
   | `predicate.runDetails.builder.id` | The Continuous Integration (CI) system that built the image. | This value points to `https://github.com/CDCgov/...`. |
   | `predicate.buildDefinition.resolvedDependencies` | The base image or images the container was built on, pinned by content digest (SHA256). | Look up these digests in Docker Hub or the vendor's registry to confirm them. |
   | `predicate.runDetails.metadata.startedOn` | The build timestamp. | This value matches the release date of the version you are pulling. |
   {: .three-column-values-table }

The following is a trimmed example of provenance output from an NBS container build, showing the fields from the preceding table:

```json
{
  "SLSA": {
    "buildDefinition": {
      "buildType": "https://github.com/moby/buildkit/blob/master/docs/attestations/slsa-definitions.md",
      "externalParameters": {
        "configSource": {
          "uri": "git+https://github.com/CDCgov/NEDSS-Modernization@refs/heads/main",
          "digest": {
            "sha1": "c43414b4b98e9ddf4203acc05f6094c867f30e3e"
          },
          "path": "Dockerfile"
        }
      },
      "resolvedDependencies": [
        {
          "uri": "pkg:docker/docker.elastic.co/elasticsearch/elasticsearch@9.4.2?platform=linux%2Famd64",
          "digest": {
            "sha256": "be5f49784ff5ec8a5b5d7ba17f944d9d6b10c067f596ee93e6b6cb82d2dd874c"
          }
        }
      ]
    },
    "runDetails": {
      "builder": {
        "id": "https://github.com/CDCgov/NEDSS-Modernization/.github/workflows/Build-and-deploy-elasticsearch.yaml@refs/heads/main"
      },
      "metadata": {
        "invocationId": "https://github.com/CDCgov/NEDSS-Modernization/actions/runs/31208223551/attempts/1",
        "startedOn": "2026-08-07T18:44:32.555259476Z",
        "finishedOn": "2026-08-07T18:44:32.967529283Z"
      }
    }
  }
}
```

Full output is much longer than this example. `mode=max` provenance includes the complete Dockerfile, embedded as base64, and full build environment details. The fields in the preceding table are the most useful fields for verification.

## Determine whether to trust the image

The image is trustworthy when the response is a populated JSON object and every field matches its expected value in the [field verification table](#inspect-the-provenance-attestation).

> If the response is empty, returns an error, or any field does not match, contact the NBS team at [nbs@cdc.gov](mailto:nbs@cdc.gov) before you deploy the image.
{: .warning }

## Resources

For background on the underlying standard and tooling referenced in this task, see:

- [Supply-chain Levels for Software Artifacts (SLSA) framework overview](https://slsa.dev)
- [Docker BuildKit attestations documentation](https://docs.docker.com/build/metadata/attestations/)
- [NBS Modernization repository on GitHub](https://github.com/CDCgov/NEDSS-Modernization)
