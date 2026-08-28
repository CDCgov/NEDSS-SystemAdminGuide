"""Generate a Pandoc reference.docx styled to resemble the Just the Docs site.

Starts from Pandoc's built-in reference document and patches:
  - the theme fonts (major/minor) to a system sans-serif (Segoe UI), matching
    the site's `system-ui` stack;
  - heading color to near-black (#1A1A1A), matching the site headings;
  - the Hyperlink character style to CDC blue (#005DAA) with an underline,
    matching `.main-content a` on the site.

Code stays Consolas (Pandoc's default VerbatimChar), which matches the site's
`SFMono-Regular, Menlo, Consolas` monospace stack closely enough.

Usage:  python scripts/make_reference.py styles.docx

"Similar, not exact" is the goal — these are print-friendly approximations, not
a pixel match. Content is never touched; this only defines styles.
"""

from __future__ import annotations

import io
import re
import subprocess
import sys
import zipfile

BODY_FONT = "Segoe UI"          # Word's closest ubiquitous match for system-ui
BODY_SIZE = "22"                # half-points -> 11pt body text
HEADING_COLOR = "1A1A1A"        # site h1 color
LINK_COLOR = "005DAA"           # site .main-content a color (CDC blue)

# NOTE: patches match by STRUCTURE (which style, which element), never by the
# specific default font/color values, because those differ across Pandoc
# versions. build_reference() then VERIFIES the result and fails loudly if any
# patch didn't take — a silent no-op previously shipped an unstyled document.

TABLE_BORDER_COLOR = "B3B3B3"   # mid-gray cell borders
TABLE_HEADER_FILL = "F0F0F0"    # light gray header row shading

# Callout palette: (background tint, left-bar accent), taken from the site's own
# callout colors (see contributing/styles.md). Boxes get a thin gray border on
# three sides and a thick colored accent bar on the left, plus the tint fill.
CALLOUTS = {
    "Note":      ("E6EFF7", "2474B6"),  # blue
    "Important": ("FBEDD6", "ECB046"),  # yellow
    "Warning":   ("F8E4EB", "CB3E6E"),  # red
    "New":       ("EAF5DC", "9ACC54"),  # green
    "Highlight": ("F1E9EE", "A1518B"),  # purple (no label)
}

# Just the Docs badge/label colors (see the site's .label-* classes), as
# character styles that shade just the badge text. (fill, text color). An
# undefined color (plain .label) falls back to gray.
BADGES = {
    "BadgeGray":   ("D9D9D9", "1A1A1A"),
    "BadgeGreen":  ("9ACC54", "1A1A1A"),
    "BadgeYellow": ("F1C577", "44434D"),
    "BadgeRed":    ("CB3E6E", "FFFFFF"),
    "BadgePurple": ("D7B7CE", "1A1A1A"),
    "BadgeBlue":   ("2C7BB6", "FFFFFF"),
}
# Color for the "defined-term" (tooltip) character style — distinct from body
# text and from hyperlinks (which are solid-underlined CDC blue) via a dotted
# underline, so reviewers can see which terms carry an in-place definition.
GLOSSARY_TERM_COLOR = "0B6E6E"  # teal


def _default_reference() -> bytes:
    return subprocess.run(
        ["pandoc", "--print-default-data-file", "reference.docx"],
        check=True, capture_output=True,
    ).stdout


def _patch_theme(xml: str) -> str:
    """Set the major (heading) and minor (body) Latin typefaces to BODY_FONT,
    whatever the default happens to be (Aptos, Calibri, etc.)."""
    xml, n_major = re.subn(
        r'(<a:majorFont>\s*<a:latin\s+typeface=")[^"]*(")',
        rf"\g<1>{BODY_FONT}\g<2>", xml, count=1)
    xml, n_minor = re.subn(
        r'(<a:minorFont>\s*<a:latin\s+typeface=")[^"]*(")',
        rf"\g<1>{BODY_FONT}\g<2>", xml, count=1)
    if not (n_major and n_minor):
        raise SystemExit(
            f"make_reference: could not set theme fonts "
            f"(major matched={n_major}, minor matched={n_minor}); "
            f"the Pandoc reference theme structure changed.")
    return xml


