---
title: Maintain NBS 7
layout: page
nav_order: 4
has_children: true
has_toc: false
description: Operational guidance for maintaining your NBS 7 deployment after go-live.
---

# Maintain your NBS {{ site.version_latest }} environment

This section covers the operational tasks that keep your NBS 7 environment healthy after go-live. It is intended for system administrators who maintain the infrastructure, platform components, and supporting configuration for a running NBS 7 deployment.

> The procedures in this section reflect NBS {{ site.version_latest }}. For earlier releases, see **Previous Versions** in the sidebar.
{: .note }

## In this section

The maintenance section of this guide contains procedures for recurring maintenance work such as upgrades, infrastructure version changes, and operational configuration updates.

{% assign children = site.pages | where: "parent", page.title | sort: "nav_order" %}
<ul>
{% for child in children %}
  <li><a href="{{ child.url | relative_url }}"><strong>{{ child.title }}</strong></a>{% if child.description %}: {{ child.description }}{% endif %}</li>
{% endfor %}
</ul>

Additional maintenance procedures are added to this section as they are documented. If the procedure you need is not yet covered here, contact [nbs@cdc.gov](mailto:nbs@cdc.gov).
