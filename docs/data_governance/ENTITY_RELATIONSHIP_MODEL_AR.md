# Entity Relationship Model — Dealix (AR)

> **Companion to:** `DATA_GOVERNANCE_OS_AR.md` §"Core Entities"

---

## 1. Top-Level Domain Groups

```
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│  IDENTITY   │  │  COMMERCE    │  │  DELIVERY    │
│             │  │              │  │              │
│ Prospect    │  │ Proposal     │  │ DeliveryTask │
│ Company     │  │ PaymentHandoff│ │ DeliveryHand │
│ Contact     │  │ Renewal      │  │ ProofPack    │
│ Partner     │  │              │  │              │
│ Vendor      │  │              │  │              │
└──────┬──────┘  └──────┬───────┘  └──────┬───────┘
       │                │                  │
       └────────────────┼──────────────────┘
                        │
                ┌───────▼────────┐
                │  CLIENT        │
                │                │
                │ ClientAssess.  │
                │ ClientPermis.  │
                │ ClientHealth   │
                │ WeeklyReport   │
                └───────┬────────┘
                        │
       ┌────────────────┼────────────────┐
       │                │                │
┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│  CONTENT    │  │  GOV        │  │  ANALYTICS  │
│             │  │             │  │             │
│ Draft       │  │ Approval    │  │ Signal      │
│ SendBatch   │  │ Risk        │  │ MetricEvent │
│ Reply       │  │ AuditEvent  │  │ AgentRun    │
│ WhatsAppS.  │  │ FounderDec. │  │             │
│ ActionCard  │  │             │  │             │
└─────────────┘  └─────────────┘  └─────────────┘
```

## 2. Key Relationships

- **Prospect → Company**: many-to-one (a company can have many prospects before converting)
- **Prospect → Contact**: many-to-one
- **Contact → Draft → Approval → SendBatch**: 1:N:N:1 per campaign
- **Proposal → PaymentHandoff → Renewal**: 1:1:1 lifecycle
- **Client → ClientAssessment → ClientHealth → WeeklyReport**: ongoing
- **Client → ClientPermission → PortalSession**: per session
- **Client → DeliveryTask → ProofPack → Renewal**: service flow
- **WhatsAppSession → Reply → ActionCard → Approval**: per-thread
- **AgentRun → AuditEvent → MetricEvent**: AI ops chain

## 3. Cardinality Rules

| Parent | Child | Cardinality | Notes |
|--------|-------|-------------|-------|
| Company | Contact | 1:N | soft delete |
| Company | Prospect | 1:N | dedup on email/phone |
| Prospect | Draft | 1:N | per campaign |
| Draft | Approval | 1:1 | required for send |
| Approval | SendBatch | 1:N | batch of approved drafts |
| SendBatch | Reply | 1:N | inbound per recipient |
| Company | Proposal | 1:N | versioned |
| Proposal | PaymentHandoff | 1:1 | required for activation |
| Company | Client | 1:1 | after first payment |
| Client | DeliveryTask | 1:N | per workflow |
| DeliveryTask | ProofPack | 1:N | per milestone |
| Client | WeeklyReport | 1:N | per week |
| Client | ClientHealth | 1:1 | latest |
| Client | Renewal | 1:N | per cycle |

## 4. Tenant Scoping

كل entity (post-conversion) carries `tenant_id`:
- Pre-conversion (Prospect, Signal): global, but PII-minimized
- Post-conversion (Client, Draft, etc.): tenant-scoped

## 5. Soft Delete

Default: soft delete (deleted_at, deleted_by, deletion_reason)
- Hard delete only via:
  - Retention policy expiry
  - PDPL erasure request
  - Founder + audit

## 6. Versioning

Entities with history:
- Proposal (versioned on edit)
- ClientPermission (audit trail)
- PricingRule (versioned)
- Policy documents (versioned via git)

## 7. Cross-references

- `docs/data/SOVEREIGN_DATA_MODEL.md` (existing detailed model)
- `schemas/data_entity.schema.json` (per-entity schemas)
- `data/data_governance/schema_registry.jsonl` (registered schemas)

---

> **Owner:** Data Lead · **Review:** كل release
