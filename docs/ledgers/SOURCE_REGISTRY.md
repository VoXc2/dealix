# Source Registry

> Every information source that any Dealix agent reads — registered, owned,
> classed, and bounded. The Source Registry is the access list for the AI
> stack: if a source is not here, agents cannot read it.

## The hard rule

```
No agent reads any information source unless that source is registered
here, with all required fields filled.
```

A read attempt against an unregistered source ID returns `BLOCK` from
`dealix/trust/policy.py`. Per
`docs/governance/AI_INFORMATION_GOVERNANCE.md`.

## Table template

| Source | Owner | Sensitivity | Allowed Use | AI Access | Freshness | Retention |
|--------|-------|-------------|-------------|-----------|-----------|-----------|
| <source name> | <named role> | Public / Internal / Confidential / Restricted | {classify, score, summarize, retrieve, draft} | {KnowledgeAgent, RevenueAgent, …} | Max age before stale | Per `DATA_RETENTION_POLICY.md` |

## Required fields

| Field | Required | Notes |
|-------|:--------:|-------|
| Source | Yes | Logical name (e.g. `sector_playbook_fintech`); also the join key for runs |
| Owner | Yes | Named role: HoData / HoP / HoLegal / HoCS / CRO |
| Sensitivity | Yes | Per `PDPL_DATA_RULES.md` |
| Allowed Use | Yes | Subset of {classify, score, summarize, retrieve, draft}. Default excludes `train` |
| AI Access | Yes | Which agents (from `AI_AGENT_INVENTORY.md`) may read |
| Freshness | Yes | E.g. `90 days`; rows older are flagged stale |
| Retention | Yes | E.g. `24 months`; reference `DATA_RETENTION_POLICY.md` |

## Optional but recommended fields

Allowed users (RBAC scopes), lawful basis under PDPL, deletion path, and
provider-terms confirmation (no training on submitted data).

## Seed catalog (Phase-1)

| Source | Owner | Sensitivity | Allowed Use | AI Access | Freshness | Retention |
|--------|-------|-------------|-------------|-----------|-----------|-----------|
| `dealix.marketing_pages` | HoP | Public | classify, summarize | All agents | 30 days | 24 months |
| `dealix.sector_playbooks` | CRO | Internal | retrieve, summarize | RevenueAgent, StrategyAgent, KnowledgeAgent | 90 days | 24 months |
| `customer.icp_definitions` | HoCS | Confidential | retrieve, score | RevenueAgent (per customer) | 90 days | 24 months |
| `customer.account_lists` | HoData | Confidential | classify, score, retrieve | DataQualityAgent, RevenueAgent | 30 days | 24 months |
| `customer.support_corpus` | HoCS | Restricted | retrieve, draft | SupportAgent, KnowledgeAgent | 30 days | 12 months |
| `customer.documents` | HoData | Confidential / Restricted | retrieve | KnowledgeAgent | 90 days | 24 months |
| `dealix.proof_packs` | HoP | Internal | retrieve, summarize | ReportingAgent | 180 days | 60 months |
| `dealix.case_studies_public` | HoP | Public | retrieve, summarize | All agents | 180 days | 60 months |
| `compliance.forbidden_claim_patterns` | HoLegal | Internal | classify | ComplianceGuardAgent | 180 days | 60 months |
| `compliance.pii_patterns` | HoLegal | Internal | classify | ComplianceGuardAgent | 180 days | 60 months |
| `vendor.subprocessor_disclosures` | HoLegal | Public | retrieve, summarize | KnowledgeAgent | 90 days | 60 months |
| `regulatory.pdpl_articles` | HoLegal | Public | retrieve, summarize | KnowledgeAgent | 180 days | 60 months |

## Lifecycle

```
Proposed → Registered → Indexed → In Use → Refreshed → Quarantined → Deleted
```

Registered rows are indexed (`EMBEDDINGS_PIPELINE.md`), refreshed at the
Freshness cadence, quarantined when stale, and hard-deleted per DSR or
retention expiry.

## Phase 2 wiring

Registry moves from markdown to a typed table in the event store. Reads
resolve by source ID; unregistered IDs `BLOCK`. The AI Control Tower
surfaces source-missing and freshness exceptions.

## Audit

Every agent read writes `{source_id, agent_id, user_id, decision}` to
`dealix/trust/audit.py`. Monthly audit reconciles against the registry;
mismatches escalate per `AI_MONITORING_REMEDIATION.md`.

## Cross-links

- `/home/user/dealix/docs/governance/AI_INFORMATION_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/PDPL_DATA_RULES.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/AI_MONITORING_REMEDIATION.md`
- `/home/user/dealix/docs/product/DATA_PRODUCTIZATION.md`
- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/DATA_RETENTION_POLICY.md`
- `/home/user/dealix/docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`
- `/home/user/dealix/dealix/trust/policy.py`
- `/home/user/dealix/dealix/trust/audit.py`
- `/home/user/dealix/auto_client_acquisition/revenue_memory/event_store.py`
