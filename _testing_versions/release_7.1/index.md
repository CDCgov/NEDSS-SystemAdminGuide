---
title: release-7.1.1
parent: Testing Versions
has_childern: true
layout: page
nav_order: 1
---

# Introduction
{: .fs-9 }
The Modernized NBS 7 system is built to provide a straightforward transition from classic NBS Version 6 systems. It integrates seamlessly, layering on improved interfaces and functions, with the with classic systems that have already been deployed. Users will see a composite of the new features from NBS 7 Modernized and old features from classic NBS 6.
{: .fs-6 .fw-300 }

## Revision History

| Date         | Description        | Author |
|:-------------|:------------------|:-------|
| December 16th, 2024 | 7.8.0 Minor Release | Anand Logan, Ragul Shanmugam, Upasana Pattnaik, Kashyap Ramakur, Aaron Chapman, Duc Nguyen, Subba Reddy Alla, Chuck Moss  |



## Purpose
The purpose of this document is to help an NBS system administrator deploy the NBS 7 infrastructure and microservices in an AWS environment. It will provide the information needed to set up the required environment, as well as convey a common understanding of the initial install.

## Runtime Environment Support
NBS 7 supports AWS and Azure as runtime options. The underlying system itself has been developed using a cloud-agnostic approach. This guide targets the AWS runtime. For more information on Azure, please contact [NBSSupport@cdc.gov](mailto:NBSSupport@cdc.gov). Future versions of this guide will cover other cloud runtime environments that support Kubernetes such as Google Cloud Platform and Azure.

## Intended Audience
This guide is intended to be used to install NBS 7, a complex cloud-native application. It assumes familiarity with cloud technologies and tools: knowledge of your cloud service provider (e.g. AWS), runtime environment (e.g. Kubernetes), experience running Terraform and Helm., and experience debugging routine systems and infrastructure problems. You will need administrator-level access to your runtime environment, and access to a local system with a set of installed prerequisites. Please see the Prerequisites and Dependencies section below.


<!-- This is a *bare-minimum* template to create a Jekyll site that uses the [Just the Docs] theme. You can easily set the created site to be published on [GitHub Pages] – the [README] file explains how to do that, along with other details.

If [Jekyll] is installed on your computer, you can also build and preview the created site *locally*. This lets you test changes before committing them, and avoids waiting for GitHub Pages.[^1] And you will be able to deploy your local build to a different platform than GitHub Pages.

More specifically, the created site:

- uses a gem-based approach, i.e. uses a `Gemfile` and loads the `just-the-docs` gem
- uses the [GitHub Pages / Actions workflow] to build and publish the site on GitHub Pages

Other than that, you're free to customize sites that you create with this template, however you like. You can easily change the versions of `just-the-docs` and Jekyll it uses, as well as adding further plugins.

[Browse our documentation][Just the Docs] to learn more about how to use this theme.

To get started with creating a site, simply:

1. click "[use this template]" to create a GitHub repository
2. go to Settings > Pages > Build and deployment > Source, and select GitHub Actions

If you want to maintain your docs in the `docs` directory of an existing project repo, see [Hosting your docs from an existing project repo](https://github.com/just-the-docs/just-the-docs-template/blob/main/README.md#hosting-your-docs-from-an-existing-project-repo) in the template README.

----

[^1]: [It can take up to 10 minutes for changes to your site to publish after you push the changes to GitHub](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/creating-a-github-pages-site-with-jekyll#creating-your-site).

[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[README]: https://github.com/just-the-docs/just-the-docs-template/blob/main/README.md
[Jekyll]: https://jekyllrb.com
[GitHub Pages / Actions workflow]: https://github.blog/changelog/2022-07-27-github-pages-custom-github-actions-workflows-beta/
[use this template]: https://github.com/just-the-docs/just-the-docs-template/generate -->
