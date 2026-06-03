# WhatsApp Client OS (post-consent)

WhatsApp is a **business workflow assistant after consent** — not a cold channel and
not a general-purpose AI chatbot. It is opened only after a real signal of interest.

---

## When WhatsApp may be used

Only after **one** of:

- a positive email reply
- a form submission
- a booking
- explicit WhatsApp consent
- an existing client relationship

No cold WhatsApp. No automation that initiates contact. Consent is recorded; the
safety gate flags any WhatsApp item without `consent=true` (`WA-CONSENT`).

---

## Principles

- Short messages, clear options, Arabic-first, Saudi B2B tone.
- Always offer **"ما أعرف — اقترح علي"** (I don't know — suggest for me).
- Action cards, not long freeform chat.
- Secrets / files → secure portal, never chat.
- **No API keys in WhatsApp**, ever.
- Human handoff always available.

---

## Flows

Welcome (after consent) → "اقترح علي" → Readiness Scan → Service recommendation →
Proposal review → Proof-pack review → Permission request → Secure-portal link →
Payment handoff → Onboarding checklist → Weekly report → Support escalation →
Renewal/upsell.

---

## Action cards

Recommendation · Approval · Permission · Proposal · Proof Pack · Payment Handoff ·
Onboarding · Support Escalation · Renewal.

Every card carries: title · summary · reason · `risk_level` · `evidence_level` ·
options · `approval_required` · `next_action` · `expires_at` · owner.

---

## Human handoff (never AI-only)

Pricing finalization · legal · complaints · privacy/deletion · sensitive data · low
confidence · payment disputes.

---

## Safety mapping

| Risk | Guard |
|------|-------|
| Cold WhatsApp | Consent required; `WA-CONSENT` finding |
| Secret over chat | `OUT-SECRET-REQUEST` finding + `tests/test_safety_gate.py` |
| Overclaim | `OUT-GUARANTEE` finding |
| Unapproved send | `requires_approval=true` + human reviewer |

---

*Version 1.0 | 2026-06-03 | Enforced via `scripts/safety_gate.py`*
