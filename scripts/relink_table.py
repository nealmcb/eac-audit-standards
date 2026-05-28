"""
Relink summary table: comment ID → per-comment page; move regs.gov to entry headers.
"""
from __future__ import annotations
import re
from pathlib import Path

REGS_BASE = "https://www.regulations.gov/comment/EAC-2026-0067-"
PAGES_BASE = "../data/processed/comments/EAC-2026-0067-"
WITHDRAWN = {"0007", "0009", "0017", "0024"}

src = Path(__file__).parent.parent / "insights" / "EAC-audit-draft_Comment_analysis.md"
text = src.read_text(encoding="utf-8")

# 1. Summary table rows -------------------------------------------------------
# Current: | [XXXX](#eac-2026-0067-XXXX) [[↗]](https://regs.../XXXX) | rest...
# Wanted:  | [XXXX](../data/processed/comments/EAC-2026-0067-XXXX.md) | rest...

def fix_table_row(m: re.Match) -> str:
    suffix = m.group(1)
    rest = m.group(2)          # everything after the ID cell fragment, up to end of row
    if suffix in WITHDRAWN:
        return m.group(0)      # leave withdrawn rows untouched
    page_link = f"[{suffix}]({PAGES_BASE}{suffix}.md)"
    return f"| {page_link}{rest}"

# Pattern covers both:
#   [XXXX](#anchor) [[↗]](regs-url) | rest
#   [XXXX](#anchor) | rest          (if regs link already removed)
text = re.sub(
    r"^\| \[(\d{4})\]\(#eac-2026-0067-\d{4}\)"
    r"(?: \[\[↗\]\]\(https://www\.regulations\.gov/comment/EAC-2026-0067-\d{4}\))?"
    r"( \|.*)",
    fix_table_row,
    text,
    flags=re.MULTILINE,
)

# 2. Individual entry headers --------------------------------------------------
# After the **Date:** line add **Source:** [Regulations.gov](...) if not already present.

def add_source_line(m: re.Match) -> str:
    suffix = m.group(1)
    heading = m.group(2)       # e.g. "### EAC-2026-0067-0002 — Ronald Rivest\n"
    date_line = m.group(3)     # e.g. "**Date:** 2026-05-20\n"
    if suffix in WITHDRAWN:
        return m.group(0)
    source = f"**Source:** [Regulations.gov]({REGS_BASE}{suffix})\n"
    return heading + date_line + source

text = re.sub(
    r"(### EAC-2026-0067-(\d{4})[^\n]*\n\n)"  # group 1+2: heading + blank line + suffix
    r"(\*\*Date:\*\*[^\n]+\n)"                # group 3: date line
    r"(?!\*\*Source:\*\*)",                   # not already present
    lambda m: m.group(1) + m.group(3) + f"**Source:** [Regulations.gov]({REGS_BASE}{m.group(2)})\n",
    text,
    flags=re.MULTILINE,
)

src.write_text(text, encoding="utf-8")
print(f"Done — wrote {src}")
