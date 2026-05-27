"""Extract text from the draft standards document and produce a Markdown summary."""

from __future__ import annotations

import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from utils import DATA_PROCESSED, DATA_RAW, DATA_SUMMARIES, ensure_dirs, load_config

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


def extract_docx(path: pathlib.Path) -> list[tuple[str, str]]:
    """Return [(style_name, paragraph_text), ...] from a .docx file."""
    from docx import Document  # type: ignore

    doc = Document(str(path))
    return [
        (para.style.name, para.text.strip())
        for para in doc.paragraphs
        if para.text.strip()
    ]


def extract_plain(path: pathlib.Path) -> list[tuple[str, str]]:
    """Fallback: read the file as plain text."""
    try:
        return [
            ("Normal", line.strip())
            for line in path.read_text(errors="replace").splitlines()
            if line.strip()
        ]
    except Exception as exc:
        log.error("Could not read %s: %s", path, exc)
        return []


def build_summary(paragraphs: list[tuple[str, str]], title: str) -> str:
    lines = [f"# Document Summary: {title}", ""]
    section_count = 0

    for style, text in paragraphs:
        sl = style.lower()
        if "heading 1" in sl:
            lines += [f"\n## {text}"]
            section_count += 1
        elif "heading 2" in sl:
            lines += [f"\n### {text}"]
        elif "heading 3" in sl or "heading 4" in sl:
            lines += [f"\n#### {text}"]
        else:
            # Truncate very long normal paragraphs in the summary view.
            words = text.split()
            if len(words) > 150:
                text = " ".join(words[:150]) + " [...]"
            lines += [text, ""]

    lines += [f"\n---\n*Extracted from {title}. Top-level sections found: {section_count}.*"]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    config = load_config()
    doc_config = config.get("document", {})
    configured_filename = doc_config.get("filename", "")

    doc_path: pathlib.Path | None = None
    if configured_filename and (DATA_RAW / configured_filename).exists():
        doc_path = DATA_RAW / configured_filename
    else:
        candidates = (
            list(DATA_RAW.glob("*.docx"))
            + list(DATA_RAW.glob("*.doc"))
            + list(DATA_RAW.glob("*.pdf"))
        )
        if candidates:
            doc_path = candidates[0]

    if doc_path is None:
        log.error(
            "No draft document found in %s. Run fetch_document.py first.", DATA_RAW
        )
        sys.exit(1)

    log.info("Processing document: %s", doc_path)
    suffix = doc_path.suffix.lower()
    paragraphs = extract_docx(doc_path) if suffix in (".docx", ".doc") else extract_plain(doc_path)
    log.info("Extracted %d paragraphs", len(paragraphs))

    summary = build_summary(paragraphs, doc_path.name)
    out_path = DATA_SUMMARIES / "document_summary.md"
    out_path.write_text(summary)
    log.info("Wrote document summary to %s", out_path)

    # Save full extracted text for downstream use.
    text_path = DATA_PROCESSED / "document_text.txt"
    with text_path.open("w") as fh:
        for _, text in paragraphs:
            fh.write(text + "\n\n")
    log.info("Wrote full extracted text to %s", text_path)


if __name__ == "__main__":
    main()
