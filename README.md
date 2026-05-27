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

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
make all
```

## Pipeline steps

### 1. Download the draft standards

```bash
python src/fetch_document.py
```

This downloads the draft standards document configured in `config/docket.yaml` into `data/raw/`.

### 2. Download public comments

```bash
python src/fetch_comments.py
```

This fetches all public comments visible for the target docket and stores raw JSON pages and a combined JSONL dataset.

### 3. Normalize comments

```bash
python src/normalize_comments.py
```

This creates a structured CSV/JSONL export with core comment metadata and cleaned text fields.

### 4. Summarize the standards document

```bash
python src/summarize_document.py
```

This produces a plain-language summary of the draft audit standards for use as context.

### 5. Summarize comments

```bash
python src/summarize_comments.py
```

This generates an overall comment summary and organizes feedback by major topic areas.

## Notes

- This MVP does not depend on proprietary APIs.
- If the draft document remains `.docx`, the first version stores it and extracts basic readable text where possible.
- Attachment text extraction for submitted PDFs can be added later.
- Optional LLM-based summarization can be layered in later behind environment variables.
