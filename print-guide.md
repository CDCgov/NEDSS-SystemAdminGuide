---
layout: default
title: Print Entire Guide
nav_exclude: true
search_exclude: true
---

<div class="print-button-container">
  <button id="print-guide-trigger" class="btn btn-primary">Print / Save as PDF</button>
</div>

<p id="print-guide-status">Preparing printable pages...</p>
<div id="print-guide-content"></div>

{% comment %}
  Build a list of printable markdown pages:
  - root intro page (index.md)
  - docs markdown pages
  Exclude unpublished pages.
{% endcomment %}
{% assign intro_pages = site.pages | where_exp: "item", "item.path == 'index.md' and item.title != nil and item.title != '' and item.published != false" %}
{% assign doc_pages = site.pages | where_exp: "item", "item.path contains 'docs/' and item.path contains '.md' and item.title != nil and item.title != '' and item.published != false" | sort: "path" %}
{% assign print_pages = intro_pages | concat: doc_pages %}

<ul id="print-guide-sources" hidden>
{% for page in print_pages %}
  {% assign page_level = 1 %}
  {% if page.parent and page.grand_parent == nil %}
    {% assign page_level = 2 %}
  {% endif %}
  {% if page.grand_parent %}
    {% assign page_level = 3 %}
  {% endif %}
  {% assign page_kind = 'docs' %}
  {% if page.path == 'index.md' %}
    {% assign page_kind = 'intro' %}
  {% endif %}
  <li data-kind="{{ page_kind }}" data-published="{{ page.published | default: true }}" data-has-children="{{ page.has_children | default: false }}" data-level="{{ page_level }}" data-title="{{ page.title | escape }}" data-url="{{ page.url | relative_url }}"></li>
{% endfor %}
</ul>
