# Market Agent Output Contract

Applies to the GTM/market subset: Sector Intelligence, Signal Detection,
Prospect Research, Draft Factory, Personalization Guard, Compliance Gate,
Deliverability, Approval Queue, Sending Ramp, Reply Handling.

Every output must include:

| Field | Rule |
|-------|------|
| `summary` | What was produced. |
| `business_impact` | No guarantees, no exaggerated claims. |
| `files_touched` | Exact paths. |
| `evidence_level` | none / assumption / anecdote / internal_data / verified / third_party_verified |
| `risk_level` | low / medium / high / critical |
| `approval_required` | `true` for anything that could lead to a send. |
| `tests_checks_run` | e.g. `pytest tests/test_gtm_quality_gate.py`. |
| `rollback` | How to revert. |
| `next_founder_action` | The human decision required next. |

**Market-specific invariants** (enforced in `core/safety/`):
- Drafts below **P1** are never send-ready.
- No fake `Re:/Fwd:` subjects; cold email must carry an unsubscribe path.
- No purchased/scraped lists; suppressed recipients are never send-ready.
- WhatsApp is post-consent only; no secrets/keys in any message.
- Positive replies route to discovery/WhatsApp/booking — **never** to payment.
