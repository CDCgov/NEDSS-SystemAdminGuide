---
title: NBS 7 full deployment
layout: page
parent: Deploy NBS 7
nav_order: 2
has_children: true
has_toc: false
description: Complete step-by-step instructions for deploying NBS 7, from prerequisites through post-deployment cleanup.
---

# Deploy the full NBS {{ site.version_latest }} environment

This section walks you through the {% include term-tooltip.html key="nbs-7" term="NBS 7" id="fulldeploy-nbs-7" %} deployment process in full detail, from prerequisites and infrastructure setup through microservices deployment and cleanup. If you are familiar with deploying NBS 7, or with your cloud provider, {% include term-tooltip.html key="terraform" term="Terraform" id="fulldeploy-terraform" %}, {% include term-tooltip.html key="kubernetes" term="Kubernetes" id="fulldeploy-kubernetes" %}, and {% include term-tooltip.html key="helm" term="Helm" id="fulldeploy-helm" %}, you can use the [Quick start](quickstart.html) instead. Both paths create the same infrastructure and services.

## In this section

Complete the following pages in order, including any nested subpages. Each phase builds on the infrastructure and configuration from the phase before it:

<!-- markdownlint-disable MD055 MD056 -->
{% assign children = site.pages | where: "parent", page.title | sort: "nav_order" %}
<ol>
{% for child in children %}
  <li><a href="{{ child.url | relative_url }}"><strong>{{ child.title }}</strong></a>{% if child.description %}: {{ child.description }}{% endif %}</li>
{% endfor %}
</ol>
