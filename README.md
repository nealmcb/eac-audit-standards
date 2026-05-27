# eac-audit-standards

Pipeline to download, normalize, and summarize public comments submitted on the U.S. Election Assistance Commission (EAC) Voluntary National Election Audit Standards docket.

## Scope

This repository is designed to:

- download the draft audit standards document
- download all public comments for the target Regulations.gov docket
- preserve raw responses and source artifacts
- normalize comments into structured datasets
- summarize the draft standards themselves
- summarize public comments in the context of the draft standards
- generate Markdown reports for review

## Target sources

- **Docket ID:** `EAC-2026-0067`
- **Draft standards document:** EAC-hosted Word document referenced by the Federal Register correction notice
- **Primary public comments source:** Regulations.gov API/public records

## Repository layout

```text
.
├── README.md
├── .gitignore
├── requirements.txt
├── Makefile
├── .env.example
├── config/
│   └── docket.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── summaries/
├── src/
│   ├── fetch_document.py
│   ├── fetch_comments.py
│   ├── normalize_comments.py
│   ├── summarize_document.py
│   ├── summarize_comments.py
│   └── utils.py
└── tests/
    └── test_normalize.py
```

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it, then install dependencies:

```bash
uv sync
```

Copy the example environment file. Optionally add a [Regulations.gov API key](https://open.gsa.gov/api/regulationsgov/) to get higher rate limits:

```bash
cp .env.example .env
# edit .env and set REGULATIONS_GOV_API_KEY (optional)
```

## Running the pipeline

Run every step in sequence:

```bash
make all
```

Or run steps individually:

```bash
make fetch-document     # download the EAC draft standards document
make fetch-comments     # download all public comments from Regulations.gov
make normalize          # normalize comments → CSV + JSONL
make summarize          # generate Markdown summaries
```

### Offline / demo mode

If you don't have a network connection or an API key yet, you can try the pipeline with synthetic fixture data:

```bash
make demo
```

This generates a realistic mock `.docx` and comment set, then runs the full normalize → summarize pipeline.

## Running tests

```bash
make test
```

## Pipeline steps

### 1. Download the draft standards

```bash
uv run python src/fetch_document.py
```

Queries Regulations.gov for supporting documents in the docket and downloads the first `.docx`/`.pdf` found into `data/raw/`. Override with a direct URL via `document.url` in `config/docket.yaml`.

### 2. Download public comments

```bash
uv run python src/fetch_comments.py
```

Pages through all public comments on Regulations.gov for the docket, saving each raw API page to `data/raw/comments_page_NNNN.json` and a consolidated `data/raw/comments.jsonl`.

### 3. Normalize comments

```bash
uv run python src/normalize_comments.py
```

Reads `data/raw/comments.jsonl`, cleans text, and writes `data/processed/comments.csv` and `data/processed/comments.jsonl` with a consistent schema.

### 4. Summarize the standards document

```bash
uv run python src/summarize_document.py
```

Extracts paragraphs from the downloaded `.docx`, preserves heading structure, and writes `data/summaries/document_summary.md`. Also saves full plain text to `data/processed/document_text.txt`.

### 5. Summarize comments

```bash
uv run python src/summarize_comments.py
```

Loads normalized comments, computes word-frequency theme analysis (stop words removed), and writes `data/summaries/comments_summary.md` with top themes and representative excerpts.

## Notes

- This MVP does not depend on proprietary APIs.
- If the draft document remains `.docx`, the first version stores it and extracts basic readable text where possible.
- Attachment text extraction for submitted PDFs can be added later.
- Optional LLM-based summarization can be layered in later behind environment variables.
