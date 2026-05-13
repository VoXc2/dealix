# Lead Intelligence Sprint — Delivery Checklist (10 business days)

Day-by-day plan. Owner: Head of Customer Success (HoCS). Counter-sign on each gate.

## Day 1 — Discovery / اليوم 1 — الاكتشاف
- [ ] 30-min recorded discovery using `intake.md` questions.
- [ ] Use case fixed in writing (binding).
- [ ] Sealed vault opened; customer uploads dataset.
- [ ] PDPL Art. 13/14 acknowledgements signed.
- [ ] Stage-1 event emitted: `discovery.completed`.

## Day 2 — Ingest & Profile / اليوم 2 — الاستيعاب
- [ ] Schema validated against `data_request.md`.
- [ ] PII scan via `dealix/trust/pii_detector.py` — Card/IBAN auto-blocked.
- [ ] Initial Data Quality Score computed (target ≥ 80 before scoring).
- [ ] Quarantine list of rows missing `source`.

## Day 3 — Normalize Saudi Entities / اليوم 3 — التطبيع
- [ ] AR/EN names normalized; CR/VAT validated.
- [ ] Phone numbers normalized to E.164 (+966).
- [ ] Domain dedupe against existing CRM if provided.
- [ ] Mid-sprint QA gate #1.

## Day 4–5 — Scoring & Banding / 4-5 — التصنيف
- [ ] Run ICP scorer; emit explainable A/B/C/D bands.
- [ ] Validate every score carries `LeadScore.features` rationale.
- [ ] Customer review of top 100 (sanity check).

## Day 6 — Top-50 Selection / اليوم 6 — أفضل 50
- [ ] Final Top-50 ranked accounts confirmed.
- [ ] Each row includes vertical, region, recommended owner.

## Day 7 — Next-Best-Action Drafts / اليوم 7 — الإجراءات
- [ ] Top-10 bilingual outreach drafts written.
- [ ] Forbidden-claims auto-check passes (`dealix/trust/forbidden_claims.py`).
- [ ] AR tone reviewed by native Saudi reviewer.

## Day 8 — Mini-CRM Build / اليوم 8 — لوحة المبيعات
- [ ] Mini-CRM board provisioned with stages.
- [ ] Top-50 imported with score, owner, next action.
- [ ] Access tiers configured.

## Day 9 — Executive Report / اليوم 9 — التقرير
- [ ] Bilingual exec report compiled per `report_template.md`.
- [ ] Proof pack assembled.
- [ ] Internal QA against `qa_checklist.md` — Quality Score ≥ 80.

## Day 10 — Handoff / اليوم 10 — التسليم
- [ ] 60-min recorded handoff session.
- [ ] Customer self-service validation.
- [ ] Renewal proposal (Monthly RevOps) delivered.
- [ ] Stage-6 event: `delivery.handoff_completed`.

## Cross-links
- QA gates: `docs/services/lead_intelligence_sprint/qa_checklist.md`
- Report skeleton: `docs/services/lead_intelligence_sprint/report_template.md`
- Handoff packet: `docs/services/lead_intelligence_sprint/handoff.md`
- 8-stage state machine: `auto_client_acquisition/customer_loop/`
- Delivery standard: `docs/strategy/dealix_delivery_standard_and_quality_system.md`
