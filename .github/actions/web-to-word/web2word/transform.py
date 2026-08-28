"""Apply namespacing and link resolution to a single page's content soup."""

from __future__ import annotations

from bs4 import BeautifulSoup, Tag

from .links import ScopeSet, namespace_anchor, resolve_link

# Tags whose id Pandoc reliably turns into a Word bookmark. For an id on any
# OTHER element (dt, dd, li, td, p, ...), Pandoc drops the bookmark, so links to
# it die — e.g. every glossary <dt id="kubernetes"> anchor. The fix is to move
# such ids onto a prepended invisible anchor span, which Pandoc does keep.
_BOOKMARKABLE_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "div", "span", "a", "table"}

# List/table container tags. Their ids are structural and auto-generated (e.g.
# the "On this page" list's markdown-toc id) — not authored link targets, so we
# leave them alone. Anchoring them isn't needed (the section heading carries the
# anchor) and prepending into one creates a phantom item, e.g. an empty "1."
# above an "On this page" list.
_CONTAINER_TAGS = {"ol", "ul", "dl", "table", "thead", "tbody", "tfoot", "tr", "colgroup"}


def transform_page(soup: BeautifulSoup, *, page_url: str, page_slug: str, scope: ScopeSet) -> BeautifulSoup:
    """Namespace every id and rewrite every href in place. Returns the soup."""

    # 1. Namespace every element id so anchors are globally unique after merge.
    for el in soup.find_all(attrs={"id": True}):
        el["id"] = namespace_anchor(page_slug, el["id"])

    # 1b. Preserve anchors Pandoc would otherwise drop: move the id from a
    #     non-bookmarkable element onto a prepended zero-width-space anchor span.
    for el in soup.find_all(attrs={"id": True}):
        if el.name in _BOOKMARKABLE_TAGS or el.name in _CONTAINER_TAGS:
            continue
        anchor = soup.new_tag("span")
        anchor["id"] = el["id"]
        anchor.string = "\u200b"  # zero-width space: invisible but non-empty
        del el["id"]
        el.insert(0, anchor)

    # 2. Wrap the whole page in a div carrying the page slug as its id. Pandoc
    #    turns a div-with-id into a bookmark spanning the content, giving every
    #    "link to top of this page" (fragment-less in-scope link) a real target.
    #    An empty <span id> does NOT survive Pandoc, so a wrapper is required.
    body = soup.body or soup
    wrapper = soup.new_tag("div", id=page_slug)
    for child in list(body.contents):
        wrapper.append(child.extract())
    body.append(wrapper)

    # 3. Collect the ids that actually exist on this page (namespaced), so we can
    #    detect same-page links that point at anchors we stripped as chrome
    #    (e.g. Just the Docs' "Back to top" -> #top, which lives on the outer
    #    page frame, not in #main-content).
    present_ids = {el["id"] for el in wrapper.find_all(attrs={"id": True})}
    present_ids.add(page_slug)
    self_prefix = page_slug + "--"

    # 3b. Resolve image sources to absolute URLs so Pandoc can fetch and embed
    #     them (relative src like "images/foo.png" is otherwise unresolvable).
    from urllib.parse import urljoin
    for img in soup.find_all("img", src=True):
        img["src"] = urljoin(page_url, img["src"])
        img.attrs.pop("srcset", None)  # avoid relative candidates in srcset

    # 4. Rewrite every link.
    for a in soup.find_all("a", href=True):
        resolved = resolve_link(a["href"], page_url=page_url, page_slug=page_slug, scope=scope)
        if resolved is None:
            continue
        href = resolved.href
        # Same-page internal target that doesn't exist -> fall back to page top,
        # so a dangling in-page anchor still lands somewhere sensible instead of
        # becoming a dead bookmark.
        if resolved.internal and href.startswith("#"):
            target = href[1:]
            is_this_page = target == page_slug or target.startswith(self_prefix)
            if is_this_page and target not in present_ids:
                href = "#" + page_slug
        a["href"] = href

    return soup


def merge(pages: list[BeautifulSoup]) -> str:
    """Concatenate transformed page bodies into one HTML string for Pandoc."""
    parts = []
    for soup in pages:
        body = soup.body or soup
        parts.append(body.decode_contents() if isinstance(body, Tag) else str(body))
    return "\n<div class=\"page-break\"></div>\n".join(parts)
