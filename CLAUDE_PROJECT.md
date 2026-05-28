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
Extracted text lives at `data/processed/attachments/{comment-id}/attachment_N.md`. The directory name is the comment ID, matching the CSV's `id` column. For comments where `comment_text` is a stub like "See attached file(s)", the attachment is the entire submission.

The raw binary files in `data/raw/attachments/` are not parseable by Claude Projects — use the `.md` versions under `data/processed/`.

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

## How to search for attachment content

**Use topical words from the document itself — not the commenter's name, not "attachment," not the file path.**

The search tool retrieves content. This file and the CSV are indexed under commenter names, so name-based searches almost always return metadata rather than the actual submission.

- **Works:** `credentialing election auditors competent` → finds Kresse's document
- **Doesn't work:** `Kresse attachment` → finds this index file and the CSV row

Use 3–5 distinctive words you'd expect to appear in the actual text. For organizations, search for their known positions or subject matter rather than their name.

---

## Comments with attachments

16 comments include file attachments. For stub-text entries the attachment is the full submission. Attachment text is extracted to `data/processed/attachments/{comment-id}/attachment_N.md`.

| Comment ID | Submitter | Subject / notes |
|---|---|---|
| EAC-2026-0067-0039 | Chris Bystroff | stub; full comment in attachment |
| EAC-2026-0067-0044 | Michigan Fair Elections Institute | substantive CSV text + supporting attachment |
| EAC-2026-0067-0047 | Mark Vaeth | substantive CSV text + 2 attachments |
| EAC-2026-0067-0049 | Victoria Cruz | stub; expertise/implementation focus — **distinct from 0070** (voter rolls) |
| EAC-2026-0067-0051 | Gregory Buck | stub; 3-point comment on independence and procedural audits |
| EAC-2026-0067-0053 | America First Legal Foundation | stub; partisan/legal objections |
| EAC-2026-0067-0055 | Honest Elections Project | stub; supportive with two specific suggestions |
| EAC-2026-0067-0056 | Michael Raisch | substantive CSV text + redline-edited draft (attachment_1) + separate PDF (attachment_2) |
| EAC-2026-0067-0058 | Verified Voting | stub; detailed substantive comment on independence, sampling, definitions |
| EAC-2026-0067-0059 | The Elections Group | stub; 2 attachments (nearly identical versions); supportive with standard-by-standard analysis |
| EAC-2026-0067-0062 | Citizens Oversight, Inc. | stub; 2 attachments; critical/skeptical perspective |
| EAC-2026-0067-0063 | John Droz | short CSV text + attachment with detailed technical objections |
| EAC-2026-0067-0065 | William Kresse | stub; proposes credentialing election auditors |
| EAC-2026-0067-0066 | Paul Burke | stub |
| EAC-2026-0067-0068 | Center for Election Confidence, Inc. | short CSV text + attachment |
| EAC-2026-0067-0069 | Neal McBurnett | stub; risk-limiting audit focus |

**Note on Cruz:** Comment 0049 (stub, focuses on expertise and implementation of audit standards) and comment 0070 (inline text, focuses on voter roll integrity and alleged algorithmic manipulation) are from the same person but are substantively distinct. Do not conflate them.

---

## How to use this project

**For a specific commenter's position:** check the table above to see if they have an attachment, then search for the substance using topical words (see search guidance above). The `comment_text` field in the CSV is complete for the 55 non-attachment comments; for the 16 above, the `.md` extraction is the primary source.

**For cross-cutting themes:** `data/summaries/comments_summary.md` covers all submissions including attachment text. `data/processed/comments.csv` has `comment_text` for all 71 — complete for the 55 inline comments, stubs only for the 16 with attachments.

**For the draft document itself:** read `data/processed/eac_draft_audit_standards.md` for the full text in Markdown form.
