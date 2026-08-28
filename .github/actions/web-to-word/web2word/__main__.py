"""CLI: python -m web2word manifest.yml"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .build import Manifest, build


def _load_manifest(path: str) -> Manifest:
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
    except ModuleNotFoundError:
        data = _mini_yaml(text)
    return Manifest(
        base_url=data["base_url"],
        pages=data["pages"],
        output=data.get("output", "output.docx"),
        style_reference=data.get("style_reference"),
        local_dir=data.get("local_dir"),
    )


def _mini_yaml(text: str) -> dict:
    """Tiny YAML subset parser so the tool runs with zero extra deps.

    Supports: `key: value` scalars and a `pages:` block of `- item` lines.
    """
    data: dict = {}
    pages: list[str] = []
    in_pages = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if in_pages and line.lstrip().startswith("- "):
            pages.append(line.split("- ", 1)[1].strip())
            continue
        in_pages = False
        if ":" in line:
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            if key == "pages" and not val:
                in_pages = True
                data["pages"] = pages
            else:
                data[key] = val
    return data


def _manifest_from_url(url: str, verbose: bool, whole_guide: bool = False) -> Manifest:
    from .discover import build_manifest as discover_manifest
    if verbose:
        print(f"discovering {'the whole guide from' if whole_guide else 'pages under'} {url} ...")
    data = discover_manifest(url, whole_guide=whole_guide)
    return Manifest(
        base_url=data["base_url"],
        pages=data["pages"],
        output=data["output"],
        style_reference=data["style_reference"],
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="web2word", description=__doc__)
    ap.add_argument("source", help="a manifest .yml file, OR a chapter URL to auto-discover")
    ap.add_argument("-o", "--output", help="override output path")
    ap.add_argument("--style-reference", metavar="PATH",
                    help="reference .docx that controls fonts/styles (overrides the manifest)")
    ap.add_argument("--public-host", metavar="ORIGIN",
                    help="public origin (e.g. https://example.github.io) to rewrite "
                         "out-of-scope links to when crawling a local build (localhost)")
    ap.add_argument("--whole-guide", action="store_true",
                    help="export the entire guide (every page in the site nav); SOURCE is "
                         "any page that renders the nav, e.g. the site home URL")
    ap.add_argument("--save-manifest", metavar="PATH",
                    help="when SOURCE is a URL, also write the discovered manifest here")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    is_url = args.source.lower().startswith(("http://", "https://"))
    manifest = (_manifest_from_url(args.source, args.verbose, args.whole_guide)
                if is_url else _load_manifest(args.source))
    if args.output:
        manifest.output = args.output
    if args.style_reference:
        manifest.style_reference = args.style_reference
    if args.public_host:
        manifest.public_host = args.public_host

    if is_url and args.save_manifest:
        from .discover import to_yaml
        Path(args.save_manifest).write_text(to_yaml({
            "base_url": manifest.base_url, "output": manifest.output,
            "style_reference": manifest.style_reference or "styles.docx",
            "pages": manifest.pages,
        }), encoding="utf-8")
        print(f"wrote manifest: {args.save_manifest}")

    print(f"web2word: {len(manifest.pages)} page(s) -> {manifest.output}")
    out = build(manifest, verbose=args.verbose)
    print(f"done: {out.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
