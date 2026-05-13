# Company Brain Sprint — Delivery Checklist (21 business days)

Day-by-day plan across 3 weeks. Owner: HoCS. Quality Score >= 80 to ship. "No source = no answer" is the hard product invariant.

## Week 1 — Ingest & Index / الأسبوع 1 — الاستيعاب والفهرسة

### Day 1 — Discovery / الاكتشاف
- [ ] 45-min recorded discovery (`intake.md`).
- [ ] Team + use case fixed (one team only).
- [ ] PDPL Art. 5 lawful basis acknowledged.
- [ ] "No source = no answer" signed by customer.
- [ ] Stage-1 event: `discovery.completed`.

### Day 2–3 — Inventory & Permissions / الجرد والصلاحيات
- [ ] Customer delivers 7-column inventory (`data_request.md`).
- [ ] Permissions matrix collected (role -> category).
- [ ] 10 sample questions collected (eval seed).
- [ ] Sensitive-doc flagging signed off.

### Day 4 — PII Sweep / فحص البيانات الشخصية
- [ ] All documents through `dealix/trust/pii_detector.py`.
- [ ] PII redacted in index; original retained per retention rule.
- [ ] Sensitive docs routed to restricted tier.
- [ ] Mid-week QA gate #1.

### Day 5 — Chunking + Embeddings / التقطيع والمتجهات
- [ ] Chunking strategy locked (heading-aware + size cap).
- [ ] Embeddings pipeline run (`docs/EMBEDDINGS_PIPELINE.md`).
- [ ] Citation metadata attached to every chunk (doc_id, page, last_modified).
- [ ] Freshness flag set (>90 days = stale, surfaced to user).

## Week 2 — Build, Evaluate, Harden / الأسبوع 2 — البناء والتقييم

### Day 6 — Query Interface MVP / الواجهة
- [ ] Web / Slack / Teams selected (one channel, MVP).
- [ ] Access tiers wired (Admin / Team / Read-only).
- [ ] Audit-log writer enabled from query #1.

### Day 7–8 — Retrieval Tuning / ضبط الاسترجاع
- [ ] Run the 10 sample questions.
- [ ] Measure citation coverage (target >= 95%).
- [ ] Tune retrieval (k, reranker, dedupe).
- [ ] Confirm "no source = no answer" — 3 out-of-corpus questions return refusal.

### Day 9 — Sensitive-Content Tests / اختبارات المحتوى الحساس
- [ ] 3 personas tested across restricted docs (verify blocking).
- [ ] PII never surfaces in answers (verified on a 50-question harness).
- [ ] AR/EN tone audited by native reviewer.

### Day 10 — Mid-Sprint Demo / عرض منتصف السبرنت
- [ ] 30-min demo with the customer team.
- [ ] Collect 10 new questions from the team -> add to eval set.
- [ ] Gate #2 signed.

## Week 3 — Polish, Train, Handoff / الأسبوع 3 — الإتقان والتسليم

### Day 11–12 — Edge Cases & Right-to-Erasure / الحالات الحدية والحذف
- [ ] Edge cases: latest-doc citation, multi-source synthesis, restricted-content blocking, out-of-corpus.
- [ ] Right-to-erasure tested: delete 1 doc -> re-test 3 questions -> citation gone in < 72 hours.

### Day 13–14 — Eval Pass / تقييم نهائي
- [ ] Full eval harness run (>= 50 questions).
- [ ] Citation coverage >= 95%.
- [ ] PII-surfacing rate = 0%.
- [ ] Restricted-access correct rate = 100%.

### Day 15 — Admin Guide / دليل المسؤول
- [ ] Admin guide drafted (>= 5 pages).
- [ ] Document-refresh SOP authored.
- [ ] Access-rule editing flow documented.

### Day 16–17 — Customer Self-Service Validation / التحقق الذاتي
- [ ] Team uses the assistant for real questions for 2 days.
- [ ] Feedback collected, 3 high-value fixes shipped.

### Day 18 — Final Internal QA / الفحص النهائي
- [ ] Quality Score >= 80 verified per `qa_checklist.md`.
- [ ] Proof pack assembled (`proof_pack_template.md`).

### Day 19 — Training Session / التدريب
- [ ] 2-hour recorded team training (separate admin + user tracks).
- [ ] Q&A captured into FAQ.

### Day 20 — Executive Report / التقرير التنفيذي
- [ ] Bilingual exec report compiled per `report_template.md`.
- [ ] Renewal proposal drafted (see `upsell.md`).

### Day 21 — Handoff / التسليم
- [ ] 60-min recorded handoff session (see `handoff.md`).
- [ ] Customer signs handoff receipt.
- [ ] Stage-6 event: `delivery.handoff_completed`.

## Cross-links
- QA gates: `docs/services/company_brain_sprint/qa_checklist.md`
- Report skeleton: `docs/services/company_brain_sprint/report_template.md`
- Handoff packet: `docs/services/company_brain_sprint/handoff.md`
- Embeddings pipeline: `docs/EMBEDDINGS_PIPELINE.md`
- Company Brain module: `auto_client_acquisition/company_brain/`
- Delivery standard: `docs/strategy/dealix_delivery_standard_and_quality_system.md`
