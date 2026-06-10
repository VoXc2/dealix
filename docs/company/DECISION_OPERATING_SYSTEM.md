# Dealix Decision Operating System

Dealix makes decisions through **evidence**, not opinion.

**Context:** Most organizations remain in experimentation or pilots; scaling enterprise-wide is still limited, and only part of the market reports EBIT impact from AI ([McKinsey — The state of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/)). Dealix’s edge is **measurable operations**—not tool sprawl.

## Decision types

1. **Sellability** — هل الخدمة تُباع رسميًا؟ → [`SELLABILITY_DECISION.md`](SELLABILITY_DECISION.md), [`SELLABILITY_POLICY.md`](SELLABILITY_POLICY.md)
2. **Delivery** — هل نُسلِّم هذا المخرج؟ → [`../delivery/DELIVERY_DECISION.md`](../delivery/DELIVERY_DECISION.md)
3. **Governance** — هل هذا الطلب آمن؟ → [`../governance/GOVERNANCE_DECISION.md`](../governance/GOVERNANCE_DECISION.md)
4. **Product build** — هل نبني feature؟ → [`../product/BUILD_DECISION.md`](../product/BUILD_DECISION.md)
5. **Pricing** — هل السعر مناسب؟ هل نرفعه؟ → [`PRICING_DECISION.md`](PRICING_DECISION.md)
6. **Retainer** — هل نعرض اشتراكًا شهريًا؟ → [`../growth/RETAINER_DECISION.md`](../growth/RETAINER_DECISION.md)
7. **Scale** — توظيف، تفويض، شريك؟ → [`SCALE_DECISION.md`](SCALE_DECISION.md)
8. **Enterprise** — هل نقبل عميل enterprise للـ AI OS؟ → [`../enterprise/ENTERPRISE_DECISION.md`](../enterprise/ENTERPRISE_DECISION.md)

**Also:** اختيار العميل → [`../sales/CLIENT_SELECTION_DECISION.md`](../sales/CLIENT_SELECTION_DECISION.md) · ما لا نبيعه بعد → [`DO_NOT_SELL_YET.md`](DO_NOT_SELL_YET.md).

## Decision rule (universal)

Every decision must have:

| Field | Meaning |
|--------|---------|
| **Evidence** | What facts, artifacts, or gates support this? |
| **Score** | Numeric or enum band where applicable |
| **Risk review** | What can go wrong; PDPL / claims / scope |
| **Owner** | Named DRI |
| **Next action** | Single next step or documented “do nothing” |

Log material governance choices in `clients/<client>/governance_events.md`.

## Constitution

- [`DECISION_RULES.md`](DECISION_RULES.md)
- [`DEALIX_STANDARD.md`](DEALIX_STANDARD.md)
- [`DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md)

## Flywheel

See [`OPERATING_FLYWHEEL.md`](OPERATING_FLYWHEEL.md).