def _set_or_insert(block: str, element_re: str, replacement: str, insert_after: str) -> str:
    """Replace the first match of element_re in block, or insert `replacement`
    right after the first `insert_after` if the element is absent."""
    if re.search(element_re, block):
        return re.sub(element_re, replacement, block, count=1)
    return re.sub(re.escape(insert_after), insert_after + replacement, block, count=1)


def _patch_body_size(xml: str) -> str:
    """Set the document-default font size (body text inherits it). Headings and
    code override their own size, so only body/callout text is affected."""
    def repl(m: re.Match) -> str:
        block = m.group(0)
        block = re.sub(r'<w:sz w:val="\d+"\s*/>', f'<w:sz w:val="{BODY_SIZE}" />', block)
        block = re.sub(r'<w:szCs w:val="\d+"\s*/>', f'<w:szCs w:val="{BODY_SIZE}" />', block)
        return block
    xml, n = re.subn(r"<w:rPrDefault>.*?</w:rPrDefault>", repl, xml, flags=re.S)
    if not n:
        raise SystemExit("make_reference: docDefaults rPrDefault not found for body size.")
    return xml


def _patch_heading_colors(xml: str) -> str:
    """Force every Heading1..9 paragraph style to HEADING_COLOR."""
    def repl(m: re.Match) -> str:
        return _set_or_insert(
            m.group(0), r"<w:color\b[^>]*/>",
            f'<w:color w:val="{HEADING_COLOR}" />', "<w:rPr>")
    xml, n = re.subn(
        r'<w:style w:type="paragraph"[^>]*w:styleId="Heading[1-9]"[^>]*>.*?</w:style>',
        repl, xml, flags=re.S)
    if not n:
        raise SystemExit("make_reference: no Heading1..9 styles found to recolor.")
    return xml


def _patch_hyperlink(xml: str) -> str:
    """Recolor the Hyperlink character style and add an underline."""
    def repl(m: re.Match) -> str:
        block = m.group(0)
        if "<w:rPr>" not in block:
            return block.replace(
                "</w:style>",
                f'<w:rPr><w:color w:val="{LINK_COLOR}" /><w:u w:val="single" /></w:rPr></w:style>')
        block = _set_or_insert(
            block, r"<w:color\b[^>]*/>",
            f'<w:color w:val="{LINK_COLOR}" />', "<w:rPr>")
        if "<w:u " not in block:
            block = block.replace("<w:rPr>", '<w:rPr><w:u w:val="single" />', 1)
        return block
    xml, n = re.subn(
        r'<w:style w:type="character"[^>]*w:styleId="Hyperlink"[^>]*>.*?</w:style>',
        repl, xml, flags=re.S)
    if not n:
        raise SystemExit("make_reference: Hyperlink style not found.")
    return xml


def _patch_heading_spacing(xml: str) -> str:
    """Widen the space above H2/H3 (cosmetic; best-effort, not asserted)."""
    def repl(m: re.Match) -> str:
        block = m.group(0)
        def sp(mm: re.Match) -> str:
            s = mm.group(0)
            if "w:before=" in s:
                return re.sub(r'w:before="\d+"', 'w:before="340"', s)
            return s.replace("<w:spacing", '<w:spacing w:before="340"')
        if re.search(r"<w:spacing\b[^>]*/>", block):
            return re.sub(r"<w:spacing\b[^>]*/>", sp, block, count=1)
        return re.sub(r"(<w:pPr>)", r'\g<1><w:spacing w:before="340" w:after="100" />',
                      block, count=1)
    return re.sub(
        r'<w:style w:type="paragraph"[^>]*w:styleId="Heading[23]"[^>]*>.*?</w:style>',
        repl, xml, flags=re.S)


def _callout_style(style_id: str, fill: str, bar: str) -> str:
    gray = "D6DEE6"
    return (
        f'<w:style w:type="paragraph" w:customStyle="1" w:styleId="{style_id}">'
        f'<w:name w:val="{style_id}" /><w:basedOn w:val="BodyText" /><w:qFormat />'
        f'<w:pPr>'
        f'<w:pBdr>'
        f'<w:top w:val="single" w:sz="4" w:space="6" w:color="{gray}" />'
        f'<w:left w:val="single" w:sz="24" w:space="8" w:color="{bar}" />'
        f'<w:bottom w:val="single" w:sz="4" w:space="6" w:color="{gray}" />'
        f'<w:right w:val="single" w:sz="4" w:space="6" w:color="{gray}" />'
        f'</w:pBdr>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}" />'
        f'<w:spacing w:before="120" w:after="120" />'
        f'<w:ind w:left="187" w:right="120" />'
        f'</w:pPr>'
        f'</w:style>'
    )


