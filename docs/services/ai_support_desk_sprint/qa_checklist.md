# AI Support Desk Sprint — QA Checklist

Project ships only when ALL gates pass AND Quality Score >= 80. The autosend-prohibition is a P0 gate; failure = halt + escalate to HoCS + CRO.

## Business QA / جودة الأعمال
- [ ] Customer's top 5 stated intents are correctly classified on a held-out sample (>= 90%).
- [ ] Customer's support manager can articulate the business win in one sentence (AR + EN).
- [ ] Weekly support-report template walks the right KPIs (volume, response time, top intents, deflection, escalations).
- [ ] Renewal pathway documented in `upsell.md` and surfaced to customer.

## Data QA / جودة البيانات
- [ ] 500-conversation sample anonymized at ingest.
- [ ] PII detector (`dealix/trust/pii_detector.py`) runs on inbound + every drafted reply.
- [ ] No PII surfaces in suggestions (verified on 50-message harness).
- [ ] FAQ entries carry `source_doc_id`; entries without source are flagged low-confidence.
- [ ] Right-to-erasure SLA tested: < 72 hours.

## AI QA / جودة الذكاء الاصطناعي
- [ ] Intent classifier held-out accuracy >= customer-agreed floor (default 85%).
- [ ] Bilingual draft generation: AR/EN tone correct, AR not literal-MT.
- [ ] Forbidden-claims auto-check passes (`dealix/trust/forbidden_claims.py`).
- [ ] Edge cases tested: AR-only / EN-only / mixed-script / numeric-only / emoji / regulator-domain.
- [ ] Suggestion confidence is surfaced to the agent UI (no silent low-quality outputs).

## Compliance QA / جودة الامتثال
- [ ] **Autosend is impossible in MVP.** Negative test: any code path attempting dispatch without an agent click fails closed.
- [ ] PDPL Art. 13/14 footer auto-attaches to every external dispatch; agents cannot remove it.
- [ ] Approval matrix routes verified (`dealix/trust/approval_matrix.py`).
- [ ] Audit log captures every inbound, every suggestion, every dispatch + actor.
- [ ] Regulator / VIP escalation paths tested end-to-end.

## Escalation QA / جودة التصعيد
- [ ] Tier 1 (low-confidence) trigger fires correctly.
- [ ] Tier 2 (refund / complaint / > SAR 5,000) trigger fires correctly.
- [ ] Tier 3 (regulator / safety / VIP) trigger fires correctly.
- [ ] Tier 4 (executive escalation) trigger fires and pages on-call.
- [ ] All escalations emit audit-log entries.

## Delivery QA / جودة التسليم
- [ ] Training recorded (1.5 hours).
- [ ] Admin guide present (>= 4 pages).
- [ ] Weekly report template configured and runs from Day-14.
- [ ] Customer signs the autosend-prohibition acknowledgement.
- [ ] 14-day retuning window opened in CRM.

## Reviewer / المراجع
- Owner: HoCS.
- Counter-sign: CRO for SOWs > SAR 15,000.
- DPO sign-off on PDPL acknowledgements.

Floor: Quality Score >= 80 to ship. Autosend-prohibition gate is P0 (binary).

## Cross-links / روابط ذات صلة
- Delivery checklist: `docs/services/ai_support_desk_sprint/delivery_checklist.md`
- Escalation rules: `docs/services/ai_support_desk_sprint/escalation_rules.md`
- Approval matrix: `dealix/trust/approval_matrix.py`
- PII detector: `dealix/trust/pii_detector.py`
- Forbidden claims: `dealix/trust/forbidden_claims.py`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
