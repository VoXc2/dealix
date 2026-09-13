# Imam Turki DMO — Compliance Matrix Template

Populate only from the current official tender documents. Never infer `COMPLIANT` from a public summary.

| ID | Requirement | Mandatory? | Tender source/page | Prime evidence | Dealix evidence | Partner evidence | Gap | Owner | Status |
|---|---|---:|---|---|---|---|---|---|---|
| E01 | Etimad supplier eligibility | TBD | TBD | TBD | TBD | TBD | Tender docs required | Legal/Commercial | UNKNOWN |
| E02 | CR activities/classification | TBD | TBD | TBD | TBD | TBD | Tender docs + company evidence | Legal | UNKNOWN |
| E03 | Tax/Zakat/VAT certificates | TBD | TBD | TBD | TBD | TBD | Tender docs + certificates | Finance | UNKNOWN |
| E04 | Preliminary/final guarantee | TBD | TBD | TBD | TBD | TBD | Exact guarantee terms | Finance | UNKNOWN |
| T01 | Operate Data Management Office | Yes per public scope | Etimad public notice | TBD | Bounded specialist only | TBD | Exact WBS required | Delivery | PARTIAL_HYPOTHESIS |
| T02 | NDMO requirements | Yes per public scope | Etimad public notice | TBD | Architecture/evidence support | TBD | Control matrix required | Data Governance | PARTIAL_HYPOTHESIS |
| T03 | NDI levels 1–2 | Yes per public scope | Etimad public notice | TBD | Evaluation/evidence support | TBD | Exact assessment criteria | Data Governance | PARTIAL_HYPOTHESIS |
| T04 | Central data warehouse | Yes per public scope | Etimad public notice | TBD | Integration adapters only | TBD | Platform requirements | Data Platform | PARTIAL_HYPOTHESIS |
| T05 | Data governance/management/quality tools | Yes per public scope | Etimad public notice | TBD | Tool-neutral integration | TBD | Approved stack required | Data Platform | PARTIAL_HYPOTHESIS |
| T06 | RAG platform | Yes per public scope | Etimad public notice | TBD | Strong bounded fit | TBD | Corpus/security/SLA details | AI/Knowledge | HYPOTHESIS_STRONG |
| T07 | AI Agents | Yes per public scope | Etimad public notice | TBD | Strong bounded fit | TBD | Agent authority/use cases | Agentic AI | HYPOTHESIS_STRONG |
| S01 | Data residency/hosting | TBD | TBD | TBD | TBD | TBD | Tender docs required | Security | UNKNOWN |
| S02 | NCA/security controls | TBD | TBD | TBD | TBD | TBD | Tender docs required | Security | UNKNOWN |
| S03 | PDPL/privacy controls | TBD | TBD | TBD | Evidence/provenance patterns | TBD | Exact obligations | Privacy | UNKNOWN |
| P01 | Staffing roles/seniority | TBD | TBD | TBD | Specialist subset only | TBD | Named CVs required | Delivery | UNKNOWN |
| P02 | On-site requirements | TBD | TBD | TBD | TBD | TBD | Tender docs required | Delivery | UNKNOWN |
| P03 | Past-performance references | TBD | TBD | TBD | NOT_PROVEN | TBD | Mandatory threshold unknown | Commercial | UNKNOWN |
| C01 | Contract duration | Planning mirror says 24 months | Must verify legal docs | TBD | TBD | TBD | Legal docs required | Commercial | UNVERIFIED_MIRROR |
| C02 | Payment milestones | TBD | TBD | TBD | TBD | TBD | Working-capital unknown | Finance | UNKNOWN |
| C03 | Penalties/SLA credits | TBD | TBD | TBD | TBD | TBD | Tender docs required | Legal/Delivery | UNKNOWN |
| C04 | Local content/SME mechanism | Planning mirror indicates SME preference | Must verify legal docs | TBD | TBD | TBD | Exact mechanism required | Commercial | UNVERIFIED_MIRROR |

## Status vocabulary
- `COMPLIANT_EVIDENCED`
- `PARTIAL_EVIDENCE`
- `GAP`
- `UNKNOWN`
- `NOT_APPLICABLE`
- `UNVERIFIED_MIRROR`
- `HYPOTHESIS_STRONG`
- `PARTIAL_HYPOTHESIS`

## Decision rule
No `GO_DIRECT_BID_CANDIDATE` until every mandatory row is either `COMPLIANT_EVIDENCED` or has a legally valid partner/subcontract allocation evidenced in the official bid structure.

Public scope facts may seed rows; only official tender documents may establish mandatory legal/commercial/scoring requirements.
