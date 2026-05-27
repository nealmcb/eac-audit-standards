"""Normalize raw comments JSONL into structured CSV and JSONL."""

from __future__ import annotations

import json
import logging
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import pandas as pd

from utils import DATA_PROCESSED, DATA_RAW, ensure_dirs

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def normalize_comment(item: dict) -> dict:
    attrs = item.get("attributes", {})
    return {
        "id": item.get("id", ""),
        "title": clean_text(attrs.get("title")),
        "first_name": clean_text(attrs.get("firstName")),
        "last_name": clean_text(attrs.get("lastName")),
        "organization": clean_text(attrs.get("organization")),
        "submitted_date": attrs.get("postedDate") or attrs.get("receiveDate") or "",
        "document_type": attrs.get("documentType", ""),
        "docket_id": attrs.get("docketId", ""),
        "comment_text": clean_text(attrs.get("comment")),
        "withdrawn": attrs.get("withdrawn", False),
        "has_attachments": bool(attrs.get("attachmentCount", 0)),
    }


def load_raw_comments(path: pathlib.Path) -> list[dict]:
    items: list[dict] = []
    if not path.exists():
        log.error("Raw comments file not found: %s", path)
        return items
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    log.warning("Skipping malformed line: %s", exc)
    return items


def main() -> None:
    ensure_dirs()
    raw_path = DATA_RAW / "comments.jsonl"
    items = load_raw_comments(raw_path)

    if not items:
        log.warning("No raw comments to normalize.")
        return

    normalized = [normalize_comment(item) for item in items]
    df = pd.DataFrame(normalized)

    csv_path = DATA_PROCESSED / "comments.csv"
    df.to_csv(csv_path, index=False)
    log.info("Wrote %d rows to %s", len(df), csv_path)

    jsonl_path = DATA_PROCESSED / "comments.jsonl"
    with jsonl_path.open("w") as fh:
        for record in normalized:
            fh.write(json.dumps(record) + "\n")
    log.info("Wrote %s", jsonl_path)


if __name__ == "__main__":
    main()
