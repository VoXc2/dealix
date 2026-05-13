# AI Support Desk Sprint — Escalation Rules / قواعد التصعيد

Day-3 deliverable, refined through Day-12. Owner: HoCS + customer support manager. The rules below are codified in `auto_client_acquisition/customer_inbox_v10/escalation.py` and `auto_client_acquisition/support_os/escalation.py`. **Reminder: no autosend in MVP — every dispatch is human-clicked. These rules govern who sees the suggestion.**

## Tiering / التراتب

| Tier / المستوى | Role | When invoked |
|---|---|---|
| Tier 0 — Self-suggest | front-line agent | default; agent reviews + clicks dispatch |
| Tier 1 — Senior agent | senior CSR | low confidence, AR-only complex tone, repeat customer |
| Tier 2 — Supervisor | supervisor / team lead | refund/complaint, > SAR 5,000 invoice impact, > 24h waiting |
| Tier 3 — SME / Domain owner | domain SME (legal / finance / product) | regulatory / contractual / safety / VIP account |
| Tier 4 — Executive | Head of CS / CRO / CEO | media exposure, regulator inquiry, named customer escalation |

## Trigger conditions / شروط التصعيد

### Auto-escalate to Tier 1
- Suggestion confidence < 0.60 from the intent classifier.
- Conversation has > 3 unresolved turns in the last 24h.
- Customer message contains AR diglossia or strong emotional markers and tier 0 agent's language strength does not match.

### Auto-escalate to Tier 2
- Intent in {refund, complaint, dispute, cancellation_with_credit}.
- Invoice / transaction value > SAR 5,000.
- Wait time > 24 hours.
- Customer-reported PDPL request (access / erasure / correction).

### Auto-escalate to Tier 3
- Intent flagged regulatory / legal / safety (e.g., SAMA, ZATCA, SFDA, CITC mentions).
- Customer is in the named-VIP list.
- Forbidden-claim detected in the customer's previous reply (suggesting prior brand exposure).

### Auto-escalate to Tier 4
- Media or social-media context detected.
- Regulator email domain detected in inbound.
- CEO / Head-of-CS name explicitly mentioned by customer.

## Hard rules / قواعد قطعيّة

1. **No autosend, ever, in MVP.** Every escalation tier sees the suggestion; only a human clicks dispatch.
2. PII detector runs BEFORE the suggestion is shown to any tier.
3. PDPL Art. 13/14 footer is auto-attached to every external dispatch — agents cannot remove it.
4. Approval-matrix overrides apply: `dealix/trust/approval_matrix.py` is the source of truth for who can approve which outbound action.
5. Every escalation event emits an immutable audit-log entry.

## SLA targets (measured, not guaranteed) / أهداف SLA

| Tier | Target first response | Notes |
|---|---|---|
| 0 | < 2 hours business | suggestion + agent click |
| 1 | < 4 hours business | senior review |
| 2 | < 8 hours business | supervisor decision |
| 3 | < 24 hours business | SME involved |
| 4 | < 4 hours, 24/7 | crisis-mode workflow |

## Day-12 ratification / تأكيد اليوم 12
- [ ] Tier matrix signed by customer support manager.
- [ ] Named contacts present for every tier.
- [ ] PDPL-request route tested end-to-end (Tier 2 path).
- [ ] Forbidden-claim trigger tested with a synthetic message.

## Cross-links / روابط ذات صلة
- Offer: `docs/services/ai_support_desk_sprint/offer.md`
- Scope: `docs/services/ai_support_desk_sprint/scope.md`
- Inbox intake: `docs/services/ai_support_desk_sprint/inbox_intake.md`
- Escalation engine: `auto_client_acquisition/customer_inbox_v10/escalation.py`
- Support escalation: `auto_client_acquisition/support_os/escalation.py`
- Approval matrix: `dealix/trust/approval_matrix.py`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
- CS framework: `docs/customer-success/cs_framework.md`
