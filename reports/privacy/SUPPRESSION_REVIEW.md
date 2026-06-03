# Suppression Review — Findings (2026-06-03)

- Schema: `schemas/suppression.schema.json` (8 reasons) — valid.
- Engine: `SuppressionList` — add-only, case/space-insensitive, `can_send=false`
  for suppressed contacts. No removal API exposed to agents.
- Auto-suppression on angry / unsubscribe / bounce / legal / privacy replies
  (`core/safety/replies.py`).
- Tests: `test_suppression_blocks_sending.py`,
  `test_outreach_suppression_blocks_send.py` — green.

**Risk checks**
- ✅ No bypass path (`bypass_suppression` globally forbidden).
- ✅ Suppressed recipient can never be send-ready.
- 🟡 Persistence: suppression is in-memory in the engine; production must back it
  with a durable store synced to the email/WhatsApp provider before any send.

**Verdict:** Logic sound. Durable persistence is the one production prerequisite.
