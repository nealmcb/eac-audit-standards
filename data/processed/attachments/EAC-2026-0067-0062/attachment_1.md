## **Comment on: Election Audit Standards** 

Submitted by: Raymond Lutz, Citizens Oversight ( https://citizensoversight.org ) Contact: raylutz@citizensoversight.org (619-820-5321) Date: April 27, 2026 

REF: M2053 

This comment is based on the following document: "Voluntary National Standards for Election Audits – A Practical Guide" Federal Register Number: 2026-03583 https://www.regulations.gov/document/EAC-2026-0067-0001 

## **Executive Summary** 

The draft provides a useful high-level framework for election auditing practices, but its content is properly characterized as a set of principles rather than operational standards. It does not define measurable procedures, conformance criteria, or implementation requirements. This distinction should be made explicit in the document itself. 

The document should be retitled to reflect its role as a principles document and should explicitly anticipate a companion set of technical standards. The scope should also be expanded to include testing activities, particularly Logic and Accuracy (L&A) testing. In addition, the document should incorporate structured mechanisms for real-time public verification, address the completeness and format of audit records, recognize multiple forms of audit evidence, and avoid implicit preference for a single audit method. 

The changes described below are intended to preserve the document’s role as a principles framework while making it more actionable, technically grounded, and aligned with real-world election processes. 

## **Title and Scope Clarification** 

The current title and framing suggest that the document defines standards, but its content does not establish enforceable or testable requirements. This should be corrected to avoid ambiguity in interpretation and use. 

The title should be revised to: 

## **Voluntary National Principles for Election Auditing and Testing** 

Page 1 

In the Introduction, a clarifying statement should be added indicating that the document defines guiding principles and that detailed procedures, formats, and conformance requirements are expected to be defined in separate technical standards documents. 

The scope should also be expanded to include testing activities. After the paragraph describing when audits may occur, the following sentence should be added: 

Pre-election and in-process testing activities, including logic and accuracy testing, are within the scope of these principles where they affect the integrity of election outcomes. 

## **Public Transparency as an Operational Requirement** 

The draft addresses transparency primarily in terms of documentation and public access. In practice, election audits and testing are often conducted by the same personnel responsible for administering the election, and full independence is not always achievable. Under these conditions, public involvement becomes a necessary component of process integrity rather than an optional feature. 

The document should introduce a new concept within the Transparency or Accountability section: 

**Public Transparency Protocol (PTP):** A scripted, in-process sequence of actions conducted in a public setting, in which critical steps are performed, explained, and documented in real time. The protocol ensures that observers can verify both the actions taken and that the recorded results accurately reflect those actions as they occur. Public Transparency Protocols are operational controls and are essential where full independence is not feasible. 

Transparency includes structured procedures that allow public verification of key steps during execution, not solely post-process reporting. 

To facilitate participation by the public, the entire process should be webcast as well as embracing in-person attendance (provide chairs, etc) and also invite the public to provide randomization selections (throw dice, select tokens, etc.) 

Page 2 

## **Real-Time Documentation and Complete Records** 

For public verification to be meaningful, documentation must be complete and contemporaneous with the actions being performed. The current draft does not explicitly require this. 

The document should add: 

All observed values, including intermediate results and repeated measurements, should be recorded as part of the official record at the time they are observed. 

Page 3 

there should be no stage in which observation or documentation occurs outside public visibility. 

Informal or temporary recording methods that are not preserved as part of the official record should not be used during procedures. Any side notes that may have been on temporary sticky notes or scratch paper should be included on the PTP documents. 

These additions ensure that the full sequence of events can be reconstructed and verified, rather than only final results. 

For example, in an audit that comprise a number of batches, then a separate PTP report would be produced for each batch, including whether the batch was counted multiple times, start and end times for count, and a comparison of the totals from the batches to the official report. 

Reports should include, when applicable: 

- Dates when audit was conducted 

- Topic(s) covered by this report 

- List of discrepancies audit found in any numbers or interpretations (usually small but not zero), and reasonable explanations. 

- Extent of audit: whether all (voters, sites, dates, contests, etc.) were covered under each topic, or random, or selective 

- Audit limitations (e.g. not able to cover some parts of the topic) and risk of missing issues (e.g. RLA risk limit) 

- Audit methods 

- Who appointed auditors: which office managed each part of the audit and where the staff came from 

- How any contractor was selected 

- Size and mix of work teams (for hand counts, site visits, etc.) 

- Links to laws, rules, contracts, guidelines and any other backup about the audit 

- Links to election results 

- Link(s) to other website(s) with relevant information, including any videos of processing, copies of tally sheets, access logs, critical reports, etc. 

## **Structured and Machine-Readable Recording** 

The draft does not address the format of audit records. This is a significant omission, as unstructured records introduce transcription errors and limit independent analysis. 

A new paragraph should be added under Transparency or Standardization: 

Page 4 

Audit and testing records should be created in structured formats that are both human-readable and machine-readable at the time of creation, enabling real-time verification and independent post-process analysis without transcription. 

Technologies such as optical mark recognition demonstrate that structured, position-based encoding of values can provide high accuracy while remaining observable and verifiable by human observers. 

Example machine readable data entry. In this example, the user would first place hand written digits in the top boxes for the value to be documented, then darken the oval next to the digit in the numeric keypad portion (like a telephone). Datamatrix code can encode the name of the value, like "BALLOTCOUNT", and serve to allow the alignment of the digit values. (This is a reference design only, and not a final standard.) 

## **Standardization and the Role of NIST** 

Although structured recording methods are well understood in other domains, no widely adopted standard exists for recording audit and testing data in election processes. This results in inconsistent practices across jurisdictions. 

The document should include the following statement: 

Development of standardized formats for audit and testing records, including structured fields and machine-readable encoding, is recommended. Collaboration with the National Institute of Standards and Technology is appropriate given its role in measurement, verification, and data integrity standards. 

Our review finds limited standardization for machine-readable data entry suitable for chain of custody and other tracking paper forms. 

This identifies a clear path toward consistent and scalable implementation without over-specifying format details within the principles document. 

## **Example: Hash Verification PTP** 

Page 5 

The document would benefit from a concrete example illustrating how these principles apply to a technical procedure. Cryptographic hash verification provides a useful case. 

For example, a Public Transparency Protocol for cryptographic hash verification may be conducted as follows: 

1. The responsible officials present the recording sheet and identify the device to be verified, including model and serial number, in view of observers. 

2. The certified hash value is obtained from an independent, authoritative source (e.g., official publication or website) in view of observers. The full value is displayed and read aloud. [This may require a device connected to the internet] 

3. The certified hash value is recorded in real time on the recording sheet in human-readable form. Observers verify that the recorded value matches the displayed value. 

4. The voting system produces its own hash value through a documented process, and is probably printed out. The resulting value is displayed and read aloud in view of observers. 

5. The device-reported hash value is recorded in real time on the same recording sheet in human-readable form. Observers verify that the recorded value matches the displayed value. 

6. A fixed subset of leading characters (e.g., the first 6–8 hexadecimal digits) from each hash value is recorded in structured fields designed for comparison and machine-readable capture. Observers verify that the subset matches the corresponding portion of the full values. 

7. The structured subset fields are compared visually to determine whether they match. The full hash values are then compared to confirm consistency. The comparison result is recorded. 

8. If any discrepancy or uncertainty arises, the process is repeated, and each result is recorded separately on the same sheet. All intermediate values and repeated measurements are preserved as part of the official record. 

9. The completed recording sheet, including all values, intermediate results, and comparison outcomes, is made available for inspection and, where applicable, scanning or digital capture. 

This procedure ensures that acquisition of values, recording of those values, and comparison of results are all observable and verifiable in real time. The use of structured fields allows both human verification during the process and reliable post-process analysis without transcription. 

This example demonstrates how real-time verification, structured recording, and public observation can be combined in practice. 

[As an attachment to this comment document, we provide a starter set of PTP procedures.] 

## **Evidence Integrity: Paper and Ballot Images** 

Page 6 

The current draft does not fully address the differing characteristics of physical ballots and ballot images. Both forms of evidence have distinct strengths and vulnerabilities. 

The document should add: 

No single form of evidence should be assumed inherently trustworthy. Physical ballots rely on chain-of-custody controls, while ballot images, when properly generated and protected, can provide a consistent and analyzable record. Audit designs should consider the strengths and limitations of each and, where feasible, incorporate multiple independent sources of evidence. 

NIST should start a project to cryptographically secure ballot images and other produced files so they cannot be altered without possible detection. 

## **Addition of Ballot Image Audits** 

The document does not currently define Ballot Image Audits, which limits its applicability to modern systems. 

The audit types section should include: 

Ballot Image Audit (BIA): An audit that utilizes the full set of ballot images produced by the voting system to evaluate results, detect anomalies such as duplication or omission, and compare interpreted outcomes with reported results, while accounting for the relationship to the underlying paper ballots. 

BIAs should include the following functionality: 

- Checking for identical images due to double uploads of images. 

- Checking hash values and signatures on ballot image files (needs standardization). 

- Comparison of results on sheet by sheet basis with the results of the voting system. 

- Reporting on all contests including focus on close contests. 

## **Ballot Accounting: Custody and Reconciliation** 

The draft references reconciliation and process auditing but does not clearly unify related concepts. In practice, chain of custody and reconciliation rely on the same records and are often evaluated together. 

The document should include: 

Ballot Accounting Audit: An audit that verifies both the secure handling of ballots (chain of custody) and the consistency of ballot counts across independent records 

Page 7 

(reconciliation). These functions rely on the same underlying documentation and may be evaluated together, while addressing distinct risks. 

## **Audit Methods and Coverage** 

The document should avoid implicitly prioritizing a single audit method. Jurisdictions employ a range of approaches, including risk-limiting audits, fixed-percentage audits, and manual tabulations, each providing different forms of assurance. 

The following should be added: 

Audit methods should be evaluated based on their coverage, scope, and ability to provide meaningful verification. Where audits focus on a limited number of contests, this limitation should be explicitly stated, and assurance should not be inferred beyond the contests examined. 

Across one or more audit activities, all contests and ballot types should receive appropriate verification. Where sampled ballots contain multiple contests, evaluate all contests present on those ballots. 

## **Transparency as In-Process Verifiability** 

The document currently treats transparency primarily as documentation and access. This should be strengthened to emphasize verifiability during execution. 

The following should be added: 

Transparency includes the ability to observe and verify key steps during execution, not solely to review results after completion. 

## **Real-Time and Ongoing Verification** 

Add under your real-time verification section: 

Jurisdictions should implement periodic, publicly verifiable backup procedures that capture and preserve audit-relevant data as it is generated, including the use of integrity checks and time-stamped records. 

## **Conclusion** 

Page 8 

The draft provides a strong foundation for a national framework. Clarifying its role as a principles document, expanding its scope to include testing, introducing Public Transparency Protocols, requiring complete and structured documentation, and supporting a range of audit methods will significantly improve its effectiveness and credibility. 

Page 9 

## **Targeted Proposed Edits to Draft Document** 

Voluntary National Standards for Election Audits – A Practical Guide (The comments provided above should be authoritative of our suggested changes.) 

## **1. Title (Global Change)** 

## **Current:** 

Voluntary National Standards for Election Audits – A Practical Guide 

## **Replace with:** 

Voluntary National Principles for Election Auditing and Testing – A Practical Guide 

## **2. Introduction Section** 

## **After paragraph:** 

“Election audits can take place before, during, or after an election.” 

## **Add:** 

Pre-election and in-process testing activities, including logic and accuracy testing, are within the scope of these principles where they affect the integrity of election outcomes. 

## **After paragraph:** 

“This guide delivers a universal set of voluntary professional standards…” 

## **Modify sentence:** 

## **Current:** 

“…a universal set of voluntary professional standards…” 

Page 10 

## **Replace with:** 

“…a universal set of voluntary professional principles…” 

## **Add new paragraph at end of Introduction:** 

This document establishes guiding principles rather than detailed procedural standards. It is expected that specific audit and testing methods, formats, and conformance requirements will be defined in separate technical standards. 

## **3. Using the Standards Section** 

## **After paragraph:** 

“These standards provide a voluntary framework…” 

## **Add:** 

The principles described herein are intended to guide the development of detailed procedures and technical standards, including structured methods for recording, verifying, and analyzing audit and testing data. 

## **4. Standards Framework → Transparency (or Accountable Topic)** 

## **Under “Transparency” discussion** 

## **Add new paragraph:** 

Transparency includes structured procedures that allow the public to observe and verify key steps during execution, not solely through post-process reporting. 

## **Add new subsection (or paragraph) under Transparency:** 

**Public Transparency Protocol (PTP):** A scripted, in-process sequence of actions conducted in a public setting, in which critical steps are performed, explained, and 

Page 11 

documented in real time. The protocol ensures that observers can verify both the actions taken and that the recorded results accurately reflect those actions as they occur. Public Transparency Protocols are operational controls and are essential where full independence is not feasible. 

Public Transparency Protocols should be applied at critical control points, including but not limited to random selection, batch verification, testing procedures, and result comparison steps. 

## **5. Standards Framework → Standardization (Professional Topic)** 

## **Under “Standardization” discussion** 

## **Add:** 

Audit and testing records should be created in structured formats that are both human-readable and machine-readable at the time of creation, enabling real-time verification and independent post-process analysis without transcription. 

Technologies such as optical mark recognition demonstrate that structured, position-based encoding of values can provide high accuracy while remaining observable and verifiable by human observers. 

Development of standardized formats for audit and testing records, including structured fields and machine-readable encoding, is recommended. Collaboration with the National Institute of Standards and Technology is appropriate given its role in measurement, verification, and data integrity standards. 

## **6. Standards Framework → Appropriateness (Effective Topic)** 

## **After paragraph discussing methodology** 

## **Add:** 

All observed values, including intermediate results and repeated measurements, should be recorded as part of the official record at the time they are observed. 

Informal or temporary recording methods that are not preserved as part of the official record should not be used for values affecting outcomes. 

Page 12 

There should be no stage in which observation or documentation occurs outside public visibility. 

## **7. Audit Types Section (Table of Audit Types)** 

## **Add new row:** 

**Audit:** Ballot Image Audit (BIA) 

## **Description:** 

An audit that utilizes the full set of ballot images produced by the voting system to evaluate results, detect anomalies such as duplication or omission, and compare interpreted outcomes with reported results, while accounting for the relationship to the underlying paper ballots. 

## **8. Audit Types → Chain of Custody / Reconciliation** 

## **Modify existing Chain of Custody Audit description:** 

## **Add sentence:** 

This audit may be evaluated in conjunction with reconciliation of ballot counts across independent records. 

## **Add new audit type:** 

**Audit:** Ballot Accounting Audit 

## **Description:** 

An audit that verifies both the secure handling of ballots (chain of custody) and the consistency of ballot counts across independent records (reconciliation). These functions rely on the same underlying documentation and may be evaluated together while addressing distinct risks. 

## **9. Secure → Privacy/Confidentiality or Security Section** 

## **Add after discussion of evidence:** 

No single form of evidence should be assumed inherently trustworthy. Physical ballots rely on chain-of-custody controls, while ballot images, when properly generated and protected, can provide a consistent and analyzable record. Audit designs should consider the strengths and limitations of each and, where feasible, incorporate multiple independent sources of evidence. 

Page 13 

## **10. Add Example** 

The following example can be provided either in the primary text as an example of a Public Transparency Protocol. 

## **Insert example paragraph:** 

For example, a Public Transparency Protocol for **cryptographic hash verification** may be conducted as follows: 

1. The responsible officials present the recording sheet and identify the device to be verified, including model and serial number, in view of observers. 

2. The certified hash value is obtained from an independent, authoritative source (e.g., official publication or website) in view of observers. The full value is displayed and read aloud. 

3. The certified hash value is recorded in real time on the recording sheet in human-readable form. Observers verify that the recorded value matches the displayed value. 

4. The voting system produces its own hash value through a documented process. The resulting value is displayed and read aloud in view of observers. 

5. The device-reported hash value is recorded in real time on the same recording sheet in human-readable form. Observers verify that the recorded value matches the displayed value. 

6. A fixed subset of leading characters (e.g., the first 6–8 hexadecimal digits) from each hash value is recorded in structured fields designed for comparison and machine-readable capture. Observers verify that the subset matches the corresponding portion of the full values. 

7. The structured subset fields are compared visually to determine whether they match. The full hash values are then compared to confirm consistency. The comparison result is recorded. 

8. If any discrepancy or uncertainty arises, the process is repeated, and each result is recorded separately on the same sheet. All intermediate values and repeated measurements are preserved as part of the official record. 

9. The completed recording sheet, including all values, intermediate results, and comparison outcomes, is made available for inspection and, where applicable, scanning or digital capture. 

This procedure ensures that acquisition of values, recording of those values, and comparison of results are all observable and verifiable in real time. The use of structured fields allows both human verification during the process and reliable post-process analysis without transcription. 

## **11. Effective → Efficacy Section** 

## **Add:** 

Page 14 

Audit methods should be evaluated based on their coverage, scope, and ability to provide meaningful verification. 

Where audits focus on a limited number of contests, this limitation should be explicitly stated, and assurance should not be inferred beyond the contests examined. 

Across one or more audit activities, all contests and ballot types should receive appropriate verification. 

Where sampled ballots contain multiple contests, consideration should be given to evaluating all contests present on those ballots. 

Please see our companion document, "Public Transparency Protocol (PTP) Procedures" 

Respectfully Submitted, 

Raymond Lutz, Executive Director, Citizens Oversight 

We appreciate all the comments made by our members in multiple meetings reviewing the topic. 

Page 15 

