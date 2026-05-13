# AI Information Governance

> The rule: an AI agent at Dealix cannot read or act on any information
> source unless that source is registered, its owner declared, its
> sensitivity known, and its allowed AI uses defined. This document codifies
> the Saudi PDPL-aligned posture for every byte of information that an
> agent might touch.

## The hard rule (the gate)

```
No agent accesses information unless ALL of:
  1. The source is registered in docs/ledgers/SOURCE_REGISTRY.md
  2. The owner is named (a role, not "the team")
  3. The sensitivity class is set (Public / Internal / Confidential / Restricted)
  4. Allowed AI uses are declared (classify / score / summarize / retrieve / draft)
  5. The requesting user's RBAC permits this access (Permission Mirroring)
```

A runtime call that fails any of the five returns `BLOCK` from
`dealix/trust/policy.py`. There is no "ad hoc" or "just this once".

## What every source must declare

| Field | Required | Notes |
|-------|:--------:|-------|
| Owner | Yes | A named role (HoData / HoP / HoLegal / HoCS / CRO) |
| Sensitivity | Yes | Public / Internal / Confidential / Restricted per `PDPL_DATA_RULES.md` |
| Allowed users | Yes | RBAC scopes that may read |
| Allowed AI uses | Yes | Subset of {classify, score, summarize, retrieve, draft}. "Train" is forbidden by default |
| Freshness | Yes | Max age before flagged stale (e.g. 90 days) |
| Retention | Yes | Per `docs/DATA_RETENTION_POLICY.md` |
| Deletion path | Yes | Per `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md` |

These fields are exactly the columns of `SOURCE_REGISTRY.md`. Registration
is the act of filling them in.

## Sensitivity classes

| Class | Examples | AI default |
|-------|----------|-----------|
| Public | Dealix marketing pages, public registries | Any allowed use; cite only |
| Internal | Sector playbooks, internal SOPs | Retrieve + summarize for staff agents |
| Confidential | Customer ICP definitions, account lists | Retrieve only for the owning customer's workspace |
| Restricted | PII (Saudi mobile, National ID, IBAN, card) | No raw retrieval; redaction via `pii_detector.py` mandatory |

Restricted data is **never** sent to a model whose provider terms permit
training on submitted data (`MODEL_PORTFOLIO.md` forbidden combinations).

## Permission Mirroring (the access rule)

From `docs/governance/RUNTIME_GOVERNANCE.md`:

> An AI agent may only access data and perform actions that the
> requesting user is authorized to access or perform.

No super-user agent, no role bypass, no "system" actor that reads more
than the requesting user could read directly. Every access logs
`actor: agent_id` bound to `session.user_id`.

## Information lifecycle

```
Proposed source → Registered → Indexed → In Use → Refreshed → Quarantined → Deleted
```

- **Registered**: row added to `SOURCE_REGISTRY.md` by HoData (or HoLegal
  for legal sources).
- **Indexed**: embeddings + retrieval entry created where applicable
  (`docs/EMBEDDINGS_PIPELINE.md`).
- **In Use**: agents may retrieve under their declared allowed uses.
- **Refreshed**: re-checked at the freshness cadence; stale rows quarantined.
- **Quarantined**: read-blocked, retained for audit; not visible to agents.
- **Deleted**: hard-deleted per data subject request or retention expiry.

## Auditing

- Every read by an agent writes to `dealix/trust/audit.py`.
- The Friday review (per `SALES_OPS_SOP.md` §10) samples reads against
  registry scope; mismatches escalate to HoLegal.
- A monthly information-governance audit (per
  `AI_MONITORING_REMEDIATION.md`) reconciles `SOURCE_REGISTRY.md` against
  actual reads in the audit log.

## Phase 2 wiring

- Source registry moves from markdown to a typed table in the event store
  (`auto_client_acquisition/revenue_memory/event_store.py`).
- Runtime calls resolve source rows by ID; an unregistered source ID
  returns `BLOCK` at the policy layer.
- The AI Control Tower (`AI_CONTROL_TOWER.md`) shows source-missing
  incidents per agent.

## Cross-links

- `/home/user/dealix/docs/governance/PDPL_DATA_RULES.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/PII_REDACTION_POLICY.md`
- `/home/user/dealix/docs/governance/AI_MONITORING_REMEDIATION.md`
- `/home/user/dealix/docs/ledgers/SOURCE_REGISTRY.md`
- `/home/user/dealix/docs/product/DATA_PRODUCTIZATION.md`
- `/home/user/dealix/dealix/trust/policy.py`
- `/home/user/dealix/dealix/trust/audit.py`
- `/home/user/dealix/dealix/trust/pii_detector.py`
