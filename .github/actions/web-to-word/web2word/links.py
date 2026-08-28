"""Link and anchor resolution.

This is the heart of the converter. When several web pages are merged into a
single Word document, three things have to happen to make links "just work":

1. Every element ``id`` must be made globally unique, because each page tends to
   reuse the same slugs (``#purpose`` appears on every page). We namespace them
   with a per-page prefix.

2. Every ``<a href>`` must be classified:
     - points at an anchor on an *in-scope* page  -> rewrite to an internal
       fragment (``#pageslug--purpose``) which Pandoc turns into a real Word
       bookmark hyperlink.
     - points anywhere else                        -> rewrite to the absolute
       live web URL so the link opens in a browser.

3. The many different URL spellings that resolve to the same page (relative,
   parent-relative, absolute-path, fully-qualified) must all normalize to one
   canonical key so matching against the scope set is reliable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urljoin, urldefrag, urlparse, urlunparse


def canonical(url: str) -> str:
    """Canonical key for a page URL, ignoring fragment and trivia.

    Lowercases the host, drops any fragment, strips a trailing ``index.html``
    and trailing slashes so that ``/docs/foo.html``, ``foo.html`` (once joined)
    and ``/docs/foo.html#x`` all collapse to the same key.
    """
    url, _frag = urldefrag(url)
    p = urlparse(url)
    path = p.path
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    path = path.rstrip("/")
    return urlunparse((p.scheme, p.netloc.lower(), path, "", "", ""))


@dataclass
class ScopeSet:
    """The set of pages included in this document, in reading order.

    Maps each page's canonical URL to the bookmark slug used to namespace its
    anchors and to serve as its "top of page" anchor.
    """

    _by_canonical: dict[str, str] = field(default_factory=dict)
    # When crawling a locally-served build (e.g. http://127.0.0.1:4000/...),
    # out-of-scope links must point at the PUBLIC site instead of localhost.
    # rewrite_from is the crawl origin, rewrite_to the public origin.
    rewrite_from: str | None = None
    rewrite_to: str | None = None

    def add(self, url: str, slug: str) -> None:
        self._by_canonical[canonical(url)] = slug

    def slug_for(self, url: str) -> str | None:
        return self._by_canonical.get(canonical(url))

    def __contains__(self, url: str) -> bool:
        return canonical(url) in self._by_canonical

    def externalize(self, url: str) -> str:
        """Rewrite a same-site (crawl-origin) URL to its public equivalent.
        Truly external URLs (a different origin) are returned unchanged."""
        if self.rewrite_from and self.rewrite_to and url.startswith(self.rewrite_from):
            return self.rewrite_to + url[len(self.rewrite_from):]
        return url


def namespace_anchor(slug: str, anchor: str) -> str:
    """Turn a page slug + local anchor id into a globally unique id."""
    return f"{slug}--{anchor}" if anchor else slug


@dataclass
class ResolvedLink:
    """Result of classifying one href."""

    href: str          # what the <a> should point to in the merged document
    internal: bool     # True -> Word bookmark, False -> external web hyperlink


def resolve_link(raw_href: str, *, page_url: str, page_slug: str, scope: ScopeSet) -> ResolvedLink | None:
    """Classify and rewrite a single href found on ``page_url``.

    Returns None for hrefs that should be left untouched (mailto:, tel:, empty).
    """
    href = (raw_href or "").strip()
    if not href:
        return None

    lower = href.lower()
    if lower.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None

    # Same-page fragment: always internal, always in scope (it's this page).
    if href.startswith("#"):
        anchor = href[1:]
        return ResolvedLink("#" + namespace_anchor(page_slug, anchor), internal=True)

    # Resolve to an absolute URL against this page's location.
    absolute = urljoin(page_url, href)
    _base, frag = urldefrag(absolute)

    target_slug = scope.slug_for(absolute)
    if target_slug is not None:
        # In-scope page -> internal bookmark. Fragment maps onto that page's
        # namespaced anchor; no fragment means link to the page's top.
        return ResolvedLink("#" + namespace_anchor(target_slug, frag), internal=True)

    # Out of scope -> point at the live web destination, rewriting a locally
    # served origin to the public site so the link works outside the build.
    return ResolvedLink(scope.externalize(absolute), internal=False)
