"""Download all public comments and attachments for the docket from Regulations.gov."""

from __future__ import annotations

import json
import logging
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from utils import DATA_RAW, ensure_dirs, get_api_key, get_json, load_config, make_session

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

REGS_BASE = "https://api.regulations.gov/v4"
ATTACHMENTS_DIR = DATA_RAW / "attachments"


def _polite_sleep(api_key: str) -> None:
    """Brief pause to stay within rate limits (1 000 req/hour for DEMO_KEY)."""
    time.sleep(1.5 if api_key == "DEMO_KEY" else 0.2)


def fetch_comment_listing(docket_id: str, api_key: str, page_size: int = 25) -> list[dict]:
    """Return lightweight listing items (id + self link, no comment text)."""
    all_items: list[dict] = []
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
        log.info("Listing page %s%s ...", page,
                 f"/{total_pages}" if total_pages is not None else "")
        data = get_json(f"{REGS_BASE}/comments", params=params)

        page_path = DATA_RAW / f"comments_page_{page:04d}.json"
        page_path.write_text(json.dumps(data, indent=2))

        items = data.get("data", [])
        all_items.extend(items)

        meta = data.get("meta", {})
        total_pages = meta.get("totalPages", 1)
        has_next = meta.get("hasNextPage", False)
        log.info("  got %d items (total so far: %d)", len(items), len(all_items))

        if not has_next or not items:
            break

        page += 1
        _polite_sleep(api_key)

    return all_items


def fetch_comment_detail(comment_id: str, api_key: str) -> dict | None:
    """Fetch full comment attributes (text, author, fileFormats) for one comment."""
    url = f"{REGS_BASE}/comments/{comment_id}"
    try:
        data = get_json(url, params={"api_key": api_key})
    except Exception as exc:
        log.error("Could not fetch detail for %s: %s", comment_id, exc)
        return None
    return data.get("data")


def fetch_attachments(comment_id: str, api_key: str) -> list[dict]:
    """Return attachment objects for a comment (may be empty)."""
    url = f"{REGS_BASE}/comments/{comment_id}/attachments"
    try:
        data = get_json(url, params={"api_key": api_key})
    except Exception as exc:
        log.warning("Could not fetch attachments for %s: %s", comment_id, exc)
        return []
    return data.get("data", [])


def download_attachment(comment_id: str, title: str, file_url: str) -> pathlib.Path | None:
    """Download one attachment file; return its path or None on failure."""
    dest_dir = ATTACHMENTS_DIR / comment_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Derive a safe filename from the URL
    url_filename = file_url.split("?")[0].rsplit("/", 1)[-1]
    dest = dest_dir / url_filename

    if dest.exists():
        log.info("  attachment already downloaded: %s", dest.name)
        return dest

    log.info("  downloading attachment: %s -> %s", title, dest.name)
    try:
        session = make_session()
        # downloads.regulations.gov blocks non-browser user agents
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )
        resp = session.get(file_url, timeout=120, stream=True)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        log.info("    saved %d bytes", len(resp.content))
        return dest
    except Exception as exc:
        log.error("    failed to download %s: %s", file_url, exc)
        return None


