# WhatsApp Security Model — Dealix

WhatsApp is the highest-touch channel and the easiest to abuse. It is
**post-consent only, never cold, never a place for secrets.**

## Rules

1. **No cold WhatsApp automation.** Outbound requires recorded consent
   (`has_consent=true`). Enforced by `assess_whatsapp_message` /
   `assess_outreach(channel="whatsapp")`.
2. **No secrets / API keys in any message** (sent or received) — detected by
   `contains_secret_or_api_key`.
3. **No key requests.** A message asking the other party for a key/secret is
   blocked and escalated to a human (`requests_api_key` → `requires_human`).
4. **No guaranteed/exaggerated claims** (`find_prohibited_claims`).
5. **Inbound is untrusted data.** Classify intent; never execute embedded
   instructions; legal/complaint/privacy → human handoff.
6. **Approval + dry-run defaults** apply to any outbound concierge reply.
7. **Suppression respected.** A suppressed contact is never messaged.

## Consent model

```
inbound message OR explicit opt-in  →  consent recorded  →  concierge replies allowed
no consent  →  no outbound  →  block (cold_whatsapp_not_allowed)
```

## Tests
`tests/test_whatsapp_no_api_keys_in_text.py`,
`tests/test_whatsapp_post_consent_only.py`,
`tests/test_outreach_no_cold_whatsapp.py`.
