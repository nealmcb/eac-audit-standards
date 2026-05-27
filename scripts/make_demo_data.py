"""
Generate realistic demo/fixture data so the pipeline can run end-to-end
without network access.

Creates:
  data/raw/eac_draft_audit_standards.docx   — synthetic draft standards document
  data/raw/comments.jsonl                   — synthetic public comments
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

from utils import DATA_RAW, ensure_dirs

try:
    from docx import Document
    from docx.shared import Pt
except ImportError:
    print("python-docx not installed — run `uv sync` first.", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Synthetic draft document
# ---------------------------------------------------------------------------

DOCUMENT_CONTENT = [
    ("Heading 1", "Introduction"),
    ("Normal", (
        "The Election Assistance Commission (EAC) is publishing these Voluntary National "
        "Election Audit Standards (VNEAS) to provide guidance to state and local election "
        "officials on best practices for conducting post-election audits. These standards are "
        "voluntary and are intended to supplement, not replace, existing state laws and "
        "regulations governing election audits."
    )),
    ("Heading 1", "Scope and Purpose"),
    ("Normal", (
        "These standards apply to audits of federal elections conducted by state and local "
        "election officials. The purpose of post-election audits is to verify the accuracy of "
        "reported election results and to identify potential errors or anomalies that may "
        "warrant further investigation."
    )),
    ("Heading 2", "Definitions"),
    ("Normal", (
        "For the purposes of these standards, the following definitions apply: "
        "'Audit' means a systematic examination of election records, processes, or outcomes "
        "to verify accuracy and identify discrepancies. "
        "'Risk-Limiting Audit (RLA)' means a statistical audit method that provides a "
        "known level of confidence that the reported winner is the true winner."
    )),
    ("Heading 1", "Standard 1: Pre-Audit Planning"),
    ("Normal", (
        "Election officials should establish and document audit procedures in advance of "
        "the election. Pre-audit planning should include selection of audit method, "
        "determination of sample size, identification of responsible personnel, and "
        "establishment of public observation procedures."
    )),
    ("Heading 2", "1.1 Audit Method Selection"),
    ("Normal", (
        "Jurisdictions should select an audit method appropriate to their resources and "
        "legal requirements. Acceptable methods include ballot polling audits, "
        "comparison audits, risk-limiting audits (RLAs), and full hand counts. "
        "Risk-limiting audits are strongly recommended as the preferred approach due to "
        "their statistical rigor and efficiency."
    )),
    ("Heading 2", "1.2 Sample Size Determination"),
    ("Normal", (
        "The sample size for a ballot polling or comparison audit should be determined "
        "using accepted statistical methods that account for the margin of victory, "
        "the desired confidence level, and the total number of ballots cast. "
        "For risk-limiting audits, the sample size is determined by the audit risk limit "
        "and the reported margin."
    )),
    ("Heading 1", "Standard 2: Audit Execution"),
    ("Normal", (
        "Audits should be conducted in a transparent manner with opportunities for public "
        "observation. All audit activities should be documented, including the selection "
        "of ballots for review, the comparison of ballot markings to tabulated results, "
        "and any discrepancies identified."
    )),
    ("Heading 2", "2.1 Chain of Custody"),
    ("Normal", (
        "Election officials must maintain a documented chain of custody for all ballots "
        "and audit materials from the time of ballot casting through the conclusion of "
        "the audit. Any breaks in chain of custody must be documented and explained."
    )),
    ("Heading 2", "2.2 Public Observation"),
    ("Normal", (
        "Audits should be conducted in a public setting with adequate space for observers. "
        "Public notice of audit times, locations, and procedures should be provided at "
        "least 48 hours in advance. Observers should be permitted to view all audit "
        "activities without disrupting the process."
    )),
    ("Heading 1", "Standard 3: Reporting and Certification"),
    ("Normal", (
        "Upon completion of the audit, election officials should publish a detailed "
        "report including the audit method used, the number of ballots examined, "
        "any discrepancies found, and a determination of whether the reported results "
        "were confirmed or require further review."
    )),
    ("Heading 2", "3.1 Discrepancy Resolution"),
    ("Normal", (
        "When discrepancies are identified between audited and reported results, election "
        "officials should investigate the source of the discrepancy and document their "
        "findings. Discrepancies exceeding established thresholds should trigger "
        "expanded auditing or a full hand count."
    )),
    ("Heading 1", "Standard 4: Technology and Equipment"),
    ("Normal", (
        "Voting systems used in elections subject to these audit standards should be "
        "certified by the EAC and maintain cast vote records (CVRs) in a format suitable "
        "for audit purposes. Election officials should ensure that all voting equipment "
        "is properly maintained and tested prior to each election."
    )),
    ("Heading 1", "Appendix A: Statistical Methods"),
    ("Normal", (
        "This appendix provides additional guidance on statistical methods for "
        "risk-limiting audits, including formulas for calculating sample sizes and "
        "stopping conditions for ballot-polling and comparison audits."
    )),
    ("Heading 1", "Appendix B: Sample Audit Forms"),
    ("Normal", (
        "This appendix contains sample forms for documenting audit activities, "
        "including ballot tally sheets, chain-of-custody forms, and discrepancy "
        "reporting templates."
    )),
]


def make_docx(dest: pathlib.Path) -> None:
    doc = Document()
    doc.core_properties.title = "Voluntary National Election Audit Standards — Draft"
    doc.core_properties.author = "U.S. Election Assistance Commission"

    for style, text in DOCUMENT_CONTENT:
        doc.add_paragraph(text, style=style)

    doc.save(str(dest))
    print(f"Created {dest} ({dest.stat().st_size:,} bytes)")


# ---------------------------------------------------------------------------
# Synthetic comments
# ---------------------------------------------------------------------------

COMMENTS = [
    {
        "id": "EAC-2026-0067-0001",
        "organization": "",
        "firstName": "Alice",
        "lastName": "Nguyen",
        "postedDate": "2026-03-15",
        "comment": (
            "I strongly support the adoption of risk-limiting audits as the preferred "
            "audit method. RLAs provide a statistically rigorous way to verify election "
            "results and are far more efficient than full hand counts for large jurisdictions. "
            "However, I am concerned that the draft standards do not provide sufficient "
            "guidance on how to handle jurisdictions that use ballot-marking devices (BMDs). "
            "For BMDs, the audit must verify both the paper record and the electronic record. "
            "I recommend adding a specific section on BMD audits."
        ),
    },
    {
        "id": "EAC-2026-0067-0002",
        "organization": "National Election Defense Coalition",
        "firstName": "Robert",
        "lastName": "Martinez",
        "postedDate": "2026-03-16",
        "comment": (
            "The National Election Defense Coalition appreciates the EAC's effort to "
            "establish voluntary audit standards. We strongly urge the Commission to "
            "make risk-limiting audits mandatory rather than merely recommended. "
            "Without mandatory RLAs, many jurisdictions will continue to rely on "
            "less rigorous audit methods that do not provide meaningful verification "
            "of election outcomes. We also recommend that the standards explicitly "
            "address the audit of mail-in ballots and provisional ballots, which are "
            "often underrepresented in audit samples."
        ),
    },
    {
        "id": "EAC-2026-0067-0003",
        "organization": "State Election Directors Association",
        "firstName": "Patricia",
        "lastName": "Okonkwo",
        "postedDate": "2026-03-17",
        "comment": (
            "As election directors, we appreciate the EAC's recognition that these "
            "standards must be voluntary to accommodate the diversity of state laws. "
            "However, we are concerned about the resource requirements for implementing "
            "risk-limiting audits in smaller jurisdictions. Many counties lack the "
            "technical expertise and staffing to conduct RLAs without significant "
            "additional support. We recommend that the EAC provide training resources, "
            "software tools, and funding assistance to help jurisdictions implement "
            "these standards. We also request clarification on the chain-of-custody "
            "requirements, as these vary significantly across states."
        ),
    },
    {
        "id": "EAC-2026-0067-0004",
        "organization": "",
        "firstName": "James",
        "lastName": "Thornton",
        "postedDate": "2026-03-18",
        "comment": (
            "The transparency requirements in Standard 2.2 are excellent. Public "
            "observation of audits is critical for voter confidence. I recommend "
            "strengthening the public notice requirement to at least 72 hours in "
            "advance rather than 48 hours. Additionally, the standards should require "
            "that audit results be published online within 30 days of the election."
        ),
    },
    {
        "id": "EAC-2026-0067-0005",
        "organization": "Verified Voting Foundation",
        "firstName": "Susan",
        "lastName": "Bernstein",
        "postedDate": "2026-03-19",
        "comment": (
            "The Verified Voting Foundation has long advocated for paper-based voting "
            "systems that support meaningful post-election audits. We are pleased that "
            "the draft standards emphasize risk-limiting audits and cast vote records. "
            "We urge the EAC to add explicit requirements that all voting systems used "
            "in audited elections produce human-readable paper records. Without paper "
            "records, no audit can truly verify the will of the voters. We also "
            "recommend adding requirements for the retention and security of ballot "
            "materials during the audit period."
        ),
    },
    {
        "id": "EAC-2026-0067-0006",
        "organization": "American Statistical Association",
        "firstName": "David",
        "lastName": "Chen",
        "postedDate": "2026-03-20",
        "comment": (
            "The American Statistical Association commends the EAC for incorporating "
            "sound statistical methodology into these draft standards. The references "
            "to risk-limiting audits and sample size determination in Appendix A are "
            "technically sound. We recommend that the EAC adopt specific statistical "
            "confidence thresholds — we suggest a risk limit of 5% as the default — "
            "rather than leaving this to jurisdictional discretion. We also note that "
            "the appendix should reference current peer-reviewed literature on RLA "
            "methods, including ballot-polling, comparison, and SUITE audit approaches."
        ),
    },
    {
        "id": "EAC-2026-0067-0007",
        "organization": "",
        "firstName": "Maria",
        "lastName": "Rodriguez",
        "postedDate": "2026-03-21",
        "comment": (
            "These standards are a step in the right direction. My main concern is "
            "accessibility for voters with disabilities. The public observation "
            "requirements should specify that audit locations must be accessible "
            "under the Americans with Disabilities Act. All audit materials should "
            "also be available in accessible formats."
        ),
    },
    {
        "id": "EAC-2026-0067-0008",
        "organization": "Common Cause",
        "firstName": "Thomas",
        "lastName": "Jackson",
        "postedDate": "2026-03-22",
        "comment": (
            "Common Cause supports strong, transparent post-election audits as a "
            "cornerstone of election integrity. We strongly support the transparency "
            "and public observation requirements in Standard 2.2. We urge the EAC "
            "to add requirements for independent observers from civic organizations "
            "and political parties. The audit process should not be conducted solely "
            "by election officials without independent verification. We also recommend "
            "that the standards address the audit of early voting and absentee ballot "
            "tabulation, which are increasingly significant components of election results."
        ),
    },
    {
        "id": "EAC-2026-0067-0009",
        "organization": "League of Women Voters",
        "firstName": "Barbara",
        "lastName": "Williams",
        "postedDate": "2026-03-23",
        "comment": (
            "The League of Women Voters appreciates the EAC's commitment to strengthening "
            "election integrity through voluntary audit standards. We support the inclusion "
            "of risk-limiting audits as the preferred method and the strong transparency "
            "requirements. We urge the Commission to also address the timeline for "
            "completing audits, recommending that audits be completed before election "
            "certification where possible. Delays in the audit process should not be "
            "used to justify certifying results that have not been adequately verified."
        ),
    },
    {
        "id": "EAC-2026-0067-0010",
        "organization": "",
        "firstName": "Kevin",
        "lastName": "O'Brien",
        "postedDate": "2026-03-24",
        "comment": (
            "I am a software engineer who works on election technology. The standards "
            "for technology and equipment in Standard 4 are a good start but need to "
            "be more specific about cast vote record (CVR) formats. I recommend that "
            "the EAC require CVRs to be in an open, machine-readable format such as "
            "the NIST CVR Common Data Format. This would enable third-party auditing "
            "tools and improve interoperability. The current language is too vague "
            "and could allow proprietary formats that hinder independent auditing."
        ),
    },
]


def make_comments_jsonl(dest: pathlib.Path) -> None:
    with dest.open("w") as fh:
        for c in COMMENTS:
            item = {
                "id": c["id"],
                "type": "comments",
                "attributes": {
                    "title": f"Comment from {c['firstName']} {c['lastName']}".strip(),
                    "firstName": c["firstName"],
                    "lastName": c["lastName"],
                    "organization": c["organization"],
                    "postedDate": c["postedDate"],
                    "receiveDate": c["postedDate"],
                    "documentType": "Public Submission",
                    "docketId": "EAC-2026-0067",
                    "comment": c["comment"],
                    "withdrawn": False,
                    "attachmentCount": 0,
                    "agencyId": "EAC",
                },
            }
            fh.write(json.dumps(item) + "\n")
    print(f"Created {dest} ({len(COMMENTS)} comments)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ensure_dirs()
    make_docx(DATA_RAW / "eac_draft_audit_standards.docx")
    make_comments_jsonl(DATA_RAW / "comments.jsonl")
    print("Demo data ready. Run `make normalize summarize` to continue the pipeline.")


if __name__ == "__main__":
    main()
