# DesignOps — First-Customer Walk-through

How a real founder runs DesignOps OS for the first paying customer. No
real names; the customer in this doc is `prospect_handle = "founder_X"`.

Every step ends with a `safe_to_send=False` artifact and a founder review
banner. Nothing is sent without the founder pasting it manually.

## Step 1 — Warm intro → diagnostic call
- Founder books a 30-minute call from a warm intro (no cold outreach).
- Notes from the call go into a local file, not into a CRM.

## Step 2 — Generate a Mini Diagnostic
```
POST /api/v1/designops/generate/mini-diagnostic
{
  "customer_handle": "founder_X",
  "pain_points": ["unclear sales motion", "no pricing baseline"]
}
```
- Returns `manifest` (with `safe_to_send: false`) + `content` (md + html).
- Founder calls `export_artifact(...)` → files land in
  `docs/designops/exports/<YYYY-MM-DD>/founder_X-mini-diag.md` (and `.html`,
  `.json`).

## Step 3 — Review the HTML in a local browser
- Open the `.html` in Firefox/Chrome locally.
- Read AR and EN side-by-side. Check the founder review banner is at the
  top.
- Re-run the safety gate. Look for forbidden tokens.

## Step 4 — Manually share the markdown
- Founder copies the `.md` content into WhatsApp / email.
- Customer receives the content; nothing automated.
- Founder logs the share in `proof_ledger` with `event_type=artifact_shared`.

## Step 5 — Customer accepts → generate Proposal page
```
POST /api/v1/designops/generate/proposal-page
{
  "customer_handle": "founder_X",
  "tier_id": "pilot_499_sar",
  "scope": ["mini diagnostic", "1 follow-up call", "written summary"]
}
```
- Founder reviews HTML, flips `safe_to_send=true` only after redaction
  confirmed, then shares manually.

## Step 6 — Customer pays → Pricing reference + Invoice
- Founder generates `pricing_reference` (founder-only artifact, never
  shared raw).
- Founder generates `invoice_draft` → JSON manifest is handed to
  `scripts/dealix_invoice.py`.
- **No live charge.** `MOYASAR_SECRET_KEY` is `sk_test_*` and
  `DEALIX_ALLOW_LIVE_CHARGE` is unset. Even if both were set, the
  `is_live_charge_allowed()` invariant still returns False.
- Founder sends the Moyasar test-mode payment link manually.

## Step 7 — Day 7 → Proof Pack
```
POST /api/v1/designops/generate/proof-pack
{
  "customer_handle": "founder_X",
  "since_iso": "2026-04-28T00:00:00Z"
}
```
- Pulls evidence from `proof_ledger` (consent-confirmed only).
- Founder reviews, anonymizes any third-party names, then shares manually.

## Step 8 — End of week → Executive Weekly Pack
```
POST /api/v1/designops/generate/executive-weekly-pack
{
  "since_iso": "2026-04-29T00:00:00Z"
}
```
- Founder-only artifact. Not shared with the customer.
- Used as the input to the founder's own weekly decision review.

## Per-step founder review banner (rendered into every customer-facing artifact)
```
─────────────────────────────────────────────────────────────
 DRAFT — safe_to_send=False — founder review required
 لا تُرسَل قبل مراجعة المؤسس
─────────────────────────────────────────────────────────────
```
The banner is removed from the artifact only after the founder edits the
manifest by hand. The exporter does not strip it.

## What can go wrong (and what to do)
- **Forbidden token leaked.** Stop. Follow incident response in
  `DESIGNOPS_ARTIFACT_SAFETY.md`.
- **Customer name appears in an artifact unintentionally.** Quarantine,
  re-run the gate, and add the phrasing pattern to the gate's regex.
- **Wrong pricing tier.** Regenerate from `finance_os.pricing_catalog`.
  The catalog is the single source of truth, not the proposal copy.
- **Live charge attempted.** Cannot happen by design — the invariant in
  `tests/test_finance_os_no_live_charge_invariant.py` blocks it.
