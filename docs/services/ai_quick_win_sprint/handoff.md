# AI Quick Win Sprint — Stage-6 (Deliver) Handoff

Owner: HoCS. Duration: 60 minutes, recorded. Emit `delivery.handoff_completed` event. Day 7 of the sprint.

## Handoff Packet Contents / محتويات الحزمة

Sent to customer 24 hours BEFORE the session:

1. Live automation in customer environment (URL + access credentials in sealed vault).
2. Runbook (>= 3 pages): how to run, monitoring alarms, escalation paths.
3. Training recording (1 hour, Day 7).
4. Audit-log query snippet + sample export (last 7 days).
5. ROI baseline report (per `report_template.md`).
6. Proof pack (per `proof_pack_template.md`).
7. Approval-matrix configuration export (`dealix/trust/approval_matrix.py` entries).
8. Pydantic input/output schemas as `.py` reference.
9. 30-day adoption plan.
10. Renewal proposal (Workflow Automation / Monthly AI Ops) — see `upsell.md`.
11. PDPL Art. 13/14 acknowledgement copies for any externally-touching outputs.

## Session Agenda — 60 minutes / جدول الاجتماع — 60 دقيقة

### 60–45 min — Outcomes Review / مراجعة النتائج (15 min)
- Walk the executive summary.
- ROI table — before vs after (last 30 runs).
- Highlight: hours saved, errors avoided, approval-gate fires.
- One number the customer can repeat to their CEO.

### 45–15 min — Working Session / جلسة عمل (30 min)
- Process owner runs the automation live on a real input.
- Walk the runbook — monitoring, common failure modes, escalation.
- Demonstrate the audit-log query (filter by `project_id`).
- Test one approval-gate scenario end-to-end.
- Show the AR/EN parity (if bilingual) and the PDPL footer if applicable.

### 15–0 min — Adoption & Renewal / التبني والتجديد (15 min)
- Walk the 30-day adoption plan (shadow -> spot-check -> steady state).
- Walk renewal pathways (`upsell.md`).
- Confirm right-to-erasure SLA (< 72 hours).
- NPS-style quick score.
- Schedule 14-day proof-pack review (Stage-7 Prove).

## Roles in the Room / الأدوار
- Dealix: HoCS (lead), automation engineer, CRO if SOW > SAR 15,000.
- Customer: process owner (required), backup operator, IT for vault handoff.

## Definition of Done / تعريف الإنجاز
- Process owner runs the automation alone and signs the receipt.
- Audit-log access verified by customer.
- All 11 packet artifacts acknowledged in writing.
- Renewal proposal opened in CRM as next stage.
- Recording uploaded to project room.

## Cross-links
- Delivery checklist: `docs/services/ai_quick_win_sprint/delivery_checklist.md`
- QA gates: `docs/services/ai_quick_win_sprint/qa_checklist.md`
- Stage events: `auto_client_acquisition/customer_loop/`
- Pilot delivery SOP: `docs/PILOT_DELIVERY_SOP.md`
- CS framework: `docs/customer-success/cs_framework.md`
- Expansion playbook: `docs/customer-success/expansion_playbook.md`
