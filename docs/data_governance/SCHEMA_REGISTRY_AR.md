# Schema Registry — Dealix (AR)

> **Source-of-truth:** `data/data_governance/schema_registry.jsonl`
> **Format:** one JSON per line, listing schema metadata

---

## 1. لماذا Schema Registry؟

- Single source-of-truth لكل schema
- Versioning + change tracking
- Discovery: أي agent يقدر يبحث عن schema
- Validation: يستخدم في tests + ingest

---

## 2. Schema Format (per entry)

```json
{
  "schema_id": "...",
  "name": "...",
  "version": "1.0.0",
  "path": "schemas/...json",
  "owner": "...",
  "domain": "commercial|delivery|governance|ai_ops|...",
  "data_class": "D0|D1|D2|D3|D4|D5",
  "tenant_scoped": true|false,
  "retention_days": 365,
  "added_at": "2026-...",
  "status": "active|deprecated|draft"
}
```

---

## 3. Current Schemas (from existing repo)

راجع `schemas/` في الـ repo للتفاصيل:

### Core
- `opportunity.schema.json`
- `discovery_note.schema.json`
- `pain_signal.schema.json`
- `icp.schema.json`
- `buyer_persona.schema.json`
- `product_offer.schema.json`
- `offer_match.schema.json`
- `pricing_rule.schema.json`
- `product_feature.schema.json`
- `product_feedback.schema.json`
- `commercial_proposal.schema.json`
- `commercial_proof_pack.schema.json`
- `funnel_event.schema.json`
- `metric_event.schema.json`
- `client_health.schema.json`
- `roadmap_item.schema.json`
- `experiment.schema.json`
- `founder_decision.schema.json`
- `partner.schema.json`
- `partner_agreement_summary.schema.json`
- `partner_opportunity.schema.json`
- `partner_referral.schema.json`

### Dealix Contracts
- `dealix/contracts/schemas/evidence_pack.schema.json`
- `dealix/contracts/schemas/event_envelope.schema.json`
- `dealix/contracts/schemas/decision_output.schema.json`
- `dealix/contracts/schemas/audit_entry.schema.json`

### Wave 3 (new)
- `enterprise_questionnaire.schema.json` (Agent 18)
- `vendor_due_diligence.schema.json` (Agent 18)
- `enterprise_risk.schema.json` (Agent 18)
- `model_registry.schema.json` (Agent 19)
- `ai_task.schema.json` (Agent 19)
- `model_usage_event.schema.json` (Agent 19)
- `ai_eval_result.schema.json` (Agent 19)
- `data_entity.schema.json` (Agent 20)
- `audit_event.schema.json` (Agent 20)
- `data_quality_issue.schema.json` (Agent 20)
- `data_retention_rule.schema.json` (Agent 20)

---

## 4. Change Control

- **New schema:** add to registry, review by data lead
- **Breaking change:** major version bump + migration plan
- **Deprecation:** mark + 30-day overlap period
- **Removal:** after deprecation period + audit

---

## 5. Validation

- All ingest paths validate against schema
- Tests use schemas for fixtures
- Dashboard surfaces schema violations

---

> **Owner:** Data Lead · **Review:** عند كل schema change
