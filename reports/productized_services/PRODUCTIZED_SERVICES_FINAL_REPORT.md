# Agent #15 — Productized Services Final Report

**Date:** 2026-06-03
**Agent:** Agent #15 — Productized Services & Delivery Templates

---

## 1. ملخص تنفيذي

`docs/services/` كان فيه 8 services + OFFER_LADDER + PRICING. Agent #15
وحّد كل ذلك في **catalog واحد (`services.yaml`)**، و 3 مكتبات مرجعية
(OS + Deliverables + Acceptance)، و schema واحد.

## 2. ما أُنشئ

| المسار | الملف |
| --- | --- |
| `docs/agent_definitions/agent_15_productized_services.md` | تعريف |
| `reports/productized_services/PRODUCTIZED_SERVICE_REVIEW.md` | Gap audit |
| `docs/productized_services/PRODUCTIZED_SERVICES_OS_AR.md` | OS |
| `data/productized_services/services.yaml` | catalog (6 services) |
| `schemas/productized_service.schema.json` | schema |
| `docs/productized_services/DELIVERABLES_LIBRARY_AR.md` | مكتبة المخرجات |
| `docs/productized_services/ACCEPTANCE_CRITERIA_LIBRARY_AR.md` | مكتبة المعايير |

## 3. الـ 6 Services (في `services.yaml`)

| # | Service | Price (SAR) | Timeline |
| - | --- | --- | --- |
| 1 | Revenue Leakage Diagnostic | 1,500–3,000 | 5–7 days |
| 2 | Follow-up Recovery Workflow | 5,000–9,000 | 10–14 days |
| 3 | AI Revenue Ops Starter | 2,999/month | 14–21 days |
| 4 | Full Revenue OS | 9,999–25,000/month | 30–45 days |
| 5 | Monthly Optimization Retainer | 4,999–7,999/month | monthly |
| 6 | Custom Company OS | 250,000+ | 60–180 days |

كل service يحدد:
- ICP، problem، price، timeline، required access، client/dealix
  responsibilities، deliverables، out-of-scope، acceptance criteria،
  risks، first-7-days، weekly reporting، renewal path.

## 4. Upgrade Path

```
[Free Diagnostic]
       ↓
[Revenue Leakage Diagnostic]
       ↓
[Follow-up Recovery Workflow]
       ↓
[AI Revenue Ops Starter]
       ↓
[Full Revenue OS]
       ↓
[Custom Company OS]
       ↑
[Monthly Optimization Retainer] (تشعب من أي مستوى)
```

## 5. Deliverables Library

10 مخرجات أساسية + 3 متخصصة. كل واحد له:
- اسم، قالب مرجعي، صيغة، owner، معيار قبول.
- مثال: Proof Pack = `data/templates/proof_pack_ar.md`، PDF، 8-12 صفحة.

## 6. Acceptance Criteria Library

- 10 معايير عالمية (U1-U10): no secrets, no fake claims, glossary
  compliance, voice compliance, etc.
- معايير خاصة لكل deliverable (PP1-PP6, PR1-PR6, WT1-WT7, etc.).
- Schema = `acceptance_criteria.jsonl` (TBD content، schema validated).

## 7. Governance

- كل تغيير على `services.yaml` ⇒ PR + founder review.
- لا agent يغيّر السعر بدون Decision Pack §S1.
- `services.yaml` = single source of truth.

## 8. Remaining Gaps

1. **6 per-service delivery playbooks** (`REVENUE_LEAKAGE_DIAGNOSTIC_DELIVERY_AR.md` etc.) — TBD.
2. **`data/productized_services/deliverables.jsonl`** — TBD (schema defined).
3. **`data/productized_services/acceptance_criteria.jsonl`** — TBD.
4. CI test: `tests/test_service_yaml_valid.py` (TBD).
5. CI test: `tests/test_pricing_in_range.py` (TBD).
6. Client intake form template (TBD).

## 9. Founder Next Actions

1. ✅ اعتماد `services.yaml` كـ single source of truth.
2. ✅ اعتماد `PRODUCTIZED_SERVICES_OS_AR.md`.
3. ⏳ كتابة 6 per-service playbooks.
4. ⏳ populate `deliverables.jsonl` و `acceptance_criteria.jsonl`.
5. ⏳ CI tests.
6. ⏳ client intake form.

## 10. Cross-Agent

- **Agent #12 (Infra):** service deploy = Railway config.
- **Agent #13 (Legal):** case study = `csp_*` APPROVED.
- **Agent #14 (Localization):** كل deliverable = voice compliance.
- **Agent #16 (Data Room):** Custom Company OS = data room section.
- **Agent #17 (Procurement):** tool cost per service = pricing basis.

## 11. المراجع

- `docs/agent_definitions/agent_15_productized_services.md`
- `reports/productized_services/PRODUCTIZED_SERVICE_REVIEW.md`
- `docs/productized_services/PRODUCTIZED_SERVICES_OS_AR.md`
- `data/productized_services/services.yaml`
- `schemas/productized_service.schema.json`
- `docs/productized_services/DELIVERABLES_LIBRARY_AR.md`
- `docs/productized_services/ACCEPTANCE_CRITERIA_LIBRARY_AR.md`
- `docs/PRICING_AND_PACKAGING_V6.md` (existing)
- `docs/OFFER_LADDER.md` (existing)
- `docs/COMPANY_SERVICE_LADDER.md` (existing)
- `docs/delivery/SCOPE_CONTROL.md` (existing)
- `docs/delivery/DELIVERY_LIFECYCLE.md` (existing)
