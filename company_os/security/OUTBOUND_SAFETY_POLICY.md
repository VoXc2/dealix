# Outbound Safety Policy

Dealix produces outbound **drafts** at volume. It does **not** send at volume.
Sending is staged, gated, and monitored. This policy is enforced by
`scripts/safety_gate.py` and `tests/`.

---

## Defaults (non-negotiable)

```
dry_run = true
approval_required = true
send_enabled = false
```

- 250 drafts/day is allowed and expected.
- 250 sends/day is **prohibited** until deliverability gates pass.
- No purchased lists. No scraping that violates terms.
- No cold WhatsApp automation. No LinkedIn automation.

---

## Send-ready gate — a draft may become send-ready ONLY if all pass

| Gate | Rule |
|------|------|
| Approval | `requires_approval=true` and a human `reviewed_by` approved it |
| Suppression | Recipient is **not** on `suppression_list.json` |
| Unsubscribe | Cold email includes a working opt-out / unsubscribe |
| Subject honesty | No fake `Re:` / `Fwd:` / `رد:` on a cold first-touch |
| No overclaim | No guaranteed-revenue/ROI language (Arabic + English) |
| Offer mapping | Maps to a real offer in the product ladder |
| Personalization | At least P1 (signal or sector pain present) |
| Evidence | Every claim carries an evidence level (L0–L5) |
| Secrets | No API keys / secrets requested in the body |

Draft generation can pass freely. **Send-ready fails unless every gate passes.**

---

## Deliverability ramp (only after gates pass)

| Week | Max sends/day |
|------|---------------|
| 0 | 0–20 |
| 1 | 25–50 |
| 2 | 50–100 |
| 3 | 100–150 |
| 4+ | 150–250 (only if domain health stays green) |

Readiness verdicts: `NOT_READY` · `DRY_RUN_ONLY` · `LIMITED_SEND_READY` ·
`RAMP_READY` · `PAUSE_REQUIRED`.

Prereqs: SPF + DKIM + DMARC, valid reply-to, one-click unsubscribe for marketing,
suppression active, bounce handling, low spam rate, domain/subdomain separation.

---

## WhatsApp (post-consent only)

Allowed only after: a positive email reply, a form submission, a booking, explicit
WhatsApp consent, or an existing client relationship. Never cold. Never positioned
as a general-purpose AI chatbot. Secrets/files go through the secure portal, never
chat. Human handoff is always available.

---

## Incident triggers → pause

Bounce spike · spam-complaint spike · opt-out failure · accidental send · suppressed
recipient contacted. Action: pause the batch, log, review, fix the gate, then resume.

---

*Version 1.0 | 2026-06-03 | Enforced via `scripts/safety_gate.py`, `tests/test_safety_gate.py`, `tests/test_governance_data.py`*
