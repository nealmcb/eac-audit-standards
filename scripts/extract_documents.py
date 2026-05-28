#!/usr/bin/env python3
"""Extract text from PDF and DOCX files in data/raw/ into Markdown under data/processed/.

Strategy:
- DOCX: MarkItDown (preserves structure well)
- PDF: MarkItDown first (pdfminer.six handles text-layer PDFs reliably); if output is
  fewer than MIN_PDF_WORDS words, fall back to PyMuPDF4LLM + Tesseract OCR (for
  scanned/image-only PDFs with no text layer).
- When both DOCX and PDF exist for the same attachment, DOCX is preferred.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

MIN_PDF_WORDS = 100  # below this, assume MarkItDown missed a scanned PDF; retry with OCR


def extract_pdf(src: Path, dest: Path) -> None:
    from markitdown import MarkItDown
    import pymupdf4llm

    md_converter = MarkItDown()
    result = md_converter.convert(str(src))
    text = result.text_content

    if len(text.split()) < MIN_PDF_WORDS:
        print(f"    MarkItDown gave {len(text.split())} words; retrying with PyMuPDF4LLM (OCR)")
        text = pymupdf4llm.to_markdown(str(src))

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")


def extract_docx(src: Path, dest: Path) -> None:
    from markitdown import MarkItDown
    md_converter = MarkItDown()
    result = md_converter.convert(str(src))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(result.text_content, encoding="utf-8")


def relative_processed_path(src: Path) -> Path:
    """Mirror src's path under PROCESSED_DIR, changing suffix to .md."""
    rel = src.relative_to(RAW_DIR)
    return PROCESSED_DIR / rel.with_suffix(".md")


def collect_sources() -> list[tuple[Path, Path]]:
    """Return (src, dest) pairs to extract, skipping PDFs that have a DOCX sibling."""
    jobs = []
    for src in sorted(RAW_DIR.rglob("*")):
        if src.suffix.lower() == ".docx":
            dest = relative_processed_path(src)
            jobs.append((src, dest))
        elif src.suffix.lower() == ".pdf":
            sibling_docx = src.with_suffix(".docx")
            if sibling_docx.exists():
                print(f"  skip  {src.relative_to(ROOT)}  (DOCX preferred)")
                continue
            dest = relative_processed_path(src)
            jobs.append((src, dest))
    return jobs


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract PDF/DOCX to Markdown")
    parser.add_argument("--force", action="store_true", help="Re-extract even if output exists")
    args = parser.parse_args()

    jobs = collect_sources()
    if not jobs:
        print("No source files found.")
        sys.exit(0)

    errors = []
    for src, dest in jobs:
        if dest.exists() and not args.force:
            print(f"  exists {dest.relative_to(ROOT)}")
            continue
        try:
            print(f"  extract {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
            if src.suffix.lower() == ".docx":
                extract_docx(src, dest)
            else:
                extract_pdf(src, dest)
        except Exception as exc:
            print(f"  ERROR {src.relative_to(ROOT)}: {exc}", file=sys.stderr)
            errors.append((src, exc))

    if errors:
        print(f"\n{len(errors)} file(s) failed.", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nDone.")


if __name__ == "__main__":
    main()
