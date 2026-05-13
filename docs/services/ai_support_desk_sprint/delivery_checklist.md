# AI Support Desk Sprint — Delivery Checklist (14 business days)

Day-by-day plan. Owner: HoCS. Quality Score >= 80 to ship. Counter-sign at Day 4, Day 9, Day 14. **Suggested-replies-only, no autosend — hardcoded.**

## Week 1 — Wire, Classify, Draft / الأسبوع 1

### Day 1 — Discovery / الاكتشاف
- [ ] 45-min recorded discovery (`inbox_intake.md`).
- [ ] One channel selected (floor) OR up to three (ceiling).
- [ ] PDPL Art. 5 lawful basis signed.
- [ ] "Suggested-replies-only, no autosend" signed by customer.
- [ ] Stage-1 event: `discovery.completed`.

### Day 2 — Ingest the 500 conversations / استيعاب 500 محادثة
- [ ] Conversation sample uploaded via sealed vault.
- [ ] PII detector run on all inbound (`dealix/trust/pii_detector.py`).
- [ ] Anonymization of customer identifiers verified.
- [ ] Audit-log writer enabled.

### Day 3 — Intent Classifier Build / تصنيف النوايا
- [ ] 6–10 intent categories drafted from customer inputs + last 500 convos.
- [ ] Initial classifier trained; held-out accuracy reported.
- [ ] Escalation rules drafted per `escalation_rules.md`.

### Day 4 — Mid-Week Gate / منتصف الأسبوع
- [ ] Customer reviews intent categories + escalation tiers.
- [ ] Sign-off on FAQ scope (top 30).
- [ ] Gate #1 signed.

### Day 5 — Reply Suggestion Engine v0 / محرك الردود
- [ ] Wire `auto_client_acquisition/customer_inbox_v10/reply_suggestion.py` to the channel.
- [ ] Bilingual draft generation tested on 50 held-out conversations.
- [ ] Forbidden-claims check enabled (`dealix/trust/forbidden_claims.py`).
- [ ] PDPL Art. 13/14 footer auto-attaches to every draft.

## Week 2 — FAQ, Tune, Train, Ship / الأسبوع 2

### Day 6–7 — Top-30 FAQ Drafting / صياغة الأسئلة الشائعة
- [ ] FAQ entries drafted from customer source docs.
- [ ] Every entry has `source_doc_id` (no source = downgraded confidence).
- [ ] SMEs ratify per `faq_request.md`.

### Day 8 — Channel Write-Back / تفعيل الإرسال البشري
- [ ] Write-back enabled BUT dispatch requires agent click. Verified.
- [ ] Synthetic-message dispatch test: agent click required for every send.
- [ ] Autosend negative test: any code path that tries to dispatch without click MUST fail closed.

### Day 9 — Mid-Sprint QA Gate / منتصف السبرنت
- [ ] Suggestion-quality eval on 100 held-out msgs (bilingual).
- [ ] Edge cases: AR-only / EN-only / mixed-script / VIP / regulator.
- [ ] PII never surfaces in drafts (50-msg harness).
- [ ] Gate #2 signed.

### Day 10–11 — Escalation Wiring / ربط التصعيد
- [ ] Tier 1–4 routing implemented and end-to-end tested.
- [ ] Approval-matrix paths verified (`dealix/trust/approval_matrix.py`).
- [ ] PDPL data-subject-request route tested.
- [ ] Audit-log entries verified for every tier transition.

### Day 12 — Agent Training / تدريب الموظفين
- [ ] 1.5-hour recorded session (admin + agent tracks).
- [ ] Agents run the suggestion + dispatch flow live.
- [ ] FAQ search verified by every agent.

### Day 13 — Final Internal QA / فحص نهائي
- [ ] All checks in `qa_checklist.md` pass.
- [ ] Weekly report template assembled (`support_report_template.md`).
- [ ] Renewal proposal drafted (`upsell.md`).

### Day 14 — Handoff / التسليم
- [ ] 60-min recorded handoff session.
- [ ] Customer signs handoff receipt + autosend-prohibition acknowledgement.
- [ ] Stage-6 event: `delivery.handoff_completed`.
- [ ] 14-day retuning window opens.

## Cross-links / روابط ذات صلة
- Offer: `docs/services/ai_support_desk_sprint/offer.md`
- QA: `docs/services/ai_support_desk_sprint/qa_checklist.md`
- Report template: `docs/services/ai_support_desk_sprint/support_report_template.md`
- Upsell: `docs/services/ai_support_desk_sprint/upsell.md`
- Customer inbox module: `auto_client_acquisition/customer_inbox_v10/`
- Support OS module: `auto_client_acquisition/support_os/`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
- Customer-success framework: `docs/customer-success/cs_framework.md`