def _sourcecode_style() -> str:
    """Paragraph style for fenced code blocks: light gray box + Consolas.

    Pandoc emits one SourceCode-styled paragraph per code line; identical borders
    on adjacent paragraphs merge into a single box in Word.
    """
    gray = "D0D7DE"
    return (
        '<w:style w:type="paragraph" w:customStyle="1" w:styleId="SourceCode">'
        '<w:name w:val="Source Code" /><w:basedOn w:val="Normal" /><w:qFormat />'
        '<w:pPr>'
        '<w:pBdr>'
        f'<w:top w:val="single" w:sz="4" w:space="4" w:color="{gray}" />'
        f'<w:left w:val="single" w:sz="4" w:space="8" w:color="{gray}" />'
        f'<w:bottom w:val="single" w:sz="4" w:space="4" w:color="{gray}" />'
        f'<w:right w:val="single" w:sz="4" w:space="8" w:color="{gray}" />'
        '</w:pBdr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="F6F8FA" />'
        '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto" />'
        '<w:ind w:left="120" w:right="120" />'
        '</w:pPr>'
        '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" /><w:sz w:val="18" /></w:rPr>'
        '</w:style>'
    )


def _badge_style(style_id: str, fill: str, text: str) -> str:
    return (
        f'<w:style w:type="character" w:customStyle="1" w:styleId="{style_id}">'
        f'<w:name w:val="{style_id}" /><w:qFormat />'
        f'<w:rPr><w:shd w:val="clear" w:color="auto" w:fill="{fill}" />'
        f'<w:color w:val="{text}" /></w:rPr>'
        f'</w:style>'
    )


def _glossary_term_style() -> str:
    # A defined term (tooltip): teal text + dotted underline, so it's clearly
    # distinct from body text and from solid-underlined hyperlinks.
    return (
        '<w:style w:type="character" w:customStyle="1" w:styleId="GlossaryTerm">'
        '<w:name w:val="GlossaryTerm" /><w:qFormat />'
        f'<w:rPr><w:color w:val="{GLOSSARY_TERM_COLOR}" />'
        '<w:u w:val="dotted" /></w:rPr>'
        '</w:style>'
    )


