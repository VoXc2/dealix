# AI Governance Program — Approval Matrix Template / مصفوفة الموافقات

Week-3 to Week-9 deliverable. Owner: HoCS + customer's HoLegal + CTO/CIO sponsor. Output: a customer-specific approval matrix that maps (action, evidence_level) -> required approver role. Implementation reuses `dealix/trust/approval_matrix.py` enums.

## Why the matrix exists / لماذا المصفوفة
Every AI action that has external side-effects (or that materially affects a person) must route through a human approver whose role matches the evidence the system carries. Lower evidence -> higher approver. This is the single P0 governance gate; without it, the program is non-compliant in MVP.

## Canonical action kinds (from `dealix/trust/approval_matrix.py`) / أنواع الإجراءات
- OUTBOUND_EMAIL
- OUTBOUND_WHATSAPP
- OUTBOUND_SMS
- PUBLIC_POST
- EXTERNAL_API_WRITE
- DATA_EXPORT
- CRM_BULK_UPDATE
- INVOICE_GENERATION
- POLICY_OVERRIDE

Customer-specific extensions get added per inventory (e.g., REFUND_DECISION, CREDIT_DECISION, EMPLOYMENT_DECISION).

## Approver roles / الأدوار
- AUTO — no human needed (only for L4–L5 evidence on internal-only actions).
- CSM / AE / Senior agent.
- HEAD_CS / supervisor.
- HEAD_LEGAL.
- CTO / CIO.
- CEO.

## Matrix template / قالب المصفوفة

| Action / الإجراء | Min evidence (L0–L5) | Approver / المعتمد | Why / السبب |
|---|---|---|---|
| Internal classification | L0 | AUTO | no external side-effect |
| Internal enrichment | L0 | AUTO | no external side-effect |
| Suggest reply to agent (no dispatch) | L0 | AUTO | human still clicks |
| Outbound email (cold) | L2 | CSM | brand + reputation risk |
| Outbound email (warm reply) | L1 | CSM | named correspondent |
| Outbound WhatsApp template | L3 | HEAD_CS | regulator + brand risk |
| Outbound WhatsApp freeform | L4 | HEAD_CS | only inside 24h window |
| Outbound SMS bulk | L3 | HEAD_CS | rate/cost + brand |
| Public post (social / website) | L4 | CEO | brand-level commitment |
| External API write (CRM, finance, gov) | L3 | CTO | system-of-record change |
| Data export to third party | L4 | HEAD_LEGAL | PDPL Art. 13/14 + DPA |
| CRM bulk update | L3 | HEAD_CS | reversibility limited |
| Invoice generation | L3 | CSM | revenue commitment |
| Refund / credit decision | L4 | HEAD_CS | revenue + customer trust |
| Credit / lending decision (BFSI) | L5 | HEAD_LEGAL + CTO | regulatory + SAMA |
| Employment decision (HR) | L5 | HEAD_LEGAL | regulatory + Saudi Labor |
| Policy override | L5 | CEO | breaks the matrix; rare and logged |

## Evidence levels (recap) / مستويات الدليل
- L0 — internal-only / synthetic.
- L1 — single source corroboration.
- L2 — two-source corroboration with at least one trusted source.
- L3 — verified provenance + corroboration.
- L4 — verified provenance + explicit consent on file.
- L5 — verified provenance + explicit consent + regulator-grade audit trail.

## Negative tests / اختبارات سلبية
- Attempt to dispatch an outbound action without a matched approver -> FAIL CLOSED. Audit-log entry: `action_blocked`.
- Attempt to escalate evidence level by self-report only -> downgrades; second-source required.
- Override attempt by anyone other than CEO -> rejected; logged.

## Output artifacts / المخرجات
- `<customer>_approval_matrix_<YYYYMMDD>.csv` (action, evidence, approver, reason_ar, reason_en).
- Implementation diff against `dealix/trust/approval_matrix.py` showing customer extensions.
- Bilingual narrative (4–8 pages) explaining each row to a non-technical sponsor.
- Test suite (negative + positive) the customer can rerun.

## Gates / بوابات
- [ ] Every action listed in `ai_tool_inventory.md` has a matrix row.
- [ ] No action is left as AUTO unless evidence is L4+ AND action has no external side-effect.
- [ ] Customer's HoLegal signs the matrix.
- [ ] CEO signs the override clause.

## Cross-links / روابط ذات صلة
- AI tool inventory: `docs/services/ai_governance_program/ai_tool_inventory.md`
- Data inventory: `docs/services/ai_governance_program/data_inventory.md`
- Risk assessment: `docs/services/ai_governance_program/risk_assessment.md`
- Policy template: `docs/services/ai_governance_program/policy_template.md`
- Audit requirements: `docs/services/ai_governance_program/audit_requirements.md`
- Approval matrix engine: `dealix/trust/approval_matrix.py`
- Approval module: `dealix/trust/approval.py`
- Policy engine: `dealix/trust/policy.py`
- Revenue OS policy rules: `docs/policy/revenue_os_policy_rules.md`
- Agent governance policy: `auto_client_acquisition/agent_governance/policy.py`
