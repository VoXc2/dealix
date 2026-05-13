# AI Support Desk Sprint — Offer / عرض

**Pillar:** Serve Customers / خدمة العملاء · **Modules:** Knowledge + Workflow + Reporting + Governance

## Promise / الوعد
Build the customer's support inbox a bilingual AI co-pilot in 14 business days that drafts suggested replies (never autosends), routes by intent, and reports weekly. Human agents stay in control.

## Commercials / التجاريات
- **Price / السعر:** SAR 12,000–30,000 (excl. VAT). Floor for single channel, ceiling for multi-channel (email + WhatsApp + web).
- **Duration / المدة:** 14 business days.
- **Payment / الدفع:** Net 14, 50% kickoff / 50% on delivery.
- **SOW template:** `templates/sow/ai_support_desk_sprint.md` (to be authored).

## MVP Product Rule / قاعدة المنتج
**Suggested-replies-only, no autosend.** Every draft requires an agent click to dispatch. Autosend is a deliberately deferred feature; it returns only with a contracted upgrade and a renegotiated approval matrix.

## Deliverables / المخرجات
1. Bilingual reply-suggestion engine wired to one inbox (email or WhatsApp or web; multi-channel at upper tier).
2. Intent classifier with 6–10 categories tuned to the customer's volume.
3. FAQ library (top 30) drafted, reviewed, and indexed.
4. Escalation rules per category (when an agent must take over).
5. Weekly support-report template (volume, response time, top intents, deflection rate).
6. Agent training (1.5 hours recorded) + admin guide.
7. Audit log of every suggestion + every dispatch decision.

## Best For / مناسب لـ
- Support teams of 3–25 agents drowning in inbound volume.
- BFSI / retail-ecomm / healthcare / logistics customers with bilingual AR/EN load.
- Customers who want speed without giving up the human touch.

## Compliance / الامتثال
- PDPL Art. 13/14 footer appears in any externally-shared message.
- PII detector runs on inbound + drafts before agent sees.
- All approvals route through `dealix/trust/approval_matrix.py` — no autosend, ever.

## Cross-links / روابط ذات صلة
- Scope: `docs/services/ai_support_desk_sprint/scope.md`
- Inbox intake: `docs/services/ai_support_desk_sprint/inbox_intake.md`
- FAQ request: `docs/services/ai_support_desk_sprint/faq_request.md`
- Escalation rules: `docs/services/ai_support_desk_sprint/escalation_rules.md`
- Service portfolio catalog: `docs/strategy/service_portfolio_catalog.md`
- CS framework: `docs/customer-success/cs_framework.md`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
- Customer inbox module: `auto_client_acquisition/customer_inbox_v10/`
- Support OS module: `auto_client_acquisition/support_os/`
