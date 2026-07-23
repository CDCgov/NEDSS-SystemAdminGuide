---
title: NBS 7 full deployment
layout: page
parent: Deploy NBS 7
nav_order: 2
has_children: true
description: Complete step-by-step instructions for deploying NBS 7, from prerequisites through post-deployment cleanup.
---

# Deploy the full NBS {{ site.version_latest }} environment

This section walks you through the NBS 7 deployment process in full detail, from prerequisites and infrastructure setup through microservices deployment and cleanup. If you are familiar with deploying NBS 7, or with your cloud provider, Terraform, Kubernetes, and Helm, you can use the [Quick start](quickstart.html) instead. Both paths create the same infrastructure and services.

> Some of the steps in this section depend on previous steps. Complete each page in this section, including any nested subpages, in order.
{: .important }

## In this section

<!-- markdownlint-disable MD055 MD056 -->
{% assign children = site.pages | where: "parent", page.title | sort: "nav_order" %}
<ol>
{% for child in children %}
  <li><a href="{{ child.url | relative_url }}"><strong>{{ child.title }}</strong></a>{% if child.description %}: {{ child.description }}{% endif %}</li>
{% endfor %}
</ol>
