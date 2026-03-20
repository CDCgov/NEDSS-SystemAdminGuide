# NBS System Admin Guide User Guide


**New contributor?** Start with the [Contributor Workflow](WORKFLOW.md) for setup instructions and daily git commands.

## Quick Guide

| Site | URL |
|------|-----|
| Production | https://cdcgov.github.io/NEDSS-SystemAdminGuide/ |
| Stakeholder preview | https://jburgh.github.io/CDCgov-NEDSS-SystemAdminGuide-preview/ _(temporary — pending CDCgov org transfer)_ |

| Action                       | Location                              |
|----------------------------|---------------------------------------|
| Stage content for stakeholder review | Push to `preview` branch — see [Stakeholder Review Workflow](#stakeholder-review-workflow) |
| Previous release versions  | Any branch named `release-<version>` is automatically added under **PREVIOUS VERSIONS** |
| Access versioned docs      | Located under **PREVIOUS VERSIONS** section |
| Publish approved content without showing it in nav yet | `_guide_preview/*.md` — see [Hidden Draft Pages](#hidden-draft-pages) |


## Implementation
GitHub Pages hosts System Admin Guide site by serving static HTML, CSS, and JS directly from this repository (via GitHub Actions).

Just the Docs is a Jekyll-based theme optimized for documentation sites, fully-compatible with GitHub Pages—providing menus, search, collections, and theming out-of-the-box.

Two GitHub Actions workflows handle builds and deploys:

**Production** (`jekyll.yml`) — triggers on push to `main`:
- Builds `docs/` and `_guide_preview/` into `_site/`
- Discovers and builds any `release-*` branches into `_previous_versions/<branch>/`
- Deploys to GitHub Pages at https://cdcgov.github.io/NEDSS-SystemAdminGuide/

**Preview** (`jekyll-preview.yml`) — triggers on push to `preview`:
- Builds the site with the preview baseurl
- Deploys to the staging repo at https://jburgh.github.io/CDCgov-NEDSS-SystemAdminGuide-preview/


## Stakeholder Review Workflow

The review workflow uses a dual long-lived branch system: `main` matches production, `preview` feeds the staging site. See the [Quick Guide](#quick-guide) table above for site URLs.

**How it works:**
1. Authors do their work on a short-lived **feature branch** created from `main`
2. When ready for review, the feature branch is merged into the long-lived **`preview` branch** and pushed — this triggers an automatic deploy to the preview site
3. Stakeholders browse the preview site and provide async feedback
4. Authors iterate: update the feature branch, re-merge to `preview`, repeat
5. Once approved, the feature branch is merged to `main` via PR — never `preview` directly to `main`, as `preview` accumulates work from multiple authors

For step-by-step git commands, see [WORKFLOW.md](WORKFLOW.md).


## Previous Versions
Branches starting with `release-` are automatically built and deployed under `/previous_versions/<branch>/` via GitHub Actions.


## Hidden Draft Pages

> **Edge case — not the standard review workflow.** Use this only when content is already approved and merged to `main`, but you want to publish it without it appearing in navigation yet — for example, while finishing out the rest of a section. For pre-approval stakeholder review, use the [Stakeholder Review Workflow](#stakeholder-review-workflow) instead.

Drop Markdown files into the `_guide_preview/` directory to serve content on the production site that is:
- **Rendered and available**, but **hidden from navigation and search**
- Accessible **only** via direct URL (e.g. `/guide_preview/my-file/`)


## Markdown & Configuration Sources
We use GitHub-Flavored Markdown (GFM) for tables, fenced code blocks, lists, etc.

Just the Docs theme renders pages according to `_config.yml`, supporting navigation, collections, syntax highlighting, and more.



## Building and Previewing Site Locally

**Which option should I use?**
- **Content authors** (text edits, new pages): Option 1 is sufficient for most work.
- **Anyone changing `_config.yml`, `_sass/`, templates, or site structure**: use Option 2 or Option 3. VS Code preview does not render theme or config changes.
- **Option 2 vs Option 3**: same result, different tooling. Use Option 3 (Docker) if you don't want to install Ruby locally.

### Option 1 — VS Code markdown preview (recommended for content authors)

VS Code has a built-in markdown preview. Open any `.md` file and press `Cmd+Shift+V` (Mac) or `Ctrl+Shift+V` (Windows) to open a rendered preview alongside your editor. This is sufficient for most content work.

For a full rendered view of the site with navigation and theme intact, push to the `preview` branch instead — see [Stakeholder Review Workflow](#stakeholder-review-workflow).

### Option 2 — Jekyll local build (requires Ruby)

Use this if you are modifying `_config.yml`, `_sass/`, or anything that affects site structure or appearance rather than content.

**Install Ruby** (required):
- Mac: `brew install ruby` (requires [Homebrew](https://brew.sh))
- Windows: use [RubyInstaller](https://rubyinstaller.org/)

**Install Bundler:**
```bash
gem install bundler
```

**Run the local server:**
```bash
bundle install
bundle exec jekyll serve --livereload
```

Preview at `http://localhost:4000`. The browser reloads automatically when you save a file. The built site is stored in `_site/`.

### Option 3 — Docker (no Ruby required)

Use this for the same purpose as Option 2, but without installing Ruby locally. Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

**Run the local server:**
```bash
docker compose up
```

Preview at `http://localhost:4000`. Live reload is enabled — the browser refreshes automatically when you save a file.

**First run:** Docker pulls the Ruby image and installs gems, which takes a few minutes. Subsequent runs are fast because gems are cached in a Docker volume.

**Stop the server:** Press `Ctrl+C` in the terminal, then run:
```bash
docker compose down
```


## Supporting Links

- [Starting with GitHub Pages](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/creating-a-github-pages-site-with-jekyll#creating-your-site).
- [GitHub Pages](https://docs.github.com/en/pages)
- [GitHub Pages Actions workflow](https://github.blog/changelog/2022-07-27-github-pages-custom-github-actions-workflows-beta/)
- [Starter Workflows](https://github.com/actions/starter-workflows/blob/main/pages/jekyll.yml)
- [Jekyll](https://jekyllrb.com)
- [jekyll-default-layout](https://github.com/benbalter/jekyll-default-layout)
- [jekyll-seo-tag](https://jekyll.github.io/jekyll-seo-tag)
- [Just the Docs](https://just-the-docs.github.io/just-the-docs/)
- [Just the Docs Template](https://github.com/just-the-docs/just-the-docs-template)
- [Bundler](https://bundler.io)