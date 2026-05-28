#!/usr/bin/env python3
"""Build one Markdown file per comment combining metadata, inline text, and attachment text.

Output: data/processed/comments/{comment-id}.md for each of the 71 comments.
These files are the primary source for Claude Projects — each is self-contained
with full content, so topical searches find the actual submission rather than
metadata stubs.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
DATA_PROCESSED = ROOT / "data" / "processed"
COMMENTS_DIR = DATA_PROCESSED / "comments"
ATTACHMENTS_DIR = DATA_PROCESSED / "attachments"
CSV_PATH = DATA_PROCESSED / "comments.csv"


def load_attachments(comment_id: str) -> list[tuple[str, str]]:
    """Return [(label, text), ...] for all extracted attachment .md files."""
    attach_dir = ATTACHMENTS_DIR / comment_id
    if not attach_dir.is_dir():
        return []
    results = []
    for md_file in sorted(attach_dir.glob("attachment_*.md")):
        text = md_file.read_text(encoding="utf-8").strip()
        if text:
            n = md_file.stem.replace("attachment_", "")
            results.append((f"Attachment {n}", text))
    return results


def is_stub(text: str) -> bool:
    t = str(text or "").strip()
    return not t or t.lower().startswith("see attached") or len(t) < 40


def build_page(row: pd.Series) -> str:
    comment_id = str(row["id"])

    def clean(val: object) -> str:
        s = str(val or "").strip()
        return "" if s in ("nan", "None") else s

    first = clean(row.get("first_name"))
    last = clean(row.get("last_name"))
    name = f"{first} {last}".strip() or "Anonymous"
    org = clean(row.get("organization"))
    submitter = f"{name} ({org})" if org else name

    date = str(row.get("submitted_date") or "").split("T")[0]

    lines = [
        f"# {comment_id} — {submitter}",
        "",
        f"**Date:** {date}",
        f"**Docket:** EAC-2026-0067",
        "",
        "---",
        "",
    ]

    csv_text = str(row.get("comment_text") or "").strip()
    attachments = load_attachments(comment_id)

    if attachments and is_stub(csv_text):
        # Attachment is the whole submission — include directly without a sub-header
        if len(attachments) == 1:
            lines.append(attachments[0][1])
        else:
            for label, text in attachments:
                lines += [f"## {label}", "", text, ""]
    elif attachments:
        # Inline text plus supplementary attachments
        lines += [csv_text, ""]
        for label, text in attachments:
            lines += [f"## {label}", "", text, ""]
    else:
        lines.append(csv_text)

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build one .md file per comment")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found. Run normalize_comments.py first.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(CSV_PATH)
    COMMENTS_DIR.mkdir(parents=True, exist_ok=True)

    for _, row in df.iterrows():
        comment_id = str(row["id"])
        dest = COMMENTS_DIR / f"{comment_id}.md"
        if dest.exists() and not args.force:
            print(f"  exists {dest.relative_to(ROOT)}")
            continue
        page = build_page(row)
        dest.write_text(page, encoding="utf-8")
        print(f"  wrote  {dest.relative_to(ROOT)}")

    print(f"\nDone. {len(df)} comment pages in {COMMENTS_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
