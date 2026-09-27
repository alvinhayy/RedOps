"""Rebuild the Corey Ball API chapters from the supplied PDF.

The PDF is rendered page-by-page with Poppler.  This keeps the layout used for
tables and examples, while the XML pass supplies the vertical position of each
figure so its Markdown link can be placed beside the matching page content.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = Path.home() / "Downloads/Corey J. Ball - Hacking APIs_ Breaking Web Application Programming Interfaces-No Starch Press (2022).pdf"
OUT = ROOT / "knowledge/api"

CHAPTERS = [
    (0, "Preparing for API Security Testing", "Part I: Preparing for API Security Testing", 29, 40, "chapter-00-preparing-api-security-testing.md"),
    (1, "How Web Applications Work", "Part I: Preparing for API Security Testing", 41, 52, "chapter-01-how-web-applications-work.md"),
    (2, "The Anatomy of Web APIs", "Part I: Preparing for API Security Testing", 53, 78, "chapter-02-anatomy-of-web-apis.md"),
    (3, "API Securities", "Part I: Preparing for API Security Testing", 79, 96, "chapter-03-api-insecurities.md"),
    (4, "Setting Up an API Hacking System", "Part II: Lab Setup", 97, 134, "chapter-04-api-hacking-system.md"),
    (5, "Setting Up Vulnerable API Targets", "Part II: Lab Setup", 135, 148, "chapter-05-vulnerable-api-targets.md"),
    (6, "Discovering APIs", "Part III: Attacking APIs", 149, 180, "chapter-06-discovering-apis.md"),
    (7, "Endpoint Analysis", "Part III: Attacking APIs", 181, 200, "chapter-07-endpoint-analysis.md"),
    (8, "Attacking API Authentication", "Part III: Attacking APIs", 201, 226, "chapter-08-api-authentication.md"),
    (9, "API Fuzzing", "Part III: Attacking APIs", 227, 248, "chapter-09-api-fuzzing.md"),
    (10, "Exploiting API Authorization", "Part III: Attacking APIs", 249, 262, "chapter-10-api-authorization.md"),
    (11, "Exploiting Mass Assignment", "Part III: Attacking APIs", 263, 274, "chapter-11-mass-assignment.md"),
    (12, "API Injection", "Part III: Attacking APIs", 275, 292, "chapter-12-api-injection.md"),
    (13, "Evasive Techniques and Rate Limit Testing", "Part IV: Real-World API Hacking", 293, 310, "chapter-13-evasive-rate-limit-testing.md"),
    (14, "Attacking GraphQL", "Part IV: Real-World API Hacking", 311, 332, "chapter-14-attacking-graphql.md"),
    (15, "Breaches and Bounties", "Part IV: Real-World API Hacking", 333, 344, "chapter-15-breaches-and-bounties.md"),
]

TABLES = {
    0: ["Table 0-1"],
    1: ["Tables 1-1 through 1-5"],
    2: ["Tables 2-1 through 2-3"],
    4: ["Tables 4-1 through 4-2"],
    5: ["Tables 5-1 through 5-2"],
    6: ["Tables 6-1 through 6-3"],
    7: ["Table 7-1 (including continuation)"],
    8: ["Table 8-1"],
    10: ["Tables 10-1 through 10-2"],
    12: ["Table 12-1"],
    13: ["Tables 13-1 through 13-3"],
}

HEADER = "Hacking APIs (Early Access) © 2022 by Corey Ball"
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def run(*args: str) -> str:
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return result.stdout


def page_text(page: int) -> list[str]:
    raw = run("pdftotext", "-layout", "-f", str(page), "-l", str(page), str(PDF), "-")
    lines = []
    for line in raw.replace("\f", "").splitlines():
        line = CONTROL_CHARS.sub("", line).replace("\u00a0", " ").rstrip()
        stripped = line.strip()
        if not stripped or HEADER in line:
            lines.append("")
            continue
        # Running page footer, e.g. "224 Chapter 10".
        if re.fullmatch(r"\d+\s+Chapter\s+\d+", stripped) or re.fullmatch(r"Chapter\s+\d+", stripped):
            lines.append("")
            continue
        # Running chapter title footer, e.g. "Exploiting API Authorization 225".
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9 .&'/-]{4,}\s+\d{2,4}", stripped):
            lines.append("")
            continue
        lines.append(line)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def page_images(xml_root: ET.Element, page: int) -> list[tuple[float, Path]]:
    assets = sorted((OUT / "assets" / f"chapter-{chapter_for_page(page):02d}").glob(f"figure-{page:03d}-*"))
    page_node = next((node for node in xml_root.findall("page") if int(node.attrib["number"]) == page), None)
    if page_node is None:
        return []
    nodes = []
    for node in page_node.findall("image"):
        if int(float(node.attrib.get("width", 0))) < 100 or int(float(node.attrib.get("height", 0))) < 100:
            continue
        nodes.append((float(node.attrib.get("top", 0)), node))
    if len(nodes) != len(assets):
        print(f"warning: page {page}: XML figures={len(nodes)}, assets={len(assets)}")
    if not nodes and assets:
        # A few PDF image objects are not reported by pdftohtml although
        # pdfimages extracts them. Keep them in page order at page start.
        return [(0.0, asset) for asset in assets]
    return [(top, asset) for (top, _), asset in zip(sorted(nodes), assets)]


def chapter_for_page(page: int) -> int:
    for number, _, _, start, end, _ in CHAPTERS:
        if start <= page <= end:
            return number
    raise ValueError(page)


def code_kind(line: str) -> str | None:
    value = line.strip()
    if not value:
        return None
    if value.startswith("$") or re.match(r"^(sudo\s+)?(curl|wget|docker|git|nmap|nikto|wfuzz|ffuf|gobuster|amass|sqlmap|jwt_tool|kr\s|python(?:3)?\s|pip\s|npm\s|openssl\s|adb\s|frida\s)", value):
        return "console"
    if re.match(r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(?:/|https?://)", value):
        return "http"
    if value.startswith(("pm.", "function ")) or value in {"});", ");", "}"}:
        return "javascript"
    if re.match(
        r"^(HTTP/\d(?:\.\d)?|Host:|Authorization:|Content-Type:|Accept(?:-Encoding)?:|Cookie:|Origin:|Referer:|User-Agent:|Content-Length:|x-[\w-]+:)",
        value,
        re.IGNORECASE,
    ):
        return "http"
    if value.startswith(("{", "}", "[", "]", '"')):
        return "json" if value.startswith(("{", "}", "[", "]", '"')) else "console"
    return None


def format_code(lines: list[str]) -> list[str]:
    """Fence obvious standalone command/request examples without touching prose tables."""
    out: list[str] = []
    open_kind: str | None = None
    continuation = False
    for line in lines:
        kind = code_kind(line)
        value = line.strip()
        if open_kind and (
            kind
            or continuation
            or value.startswith(("--", "-H ", "-d ", "-X "))
        ):
            out.append(line.strip())
            continuation = value.endswith(("/", "\\"))
            continue
        if open_kind:
            out.append("```")
            open_kind = None
            continuation = False
        if kind:
            open_kind = kind
            out.append(f"```{kind}")
            out.append(line.strip())
            continuation = value.endswith(("/", "\\"))
        else:
            out.append(line.lstrip() if line.startswith(" ") else line)
    if open_kind:
        out.append("```")
    return out


def table_section(number: int) -> list[str]:
    items = TABLES.get(number)
    if not items:
        return ["## Tables referenced in this chapter", "", "No separately labeled tables were found; tabular content is retained in the page-layout extraction above."]
    return ["## Tables referenced in this chapter", "", *[f"- {item}; the table rows are retained in the page-layout extraction above." for item in items]]


def rebuild(number: int, title: str, part: str, start: int, end: int, filename: str, xml_root: ET.Element) -> None:
    body: list[str] = []
    for page in range(start, end + 1):
        lines = page_text(page)
        images = page_images(xml_root, page)
        # A page-level marker makes provenance and figure placement explicit.
        page_events: dict[int, list[Path]] = {}
        for top, asset in images:
            position = min(len(lines), max(0, round((top / 999.0) * max(len(lines), 1))))
            page_events.setdefault(position, []).append(asset)
        page_body: list[str] = [f"<!-- PDF page {page} -->"]
        for index, line in enumerate(lines):
            for asset in page_events.get(index, []):
                rel = Path("assets") / f"chapter-{number:02d}" / asset.name
                page_body.extend([f"![PDF page {page} figure]({rel.as_posix()})", ""])
            page_body.append(line)
        for asset in page_events.get(len(lines), []):
            rel = Path("assets") / f"chapter-{number:02d}" / asset.name
            page_body.extend(["", f"![PDF page {page} figure]({rel.as_posix()})"])
        body.extend(page_body)
        body.append("")

    frontmatter = [
        "---",
        f'title: "Chapter {number}: {title}"',
        'author: "Corey J. Ball"',
        'published: "2022"',
        'source: "Operator-provided local PDF; direct Poppler layout extraction"',
        'source_url: "file:///Users/alvinhayyi/Downloads/Corey%20J.%20Ball%20-%20Hacking%20APIs_%20Breaking%20Web%20Application%20Programming%20Interfaces-No%20Starch%20Press%20(2022).pdf"',
        "category: api",
        f'part: "{part}"',
        f'chapter: "{number}"',
        'quality: "Direct PDF layout extraction; verify commands and claims against current primary documentation"',
        "---",
        "",
        f"# Chapter {number}: {title}",
        "",
        f"> Extracted from the operator-provided PDF (PDF pages {start}–{end}). Page markers and figure links preserve source order; command/request examples are fenced when identifiable.",
        "",
    ]
    rendered = "\n".join(frontmatter + format_code(body) + [""] + table_section(number) + [""])
    (OUT / filename).write_text(rendered, encoding="utf-8")


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"PDF not found: {PDF}")
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="redops-api-pdf-") as tmp:
        xml_path = Path(tmp) / "chapters"
        run("pdftohtml", "-xml", "-hidden", "-f", "29", "-l", "344", str(PDF), str(xml_path))
        root = ET.parse(f"{xml_path}.xml").getroot()
        for chapter in CHAPTERS:
            rebuild(*chapter, root)


if __name__ == "__main__":
    main()