def enrich_comments(
    listing: list[dict], api_key: str, existing_ids: set[str]
) -> list[dict]:
    """For each listing item, fetch full details + attachments; return enriched list."""
    enriched: list[dict] = []
    total = len(listing)

    for i, item in enumerate(listing, 1):
        comment_id = item.get("id", "")
        if not comment_id:
            log.warning("[%d/%d] item has no id, skipping", i, total)
            continue

        log.info("[%d/%d] %s", i, total, comment_id)

        if comment_id in existing_ids:
            log.info("  already fetched, skipping")
            continue

        # Fetch full detail
        _polite_sleep(api_key)
        detail = fetch_comment_detail(comment_id, api_key)
        if detail is None:
            continue

        # Fetch and download attachments
        _polite_sleep(api_key)
        attachments = fetch_attachments(comment_id, api_key)

        attachment_paths: list[str] = []
        for att in attachments:
            att_attrs = att.get("attributes", {})
            if att_attrs.get("restrictReasonType"):
                continue
            title = att_attrs.get("title", "attachment")
            file_formats = att_attrs.get("fileFormats") or []
            for fmt in file_formats:
                file_url = fmt.get("fileUrl", "")
                if not file_url:
                    continue
                path = download_attachment(comment_id, title, file_url)
                if path:
                    attachment_paths.append(str(path.relative_to(DATA_RAW)))

        # Also check fileFormats on the comment itself (inline content)
        detail_attrs = detail.get("attributes", {})
        for fmt in detail_attrs.get("fileFormats") or []:
            file_url = fmt.get("fileUrl", "")
            if not file_url:
                continue
            title = detail_attrs.get("title", comment_id)
            path = download_attachment(comment_id, title, file_url)
            if path:
                attachment_paths.append(str(path.relative_to(DATA_RAW)))

        # Embed attachment paths into detail for downstream use
        detail.setdefault("attributes", {})["_attachment_paths"] = attachment_paths
        detail["attributes"]["_attachment_count"] = len(attachments)

        enriched.append(detail)
        log.info("  done (%d attachments)", len(attachment_paths))

    return enriched


def load_existing_ids(path: pathlib.Path) -> set[str]:
    ids: set[str] = set()
    if not path.exists():
        return ids
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    ids.add(json.loads(line).get("id", ""))
                except json.JSONDecodeError:
                    pass
    return ids


def download_all_attachments(out_path: pathlib.Path, api_key: str) -> None:
    """Re-scan comments.jsonl and download any attachments not yet on disk."""
    items = []
    with out_path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    total = len(items)
    for i, item in enumerate(items, 1):
        comment_id = item.get("id", "")
        log.info("[%d/%d] attachments for %s", i, total, comment_id)
        attachments = fetch_attachments(comment_id, api_key)

        attachment_paths: list[str] = []
        for att in attachments:
            att_attrs = att.get("attributes", {})
            if att_attrs.get("restrictReasonType"):
                continue
            title = att_attrs.get("title", "attachment")
            file_formats = att_attrs.get("fileFormats") or []
            for fmt in file_formats:
                file_url = fmt.get("fileUrl", "")
                if not file_url:
                    continue
                path = download_attachment(comment_id, title, file_url)
                if path:
                    attachment_paths.append(str(path.relative_to(DATA_RAW)))
                _polite_sleep(api_key)

        if attachment_paths:
            log.info("  downloaded %d file(s)", len(attachment_paths))


def main() -> None:
    ensure_dirs()
    ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)

    config = load_config()
    docket_id = config["docket_id"]
    api_key = get_api_key()
    page_size = config.get("regulations_gov", {}).get("page_size", 25)

    # Step 1: listing (get all IDs)
    listing = fetch_comment_listing(docket_id, api_key, page_size=page_size)
    if not listing:
        log.warning("No comments found for docket %s", docket_id)
        return
    log.info("Listing complete: %d comments", len(listing))

    # Step 2: enrich (fetch detail + attachments for each)
    out_path = DATA_RAW / "comments.jsonl"
    existing_ids = load_existing_ids(out_path)
    if existing_ids:
        log.info("Resuming: %d comments already in %s", len(existing_ids), out_path)

    new_items = enrich_comments(listing, api_key, existing_ids)

    # Append new items to the JSONL file
    with out_path.open("a") as fh:
        for item in new_items:
            fh.write(json.dumps(item) + "\n")

    total_written = len(existing_ids) + len(new_items)
    log.info("Total comments in %s: %d", out_path, total_written)

    # Step 3: download attachments (separate pass so browser UA is used)
    log.info("Downloading attachments...")
    download_all_attachments(out_path, api_key)


if __name__ == "__main__":
    main()
