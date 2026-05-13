# AI Support Desk Sprint — Scope / النطاق

## Included / متضمَّن
- One inbox channel wired (email OR WhatsApp OR web chat) at the floor price; up to three channels at the ceiling.
- Bilingual reply suggestions (AR + EN), every draft visible to an agent before dispatch.
- Intent classifier with 6–10 categories tuned on the customer's last 500 conversations.
- FAQ library: top 30 questions drafted + indexed with source citations (from customer docs).
- Escalation rules: per-category routing to senior agent / supervisor / domain SME.
- Weekly support-report template (`support_report_template.md`).
- 1.5-hour recorded agent training + admin guide (>= 4 pages).
- Audit log: every inbound, every suggestion, every dispatch decision (kept 13 months).
- 14-day post-launch retuning window for the classifier (one retraining round).

## Excluded (out of scope) / مستثنى
- **Any autosend.** All dispatches require an agent click in MVP.
- Voice support (telephony / IVR / call transcription).
- Sentiment-based VIP routing (separate add-on).
- CRM ticket-system migration.
- Customer self-service chatbot (deflection-only is fine; "customer-facing autonomous bot" is not).
- Performance SLAs on response time (we measure; we do not guarantee).
- Integration to ticketing systems beyond one (Zendesk, Freshdesk, HubSpot Service Hub).

## Customer responsibilities / مسؤوليات العميل
- Provide read-access to the last 500 conversations (sealed vault).
- Confirm intent categories and escalation tiers on Day 3.
- Review top 30 FAQ drafts on Day 7.
- Attend agent training on Day 12.
- Designate a DPO contact for PDPL acknowledgements.

## Hard stops / حدود فاصلة
- Customer asks for autonomous reply send -> halt, escalate to HoCS + CRO; this requires a different product.
- PII surfaces in suggested replies unredacted -> halt, fix, re-verify.
- Customer cannot deliver the 500-conversation sample -> reduce scope to FAQ + classifier only (price-adjusted).

## Cross-links / روابط ذات صلة
- Offer: `docs/services/ai_support_desk_sprint/offer.md`
- Inbox intake: `docs/services/ai_support_desk_sprint/inbox_intake.md`
- FAQ request: `docs/services/ai_support_desk_sprint/faq_request.md`
- Escalation rules: `docs/services/ai_support_desk_sprint/escalation_rules.md`
- QA: `docs/services/ai_support_desk_sprint/qa_checklist.md`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
- Support journey module: `auto_client_acquisition/support_journey/`
- Customer inbox module: `auto_client_acquisition/customer_inbox_v10/`
