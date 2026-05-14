# Market Feedback Capture

The honest signal that the market is responding. Public endpoint with
consent + honeypot + email redaction.

## Endpoints

```
POST /api/v1/public/market-feedback
GET  /api/v1/public/market-feedback/summary
```

POST body:

```json
{
  "signal_type": "objection",
  "message": "Pricing seems steep for a sprint.",
  "consent": true,
  "role": "Director of Strategy",
  "sector": "professional_services"
}
```

Valid `signal_type`: `objection | request | praise | idea`.

## Honesty Discipline

- Honeypot: a non-empty `website` field silently drops the request.
- Emails inside `message` are redacted to `[email]` before storage.
- `name` and `email` fields are accepted but **NEVER** returned by any
  public read. Internally only `name_present` / `email_present` are
  recorded.
- The summary endpoint exposes only counts + 5 recent anonymized
  quotes (max 200 chars each).

## Storage

Append-only JSONL at `data/_state/market_feedback.jsonl`. One row per
event. Provenance: `feedback_id` (UUID hex) + `received_at` (UTC ISO).

## Operating Loop

- `scripts/market_feedback_summary.py` writes
  `data/_state/market_feedback_summary.{json,md}` for the daily routine
  to surface in the founder brief.
- The verifier rewards score 5 only when the summary has >= 1 entry in
  the last 30 days (see Master Verification Matrix row 24).

## Doctrine

No names. No emails. No phone numbers. Only signal type, redacted
quote, and sector if provided. Consent is required for storage.

## Suggested Founder Cadence

After every partner / customer / advisor conversation, the founder
opens the JSON page (or copy-pastes a short message) into the public
endpoint as the "what did I learn" capture. The summary in the daily
brief makes the running tally visible without re-narrating.
