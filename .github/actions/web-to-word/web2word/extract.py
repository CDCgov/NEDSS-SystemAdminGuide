"""Fetch a page and isolate its real content from the site chrome."""

from __future__ import annotations

import urllib.request

from bs4 import BeautifulSoup

# Content container selectors, most-specific first. Just the Docs (the theme the
# NBS 7 guide uses) puts body content in #main-content; the others are sensible
# fallbacks for other Jekyll themes.
CONTENT_SELECTORS = [
    "#main-content",
    "main.main-content",
    "article.post-content",
    "main",
    "article",
]

# Elements that are navigation/chrome even when they live inside the content
# container (breadcrumbs, "edit this page", auto-generated child-page lists that
# a theme appends, etc.). Tuned conservatively.
CHROME_SELECTORS = [
    "nav",
    ".breadcrumb-nav",
    ".aux-nav",
    ".site-footer",
    "footer",             # Just the Docs nests a mobile footer (the "This site
                          # uses Just the Docs..." tagline) inside #main-content
    "button",
    "a.anchor-heading",   # Just the Docs decorative heading-link icon
    "svg.anchor-heading-icon",
    ".anchor-heading",
]

# Just the Docs callout types -> (Word paragraph style, injected label). The
# label is CSS-generated on the site (not in the HTML), so we add it back so the
# Word callout is as recognizable as the rendered page. `highlight` has no label
# by design. Styles are defined in the styled reference doc.
CALLOUT_TYPES = {
    "note": ("Note", "Note"),
    "important": ("Important", "Important"),
    "warning": ("Warning", "Warning"),
    "new": ("New", "New"),
    "highlight": ("Highlight", None),
}
# `-title` variants are blockquotes whose first paragraph is a custom label; they
# reuse the base type's box style.
CALLOUT_TITLE_VARIANTS = {
    "note-title": "Note",
    "important-title": "Important",
    "warning-title": "Warning",
    "new-title": "New",
}


