# 📘NBS System Admin Guide User Guide


## Quick Guide

**GitHub Pages URL** https://cdcgov.github.io/NEDSS-SystemAdminGuide/

| Action                       | Location                              |
|----------------------------|---------------------------------------|
| Add draft docs             | `_guide_preview/*.md`                |
| View a draft page          | `/guide_preview/<file_path>/`. Example ../docs/1_introduction/architecture_and_microservices.html -> ../guide_preview/1_introduction/architecture_and_microservices.html         |
| Previous release versions  | Any branch naming with convention `release-<version>`, will be automatacally added under **PREVIOUS VERSIONS** section |
| Access versioned docs      | Located under **PREVIOUS VERSIONS** section |


## Implementation
GitHub Pages hosts System Admin Guide site by serving static HTML, CSS, and JS directly from this repository (via GitHub Actions) .

Just the Docs is a Jekyll-based theme optimized for documentation sites, fully-compatible with GitHub Pages—providing menus, search, collections, and theming out-of-the-box .

GitHub Actions Workflow builds and deploys content through these steps:

- Build main branch into _site/. from docs directory and separately _guide_preview
- Discover and build any release-* branches into _previous_versions/<branch>/.
- Upload and deploy everything via GitHub Pages.
- Jekyll renders navigation, hides preview docs, and adds version management.


## Draft & Preview Content

You can drop Markdown files into the `_guide_preview/` directory to serve **draft or preview documentation** that is:
- **Rendered and available**, but **hidden from navigation and search**.
- Accessible **only** via direct URL (e.g. `/guide_preview/my-file/`).


## Previous Versions
Branches starting with release- are automatically built and deployed under `/previous_versions/<branch>/` via GitHub Actions.


## Markdown & Configuration Sources
We use GitHub-Flavored Markdown (GFM) for tables, fenced code blocks, lists, etc.

Just the Docs theme renders pages according to _config.yml, supporting navigation, collections, syntax highlighting, and more .



## Building and Previewing Site locally

Assuming Jekyll and Bundler are installed on your computer:

1.  Change your working directory to the root directory of your site.
2.  Run `bundle install`.
3.  Run `bundle exec jekyll serve` to build your site and preview it at `localhost:4000`. The built site is stored in the directory `_site`.



## Supporting Links

- [Starting with GitHub Pages](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/creating-a-github-pages-site-with-jekyll#creating-your-site).
- [Jekyll](https://jekyllrb.com)
- [Just the Docs](https://just-the-docs.github.io/just-the-docs/)
- [Just the Docs Template](https://github.com/just-the-docs/just-the-docs-template)
- [GitHub Pages](https://docs.github.com/en/pages)
- [GitHub Pages Actions workflow](https://github.blog/changelog/2022-07-27-github-pages-custom-github-actions-workflows-beta/)
- [Bundler](https://bundler.io)
- [jekyll-default-layout](https://github.com/benbalter/jekyll-default-layout)
- [jekyll-seo-tag](https://jekyll.github.io/jekyll-seo-tag)
- [Starter Workflows](https://github.com/actions/starter-workflows/blob/main/pages/jekyll.yml)
