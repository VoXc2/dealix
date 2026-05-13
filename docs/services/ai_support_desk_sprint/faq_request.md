# AI Support Desk Sprint — FAQ Request / طلب الأسئلة الشائعة

Day-3 to Day-7 task. The top-30 FAQ library is the backbone of the suggestion engine. Every FAQ answer must carry a source citation (no source = downgrade the suggestion's confidence).

## What the customer must provide / ما يقدمه العميل

### Required / مطلوب
1. **Top 30 questions** — bilingual list (AR + EN), one row per question.
2. **Approved answers** for at least the top 15 (bilingual). Format: question, answer, source doc, last_reviewed date.
3. **Source documents** (the doc inventory for each FAQ answer) uploaded to the sealed vault.
4. **Owner email** per FAQ category (HR, billing, shipping, returns, etc.) — the SME we ping for answer ratification.

### Recommended / مفضّل
- Last 90 days of support tickets, anonymized, so we can mine actual top-asked questions (corroborates the customer-stated top 30).
- Brand-voice samples (3–5 approved past answers).
- Forbidden phrases list (e.g., regulatory or pricing language).

### Optional / اختياري
- Existing public FAQ page (web URL).
- Bilingual glossary if AR/EN terminology diverges.

## FAQ schema / مخطط

| Field | Required? | Notes |
|---|---|---|
| `faq_id` | yes | stable identifier |
| `question_ar` | yes | Arabic |
| `question_en` | yes | English |
| `answer_ar` | yes | drafted by us, ratified by SME |
| `answer_en` | yes | drafted by us, ratified by SME |
| `source_doc_id` | yes | citation; if missing, suggestion confidence is downgraded |
| `category` | yes | maps to intent classifier |
| `owner_email` | yes | SME contact |
| `last_reviewed` | yes | ISO date; > 90 days = stale flag |
| `sensitivity` | yes | public / internal / restricted |

## Day-7 ratification gate / بوابة التأكيد

- [ ] All 30 FAQ entries reviewed and signed by SMEs.
- [ ] No FAQ without a source citation.
- [ ] PDPL Art. 13/14 wording verified for any externally-shared answer.
- [ ] Forbidden-claims auto-check passes (`dealix/trust/forbidden_claims.py`).
- [ ] AR tone reviewed by native Saudi reviewer.
- [ ] PII detector run on every answer; no PII in published library.

## Provenance & compliance rules / قواعد المصدر والامتثال

1. Every FAQ answer carries a `source_doc_id`. Without a citation, the answer ships behind a lower-confidence label in the suggestion UI.
2. PII detector (`dealix/trust/pii_detector.py`) runs on every drafted answer.
3. The suggestion engine refuses to use any FAQ tagged `restricted` for unauthorized roles.
4. Right-to-erasure: deletion of an underlying source doc invalidates the FAQ within 72 hours.

## Cross-links / روابط ذات صلة
- Offer: `docs/services/ai_support_desk_sprint/offer.md`
- Inbox intake: `docs/services/ai_support_desk_sprint/inbox_intake.md`
- Escalation rules: `docs/services/ai_support_desk_sprint/escalation_rules.md`
- Knowledge answer engine: `auto_client_acquisition/support_os/knowledge_answer.py`
- Reply suggestion: `auto_client_acquisition/customer_inbox_v10/reply_suggestion.py`
- Forbidden claims: `dealix/trust/forbidden_claims.py`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
