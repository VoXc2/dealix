---
title: Renewal Process — Stage 8 Ritual and Retainer Conversion Playbook
doc_id: W6.T36.renewal
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T36, W5.T19, W5.T10]
kpi:
  metric: sprint_to_retainer_conversion
  target: 40
  window: 30d_post_handoff
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 0.5
  score: delivery-operating
---

# Renewal Process

## 1. Context

Stage 8 (Expand) is the commercial purpose of the Delivery Standard. Every
Sprint and Pilot is *designed* to open a conversation about the next thing —
either an additional Sprint, a monthly retainer, or an enterprise upgrade.
A delivery that does not produce a written next step (signed renewal or
documented "no") is incomplete, regardless of how good the build was.

## 2. Audience

AE (lead on the commercial conversation), CSM (relationship owner, presents
the data), HoCS (approves discounts and multi-month commits), customer's
exec sponsor + economic buyer (decision-makers).

## 3. Gate Conditions (Before Renewal Conversation)

- Stage 6 (Deliver) handoff is signed.
- Stage 7 (Prove) Impact Brief has been delivered and acknowledged by the
  customer.
- `renewal_recommendation.recommend(...)` has produced a recommendation
  (retainer / additional sprint / enterprise / "not now") with rationale.
- Internal price + scope pre-approved by HoCS.

## 4. The Day +30 Conversation

Booked at handoff, held within 30 days of Day N. 45 minutes.

1. **0–10 min — Outcome restatement.** CSM walks the Impact Brief: hours
   saved, leads generated, tickets resolved, pipeline created, AR/EN tone
   results. Tie every number to the success metrics signed at kickoff.
2. **10–25 min — Next-step proposal.** AE presents one **anchor** option
   (the `renewal_recommendation` output) and one **stretch** option. No
   menu of five — choose architecture, not buffet.
3. **25–35 min — Customer reaction + objections.** Use the objection map
   in the Saudi GTM playbooks. Common objections: budget cycle, internal
   alignment, "let us run it for 30 days first".
4. **35–45 min — Commitment.** Three valid outcomes: signed, scheduled
   follow-up with a date, or written "no" with the reason captured.

## 5. Retainer Conversion Playbook

The default Stage 8 motion when the customer has reached their KPIs.

| Step | Mechanic |
|------|----------|
| Anchor offer | Monthly retainer scoped to keep the deliverable running + 1 incremental workflow per quarter. |
| Price | Set at 30–40% of the original Sprint fee per month. |
| Term | 6 months default; 12 months with a 10% credit; multi-year flows through the Expansion Playbook. |
| Stop-loss | First 30 days: refund-on-no-fit clause. Forces both sides to validate. |
| Onboarding | None — relationship is continuous; CSM remains the same. |

Multi-year, vertical, seat-expansion, and GCC co-sell motions are covered
in [`../customer-success/expansion_playbook.md`](../customer-success/expansion_playbook.md).

## 6. The Written "No" Outcome

A documented "no" is a valid Stage 8 outcome — provided the reason is
captured. CSM logs: blocker (budget / fit / timing / champion change),
re-approach date, what would have to change. The lead returns to nurture
in CRM, not to oblivion.

## 7. Anti-Patterns

- **Discount-led renewal**: opening with a price drop signals weakness.
  Anchor on outcomes first.
- **Renewal without exec sponsor**: a day-to-day owner cannot commit a
  retainer. Re-route.
- **Stretched timelines**: a "let's revisit in Q2" with no date is a soft
  no. Capture it as such.
- **Ignoring the no**: skipping the written "no" loses the institutional
  learning. CSM is responsible for the log.

## 8. Cross-links

- Delivery Standard: [`DELIVERY_STANDARD.md`](DELIVERY_STANDARD.md)
- Lifecycle: [`DELIVERY_LIFECYCLE.md`](DELIVERY_LIFECYCLE.md)
- Handoff: [`HANDOFF_PROCESS.md`](HANDOFF_PROCESS.md)
- Expansion Playbook: [`../customer-success/expansion_playbook.md`](../customer-success/expansion_playbook.md)
- CS framework: [`../customer-success/cs_framework.md`](../customer-success/cs_framework.md)
- Code: `auto_client_acquisition/delivery_factory/renewal_recommendation.py`

## 9. Owner & Review Cadence

- **Owner**: HoCS (delivery) + CRO (commercial).
- **Review**: monthly first 90 days, then quarterly.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial Stage-8 ritual + retainer playbook |
