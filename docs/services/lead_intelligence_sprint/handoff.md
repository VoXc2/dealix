# Lead Intelligence Sprint — Stage-6 (Deliver) Handoff

Owner: HoCS. Duration: 60 minutes, recorded. Emit `delivery.handoff_completed` event.

## Handoff Packet Contents / محتويات الحزمة

Sent to customer 24 hours BEFORE the session:
1. Cleaned dataset CSV (≤ 5,000 rows) with `source` and `data_quality_score` columns.
2. Top-50 ranked accounts file (PDF + CSV).
3. Top-10 next-best-action drafts (AR + EN) with PDPL Art. 13/14 footer.
4. Mini-CRM access credentials (sealed vault) + access tier matrix.
5. Bilingual executive report (PDF + PPT) per `report_template.md`.
6. Proof pack per `proof_pack_template.md`.
7. 30-day activation plan with owner per task.
8. Renewal proposal (Monthly RevOps) — see `upsell.md`.
9. Audit log export (event_store filter by `project_id`).
10. PDPL Art. 13/14 acknowledgement copies.

## Session Agenda — 60 minutes / جدول الاجتماع — 60 دقيقة

### 60–45 min: Outcomes Review / مراجعة النتائج (15 min)
- Walk the executive summary.
- KPI table — before vs after.
- Top-3 wins, top-3 surprises.

### 45–15 min: Working Session / جلسة عمل (30 min)
- Live demo of Mini-CRM with the customer's data.
- Review Top-10 drafts; mark approved / hold / reject.
- Confirm process owner for each Top-10 action.
- Set the cadence for the next 30 days (who, what, when).

### 15–0 min: Renewal & Compliance / التجديد والامتثال (15 min)
- Walk renewal pathways (`upsell.md`).
- Sign-off PDPL audit-trail receipt.
- Confirm right-to-erasure SLA (< 72 hours).
- Customer sentiment captured (NPS-style quick score).
- Schedule 14-day proof-pack review (Stage-7 Prove).

## Roles in the Room / الأدوار
- Dealix: HoCS (lead), one analyst, one CRO if SOW > SAR 15,000.
- Customer: Head of Sales (required), Sales ops lead, IT/data steward (for vault handoff).

## Definition of Done / تعريف الإنجاز
- Recording uploaded to project room.
- All 10 packet artifacts acknowledged in writing.
- Customer signs the handoff receipt.
- Renewal proposal opened in CRM as next stage.

## Cross-links
- Delivery checklist: `docs/services/lead_intelligence_sprint/delivery_checklist.md`
- Stage events: `auto_client_acquisition/customer_loop/`
- Pilot delivery SOP: `docs/PILOT_DELIVERY_SOP.md`
- CS framework: `docs/customer-success/cs_framework.md`
- Expansion playbook: `docs/customer-success/expansion_playbook.md`
