# Diagnostic Delivery SOP — إجراءات تسليم التشخيص المجاني

> Purpose — الغرض: a one-page founder runbook for converting a fresh diagnostic intake into a delivered, governed, bilingual diagnostic in less than 24 hours. This SOP covers the **Free Risk Score** (Rung 0 of the Governed Revenue & AI Ops ladder); its job is to demonstrate methodology, not to make claims, and to route the prospect into the paid 7-Day Diagnostic. Cross-link: [REVENUE_INTELLIGENCE_SPRINT.md](./REVENUE_INTELLIGENCE_SPRINT.md), [OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md), [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).

الغرض: دليل تشغيلي من صفحة واحدة لتحويل طلب تشخيص جديد إلى تسليم مُحوكَم ثنائي اللغة في أقل من 24 ساعة. التشخيص المجاني هو المدخل لسُلَّم العروض، ووظيفته إثبات المنهجية لا إطلاق وعود.

---

## 1. Intake check — فحص الاستلام

Before any work, confirm the intake form captured all six anchor questions. If any is missing, request it before scheduling generation:

1. Company name + sector + city.
2. Approximate number of accounts/contacts in scope.
3. Named workflow owner (sales lead / growth lead / founder).
4. Source of the data (CRM export / CSV / manual list — never scraped).
5. Languages required for outreach (AR, EN, or both).
6. The single business question the founder wants answered.

If any answer is missing → respond with the bilingual "intake incomplete" template; do not generate.

إذا نقص أي عنصر، نُرسل قالب "الاستلام غير مكتمل" ولا نولد المخرجات.

---

## 2. Source Passport pre-check — فحص جواز المصدر

Every diagnostic intake is itself a data event. Before generation, draft a Source Passport stub (`data_os.SourcePassport`) covering: `owner`, `source_type`, `allowed_use=diagnostic_only`, `pii_flag`, `retention_days=30`. No passport → no generation. This enforces non-negotiable #1 and #4.

---

## 3. Sector match — مطابقة القطاع

Pick the closest sector profile from [SECTOR_PLAYBOOKS.md](../SECTOR_PLAYBOOKS.md). If no clean match exists, mark the diagnostic as `sector=generic_b2b_services` and flag it for sector taxonomy improvement (Capital Ledger candidate).

---

## 4. Generation — التوليد

Run the governed build endpoint:

```bash
curl -X POST "$DEALIX_API/api/v1/diagnostic-workflow/build" \
  -H "Authorization: Bearer $DEALIX_TOKEN" \
  -H "Content-Type: application/json" \
  -d @intake_payload.json
```

Or via the CLI helper:

```bash
python -m cli diagnostic build --intake intake_payload.json --out out/diagnostic_<engagement_id>.json
```

The build call returns a structured diagnostic: problem framing, hypothesis tree, recommended next step, and an estimated Sprint scope. Outputs are marked `draft_only` until founder approval (non-negotiable #8).

---

## 5. Founder review checklist (10 items) — مراجعة المؤسس

Tick every item before approval:

1. Source Passport stub present and complete.
2. No PII appears in the diagnostic body (only counts, not names).
3. No guaranteed-outcome language ("we will close", "guaranteed", "ensure").
4. Every claim is labeled `Estimated` / `Sample` / `Hypothetical`.
5. Sector match is honest; no fabricated sector expertise.
6. Bilingual sections are mirror-equivalent (AR not a thin summary of EN or vice versa).
7. Recommended next step is the paid 7-Day Governed Revenue & AI Ops Diagnostic (Starter 4,999 SAR and up), not a custom quote.
8. Proposal attachment is the current Sprint template version.
9. Any redactions logged in the governance decisions log.
10. Approver identity + timestamp recorded (non-negotiable #9).

If any item fails → revise; do not send.

---

## 6. Approval before send — اعتماد قبل الإرسال

Per non-negotiable #8 and Article 8 (every external output is an estimate, not a verified result), the founder explicitly approves the diagnostic via:

```bash
python -m cli governance approve \
  --artifact out/diagnostic_<engagement_id>.json \
  --approver founder@dealix.sa \
  --note "diagnostic_v1_reviewed"
```

This writes an approval record into the governance ledger.

---

## 7. Bilingual delivery — التسليم ثنائي اللغة

Send one PDF + one editable Markdown:

- AR section first (Saudi audience default), EN section second.
- File naming: `dealix_diagnostic_<customer_handle>_<YYYYMMDD>.pdf`.
- Email subject: `تشخيص ديليكس — <اسم العميل> / Dealix Diagnostic — <Customer>`.
- Channel: business email only. No cold WhatsApp (non-negotiable #2). No LinkedIn automation (non-negotiable #3).

---

## 8. Sprint proposal attached — مرفق عرض السبرنت

Attach the rendered proposal from [PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2](../../templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2) with the customer-specific Jinja variables filled. The proposal cites the applicable 7-Day Diagnostic tier price (4,999 / 9,999 / 15,000 / 25,000 SAR), 7-day delivery, and explicit exclusions.

---

## 9. Follow-up cadence — متابعة

- **Day 0:** Diagnostic + proposal delivered.
- **Day 3:** One nudge — short, no pressure, links to a 15-minute scoping call. Template lives in [FIRST_10_WARM_MESSAGES_AR_EN.md](../FIRST_10_WARM_MESSAGES_AR_EN.md).
- **Day 7:** Close-out message: either "ready to start the Sprint" or "we'll archive this engagement; you can come back any time." No further chasing.

Every nudge is recorded as a friction event in `friction_log` if the prospect goes silent without explanation — this becomes input to the sector taxonomy.

---

## 10. Closing rule — قاعدة الإغلاق

A diagnostic is "delivered" only when: (a) the Source Passport stub exists, (b) the founder approval is logged, (c) the bilingual file is sent, (d) the proposal is attached, (e) the engagement is created in the engagement registry with status `diagnostic_delivered`. Anything less is "in-flight," not delivered.

التسليم لا يُعدّ مكتملاً إلا إذا اكتملت الخطوات الخمس أعلاه.

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
