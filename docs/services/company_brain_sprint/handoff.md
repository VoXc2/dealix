# Company Brain Sprint — Stage-6 (Deliver) Handoff

Owner: HoCS. Duration: 60 minutes, recorded. Day 21. Emit `delivery.handoff_completed` event. "No source = no answer" is rehearsed live with the customer.

## Handoff Packet Contents / محتويات الحزمة

Sent to customer 24 hours BEFORE the session:

1. Query-interface access URL + credentials (sealed vault).
2. Document inventory CSV (final) with category, owner, sensitivity, last_modified.
3. Access-tier matrix (Admin / Team / Read-only) + role-to-category map.
4. Eval report (50-question harness) — citation coverage, PII-surfacing, restricted-access correctness.
5. Bilingual executive report (per `report_template.md`).
6. Proof pack (per `proof_pack_template.md`).
7. Admin guide (>= 5 pages): how to refresh, edit access rules, retire docs.
8. Training recording (2 hours, Day 19) split by admin / user track.
9. Audit-log query snippet + sample export (last 14 days).
10. Right-to-erasure SOP (< 72-hour SLA) + 1 tested example.
11. PDPL Art. 13/14 footer template for externally-shared answers.
12. Renewal proposal (see `upsell.md`).

## Session Agenda — 60 minutes / جدول الاجتماع — 60 دقيقة

### 60–45 min — Outcomes Review / مراجعة النتائج (15 min)
- Walk the executive summary.
- Show: citation coverage, PII-surfacing = 0, search-time delta.
- Demonstrate the audit-log snapshot.

### 45–15 min — Working Session / جلسة عمل (30 min)
- 3 live questions from the team head -> assistant answers with citations.
- 1 out-of-corpus question -> assistant refuses ("no source = no answer").
- 1 restricted-content question with an unauthorized persona -> blocked.
- Right-to-erasure live test: delete one doc -> ask same question -> citation gone within minutes (full SLA < 72 hours).
- Walk the admin guide: refresh doc, edit access rule, retire doc.

### 15–0 min — Adoption & Renewal / التبني والتجديد (15 min)
- 30-day adoption plan (shadow -> open beta -> steady state).
- Walk renewal pathways (`upsell.md`).
- Confirm DPO contact + erasure SLA.
- NPS-style quick score.
- Schedule 14-day proof-pack review (Stage-7 Prove).

## Roles in the Room / الأدوار
- Dealix: HoCS (lead), brain engineer, AR reviewer, CRO if SOW >= SAR 15,000.
- Customer: department head (required), document owner per category, IT/data steward.

## Definition of Done / تعريف الإنجاز
- Customer admin runs a refresh end-to-end during the session.
- All 12 packet artifacts acknowledged in writing.
- Customer signs the handoff receipt.
- Renewal proposal opened in CRM as next stage.
- Recording uploaded to project room.

## Cross-links
- Delivery checklist: `docs/services/company_brain_sprint/delivery_checklist.md`
- QA gates: `docs/services/company_brain_sprint/qa_checklist.md`
- Stage events: `auto_client_acquisition/customer_loop/`
- Pilot delivery SOP: `docs/PILOT_DELIVERY_SOP.md`
- CS framework: `docs/customer-success/cs_framework.md`
- Expansion playbook: `docs/customer-success/expansion_playbook.md`
- Data governance: `docs/trust/data_governance.md`
