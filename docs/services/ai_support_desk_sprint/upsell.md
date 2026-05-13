# AI Support Desk Sprint — Stage-8 (Expand) Renewal Pathways / مسارات التجديد

Stage-8 in the 8-stage customer loop. Renewal opened at Day-14 handoff; decision point at Day 45 (after the retuning window). HoCS owns; CRO countersigns deals >= SAR 15,000.

## When to pitch / متى نقترح
- Trigger: agents are using the suggestion engine on >= 60% of in-scope inbound, customer-stated KPI improvement is visible in the weekly report.
- Window: Day-45 proof-pack review (Stage-7 Prove).
- Disqualifier: classifier accuracy below customer-agreed floor in week 4 -> tune first, then expand.

## Pathway 1 — Monthly Support Co-pilot Retainer / احتفاظ شهري
**SAR 5,000–20,000 / month, 6-month commit.**
- Monthly classifier retuning + FAQ refresh.
- Weekly support-report review (HoCS analyst attends).
- Suggestion-engine prompt tuning + bilingual tone improvements.
- Quarterly business review with the customer's Head of CS.
- Best for: floor-tier customers who need ongoing classifier hygiene.
- **No autosend in this tier either. Same MVP rule.**

## Pathway 2 — Channel Expansion (additional sprint) / إضافة قناة
**SAR 8,000–18,000, 7 business days per added channel.**
- Adds one new inbound channel (email + WhatsApp + web -> the missing one).
- Reuses the classifier and FAQ; new channel-specific tone adapters.
- Audit + escalation paths inherit from the existing wiring.
- Best for: customers who started on email and want WhatsApp next (or vice versa).

## Pathway 3 — WhatsApp Operations Setup / إعداد عمليات الواتساب
**SAR 8,000–30,000 setup, 14 business days.**
- Full WhatsApp Business Platform setup (templates, opt-in flows, broadcast policy).
- Bilingual broadcast governance (PDPL Art. 13/14 every message).
- Categories, SLA rules, escalation logic, conversation summaries.
- Best for: retailers / D2C / clinics scaling WhatsApp as primary support.

## Pathway 4 — Customer Feedback Intelligence / استخبارات تجربة العملاء
**SAR 7,500–25,000, 14 business days.**
- Sentiment + topic analytics on the existing conversation stream.
- Weekly branch / product / SKU comparisons.
- Quarterly Voice-of-Customer report for the CEO.
- Best for: customers ready to mine the conversation data for product/CX wins.

## Pathway 5 — Enterprise Support OS / مؤسسي
**SAR 90,000+ setup + SAR 20,000+ / month, MSA + DPA required.**
- Multi-channel, multi-team, KSA-resident storage option.
- Custom ticketing integration (Zendesk / Freshdesk / HubSpot / ServiceNow).
- Named delivery team, SLA-backed.
- **Autosend feature evaluated under a renegotiated approval matrix.** Out of MVP scope.
- Best for: enterprises >= 100 support seats.

## Renewal Math / حساب التجديد
- Hours saved per week (agent-side) * SAR/hour * 50 weeks = annual savings anchor.
- Inbound-volume * deflection delta * cost-per-touch = SAR avoided.
- If annual savings >= 4x Pathway 1 floor (SAR 60k vs SAR 5k floor) -> Pathway 1 is the obvious renewal.

## Cross-links / روابط ذات صلة
- Expansion playbook: `docs/customer-success/expansion_playbook.md`
- Pricing strategy: `docs/PRICING_STRATEGY.md`
- WhatsApp operator flow: `docs/WHATSAPP_OPERATOR_FLOW.md`
- Expansion engine module: `auto_client_acquisition/expansion_engine/`
- Service portfolio catalog: `docs/strategy/service_portfolio_catalog.md`
- SOW templates: `templates/sow/`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
