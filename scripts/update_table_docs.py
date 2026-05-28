"""
Update summary table in analysis doc:
- Re-add [[↗]] Regulations.gov link to each ID cell
- Add a Documents column with attachment links for rows that have them
"""
from __future__ import annotations
import re
from pathlib import Path

REGS_BASE = "https://www.regulations.gov/comment/EAC-2026-0067-"
ATTACH_BASE = "../data/raw/attachments"
WITHDRAWN = {"0007", "0009", "0017", "0024"}

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
    files = ATTACHMENTS.get(suffix, [])
    parts = []
    for fname in files:
        ext = fname.rsplit(".", 1)[-1].upper()
        n = fname.split("attachment_")[1].split(".")[0]
        label = ext if len(files) == 1 else f"{ext} ({n})"
        path = f"{ATTACH_BASE}/EAC-2026-0067-{suffix}/{fname}"
        parts.append(f"[{label}]({path})")
    return " · ".join(parts)


src = Path(__file__).parent.parent / "insights" / "EAC-audit-draft_Comment_analysis.md"
text = src.read_text(encoding="utf-8")

# 1. Update table header to add Documents column
text = text.replace(
    "| Comment ID | Submitter | Contact / Affiliation | One-Line Summary |",
    "| Comment ID | Submitter | Contact / Affiliation | One-Line Summary | Documents |",
    1,
)
text = text.replace(
    "|---|---|---|---|",
    "|---|---|---|---|---|",
    1,
)

# 2. Update each data row
def fix_row(m: re.Match) -> str:
    suffix = m.group(1)
    rest = m.group(2)   # " | Submitter | ... | Summary |"

    if suffix in WITHDRAWN:
        # Withdrawn rows: no links, just append — to the new column
        return f"| {suffix} | *(withdrawn/non-public)* | — | Withdrawn or non-public submission; not returned by Regulations.gov API. | — |"

    page_link = f"[{suffix} (text)](../data/processed/comments/EAC-2026-0067-{suffix}.md)"
    regs_link = f"[[↗]]({REGS_BASE}{suffix})"
    id_cell = f"{page_link} {regs_link}"

    attach = attachment_links(suffix)
    docs_cell = attach if attach else "—"

    # Strip trailing " |" from rest, then append the docs column
    body = rest.rstrip()
    if body.endswith(" |"):
        body = body[:-2]
    return f"| {id_cell}{body} | {docs_cell} |"

# Match public rows (have a per-comment page link)
text = re.sub(
    r"^\| \[(\d{4})\]\(\.\./data/processed/comments/EAC-2026-0067-\d{4}\.md\)( \|.*)",
    fix_row,
    text,
    flags=re.MULTILINE,
)

# Also fix withdrawn rows (no link, just the plain number)
text = re.sub(
    r"^\| (0007|0009|0017|0024) \| \*\(withdrawn/non-public\)\* \| — \| Withdrawn[^|]+\|$",
    lambda m: f"| {m.group(1)} | *(withdrawn/non-public)* | — | Withdrawn or non-public submission; not returned by Regulations.gov API. | — |",
    text,
    flags=re.MULTILINE,
)

src.write_text(text, encoding="utf-8")
print(f"Done — wrote {src}")
