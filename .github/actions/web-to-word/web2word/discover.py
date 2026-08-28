"""Auto-discover the pages of a chapter from a single starting URL.

Given a chapter landing page (e.g. .../docs/before-you-deploy.html), find every
sub-page that belongs to it so the caller doesn't have to list pages by hand.

Strategy: a chapter's pages live under the landing page's path prefix — the
landing page ``.../before-you-deploy.html`` owns everything under
``.../before-you-deploy/``. We breadth-first crawl content links, keeping only
pages under that prefix. BFS from the landing page yields a natural reading
order: the landing page first, then its children in the order it lists them,
then their children.
"""

from __future__ import annotations

import sys
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

from .extract import extract_content, fetch
from .links import canonical


def _child_prefix(start_url: str) -> str:
    """Path prefix (with trailing slash) that a chapter's sub-pages live under."""
    base = urldefrag(start_url)[0]
    if base.endswith(".html"):
        base = base[: -len(".html")]
    return base.rstrip("/") + "/"


def _under_prefix(url: str, prefix: str) -> bool:
    u, p = urlparse(canonical(url)), urlparse(canonical(prefix))
    return u.netloc == p.netloc and u.path.startswith(p.path.rstrip("/") + "/")


# Extensions that are assets, not content pages. A URL is treated as a page if
# it ends in .html/.htm or has no file extension (a clean/dir URL); anything with
# a different extension (images, PDFs, CSS, ...) must never become a "page".
def _is_page_url(url: str) -> bool:
    tail = urlparse(url).path.rsplit("/", 1)[-1]
    if "." not in tail:
        return True
    return tail.rsplit(".", 1)[-1].lower() in ("html", "htm")


def _nav_source(input_url: str, timeout: int) -> tuple[str | None, str | None]:
    """Return ``(url, raw_html)`` of a page that renders the sidebar nav, so a
    section's pages can be read from it. The nav is identical on every page, so
    when the entered ``<path>.html`` doesn't exist (a section whose landing has
    an arbitrary name, e.g. ``microservices-deployment`` ->
    ``.../deploy-nbs7-microservices.html``), fall back to the inside-directory
    landing and then the nearest fetchable ancestor page."""
    candidates = [input_url]
    stem = input_url[:-5] if input_url.endswith(".html") else input_url.rstrip("/")
    candidates.append(f"{stem}/{stem.rsplit('/', 1)[-1]}.html")  # inside-dir landing
    p = urlparse(input_url)
    segs = p.path.split("/")                                     # walk up ancestors
    for i in range(len(segs) - 2, 0, -1):
        anc = "/".join(segs[:i + 1])
        candidates.append(urlunparse((p.scheme, p.netloc, anc + ".html", "", "", "")))
        candidates.append(urlunparse((p.scheme, p.netloc, anc + "/", "", "", "")))
    for url in candidates:
        try:
            return url, fetch(url, timeout=timeout)
        except Exception:
            continue
    return None, None


def _nav_pages(raw_html: str, page_url: str, prefix: str, also: set[str]) -> list[str]:
    """Pages listed in the Just the Docs sidebar nav that belong to this section,
    in reading order (``nav_order``): everything under ``prefix`` plus any URL
    whose canonical form is in ``also`` (the section landing / entered page).
    The nav is the authoritative source of *which* pages a section contains — a
    landing doesn't always link to its children in content. [] if there's no nav."""
    nav = BeautifulSoup(raw_html, "lxml").select_one("nav#site-nav, nav.site-nav, #site-nav")
    if nav is None:
        return []
    ordered: list[str] = []
    seen: set[str] = set()
    for a in nav.find_all("a", href=True):
        full = urldefrag(urljoin(page_url, a["href"]))[0]
        c = canonical(full)
        if c in seen or not _is_page_url(full):
            continue
        if c in also or _under_prefix(full, prefix):
            seen.add(c)
            ordered.append(full)
    return ordered


