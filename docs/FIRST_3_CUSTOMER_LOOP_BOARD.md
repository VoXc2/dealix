# First 3 Customer Loop Board / لوحة أوّل ٣ عملاء

> Track 3 real warm intros from your network through the full v5
> journey. **No real customer names** in this file — use placeholders
> like `Slot-A` / `Slot-B` / `Slot-C` and keep real names + emails in
> a private note (PDPL-compliant).

**Date opened:** 2026-05-05
**Owner:** Founder
**Hard rule:** All sources are warm intros / inbound / founder network.
NO cold WhatsApp. NO LinkedIn automation. NO purchased lists.

---

## Slot board

| Slot | Company (placeholder) | Source | Consent/source recorded? | Segment | Problem | Diagnostic status | Pilot status | Proof status | Next action | Owner |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** | Slot-A | warm intro from `__________` | ☐ | b2b_services | (TBD) | not_started | not_offered | not_assembled | book Diagnostic call | Founder |
| **B** | Slot-B | inbound (founder network) | ☐ | b2b_saas | (TBD) | not_started | not_offered | not_assembled | book Diagnostic call | Founder |
| **C** | Slot-C | warm intro from `__________` | ☐ | training_consulting | (TBD) | not_started | not_offered | not_assembled | book Diagnostic call | Founder |

**Note on Consent/source recorded?**
Tick when you've recorded the source + consent locally in the Customer
Data Plane: `auto_client_acquisition.customer_data_plane.consent_registry.grant(...)`.

---

## State legend

### Diagnostic status
- `not_started` — no contact yet
- `requested` — call booked
- `sent` — bilingual brief delivered
- `declined` — prospect said no
- `out_of_scope` — Dealix can't help; document why

### Pilot status
- `not_offered` — no Pilot offer yet (correct until Diagnostic is delivered)
- `offered` — invoice URL sent
- `payment_pending` — invoice sent, no confirmation yet
- `paid_or_committed` — paid via Moyasar OR written commitment
- `declined` — prospect said no Pilot

### Proof status
- `not_assembled` — Pilot not delivered yet
- `assembled_internal` — Proof Pack ready, customer not yet sent
- `sent_to_customer` — customer received Pack
- `published_with_consent` — customer signed publication consent

---

## Hard-rule status (re-asserted per slot)

For every slot, the following MUST stay true:

- ❌ NO cold WhatsApp / cold email
- ❌ NO LinkedIn automation
- ❌ NO scraping / purchased list
- ❌ NO marketing claim using `نضمن` / `guaranteed` / `blast`
- ❌ NO auto-charge (Moyasar test-mode + manual invoice)
- ❌ NO live customer outbound from any agent
- ✅ Founder approval gate before any external send
- ✅ Source + consent recorded before contacting
- ✅ Diagnostic brief generated via `python scripts/dealix_diagnostic.py`
- ✅ Bilingual outputs (Arabic primary)

---

## How to advance a slot

```bash
# Step 1 — book the Diagnostic call
# (manual; book a 30-min slot in your calendar)

# Step 2 — generate a Diagnostic brief
python scripts/dealix_diagnostic.py \
  --company "Slot-A" \
  --sector b2b_services \
  --region riyadh \
  --pipeline-state "<one-line current state>"

# Step 3 — advance journey state
curl -X POST http://localhost:8000/api/v1/customer-loop/journey/advance \
  -H 'content-type: application/json' \
  -d '{"current_state":"lead_intake","target_state":"diagnostic_requested","customer_handle":"Slot-A"}'

# Step 4 — when Diagnostic is delivered
curl -X POST http://localhost:8000/api/v1/customer-loop/journey/advance \
  -H 'content-type: application/json' \
  -d '{"current_state":"diagnostic_requested","target_state":"diagnostic_sent","customer_handle":"Slot-A"}'

# Step 5 — if customer accepts Pilot
python scripts/dealix_invoice.py --email <real-email> --amount-sar 499 \
  --description "Dealix Growth Starter Pilot — 7 days"
# (then advance journey to pilot_offered → payment_pending)

# Step 6 — Day 7 of delivery: assemble Proof Pack
python scripts/dealix_proof_pack.py --customer-handle "Slot-A"
```

---

## Update cadence

- **Daily** (7AM KSA) — open this file, update the Next action column for each slot
- **End of week** — count: how many slots advanced one column?
- **End of 2 weeks** — at least 1 slot should be at `pilot_status=paid_or_committed` for the v6 Operating Reality Report to flip to `OUTREACH_GO=yes`

---

## ⚠️ When a slot fails

If a slot hits `declined` or `out_of_scope`:
1. Document the reason in `docs/proof-events/<slot>-decline.json`
2. Keep the customer info OUT of the public repo (PDPL — local note only)
3. Add the objection pattern to `docs/OBJECTION_HANDLING_V6.md`
4. Move to a new warm intro for the next slot

— First 3 Customer Loop Board v1.0 · 2026-05-05 · Dealix
