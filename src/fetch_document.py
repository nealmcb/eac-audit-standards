"""Download the EAC draft audit standards document."""

from __future__ import annotations

import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from utils import (
    DATA_RAW,
    ensure_dirs,
    get_api_key,
    get_json,
    load_config,
    make_session,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

REGS_BASE = "https://api.regulations.gov/v4"


def find_document_url(docket_id: str, api_key: str) -> tuple[str, str] | None:
    """Query Regulations.gov for a downloadable document in the docket.

    Returns (url, filename) or None.
    """
    params = {
        "filter[docketId]": docket_id,
        "api_key": api_key,
        "page[size]": 25,
    }
    try:
        data = get_json(f"{REGS_BASE}/documents", params=params)
    except Exception as exc:
        log.warning("Could not query documents API: %s", exc)
        return None

    for doc in data.get("data", []):
        attrs = doc.get("attributes", {})
        file_formats = attrs.get("fileFormats") or []
        for fmt in file_formats:
            url = fmt.get("fileUrl", "")
            ext = fmt.get("format", "").lower()
            if url and ext in ("docx", "doc", "pdf"):
                title = attrs.get("title", doc.get("id", "document"))
                safe_title = title[:60].replace("/", "_").replace(" ", "_")
                filename = f"{safe_title}.{ext}"
                log.info("Found document: %s (%s)", title, ext)
                return url, filename

    return None


def download_file(url: str, dest: pathlib.Path, api_key: str) -> None:
    session = make_session()
    sep = "&" if "?" in url else "?"
    full_url = f"{url}{sep}api_key={api_key}"
    log.info("Downloading %s -> %s", url, dest)
    resp = session.get(full_url, timeout=120, stream=True)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    log.info("Saved %d bytes to %s", len(resp.content), dest)


def main() -> None:
    ensure_dirs()
    config = load_config()
    docket_id = config["docket_id"]
    api_key = get_api_key()

    doc_config = config.get("document", {})
    doc_url = (doc_config.get("url") or "").strip()
    doc_filename = doc_config.get("filename", "draft_standards.docx")

    if not doc_url:
        log.info(
            "No document URL configured; querying Regulations.gov for docket %s",
            docket_id,
        )
        result = find_document_url(docket_id, api_key)
        if result:
            doc_url, doc_filename = result
        else:
            log.error(
                "Could not find a downloadable document in docket %s. "
                "Set document.url in config/docket.yaml or provide REGULATIONS_GOV_API_KEY.",
                docket_id,
            )
            sys.exit(1)

    dest = DATA_RAW / doc_filename
    if dest.exists():
        log.info("Document already downloaded: %s", dest)
        return

    download_file(doc_url, dest, api_key)


if __name__ == "__main__":
    main()
