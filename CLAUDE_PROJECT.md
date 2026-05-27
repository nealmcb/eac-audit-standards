# EAC Election Audit Standards — Claude Project Guide

## What this is

This repository contains the full public record for **EAC docket EAC-2026-0067**, the U.S. Election Assistance Commission's request for comment on its draft *Voluntary National Standards for Election Audits — A Practical Guide*.

The comment period closed in late April/early May 2026. There are **71 public comments** from individuals and organizations.

---

## Files in this project

### The draft document
- `data/processed/eac_draft_audit_standards.md` — **readable Markdown extraction** (use this)
- `data/processed/document_text.txt` — plain-text extraction (older, less structured)
- `data/raw/eac_draft_audit_standards.docx` — original binary (not parseable by Claude Projects)
- `data/summaries/document_summary.md` — structured outline with headings preserved

The document has six top-level sections: Executive Summary, Introduction, Using the Standards, Standards Framework, Discussion of Standards (the bulk — organized into four topics: Objective, Effective, Secure, Accountable), and a closing section. Each standard entry has a statement, a Discussion section, Considerations, and Sample Language.

### Comments dataset
- `data/processed/comments.csv` — one row per comment; columns: `id`, `title`, `first_name`, `last_name`, `organization`, `submitted_date`, `comment_text`, `has_attachments`, `attachment_count`, `attachment_paths`
- `data/processed/comments.jsonl` — same data as newline-delimited JSON
- `data/raw/comments.jsonl` — full raw API responses (includes all original fields)

### PDF/DOCX attachments (extracted)
`data/processed/attachments/{comment-id}/attachment_N.md` — **readable Markdown extractions** (use these). The directory name is the comment ID, matching the CSV's `id` column. For comments where `comment_text` is a stub like "See attached file(s)", the attachment is the entire submission.

The raw binary files in `data/raw/attachments/` are the originals but **not parseable by Claude Projects** — always use the `.md` versions under `data/processed/`.

---

## What to include when importing this repo into a Claude Project

Claude Projects cannot parse binary files from GitHub — PDFs and DOCX files are silently skipped. Import only the files Claude can actually read:

**Include:**
- `data/processed/` — all `.md` extractions, `comments.csv`, `comments.jsonl`
- `data/summaries/` — `document_summary.md`, `comments_summary.md`
- `data/raw/comments.jsonl` — full raw API responses; useful if you need original fields not in the processed CSV (submitter metadata, raw comment structure)
- `CLAUDE_PROJECT.md`, `README.md`

**Exclude (Claude can't read these):**
- `data/raw/attachments/` — binary PDFs and DOCXs; the `.md` extractions in `data/processed/attachments/` cover everything
- `data/raw/eac_draft_audit_standards.docx` — binary; `data/processed/eac_draft_audit_standards.md` is the readable version
- `data/raw/comments_page_*.json` — redundant with `data/raw/comments.jsonl`

---

## Attachment index

The following 16 comments include file attachments. For stub-text entries the PDF/DOCX *is* the comment — read the file for the submitter's actual position.

| Comment ID | Submitter | Text in CSV | Extracted Markdown |
|---|---|---|---|
| EAC-2026-0067-0039 | Chris Bystroff | stub | `data/processed/attachments/EAC-2026-0067-0039/attachment_1.md` |
| EAC-2026-0067-0044 | Michigan Fair Elections Institute | substantive (also has attachment) | `data/processed/attachments/EAC-2026-0067-0044/attachment_1.md` |
| EAC-2026-0067-0047 | Mark Vaeth | substantive (also has attachments) | `…/EAC-2026-0067-0047/attachment_1.md`, `attachment_2.md` |
| EAC-2026-0067-0049 | Victoria Cruz | stub | `data/processed/attachments/EAC-2026-0067-0049/attachment_1.md` |
| EAC-2026-0067-0051 | Gregory Buck | stub | `data/processed/attachments/EAC-2026-0067-0051/attachment_1.md` |
| EAC-2026-0067-0053 | America First Legal Foundation | stub | `data/processed/attachments/EAC-2026-0067-0053/attachment_1.md` |
| EAC-2026-0067-0055 | Honest Elections Project | stub | `data/processed/attachments/EAC-2026-0067-0055/attachment_1.md` |
| EAC-2026-0067-0056 | Michael Raisch | substantive text + redline edits | `…/EAC-2026-0067-0056/attachment_1.md` (redline), `attachment_2.md` |
| EAC-2026-0067-0058 | Verified Voting | stub | `data/processed/attachments/EAC-2026-0067-0058/attachment_1.md` |
| EAC-2026-0067-0059 | The Elections Group | stub | `…/EAC-2026-0067-0059/attachment_1.md`, `attachment_2.md` |
| EAC-2026-0067-0062 | Citizens Oversight, Inc. | stub | `…/EAC-2026-0067-0062/attachment_1.md`, `attachment_2.md` |
| EAC-2026-0067-0063 | John Droz | short text + see attachment | `data/processed/attachments/EAC-2026-0067-0063/attachment_1.md` |
| EAC-2026-0067-0065 | William Kresse | stub | `data/processed/attachments/EAC-2026-0067-0065/attachment_1.md` |
| EAC-2026-0067-0066 | Paul Burke | stub | `data/processed/attachments/EAC-2026-0067-0066/attachment_1.md` |
| EAC-2026-0067-0068 | Center for Election Confidence, Inc. | short text + see attachment | `data/processed/attachments/EAC-2026-0067-0068/attachment_1.md` |
| EAC-2026-0067-0069 | Neal McBurnett | stub | `data/processed/attachments/EAC-2026-0067-0069/attachment_1.md` |

---

## How to use this project

**For a specific commenter's position:** look up their comment ID in the table above, then read the corresponding `data/processed/attachments/{id}/attachment_N.md` file. The `comment_text` field in the CSV is reliable for the 55 non-attachment comments; for the 16 above, treat the `.md` extraction as the primary source.

**For cross-cutting themes:** `data/processed/comments.csv` has clean plain-text `comment_text` for all 71 comments. The 55 without attachments are fully represented there. The 16 with attachments are partially represented (stubs) — supplement with the extracted `.md` files.

**For the draft document itself:** read `data/processed/eac_draft_audit_standards.md` for the full text in Markdown form.

**Summary of the public record:** `data/summaries/comments_summary.md` gives top themes and representative excerpts across all 71 comment texts.
