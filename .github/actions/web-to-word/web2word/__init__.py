"""web2word: convert a set of published web pages into one Word document
with working internal (bookmark) and external (web) links."""

from .build import Manifest, build

__all__ = ["Manifest", "build"]
