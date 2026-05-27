.PHONY: all fetch fetch-document fetch-comments normalize summarize \
        summarize-document summarize-comments test clean clean-comments setup

## Run the full pipeline: fetch → normalize → summarize
all: fetch normalize summarize

## Install dependencies with uv
setup:
	uv sync

## Fetch both the document and public comments
fetch: fetch-document fetch-comments

## Download the EAC draft audit standards document
fetch-document:
	uv run python src/fetch_document.py

## Download all public comments from Regulations.gov
fetch-comments:
	uv run python src/fetch_comments.py

## Normalize raw comments into structured CSV / JSONL
normalize:
	uv run python src/normalize_comments.py

## Generate both summaries
summarize: summarize-document summarize-comments

## Generate a Markdown summary of the draft standards document
summarize-document:
	uv run python src/summarize_document.py

## Generate a Markdown summary of the public comments
summarize-comments:
	uv run python src/summarize_comments.py

## Run the test suite
test:
	uv run pytest tests/ -v

## Run the full pipeline using local fixture data (no network required)
demo:
	uv run python scripts/make_demo_data.py
	uv run python src/normalize_comments.py
	uv run python src/summarize_document.py
	uv run python src/summarize_comments.py
	@echo ""
	@echo "=== Pipeline complete. Outputs ==="
	@echo "  data/processed/comments.csv"
	@echo "  data/processed/comments.jsonl"
	@echo "  data/processed/document_text.txt"
	@echo "  data/summaries/document_summary.md"
	@echo "  data/summaries/comments_summary.md"

## Remove all generated data files (keeps directory structure)
clean:
	rm -f data/raw/*.json data/raw/*.jsonl data/raw/*.docx data/raw/*.pdf data/raw/*.doc
	rm -rf data/raw/attachments
	rm -f data/processed/*.csv data/processed/*.jsonl data/processed/*.txt
	rm -f data/summaries/*.md
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

## Re-fetch comments and attachments only (keep document)
clean-comments:
	rm -f data/raw/comments*.json data/raw/comments*.jsonl
	rm -rf data/raw/attachments