def _patch_styles(xml: str) -> str:
    xml = _patch_body_size(xml)           # 11pt body text
    xml = _patch_heading_colors(xml)      # near-black headings
    xml = _patch_hyperlink(xml)           # CDC-blue underlined links
    xml = _patch_heading_spacing(xml)     # more space above H2/H3

    # Code font size. Pandoc styles code runs (both inline and block) with the
    # VerbatimChar character style, whose run props OVERRIDE the SourceCode
    # paragraph style, so the size must be set HERE to take effect. 18 = 9pt.
    def _patch_verbatim(m: re.Match) -> str:
        return _set_or_insert(
            m.group(0), r"<w:sz\b[^>]*/>", '<w:sz w:val="18" />', "<w:rPr>")

    xml = re.sub(
        r'<w:style [^>]*w:styleId="VerbatimChar".*?</w:style>',
        _patch_verbatim, xml, flags=re.S,
    )

    # Table: borders on every cell + a shaded header row.
    borders = (
        '<w:tblBorders>'
        f'<w:top w:val="single" w:sz="4" w:color="{TABLE_BORDER_COLOR}" />'
        f'<w:left w:val="single" w:sz="4" w:color="{TABLE_BORDER_COLOR}" />'
        f'<w:bottom w:val="single" w:sz="4" w:color="{TABLE_BORDER_COLOR}" />'
        f'<w:right w:val="single" w:sz="4" w:color="{TABLE_BORDER_COLOR}" />'
        f'<w:insideH w:val="single" w:sz="4" w:color="{TABLE_BORDER_COLOR}" />'
        f'<w:insideV w:val="single" w:sz="4" w:color="{TABLE_BORDER_COLOR}" />'
        '</w:tblBorders>'
    )

    def _patch_table(m: re.Match) -> str:
        block = m.group(0)
        if "<w:tblBorders>" not in block:
            block = block.replace("<w:tblPr>", "<w:tblPr>" + borders, 1)
        # Shade + embolden the header row.
        header_props = (
            f'<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{TABLE_HEADER_FILL}" />'
            '<w:tcBorders><w:bottom w:val="single" w:sz="8" '
            f'w:color="{TABLE_BORDER_COLOR}" /></w:tcBorders>'
            '<w:vAlign w:val="bottom" /></w:tcPr>'
        )
        block = re.sub(r'<w:tcPr>.*?</w:tcPr>', header_props, block, count=1, flags=re.S)
        # Add bold run props to the first-row style def if not present.
        block = block.replace(
            '<w:tblStylePr w:type="firstRow">',
            '<w:tblStylePr w:type="firstRow"><w:rPr><w:b /></w:rPr>',
        )
        return block

    xml = re.sub(
        r'<w:style w:type="table"[^>]*w:styleId="Table".*?</w:style>',
        _patch_table, xml, flags=re.S,
    )

    # Inject callout + code-block paragraph styles and badge/term character
    # styles before the closing tag.
    extra_xml = (
        "".join(_callout_style(sid, fill, bar) for sid, (fill, bar) in CALLOUTS.items())
        + _sourcecode_style()
        + "".join(_badge_style(sid, fill, text) for sid, (fill, text) in BADGES.items())
        + _glossary_term_style()
    )
    xml = xml.replace("</w:styles>", extra_xml + "</w:styles>")
    return xml


def _verify(theme_xml: str, styles_xml: str) -> None:
    """Fail loudly if any expected styling is missing from the patched XML.

    A silent patch no-op (e.g. from a Pandoc version whose reference differs)
    previously shipped an unstyled document; this turns that into a hard error.
    """
    problems = []
    if f'typeface="{BODY_FONT}"' not in theme_xml:
        problems.append(f"body/heading font '{BODY_FONT}' not set in theme")
    if f'<w:sz w:val="{BODY_SIZE}" />' not in styles_xml:
        problems.append(f"body size {BODY_SIZE} half-pt not applied")
    if f'<w:color w:val="{HEADING_COLOR}" />' not in styles_xml:
        problems.append(f"heading color #{HEADING_COLOR} not applied")
    if f'<w:color w:val="{LINK_COLOR}" />' not in styles_xml:
        problems.append(f"hyperlink color #{LINK_COLOR} not applied")
    if "<w:u " not in styles_xml:
        problems.append("hyperlink underline not applied")
    for sid in (*CALLOUTS, "SourceCode", *BADGES, "GlossaryTerm"):
        if f'w:styleId="{sid}"' not in styles_xml:
            problems.append(f"style '{sid}' missing")
    if "<w:tblBorders>" not in styles_xml:
        problems.append("table cell borders not applied")
    if problems:
        raise SystemExit(
            "make_reference: reference document is not styled correctly:\n  - "
            + "\n  - ".join(problems)
            + "\n(likely a Pandoc version whose reference.docx differs from the "
              "one this script targets — pin Pandoc or update the patcher.)")


def build_reference(out_path: str) -> str:
    src = _default_reference()
    zin = zipfile.ZipFile(io.BytesIO(src))

    theme_xml = styles_xml = None
    patched: dict[str, bytes] = {}
    for name in zin.namelist():
        data = zin.read(name)
        if name == "word/theme/theme1.xml":
            theme_xml = _patch_theme(data.decode("utf-8"))
            data = theme_xml.encode("utf-8")
        elif name == "word/styles.xml":
            styles_xml = _patch_styles(data.decode("utf-8"))
            data = styles_xml.encode("utf-8")
        patched[name] = data

    if theme_xml is None or styles_xml is None:
        raise SystemExit("make_reference: reference.docx missing theme or styles part.")
    _verify(theme_xml, styles_xml)

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in patched.items():
            zout.writestr(name, data)
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "styles.docx"
    path = build_reference(out)
    print(f"wrote {path}")
