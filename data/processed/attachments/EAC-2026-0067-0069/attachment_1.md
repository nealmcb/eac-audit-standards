## **Neal McBurnett, Comments on Voluntary National Standards for Election Audits draft** 

Submitted 2026-04-27. 

I am an computer scientist and expert in election auditing. I have helped promote and enhance Colorado’s audits since 2003. In 2010 I pioneered risk-limiting audits in Colorado, and have consulted with other states on their audits for over 2 decades. 

An excellent framework for goals and approaches of election auditing is: 

- Evidence-Based Elections: Create a Meaningful Paper Trail, then Audit by Andrew W. Appel and Philip B. Stark Georgetown Law Technology Review - CITE AS: 4 GEO. L. TECH. REV. 523 (2020) https:// - - 

- georgetownlawtechreview.org/wp content/uploads/2020/07/4.2 p523-541-Appel-Stark.pdf 

Specifically for post-election tabulation audits, this is excellent and supported by experts: 

- Principles and Best Practices for Post-Election Tabulation Audits http:// electionaudits.org/principles/ 

Both documents should be cited in the EAC’s voluntary standards and used to frame the relevant aspects of the document. 

The document should also be clearer about several important aspects of election auditing, as noted below. 

## **Evidence, Transparency, and Verifiability** 

Election audits should be grounded in evidence that can be independently assessed to the greatest extent practicable. Jurisdictions should prioritize transparency and verifiability through the publication of machine-readable data, documented procedures, and audit artifacts. Where full public reproducibility is not feasible, audits should instead provide structured opportunities for advance notice, public observation, and clearly documented evidence trails sufficient for stakeholders to evaluate the integrity of the process. 

Wherever possible, election records and audit artifacts should be protected and authenticated using modern integrity mechanisms such as digital signatures, cryptographic hashes, or equivalent controls. These techniques can help ensure that materials presented during audits are complete, unaltered, and traceable to their origin, even when direct public access to underlying materials is restricted. 

## **Transparency in Sample Selection and Randomization (proposed addition)** 

When audits rely on random sampling, transparency requires that the population from which samples are drawn be clearly defined and publicly documented before the random selection process begins. This includes publishing the relevant audit universe (e.g., ballot manifests, cast-vote records (redacted as necessary), contest lists, batches, or other units of selection) in sufficient detail to allow stakeholders to verify that the population is complete and appropriate. The random selection process itself should be conducted in a manner that is publicly observable and independently verifiable, using methods that allow external parties to reproduce the selection given the same inputs (e.g., publicly generated random seeds or equivalent procedures). Together, these steps help ensure that sampling is not only fair in principle but demonstrably free from manipulation, strengthening confidence in audits that depend on statistical or randomized methods. 

One good example is Colorado’s practice of publishing ballot manifests and hashes of them on their Audit Center, prior to the ceremony at which 20 dice are rolled by members of the public. The outcome of the dice roll is then provided as the “seed” for a well-documented open-source pseudo-randomnumber generator to choose the ballots to be sampled. 

Observers can then generate the ballot “pull lists” themselves and confirm that the right ballots were audited. 

## **Independence through Transparency and Verifiability (revision to Independence section)** 

Independence in election audits is not solely a matter of organizational separation, but also of public verifiability. While election officials must of course retain custody of ballots, equipment, and other sensitive materials, independence should be still be reinforced through transparency: audit processes should generate records, logs, and artifacts that allow external stakeholders to assess whether procedures were followed and whether conclusions are supported by the evidence. 

Jurisdictions are encouraged to establish independent, politically balanced bodies to define audit procedures and transparency requirements, including what data and artifacts must be produced and how they are to be documented and shared. Election officials can then carry out audits within these frameworks while maintaining custody of materials. This approach balances operational realities with the need for credible, independent oversight. 

## **Chain of Custody as Verifiable Evidence (revision to Security / Chain of Custody)** 

Chain-of-custody procedures should be documented in a manner that produces verifiable evidence, not just internal records. Documentation of the 

