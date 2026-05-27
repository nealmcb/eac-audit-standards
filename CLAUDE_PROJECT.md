# EAC Election Audit Standards — Claude Project Guide

## What this is

This repository contains the full public record for **EAC docket EAC-2026-0067**, the U.S. Election Assistance Commission's request for comment on its draft *Voluntary National Standards for Election Audits — A Practical Guide*.

The comment period closed in late April/early May 2026. There are **71 public comments** from individuals and organizations.

---

## Files in this project

### The draft document
- `data/raw/eac_draft_audit_standards.docx` — the full draft document (authoritative source)
- `data/processed/document_text.txt` — plain-text extraction of the same document
- `data/summaries/document_summary.md` — structured outline with headings preserved

The document has six top-level sections: Executive Summary, Introduction, Using the Standards, Standards Framework, Discussion of Standards (the bulk — organized into four topics: Objective, Effective, Secure, Accountable), and a closing section. Each standard entry has a statement, a Discussion section, Considerations, and Sample Language.

### Comments dataset
- `data/processed/comments.csv` — one row per comment; columns: `id`, `title`, `first_name`, `last_name`, `organization`, `submitted_date`, `comment_text`, `has_attachments`, `attachment_count`, `attachment_paths`
- `data/processed/comments.jsonl` — same data as newline-delimited JSON
- `data/raw/comments.jsonl` — full raw API responses (includes all original fields)

### PDF/DOCX attachments
`data/raw/attachments/{comment-id}/` — files submitted alongside the comment. **The directory name is the comment ID**, so you can cross-reference directly with the CSV's `id` column. For comments where `comment_text` is a stub like "See attached file(s)", the attachment is the entire submission.

---

## Attachment index

The following 16 comments include file attachments. For stub-text entries the PDF/DOCX *is* the comment — read the file for the submitter's actual position.

| Comment ID | Submitter | Text in CSV | Files |
|---|---|---|---|
| EAC-2026-0067-0039 | Chris Bystroff | stub — see PDF/DOCX | `attachments/EAC-2026-0067-0039/attachment_1.pdf`, `attachment_1.docx` |
| EAC-2026-0067-0044 | Michigan Fair Elections Institute | substantive (also has PDF) | `attachments/EAC-2026-0067-0044/attachment_1.pdf` |
| EAC-2026-0067-0047 | Mark Vaeth | substantive (also has attachments) | `attachments/EAC-2026-0067-0047/attachment_1.pdf`, `attachment_1.docx`, `attachment_2.pdf` |
| EAC-2026-0067-0049 | Victoria Cruz | stub — see PDF/DOCX | `attachments/EAC-2026-0067-0049/attachment_1.pdf`, `attachment_1.docx` |
| EAC-2026-0067-0051 | Gregory Buck | stub — see PDF/DOCX | `attachments/EAC-2026-0067-0051/attachment_1.pdf`, `attachment_1.docx` |
| EAC-2026-0067-0053 | America First Legal Foundation | stub — see PDF | `attachments/EAC-2026-0067-0053/attachment_1.pdf` |
| EAC-2026-0067-0055 | Honest Elections Project | stub — see PDF | `attachments/EAC-2026-0067-0055/attachment_1.pdf` |
| EAC-2026-0067-0056 | Michael Raisch | substantive text + redline edits | `attachments/EAC-2026-0067-0056/attachment_1.pdf`, `attachment_1.docx` (redline), `attachment_2.pdf` |
| EAC-2026-0067-0058 | Verified Voting | stub — see PDF | `attachments/EAC-2026-0067-0058/attachment_1.pdf` |
| EAC-2026-0067-0059 | The Elections Group | stub — see PDFs | `attachments/EAC-2026-0067-0059/attachment_1.pdf`, `attachment_2.pdf` |
| EAC-2026-0067-0062 | Citizens Oversight, Inc. | stub — see PDFs | `attachments/EAC-2026-0067-0062/attachment_1.pdf`, `attachment_2.pdf` |
| EAC-2026-0067-0063 | John Droz | short text + see PDF | `attachments/EAC-2026-0067-0063/attachment_1.pdf` |
| EAC-2026-0067-0065 | William Kresse | stub — see PDF | `attachments/EAC-2026-0067-0065/attachment_1.pdf` |
| EAC-2026-0067-0066 | Paul Burke | stub — see PDF | `attachments/EAC-2026-0067-0066/attachment_1.pdf` |
| EAC-2026-0067-0068 | Center for Election Confidence, Inc. | short text + see PDF | `attachments/EAC-2026-0067-0068/attachment_1.pdf` |
| EAC-2026-0067-0069 | Neal McBurnett | stub — see PDF | `attachments/EAC-2026-0067-0069/attachment_1.pdf` |

---

## How to use this project

**For a specific commenter's position:** look up their comment ID in the table above, then read the corresponding PDF or DOCX file. The `comment_text` field in the CSV is reliable for the 55 non-attachment comments; for the 16 above, treat the file as the primary source.

**For cross-cutting themes:** `data/processed/comments.csv` has clean plain-text `comment_text` for all 71 comments. The 55 without attachments are fully represented there. The 16 with attachments are partially represented (stubs) — supplement with the PDFs.

**For the draft document itself:** read `data/raw/eac_draft_audit_standards.docx` end-to-end for the authoritative text. `data/processed/document_text.txt` is a plain-text extraction if you need searchable prose.

**Summary of the public record:** `data/summaries/comments_summary.md` gives top themes and representative excerpts across all 71 comment texts.