def discover_pages(input_url: str, *, max_pages: int = 200, timeout: int = 30) -> list[str]:
    """Return the section's page URLs in the site's reading order.

    The section is everything under the entered path's directory prefix. Pages
    and their order come primarily from the Just the Docs sidebar nav (the site's
    real ``nav_order``); a breadth-first content crawl adds any content-linked
    page the nav omits. Unreachable links are skipped with a warning.
    """
    input_url = urldefrag(input_url)[0]
    prefix = _child_prefix(input_url)                     # the section directory
    also = {canonical(input_url)}                         # the entered page, if it's a page

    # The nav (from the entered page or a fetchable ancestor) is the source of
    # truth for which pages belong to the section and their reading order.
    nav_source_url, nav_raw = _nav_source(input_url, timeout)
    nav_urls = _nav_pages(nav_raw, nav_source_url, prefix, also) if nav_raw else []

    # Crawl the section (seeded from the nav pages) to add any content-linked
    # page the nav omits; fall back to the entered URL when there's no nav.
    found: dict[str, str] = {}
    seen = set(also) | {canonical(u) for u in nav_urls}
    queue = list(nav_urls) if nav_urls else [input_url]
    while queue and len(found) < max_pages:
        url = queue.pop(0)
        try:
            content = extract_content(fetch(url, timeout=timeout))
        except Exception as exc:
            print(f"  WARNING: skipping unreachable page {url} ({exc})", file=sys.stderr)
            continue
        found[canonical(url)] = url
        for a in content.find_all("a", href=True):
            target = urldefrag(urljoin(url, a["href"]))[0]
            key = canonical(target)
            if key in seen or not _under_prefix(target, prefix) or not _is_page_url(target):
                continue
            seen.add(key)
            queue.append(target)

    rank = {canonical(u): i for i, u in enumerate(nav_urls)}
    pages: dict[str, str] = dict(found)
    for u in nav_urls:
        pages.setdefault(canonical(u), u)                 # include nav-only pages

    base = input_url.rsplit("/", 1)[0] + "/"

    def sort_key(u: str):
        c = canonical(u)
        if c in rank:
            return (0, rank[c], "")
        rel = u[len(base):] if u.startswith(base) else u
        return (1, 0, rel)

    return sorted(pages.values(), key=sort_key)


def discover_all(start_url: str, *, max_pages: int = 500, timeout: int = 30) -> list[str]:
    """Every page in the whole guide, in reading order — for a full-guide export.

    The guide has no single parent page (its top level is several sibling
    chapters), but the sidebar nav lists every page in ``nav_order``. ``start_url``
    only needs to be any page that renders the nav (e.g. the site home)."""
    try:
        raw = fetch(start_url, timeout=timeout)
    except Exception:
        return []
    nav = BeautifulSoup(raw, "lxml").select_one("nav#site-nav, nav.site-nav, #site-nav")
    if nav is None:
        return []
    host = urlparse(start_url).netloc
    ordered: list[str] = []
    seen: set[str] = set()
    for a in nav.find_all("a", href=True):
        full = urldefrag(urljoin(start_url, a["href"]))[0]
        c = canonical(full)
        if c in seen or not _is_page_url(full) or urlparse(full).netloc != host:
            continue
        seen.add(c)
        ordered.append(full)
        if len(ordered) >= max_pages:
            break
    return ordered


def build_manifest(start_url: str, *, output: str = "review-document.docx",
                   style_reference: str = "styles.docx", whole_guide: bool = False,
                   **kw) -> dict:
    """Discover pages and return a manifest dict (base_url + relative pages).
    With ``whole_guide=True``, include the entire guide (every nav page)."""
    urls = discover_all(start_url, **kw) if whole_guide else discover_pages(start_url, **kw)
    base_url = start_url if start_url.endswith("/") else start_url.rsplit("/", 1)[0] + "/"
    pages = [u[len(base_url):] if u.startswith(base_url) else u for u in urls]
    return {
        "base_url": base_url,
        "output": output,
        "style_reference": style_reference,
        "pages": pages,
    }


def to_yaml(manifest: dict) -> str:
    lines = [
        f"base_url: {manifest['base_url']}",
        f"output: {manifest['output']}",
        f"style_reference: {manifest['style_reference']}",
        "pages:",
    ]
    lines += [f"  - {p}" for p in manifest["pages"]]
    return "\n".join(lines) + "\n"
