# Data Productization

> Every recurring dataset that Dealix touches becomes a **data product** —
> with a schema, an owner, a freshness contract, and a use policy. Customer
> CSV imports stop being one-off files and become typed assets that
> agents, reports, and proof packs can rely on.

## Rule (the gate)

```
No Dealix service is delivered against an unstructured blob.
Every recurring dataset has a schema (Pydantic / SQLModel),
an owner, a sensitivity class, and a registered source row.
```

A service that operates on data without a schema is rejected at design
review.

## What a "data product" includes

| Component | Required | Notes |
|-----------|:--------:|-------|
| Name | Yes | `service.dataset.purpose`, e.g. `lead_intel.accounts.import` |
| Schema | Yes | Pydantic model in `auto_client_acquisition/<service>/schemas.py` |
| Owner | Yes | Named role (HoData / HoP / CRO / HoCS) |
| Source row | Yes | Entry in `docs/ledgers/SOURCE_REGISTRY.md` |
| Sensitivity | Yes | per `docs/governance/PDPL_DATA_RULES.md` (Public / Internal / Confidential / Restricted) |
| Allowed AI uses | Yes | Subset of {classify, score, summarize, retrieve, draft, train} — training is forbidden by default |
| Freshness contract | Yes | Max-age before flagged stale (e.g. 90 days) |
| Retention | Yes | Per `docs/DATA_RETENTION_POLICY.md` |
| Deletion path | Yes | Per `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md` |

## Seed catalog

### Lead Dataset (`lead_intel.accounts`)

| Field | Type | Notes |
|-------|------|-------|
| account_id | string | Stable hash; PII-free |
| legal_name_ar | string | Source: customer-provided |
| legal_name_en | string | Source: customer-provided |
| sector | enum | Per Dealix sector taxonomy |
| city | string | Saudi cities canonical list |
| contact_role_pattern | string | "CFO / Procurement Head" — role, not person |
| contact_email_hash | sha256 | Email never stored in cleartext |
| icp_match_score | float 0–1 | RevenueAgent output |
| source | string | Linked to `SOURCE_REGISTRY.md` row |
| imported_at | datetime | Freshness anchor |

Sensitivity: Confidential. PII fields (email, mobile) are hashed at
ingest; raw values live only inside the redacted, time-limited workspace.

### Support Dataset (`support.tickets`)

| Field | Type | Notes |
|-------|------|-------|
| ticket_id | string | Customer-side ID, hashed if PII |
| channel | enum | whatsapp / email / portal |
| language | enum | ar / en / mixed |
| topic_label | enum | SupportAgent triage output |
| priority | enum | low / medium / high / urgent |
| body_redacted | string | Through `pii_detector.py` before storage |
| customer_account_id | string | Foreign key to Lead Dataset where relevant |
| created_at | datetime | Freshness anchor |
| resolution_status | enum | open / pending / resolved |

Sensitivity: Restricted (may contain Saudi mobile, national ID).
Allowed AI uses: classify, draft (with approval). No training.

### Document Dataset (`brain.documents`)

| Field | Type | Notes |
|-------|------|-------|
| doc_id | string | Stable per-document hash |
| owner_id | string | Document owner (Permission Mirroring anchor) |
| sensitivity | enum | Per `PDPL_DATA_RULES.md` |
| allowed_users | list | RBAC scope mirror |
| source | string | `SOURCE_REGISTRY.md` row |
| indexed_at | datetime | Freshness anchor |
| last_used_at | datetime | Drives freshness sweep workflow |
| retention_until | datetime | Auto-quarantine after |

Sensitivity: variable. Retrieved by `KnowledgeAgent` only when the asking
user's RBAC overlaps `allowed_users`.

## Phase-1 vs Phase-2

- **Phase 1**: schemas live in `auto_client_acquisition/<service>/schemas.py`
  next to the workflow code; CSV imports are validated by the Pydantic model
  before any AI step.
- **Phase 2**: an explicit Data Product Registry surfaces in the Control
  Tower; the event store
  (`auto_client_acquisition/revenue_memory/event_store.py`) is the spine
  that links datasets to runs and proof events.

## Cross-links

- `/home/user/dealix/docs/product/SERVICE_RUNTIME_TABLE.md`
- `/home/user/dealix/docs/ledgers/SOURCE_REGISTRY.md`
- `/home/user/dealix/docs/governance/PDPL_DATA_RULES.md`
- `/home/user/dealix/docs/governance/PII_REDACTION_POLICY.md`
- `/home/user/dealix/docs/DATA_RETENTION_POLICY.md`
- `/home/user/dealix/docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`
- `/home/user/dealix/dealix/trust/pii_detector.py`
- `/home/user/dealix/auto_client_acquisition/customer_data_plane/`
