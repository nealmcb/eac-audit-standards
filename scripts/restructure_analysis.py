"""Restructure the comment analysis: TOC → Synthesis → Findings → Table → Entries."""

from pathlib import Path

src = Path(__file__).parent.parent / "insights" / "EAC-audit-draft_Comment_analysis.md"
text = src.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)

# Find section start lines (0-based)
section_starts: dict[str, int] = {}
for i, ln in enumerate(lines):
    if ln.startswith("## "):
        section_starts[ln.strip()] = i

print("Found sections:")
for k, v in sorted(section_starts.items(), key=lambda x: x[1]):
    print(f"  line {v+1}: {k!r}")

# Identify the boundaries
exec_sum_line   = section_starts["## Executive Summary"]
table_line      = section_starts["## 1. Summary Table"]
entries_line    = section_starts["## 2. Individual Comment Entries"]
synthesis_line  = section_starts["## 3. Topical Synthesis"]
conclusion_line = section_starts["## 4. Conclusion"]
total = len(lines)

# Extract each chunk (lines up to but not including the next section)
def chunk(start: int, end: int) -> str:
    return "".join(lines[start:end])

preamble   = chunk(0, exec_sum_line)           # title, docket line, ---
exec_sum   = chunk(exec_sum_line, table_line)  # Executive Summary + ---
table      = chunk(table_line, entries_line)   # Summary Table
entries    = chunk(entries_line, synthesis_line)  # Individual Entries
synthesis  = chunk(synthesis_line, conclusion_line)  # Topical Synthesis
conclusion = chunk(conclusion_line, total)     # Conclusion (to EOF)

# Rename headings and strip old numbers
exec_sum   = exec_sum.replace("## Executive Summary", "## Executive Summary", 1)
table      = table.replace("## 1. Summary Table", "## Summary Table", 1)
entries    = entries.replace("## 2. Individual Comment Entries", "## Individual Comment Entries", 1)
synthesis  = synthesis.replace("## 3. Topical Synthesis", "## Topical Synthesis", 1)
conclusion = conclusion.replace("## 4. Conclusion", "## Findings and Recommendations", 1)

# Build table of contents
toc = """\
## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Topical Synthesis](#topical-synthesis)
3. [Findings and Recommendations](#findings-and-recommendations)
4. [Summary Table](#summary-table)
5. [Individual Comment Entries](#individual-comment-entries)

---

"""

# Assemble in new order
result = preamble + exec_sum + toc + synthesis + "\n---\n\n" + conclusion + "\n---\n\n" + table + entries

src.write_text(result, encoding="utf-8")
print(f"\nWrote {len(result.splitlines())} lines to {src}")
