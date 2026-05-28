# EAC Voluntary National Standards for Election Audits — Public Comment Record

> **AI-generated analysis, lightly reviewed by a human.** The comment analysis below was produced by an AI assistant (Claude) using the full text of all public submissions. It has been reviewed but not exhaustively fact-checked.

**Docket:** [EAC-2026-0067](https://www.regulations.gov/docket/EAC-2026-0067) · U.S. Election Assistance Commission  
**Comment period closed:** late April / early May 2026  
**Public comments analyzed:** 67

---

# [→ Comment Analysis](https://nealmcb.github.io/eac-audit-standards/insights/EAC-audit-draft_Comment_analysis)

Comprehensive analysis of all 67 public submissions on the EAC's draft *Voluntary National Standards for Election Audits*. Includes:

- **Executive Summary** — who commented, what they agreed on, the four clearest actionable recommendations, and the unresolved tensions
- **Topical Synthesis** — independence, RLAs, transparency, discrepancy resolution, credentialing, scope, and six other major themes
- **Findings and Recommendations** — the clearest mandates from commenters and the hardest tradeoffs
- **Summary Table** — all 71 docket entries with one-line summaries and direct links to Regulations.gov
- **Individual Entries** — detailed analysis of each submission with links to PDF/DOCX attachments

---

### Key documents

| Document | Link |
|---|---|
| Draft audit standards (full text) | [Markdown](data/processed/eac_draft_audit_standards.md) · [DOCX](data/raw/eac_draft_audit_standards.docx) |
| Comment analysis | [GitHub Pages](https://nealmcb.github.io/eac-audit-standards/insights/EAC-audit-draft_Comment_analysis) · [Markdown source](insights/EAC-audit-draft_Comment_analysis.md) |
| All comments (structured) | [CSV](data/processed/comments.csv) · [JSONL](data/processed/comments.jsonl) |

---

## Pipeline

Pipeline to download, normalize, and summarize public comments submitted on the U.S. Election Assistance Commission (EAC) Voluntary National Election Audit Standards docket.

## Scope

This repository is designed to:

- download the draft audit standards document
- download all public comments for the target Regulations.gov docket
- preserve raw responses and source artifacts
- extract text from PDF and DOCX attachments into Markdown
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
│   │   ├── eac_draft_audit_standards.docx
│   │   └── attachments/{comment-id}/attachment_N.{pdf,docx}
│   ├── processed/
│   │   ├── eac_draft_audit_standards.md      ← extracted Markdown
│   │   ├── comments/{comment-id}.md          ← per-comment pages (primary)
│   │   ├── attachments/{comment-id}/attachment_N.md
│   │   ├── comments.csv
│   │   └── comments.jsonl
│   └── summaries/
├── scripts/
│   └── extract_documents.py
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
make extract            # extract text from PDF/DOCX attachments → Markdown
make normalize          # normalize comments → CSV + JSONL
make build-pages        # build one .md per comment (metadata + text + attachments merged)
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

### 3. Extract attachment text

```bash
uv run python scripts/extract_documents.py
```

Converts all PDF and DOCX files under `data/raw/attachments/` and `data/raw/eac_draft_audit_standards.docx` into Markdown under `data/processed/`, mirroring the raw directory structure. For PDFs, tries MarkItDown (pdfminer.six) first; falls back to PyMuPDF4LLM + Tesseract OCR for scanned/image-only PDFs. Uses MarkItDown for DOCX. When both formats exist for the same attachment, DOCX is preferred. Pass `--force` to re-extract files that already have output.

### 4. Normalize comments

```bash
uv run python src/normalize_comments.py
```

Reads `data/raw/comments.jsonl`, cleans text, and writes `data/processed/comments.csv` and `data/processed/comments.jsonl` with a consistent schema.

### 5. Summarize the standards document

```bash
uv run python src/summarize_document.py
```

Extracts paragraphs from the downloaded `.docx`, preserves heading structure, and writes `data/summaries/document_summary.md`. Also saves full plain text to `data/processed/document_text.txt`.

### 6. Summarize comments

```bash
uv run python src/summarize_comments.py
```

Loads normalized comments, computes word-frequency theme analysis (stop words removed), and writes `data/summaries/comments_summary.md` with top themes and representative excerpts.

## Notes

- This MVP does not depend on proprietary APIs.
- Attachment text extraction uses PyMuPDF4LLM (PDF) and MarkItDown (DOCX). Tesseract OCR is used automatically for scanned PDFs.
- Claude Projects cannot parse binary files from GitHub; the extracted `.md` files under `data/processed/` are the Claude-readable versions.
- Optional LLM-based summarization can be layered in later behind environment variables.