handling, transfer, and access to ballots, equipment, and audit materials should be complete, time-stamped, and, where feasible, cryptographically protected to prevent tampering or retroactive alteration. 

Emerging approaches—such as provenance tracking systems that record the lifecycle of ballots via ballot images and cryptographic commitments—offer additional mechanisms for strengthening trust. While implementation will vary across jurisdictions, audit frameworks should encourage the development and use of systems that make chain-of-custody records more transparent, auditable, and resistant to manipulation. 

## **Public Communication of Audit Strength and Limits (refinement)** 

The purpose of public communication is to accurately convey the strength, limits, and uncertainty of audit findings. Audit reports and public materials should clearly distinguish between what was directly verified, what was inferred, and what was outside the scope of the audit. Where constraints— legal, logistical, or technical—limit the scope or transparency of an audit, those constraints should be explicitly described, along with any steps taken to mitigate their impact. 

## **Facilitating External Review (“Audit of the Audit”)** 

Audit processes should be designed to enable meaningful external review by stakeholders such as political parties, nonpartisan organizations, academic researchers, and other qualified observers. This includes providing access— consistent with legal and privacy constraints—to audit documentation, methodologies, and relevant artifacts in forms that can be analyzed independently. This approach supports continuous improvement, encourages public trust, and allows a broader ecosystem of stakeholders to contribute to election integrity. 

## **On Tabulation Audits and Method Diversity** 

Within tabulation audits, jurisdictions may employ a variety of methods, including risk-limiting audits and other approaches appropriate to the electoral system and contest type. Different voting systems and contest structures (such as multi-winner proportional representation systems) may require different audit strategies. The key requirement is that the chosen method, together with the supporting evidence, provides a credible basis for evaluating the accuracy of reported results and is transparently documented for public understanding. 

## **Proposed Addition: Standards for Audit Reports** 

To support transparency, comparability, and continuous improvement across jurisdictions, election audits should produce standardized reports that document key aspects of the audit process and findings. Consistent 

reporting enables external review and supports future data collection efforts, including national surveys such as the Election Administration and Voting Survey (EAVS) and related policy assessments. 

Audit reports should include, where applicable: 

## • **Audit Timing** 

- Dates of the audit 

- Time expended, including both elapsed (wall-clock) time and estimated person-hours 

## **Scope and Coverage** 

- 

- Topic(s) addressed by the audit 

- Extent of coverage (e.g., full population, random sample, or targeted selection of contests, ballots, voters, sites, or time periods) 

- Any portions of the intended scope that were not covered, with explanation 

## **Methods** 

- 

   - Description of audit methods used 

   - Basis for selection of samples or focus areas, if applicable 

   - Any deviations from standard procedures 

- **Findings** 

   - List of discrepancies identified 

   - Explanations or context sufficient to understand their cause, significance, and resolution (if applicable) 

## **Transparency and Observation** 

- 

   - Whether the audit was open to public observation, and under what conditions 

   - Description of any limitations on observation 

- **Audit Team** 

   - Size and composition of audit teams 

   - Roles and types of participants (e.g., election staff, bipartisan teams, external observers) 

## **Legal and Procedural References** 

- 

   - Links or citations to relevant laws, regulations, procedures, contracts, or guidelines governing the audit 

- **Supporting Materials and Artifacts** 

   - Links to additional resources, such as: 

      - Videos or recordings of audit activities 

      - Tally sheets or summary records 

      - Access logs or chain-of-custody documentation 

      - Related reports or datasets 

Where feasible, report elements should be provided in machine-readable formats to support analysis, comparison, and independent review. 

Standardized audit reporting supports: 

## **Transparency and public understanding** 

- 

- **Independent review by stakeholders** , including political parties, nonpartisan organizations, and researchers 

## **Comparability across jurisdictions and over time** 

- 

## • **Improved policy analysis and resource planning** 

It also enables the development of consistent, structured data collection at the national level, including survey questions related to: 

- The **length, scope, and methods** of audits conducted by state and local election offices 

- The **size and composition of audit teams** 

- The **frequency and types of discrepancies identified** 

