# Imam Turki Reserve DMO — Internal Bid Decision Packet

Status: `GO_PARTNER_FIRST_CANDIDATE__DIRECT_HOLD_MISSING_EVIDENCE`
Reference: `260839010463`
Deadline: `2026-09-16`
Authority: INTERNAL L0-L4 ONLY

## Verified public scope
Official Etimad notice describes operation of the Data Management Office for Imam Turki bin Abdullah Royal Reserve, including data governance, data management and quality tooling, a central data warehouse, RAG and AI Agents for decision support and knowledge-task automation, full NDMO requirements, and NDI maturity levels 1–2.

Official public source:
https://tenders.etimad.sa/Tender/OpenTenderDetailsReportForVisitor?tenderIdString=agTf49N5VLl1QZBRAQk5dw%3D%3D

## Decision
Direct prime bid is HOLD until every mandatory eligibility item is evidenced from authorized company/tender records. Technical fit alone is not bid eligibility.

Parallel option: prepare a partner/subcontract workstream because the deadline is near and Dealix has a strong bounded fit for governed RAG/AI-agent execution, knowledge automation, evidence provenance, approval orchestration and acceptance/proof tooling.

## Direct-bid binary gate
Evidence required before `GO_DIRECT_BID_CANDIDATE`:
- exact Dealix legal bidding entity and active Etimad supplier status;
- CR legal name, activities and validity for the required scope;
- required ZATCA/Zakat/VAT and other certificates;
- SME certificate/status only if legitimately claimed;
- preliminary/final guarantee capability;
- purchased/current tender documents and complete attachments;
- mandatory financial statements/insurance/certifications;
- named qualified DMO/data-governance team and CVs;
- acceptable relevant past-performance references;
- exact NDMO/NDI methodology evidence;
- consortium/subcontract authority where applicable;
- conflict/debarment declarations.

Any mandatory missing item before deadline => direct-bid HOLD.

## Dealix bounded workstream hypothesis
Dealix should not propose to replace the prime DMO/data-platform integrator. Preferred bounded scope:
1. governed RAG knowledge layer;
2. AI-agent workflows for approved knowledge tasks and decision support;
3. Arabic/English knowledge automation;
4. retrieval provenance and source attribution;
5. human approval boundaries for consequential actions;
6. prompt/tool/model governance and evaluation;
7. acceptance telemetry and proof receipts;
8. integration adapters to approved data/catalog/warehouse platforms.

## Delivery architecture skeleton
`Approved Data Sources -> Governance/Catalog/Quality Layer -> Warehouse/Lakehouse -> Retrieval Index -> Governed RAG -> Agent Workflows -> Human Approval -> Audit/Telemetry -> Acceptance/Proof`

Dealix must remain tool-neutral. Exact storage, catalog, IAM, vector retrieval, hosting and model choices follow tender requirements and prime architecture.

## Proposed acceptance principles
- no answer without source/provenance when evidence is required;
- Arabic/English retrieval quality measured on approved corpus;
- role-based access enforced end-to-end;
- no autonomous material action outside approved authority;
- tool calls and model outputs traceable;
- hallucination/error evaluation dataset defined before go-live;
- latency/availability targets tied to actual tender SLA;
- rollback and incident path documented;
- customer/prime validates final proof.

## Internal economics placeholders
Do not issue an external price yet. Estimate internally only after official documents:
- specialist FTE-months;
- Arabic knowledge/data engineering;
- security/governance engineering;
- model/inference costs;
- data platform/integration costs allocated to prime vs Dealix;
- on-site requirements;
- support/SLA coverage;
- bid/final guarantees if Dealix is prime;
- payment milestone and working-capital exposure;
- contingency and subcontractor costs;
- opportunity cost versus current closeable revenue lanes.

## Kill / hold conditions
- legal/Etimad eligibility cannot be proven by deadline;
- mandatory tender documents unavailable;
- guarantee or working-capital requirement unacceptable;
- mandatory references/certifications cannot be satisfied;
- no credible prime/partner route in time;
- unacceptable data/security/hosting obligation;
- economics fail risk-adjusted threshold.

## Truth firewall
`PUBLIC_TENDER_SIGNAL != RELATIONSHIP != PIPELINE != AWARD`

No tender submission, purchase/payment, bond, contract, customer contact, pricing commitment or consortium representation is authorized by this document.
