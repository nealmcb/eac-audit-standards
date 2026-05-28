"""Add Regulations.gov links and attachment links to the comment analysis document."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REGS_BASE = "https://www.regulations.gov/comment/EAC-2026-0067-"
# Relative path from insights/ to data/raw/attachments/
ATTACH_BASE = "../data/raw/attachments"

# All tracked attachment files, keyed by the four-digit suffix
ATTACHMENTS: dict[str, list[str]] = {
    "0039": ["attachment_1.docx", "attachment_1.pdf"],
    "0044": ["attachment_1.pdf"],
    "0047": ["attachment_1.docx", "attachment_1.pdf", "attachment_2.pdf"],
    "0049": ["attachment_1.docx", "attachment_1.pdf"],
    "0051": ["attachment_1.docx", "attachment_1.pdf"],
    "0053": ["attachment_1.pdf"],
    "0055": ["attachment_1.pdf"],
    "0056": ["attachment_1.docx", "attachment_1.pdf", "attachment_2.pdf"],
    "0058": ["attachment_1.pdf"],
    "0059": ["attachment_1.pdf", "attachment_2.pdf"],
    "0062": ["attachment_1.pdf", "attachment_2.pdf"],
    "0063": ["attachment_1.pdf"],
    "0065": ["attachment_1.pdf"],
    "0066": ["attachment_1.pdf"],
    "0068": ["attachment_1.pdf"],
    "0069": ["attachment_1.pdf"],
}


def attachment_links(suffix: str) -> str:
    """Return a markdown string with links for all attachments of the given comment."""
    files = ATTACHMENTS.get(suffix, [])
    parts = []
    seen_stems: set[str] = set()
    for fname in files:
        ext = fname.rsplit(".", 1)[-1].upper()
        n = fname.split("attachment_")[1].split(".")[0]
        # When both PDF and DOCX exist for same number, show both
        key = f"{n}-{ext}"
        if key in seen_stems:
            continue
        seen_stems.add(key)
        label = ext if len(files) <= 1 else f"{ext} ({n})"
        path = f"{ATTACH_BASE}/EAC-2026-0067-{suffix}/{fname}"
        parts.append(f"[{label}]({path})")
    return " · ".join(parts)


def update_table(text: str) -> str:
    """Add Regulations.gov link to the ID cell of each data row in the summary table."""

    def replace_row(m: re.Match) -> str:
        suffix = m.group(1)
        inner = m.group(2)
        regs = f" [[↗]]({REGS_BASE}{suffix})"
        return f"| [{suffix}](#{suffix_to_anchor(suffix)}){regs}{inner}"

    # Match rows: | [XXXX](#eac-2026-0067-XXXX) | rest...
    pattern = r"^\| \[(\d{4})\]\(#eac-2026-0067-\d{4}\)( \|.*)"
    return re.sub(pattern, replace_row, text, flags=re.MULTILINE)


def suffix_to_anchor(suffix: str) -> str:
    return f"eac-2026-0067-{suffix}"


def add_attachment_links_to_entry(entry: str, suffix: str) -> str:
    """Inject an Attachments line into an entry's metadata block if it has attachments."""
    if suffix not in ATTACHMENTS:
        return entry
    # Skip if already has a path-based link (already processed)
    if ATTACH_BASE in entry:
        return entry

    attach = attachment_links(suffix)

    # Try to update an existing **Attachment:** or **Attachments:** line
    def upgrade_attach_line(m: re.Match) -> str:
        label = m.group(1)  # "Attachment" or "Attachments" (no colon)
        desc = m.group(2).strip()
        return f"**{label}:** {desc} — {attach}\n"

    new_entry, count = re.subn(
        r"\*\*(Attachments?):?\*\*([^\n]+)\n",
        upgrade_attach_line,
        entry,
        flags=re.MULTILINE,
    )
    if count > 0:
        return new_entry

    # No existing attachment line — insert one after the last **Key:** metadata line
    lines = entry.splitlines(keepends=True)
    last_meta_idx = -1
    for i, ln in enumerate(lines):
        if re.match(r"\*\*\w[\w /]*:\*\*", ln):
            last_meta_idx = i
    if last_meta_idx >= 0:
        lines.insert(last_meta_idx + 1, f"**Attachments:** {attach}\n")
    return "".join(lines)


def process_section2(text: str) -> str:
    """Process all ### EAC-2026-0067-XXXX entries in Section 2."""
    # Split text into blocks at each ### heading
    # Use a regex that captures the heading start
    parts: list[str] = re.split(r"(?=\n### EAC-2026-0067-\d{4})", text)
    result: list[str] = []
    for part in parts:
        m = re.match(r"\n### EAC-2026-0067-(\d{4})", part)
        if m:
            suffix = m.group(1)
            part = add_attachment_links_to_entry(part, suffix)
        result.append(part)
    return "".join(result)


def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = update_table(text)
    text = process_section2(text)
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path}")


if __name__ == "__main__":
    target = Path(__file__).parent.parent / "insights" / "EAC-audit-draft_Comment_analysis.md"
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
    process_file(target)
