# AI Governance Program — Audit Requirements / متطلبات المراجعة

Week-4 to Week-12 deliverable depending on tier. Owner: HoCS + customer's DPO + CTO. Output: an audit-trail blueprint, a monthly evidence-pack template, and a regulator-inspection-ready dossier specification.

## Audit principles / المبادئ
1. **Immutability.** Every AI invocation, every approval decision, every override, every PDPL-related event lands in an append-only event store (`dealix/trust/audit.py`).
2. **Linkability.** Every event references a Decision Passport ID (per `docs/policy/revenue_os_policy_rules.md`).
3. **Bilingual readability.** AR + EN summaries for every event class, so an inspector can review without an interpreter.
4. **Retention.** Minimum 13 months, longer where regulator-specific (e.g., SAMA, ZATCA) requires.
5. **Right-to-erasure consistent.** Erasure of underlying data removes derived caches but the audit-log entries remain — events keep hashes, not raw PII.

## Event taxonomy / تصنيف الأحداث

| Event class | Examples | Owner module |
|---|---|---|
| `tool_invocation` | model call, agent step, RAG retrieval | `dealix/trust/audit.py` |
| `approval_event` | approve, reject, escalate | `dealix/trust/approval.py` |
| `policy_decision` | passport, evidence check, rule firing | `dealix/trust/policy.py` |
| `consent_event` | give / withdraw / refresh | `auto_client_acquisition/compliance_os/consent_ledger.py` |
| `dsr_event` | access / correction / erasure | `auto_client_acquisition/compliance_os/data_subject_requests.py` |
| `vendor_event` | DPA sighted, sub-processor disclosed | `auto_client_acquisition/compliance_os/vendor_registry.py` |
| `incident_event` | breach detected, escalated, closed | `docs/PDPL_BREACH_RESPONSE_PLAN.md` |
| `policy_override` | rare; CEO only | `dealix/trust/policy.py` |

## Minimum fields per event / الحد الأدنى من الحقول

| Field | Required? | Notes |
|---|---|---|
| `event_id` | yes | UUID |
| `event_class` | yes | from taxonomy above |
| `tenant_id` | yes | customer scope |
| `tool_id` | yes (if applicable) | from `ai_tool_inventory.md` |
| `dataset_id` | yes (if applicable) | from `data_inventory.md` |
| `passport_id` | yes (if action with side-effect) | per revenue OS policy rules |
| `actor` | yes | user / agent ID |
| `approver_role` | yes (for approval events) | from `approval_matrix.md` |
| `evidence_level` | yes (for actions) | L0–L5 |
| `pdpl_basis` | yes (for data events) | Art. 5 lawful basis |
| `summary_ar` | yes | bilingual short text |
| `summary_en` | yes | |
| `payload_hash` | yes | not raw payload (PII safety) |
| `timestamp` | yes | ISO 8601 UTC |

## Monthly evidence pack / حزمة الأدلة الشهرية

Generated on the 1st business day of every month. Bilingual PDF + CSV exports.

Sections:
1. Executive summary (1 page).
2. Total events by class.
3. Approvals fired: by action, by approver role, by evidence level.
4. Overrides used (must be near-zero; explained).
5. PDPL events: consent, DSR, breach (none expected; if any, full incident report).
6. Vendor changes (sub-processors added/removed, DPAs renewed).
7. Top 10 high-risk events flagged for follow-up.
8. Open audit findings with target close dates.
9. Regulator-readiness checklist status.

## Regulator-inspection dossier / حزمة المراجعة التنظيمية

Kept always-current; assembled on request within 24 hours:
- AI tool inventory CSV (latest).
- Data inventory ROPA CSV (latest).
- Risk register CSV (latest).
- AI usage policy (versioned).
- Approval matrix snapshot.
- Last 12 monthly evidence packs.
- Open incidents register.
- DPO contact + sub-processor list.

## SLAs / مستويات الخدمة
- DSR access response: < 30 days (PDPL Art. 19), target < 14 days.
- DSR erasure: < 72 hours technical; < 30 days legal acknowledgement.
- Breach notification to NDMO: < 72 hours from detection.
- Monthly evidence pack: published by 5th business day of the month.
- Regulator dossier on request: < 24 hours.

## Compliance gates / بوابات الامتثال
- [ ] Audit-log coverage of every AI invocation = 100%.
- [ ] PDPL Art. 13/14 events visible in the dossier.
- [ ] Approval-matrix override count for the period documented.
- [ ] Sub-processor changes reflected within 7 days.
- [ ] Customer's DPO signs every monthly evidence pack.

## Cross-links / روابط ذات صلة
- AI tool inventory: `docs/services/ai_governance_program/ai_tool_inventory.md`
- Data inventory: `docs/services/ai_governance_program/data_inventory.md`
- Risk assessment: `docs/services/ai_governance_program/risk_assessment.md`
- Approval matrix: `docs/services/ai_governance_program/approval_matrix.md`
- Policy template: `docs/services/ai_governance_program/policy_template.md`
- Audit module: `dealix/trust/audit.py`
- Approval module: `dealix/trust/approval.py`
- Policy engine: `dealix/trust/policy.py`
- Revenue OS policy rules: `docs/policy/revenue_os_policy_rules.md`
- PDPL breach response: `docs/PDPL_BREACH_RESPONSE_PLAN.md`
- Trust pack — incident response: `docs/trust/incident_response.md`
- Trust pack — data governance: `docs/trust/data_governance.md`
- Compliance OS: `auto_client_acquisition/compliance_os/`
