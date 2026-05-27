---
title: Glossary
layout: page
nav_order: 6
description: Reference list of acronyms and technical terms used throughout the guide.
published: false
---

# Glossary

This page is generated from `_data/glossary.yml` and defines the acronyms and technical terms used throughout the guide.

<!--
Contributor note:
- This page is generated from _data/glossary.yml. Do not hand-edit the rendered content below.
- If you need to change a definition or cross-link, update the YAML data file instead.
-->

{% assign glossary_entries = site.data.glossary | sort: 'term' -%}
{% assign letters = 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z' | split: ',' -%}
{% assign glossary_href_prefix = site.baseurl | append: '/docs/glossary.html#' -%}

{% for letter in letters -%}
{% assign has_entries = false -%}
{% for entry in glossary_entries -%}
{% assign entry_letter = entry.term | slice: 0, 1 | upcase -%}
{% if entry_letter == letter -%}
{% unless has_entries -%}
## {{ letter }}

---

<!-- markdownlint-disable-next-line MD051 -->
[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · Q · [R](#r) · [S](#s) · [T](#t) · U · [V](#v) · [W](#w) · X · Y · Z

---

{% assign has_entries = true -%}
<dl class="glossary-list">
{% endunless -%}
<dt id="{{ entry.term | slugify }}">{{ entry.term }}</dt>
<dd>{{ entry.definition | replace: '/NEDSS-SystemAdminGuide/docs/glossary.html#', glossary_href_prefix | markdownify }}</dd>
{% endif -%}
{% endfor -%}
{% if has_entries -%}
</dl>

{% endif -%}
{% endfor -%}
