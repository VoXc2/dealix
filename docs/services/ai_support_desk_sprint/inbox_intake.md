# AI Support Desk Sprint — Inbox Intake / استيعاب صندوق الوارد

Day-1 to Day-2 task. Owner: HoCS + customer support manager. Sealed-credentials vault is the only acceptable transfer channel. PDPL Art. 5 lawful basis (contract) recorded.

## Day-1 Discovery (45 min, recorded) / اكتشاف اليوم 1

1. Which inbox channel is the highest pain — email, WhatsApp, web chat? Pick ONE for the floor tier; up to three for the ceiling.
2. Average daily volume on that channel (msgs/day, last 30 days)?
3. Current agent count + shift coverage?
4. Top 5 customer intents you see today (in customer's words, AR + EN)?
5. Categories that MUST always go to a human (e.g., refunds, complaints, legal threats)?
6. Bilingual mix: % AR / % EN / mixed?
7. Tone constraints (formal / friendly / brand-voice-locked)?
8. Forbidden phrases or claims (e.g., regulatory wording)?
9. Existing FAQ doc (if any) location?
10. The one outcome you want at end of Day 14.

## Required artifacts / الأدوات المطلوبة

| Artifact / المخرج | Form | Notes |
|---|---|---|
| Conversation sample | 500 msgs minimum | Last 30 days, all channels in scope, anonymized if needed. |
| Channel credentials | sealed vault | Read-only first; write-back enabled only at Day 8 after agent training. |
| Agent roster | CSV | name, email, shift, language, seniority. |
| Brand-voice notes | doc | bilingual; 1–2 pages. |
| Escalation tiers | doc | tier 1 / 2 / 3 + named SMEs. |
| DPO contact | email | for PDPL Art. 13/14 acknowledgements. |

## Inbound schema (after ingest) / مخطط الرسائل الواردة

| Field | Required? | Notes |
|---|---|---|
| `message_id` | yes | unique |
| `channel` | yes | email / whatsapp / web |
| `customer_id` | yes | hashed if PII-sensitive |
| `lang` | yes | ar / en / mixed |
| `timestamp` | yes | ISO 8601 |
| `text` | yes | UTF-8, PII detector runs before LLM |
| `intent_category` | inferred | one of customer-defined |
| `priority` | inferred | based on intent + sentiment |
| `assigned_agent_id` | optional | for human-routed cases |

## Compliance acknowledgements / إقرارات الامتثال

- [ ] PDPL Art. 13/14 notice template approved and attached to every external dispatch.
- [ ] PII detector (`dealix/trust/pii_detector.py`) runs on inbound + drafts before any agent sees the text.
- [ ] Right-to-erasure SLA < 72 hours acknowledged.
- [ ] **Suggested-replies-only.** Customer signs that autosend is NOT enabled in MVP.
- [ ] Audit log retained 13 months.

## Cross-links / روابط ذات صلة
- Offer: `docs/services/ai_support_desk_sprint/offer.md`
- FAQ request: `docs/services/ai_support_desk_sprint/faq_request.md`
- Escalation rules: `docs/services/ai_support_desk_sprint/escalation_rules.md`
- Customer inbox module: `auto_client_acquisition/customer_inbox_v10/`
- Reply suggestion: `auto_client_acquisition/customer_inbox_v10/reply_suggestion.py`
- Routing policy: `auto_client_acquisition/customer_inbox_v10/routing_policy.py`
- PDPL readiness: `docs/PRIVACY_PDPL_READINESS.md`
