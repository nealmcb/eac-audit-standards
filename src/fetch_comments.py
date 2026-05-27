"""Download all public comments for the docket from Regulations.gov."""

from __future__ import annotations

import json
import logging
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from utils import DATA_RAW, ensure_dirs, get_api_key, get_json, load_config

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

REGS_BASE = "https://api.regulations.gov/v4"


def fetch_all_comments(docket_id: str, api_key: str, page_size: int = 25) -> list[dict]:
    all_comments: list[dict] = []
    page = 1
    total_pages: int | None = None

    while True:
        params = {
            "filter[docketId]": docket_id,
            "api_key": api_key,
            "page[size]": page_size,
            "page[number]": page,
            "sort": "postedDate",
        }
        log.info(
            "Fetching page %s%s ...",
            page,
            f"/{total_pages}" if total_pages is not None else "",
        )
        try:
            data = get_json(f"{REGS_BASE}/comments", params=params)
        except Exception as exc:
            log.error("Failed to fetch page %d: %s", page, exc)
            break

        page_path = DATA_RAW / f"comments_page_{page:04d}.json"
        page_path.write_text(json.dumps(data, indent=2))

        items = data.get("data", [])
        all_comments.extend(items)

        meta = data.get("meta", {})
        total_pages = meta.get("totalPages", 1)
        has_next = meta.get("hasNextPage", False)
        log.info("  got %d comments (total so far: %d)", len(items), len(all_comments))

        if not has_next or not items:
            break

        page += 1
        # Be polite to the DEMO_KEY rate limit (1 000 req/hour).
        if api_key == "DEMO_KEY":
            time.sleep(1)

    return all_comments


def main() -> None:
    ensure_dirs()
    config = load_config()
    docket_id = config["docket_id"]
    api_key = get_api_key()
    page_size = config.get("regulations_gov", {}).get("page_size", 25)

    comments = fetch_all_comments(docket_id, api_key, page_size=page_size)

    if not comments:
        log.warning("No comments fetched for docket %s", docket_id)
    else:
        log.info("Total comments fetched: %d", len(comments))

    out_path = DATA_RAW / "comments.jsonl"
    with out_path.open("w") as fh:
        for item in comments:
            fh.write(json.dumps(item) + "\n")
    log.info("Wrote %s", out_path)


if __name__ == "__main__":
    main()
