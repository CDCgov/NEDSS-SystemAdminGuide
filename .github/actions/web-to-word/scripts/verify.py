"""Verify a generated .docx: report link/bookmark counts and dead internal links.

    python scripts/verify.py path/to/output.docx

A "dead" internal link is a hyperlink whose w:anchor has no matching bookmark —
i.e. a click that would go nowhere in Word. A clean document reports 0.
"""

from __future__ import annotations

import re
import sys
import zipfile


def verify(path: str) -> int:
    z = zipfile.ZipFile(path)
    doc = z.read("word/document.xml").decode("utf-8")
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")

    bookmarks = set(re.findall(r'<w:bookmarkStart[^>]*w:name="([^"]+)"', doc))
    anchors = re.findall(r'<w:hyperlink[^>]*w:anchor="([^"]+)"', doc)
    external = re.findall(r'Target="([^"]+)"[^>]*TargetMode="External"', rels)
    dead = sorted({a for a in anchors if a not in bookmarks})

    print(f"bookmarks:           {len(bookmarks)}")
    print(f"internal link jumps: {len(anchors)}")
    print(f"external web links:  {len(external)}")
    print(f"dead internal links: {len(dead)}")
    for d in dead:
        print(f"  DEAD -> #{d}")

    return 1 if dead else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(verify(sys.argv[1]))
