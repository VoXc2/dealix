# Key Rotation Runbook

## Why
A compromised key is a question of *when*, not *if*. Pre-scheduled rotation limits blast radius. Compromise rotation must be a 5-minute paper-trail, not a 5-hour scramble.

## Inventory (source of truth)

| Key | Where stored | Purpose | Rotation interval | Owner |
|-----|--------------|---------|-------------------|-------|
| `APP_SECRET_KEY` | Railway env + 1Password | Sign cookies, CSRF | **90 days** | CTO |
| `JWT_SECRET_KEY` | Railway env + 1Password | JWT signing | **90 days** | CTO |
| `API_KEYS` (per-tenant) | Railway env + per-customer record | Tenant API access | **180 days** + on customer request | Founder |
| `ADMIN_API_KEYS` | Railway env + 1Password | /api/v1/admin/* | **90 days** | Founder + CTO only |
| `MOYASAR_SECRET_KEY` (`sk_live_`) | Railway env + 1Password | Moyasar API | Per Moyasar policy (annual) | Founder |
| `MOYASAR_WEBHOOK_SECRET` | Railway env + Moyasar dashboard | HMAC verify | **90 days** | Founder |
| `CALENDLY_WEBHOOK_SECRET` | Railway env + Calendly dashboard | HMAC verify | 180 days | Ops |
| `WHATSAPP_APP_SECRET` | Railway env + Meta dashboard | HMAC verify | 90 days | Ops |
| `WHATSAPP_ACCESS_TOKEN` | Railway env + Meta dashboard | Send API | Per Meta policy (60 days) | Ops |
| `GMAIL_REFRESH_TOKEN` | Railway env | Email send | On 401/invalid_grant only | Ops |
| `SENTRY_DSN` | Railway env | Sentry ingest | Project-level (rare) | CTO |
| `POSTHOG_API_KEY` | Railway env | Analytics ingest | Project-level (rare) | CTO |
| `RAILWAY_TOKEN` | GitHub secrets | Deploy from CI | **90 days** | CTO |
| `BACKUP_ENCRYPTION_KEY` | 1Password only (NOT Railway) | Encrypt pg_dump | **365 days** | CTO + Founder |
| `AWS_ACCESS_KEY_ID/SECRET` | Railway env + 1Password | S3 backups | 90 days | CTO |
| LLM keys (Anthropic / OpenAI / Groq) | Railway env | LLM calls | 180 days | CTO |

## Scheduled rotation (calendar)

| Month | Rotate |
|-------|--------|
| Jan, Apr, Jul, Oct | APP_SECRET_KEY, JWT_SECRET_KEY, ADMIN_API_KEYS, RAILWAY_TOKEN, MOYASAR_WEBHOOK_SECRET, AWS keys, WHATSAPP_APP_SECRET |
| Mar, Sep | API_KEYS, CALENDLY_WEBHOOK_SECRET, LLM keys |
| Annually (Jan) | BACKUP_ENCRYPTION_KEY (with backup file re-keying — see below) |

Add Calendar invites to founder + CTO on day -7 of each rotation window.

## Standard rotation procedure (zero-downtime)

1. **Pre-flight** — confirm no active incident; staging is green.
2. **Generate new value** — never re-use old:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"      # for 64-byte hex
   python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"   # for url-safe
   ```
3. **Stage as `_NEXT` env var** — e.g. add `JWT_SECRET_KEY_NEXT` alongside the live `JWT_SECRET_KEY`. App code already supports dual-verify on JWT (verifies with primary; falls back to NEXT). Deploy.
4. **Promote** — once deployed and verified (smoke test passes), rename `JWT_SECRET_KEY_NEXT` → `JWT_SECRET_KEY` and remove the old. Deploy.
5. **Update 1Password** — overwrite the entry, attach a short note: `rotated_at = ISO timestamp`, `rotated_by = name`, `reason = scheduled|compromise`.
6. **Log** — append a line to `docs/security/key_rotation_log.md`.

For symmetric webhook HMACs (Moyasar/Calendly/WhatsApp), there is **no dual-secret support out of the box** — coordinate a 5-minute window:
- Update Railway env first
- Update the external dashboard immediately after
- During the gap, webhook signatures may fail and re-queue via DLQ. Replay after rotation.

## Compromise rotation (emergency)

If a key is suspected compromised:

```bash
# 1. Mark compromised in 1Password (red flag)
# 2. Generate new value
# 3. Replace in Railway IMMEDIATELY — don't wait for graceful path
# 4. For external services (Moyasar, Meta, Google), update their dashboard right after
# 5. Force-revoke any tokens minted with the old secret (JWT: rotate JWT_SECRET_KEY same time)
# 6. Open SEV-2 incident, document in INCIDENT_RUNBOOK format
# 7. If personal data exposure suspected → PDPL_BREACH_RUNBOOK
```

## Verification after rotation

Smoke test pack (run from `scripts/post_rotation_smoke.sh`, to be written):
- Login with a known account → JWT signing works
- Submit demo request → API key auth still works
- Trigger Moyasar test webhook → HMAC verifies
- Send Calendly test webhook → HMAC verifies
- Send WhatsApp echo → HMAC verifies

If any smoke fails: rollback the rotated key from 1Password's previous version, investigate.

## Backup encryption key — special case

Rotating `BACKUP_ENCRYPTION_KEY` requires re-encrypting in-flight backups:
1. Generate new key
2. For the next 30 days, encrypt with **both** old + new (dual-write) — script: `scripts/dual_backup_during_rotation.sh`
3. After 30 days, old backups expired naturally; switch to new-only
4. Test restore with new key in a drill before purging old key from 1Password

## Logging

`docs/security/key_rotation_log.md` is append-only. Each entry:
```
| Date (UTC) | Key | Reason | Rotated by | Verified by | Notes |
```

Never include the old or new value, only the metadata.