def fetch(url: str, *, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "web2word/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def read_local(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def _strip_child_page_toc(container) -> None:
    """Remove Jekyll's auto-generated end-of-page "Table of contents".

    On Just the Docs parent pages this is a ``<hr>`` + ``<h2 class="text-delta">
    Table of contents</h2>`` + a ``<ul>`` list of child pages. It is generated
    navigation, not authored content, and the user does not want it.

    The in-page "On this page" TOC uses the same ``text-delta`` class but a
    different heading text (and an ``id="markdown-toc"`` list), so matching on
    the heading text keeps it untouched.
    """
    for h in container.find_all(["h1", "h2", "h3", "h4"]):
        if h.get_text(strip=True).lower() != "table of contents":
            continue
        # Remove the list that follows the heading, then the heading, then a
        # trailing/leading <hr> that framed the section.
        nxt = h.find_next_sibling()
        prev = h.find_previous_sibling()
        if nxt is not None and nxt.name in ("ul", "ol"):
            nxt.decompose()
        if prev is not None and prev.name == "hr":
            prev.decompose()
        h.decompose()


def _map_callouts(container) -> None:
    """Wrap Just the Docs callouts so Pandoc styles them as boxed admonitions.

    Callouts are authored as ``<p class="note">`` (base) or
    ``<blockquote class="note-title">`` (custom-title variant). Pandoc's AST
    drops classes on plain paragraphs, and ``custom-style`` only takes effect on
    a ``<div>``, so we wrap each callout in a ``<div custom-style="Note">`` that
    maps to a boxed/shaded paragraph style in the reference doc.

    Selection is restricted to ``p``/``blockquote`` on purpose: Rouge wraps code
    blocks in ``<div class="highlight">``, which must NOT be treated as a
    highlight callout. Authored text is preserved verbatim; the only added text
    is the type label (e.g. "Note:"), which the site shows via CSS.
    """
    from bs4 import BeautifulSoup as _BS
    dummy = _BS("", "lxml")

    def _bold_inline(el):
        strong = dummy.new_tag("strong")
        for child in list(el.contents):
            strong.append(child.extract())
        el.append(strong)

    def _first_p(el):
        return el.find("p", recursive=False) if el.name == "blockquote" else el

    def _make_callout(el, style, *, label=None, title=False):
        """Wrap a callout element in <div custom-style=...>. A <blockquote> is
        UNWRAPPED (its blocks moved into the div) so Pandoc applies the paragraph
        style to each paragraph directly instead of treating it as a quote."""
        wrapper = dummy.new_tag("div")
        wrapper["custom-style"] = style
        el.insert_before(wrapper)

        head = _first_p(el)
        if label and head is not None:
            lab = dummy.new_tag("strong")
            lab.string = f"{label}: "
            head.insert(0, lab)
        if title and head is not None:
            _bold_inline(head)

        if el.name == "blockquote":
            for child in list(el.children):   # move ALL nodes (preserve content)
                wrapper.append(child.extract())
            el.decompose()
        else:
            wrapper.append(el.extract())

    # Title variants first (their first paragraph is a custom label to bold).
    for cls, style in CALLOUT_TITLE_VARIANTS.items():
        for el in container.select(f"p.{cls}, blockquote.{cls}"):
            _make_callout(el, style, title=True)

    # Base types: prepend a bold type label (except highlight, which has none).
    for cls, (style, label) in CALLOUT_TYPES.items():
        for el in container.select(f"p.{cls}, blockquote.{cls}"):
            _make_callout(el, style, label=label)


# Just the Docs badge color class -> reference-doc character style. A plain
# `.label` with no color class falls back to gray.
_BADGE_STYLES = {
    "label-green": "BadgeGreen",
    "label-yellow": "BadgeYellow",
    "label-red": "BadgeRed",
    "label-purple": "BadgePurple",
    "label-blue": "BadgeBlue",
}


def _map_inline_ui(container) -> None:
    """Style two Just the Docs UI elements for the Word doc:

    - Tooltips (`<span class="glossary-term">…<button …>term</button>…</span>`):
      replaced with the term text in a distinct "defined-term" style. The tooltip
      can't function in a docx, but the styling signals that the term has an
      in-place definition.
    - Badges (`<p class="label label-green">…</p>`): the text is shaded with the
      matching label color (gray when no color class is given).
    """
    from bs4 import BeautifulSoup as _BS
    dummy = _BS("", "lxml")

    def _restyle(el, style, *, source=None, replace=False):
        wrapper = dummy.new_tag("span")
        wrapper["custom-style"] = style
        for child in list((source or el).contents):
            wrapper.append(child.extract())
        if replace:
            el.replace_with(wrapper)
        else:
            el.append(wrapper)

    for term in container.select("span.glossary-term"):
        trigger = term.select_one(".glossary-term__trigger")
        _restyle(term, "GlossaryTerm", source=trigger or term, replace=True)

    for badge in container.select("p.label, span.label, div.label"):
        classes = badge.get("class", [])
        style = next((_BADGE_STYLES[c] for c in classes if c in _BADGE_STYLES), "BadgeGray")
        _restyle(badge, style)


def extract_content(html: str) -> BeautifulSoup:
    """Return a soup containing just the main content region, chrome removed."""
    soup = BeautifulSoup(html, "lxml")

    container = None
    for sel in CONTENT_SELECTORS:
        container = soup.select_one(sel)
        if container is not None:
            break
    if container is None:
        container = soup.body or soup

    # Map tooltips/badges BEFORE chrome removal: the tooltip term lives inside a
    # <button>, which the chrome pass strips — so capture it first.
    _map_inline_ui(container)

    for sel in CHROME_SELECTORS:
        for el in container.select(sel):
            el.decompose()

    _strip_child_page_toc(container)
    _map_callouts(container)

    # Flatten HTML5 sectioning wrappers. Pandoc's HTML reader treats <main>,
    # <section>, etc. specially and, when they wrap our per-page anchor div, it
    # discards that div's id (and with it the page's "top" bookmark). Unwrapping
    # keeps their children while removing the element itself.
    for tag_name in ("main", "section", "article"):
        for el in container.find_all(tag_name):
            el.unwrap()

    return BeautifulSoup(container.decode(), "lxml")
