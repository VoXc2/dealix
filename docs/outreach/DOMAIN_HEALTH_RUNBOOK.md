# Domain Health Runbook

## Daily / pre-send checks
1. SPF, DKIM, DMARC resolve and align.
2. Sending domain not on major blocklists (Spamhaus, etc.).
3. Postmaster Tools reputation = High/Medium (not Low/Bad).
4. Bounce rate < 2% (warn at 2–5%, **PAUSE** at >5%).
5. Spam complaint rate < 0.1% (**PAUSE** at ≥ 0.3%).

## If reputation drops
1. **Pause** all sending (verdict → `PAUSE_REQUIRED`).
2. Identify cause: list quality, content, volume jump, auth break.
3. Clean list (remove invalid/risky → suppression `invalid_email`/`duplicate_risky`).
4. Re-warm slowly per `SENDING_RAMP_PLAN_AR.md`.
5. Resume only after reputation recovers + founder approval.

## Separation
- Use a **subdomain** for cold outreach, separate from the primary corporate domain.
- Keep transactional and marketing streams separate.
