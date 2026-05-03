# Support Bot — Reality Matrix

> Source: live `https://api.dealix.me/api/v1/support/*` (verified 2026-05-03).
> The support stack lives on the deploy branch only.

## Surface

| Endpoint | Method | Purpose | Status |
| --- | --- | --- | --- |
| `/api/v1/support/classify` | POST | classify message → priority/category/SLA, escalate flag | PROVEN_LIVE |
| `/api/v1/support/sla` | GET | SLA matrix P0–P3 with Arabic labels | PROVEN_LIVE |
| `/api/v1/support/tickets` | POST/GET | create or read tickets (requires `email_or_session_required`) | CODE_EXISTS_NOT_PROVEN (write path not exercised) |
| `/api/v1/support/tickets/{ticket_id}` | GET | single ticket | CODE_EXISTS_NOT_PROVEN |

## SLA matrix (live response)

```
P0  → 1 hour    "خلال ساعة"      أمان / إرسال خاطئ / تعطل كامل
P1  → 8 hours   "نفس اليوم"      خدمة مهمة لا تعمل
P2  → 24 hours  "24 ساعة"        connector / Proof Pack متأخر
P3  → 48 hours  "48 ساعة"        سؤال أو طلب تحسين
```

## Capability checklist (verified vs. spec)

| Topic | Verified? | Notes |
| --- | --- | --- |
| What is Dealix | CODE_EXISTS_NOT_PROVEN | classifier only categorizes; long-form answer not exercised here |
| Pricing | CODE_EXISTS_NOT_PROVEN | falls back to `/api/v1/business/pricing` (live, working) |
| How Growth Starter works | CODE_EXISTS_NOT_PROVEN | bundle catalog covers it (`/api/v1/services/growth_starter`) |
| How Data to Revenue works | CODE_EXISTS_NOT_PROVEN | covered by services catalog |
| How Partnership Growth works | CODE_EXISTS_NOT_PROVEN | covered by services catalog |
| How Proof Pack works | CODE_EXISTS_NOT_PROVEN | covered by `/api/v1/business/proof-pack/demo` |
| Privacy / safety / PDPL | CODE_EXISTS_NOT_PROVEN | trust-center.html exists |
| WhatsApp do/don't | CODE_EXISTS_NOT_PROVEN | covered in WHATSAPP_POLICY_AND_FLOW |
| How to start Diagnostic | PROVEN_LIVE | `POST /api/v1/operator/service/start {bundle_id:"free_diagnostic",…}` |
| How to book a call | CODE_EXISTS_NOT_PROVEN | calendly link present in inbound responses |
| Payment / invoice questions | PROVEN_LOCAL | `payments/manual-request` returns bank-transfer SOP |
| Human handoff | PROVEN_LIVE | classifier returns `escalate_human=true` for P0/P1 keywords |

## Anti-pattern checklist (must NOT do)

| Pattern | Status | Evidence |
| --- | --- | --- |
| Promise guaranteed sales | not present in catalog or pricing responses | grep on "guaranteed" / "نضمن" returns nothing in live responses |
| Offer cold WhatsApp blasting | blocked at compliance gate AND (most) operator intents | gate: `WHATSAPP_ALLOW_LIVE_SEND=false`; operator: 10/14 — see operator matrix |
| Claim legal advice | not exposed | n/a |
| Auto-charge | blocked by absence of `MOYASAR_SECRET_KEY` env on this account; live charge code path requires explicit key | `payments/manual-request` returns bank-transfer fallback |
| Auto-send customer messages | blocked | `WHATSAPP_ALLOW_LIVE_SEND=false`, gmail not configured |

## Escalation triggers (verified in code)

The classifier escalates `human=true` when message contains: billing dispute
keywords (refund / dispute / chargeback), legal/privacy complaint keywords
(legal / lawyer / pdpl violation), production outage / `down`. P3 (the
default for benign questions) does NOT escalate.

## Known gaps (BACKLOG)

- No long-form FAQ generator on the support endpoint — relies on the
  caller to render the SLA / classification + redirect to docs.
- Tickets store is not exercised here. The `email_or_session_required` 400
  on `GET /api/v1/support/tickets` confirms a guard exists but content was
  not verified.
- No Arabic-Saudi tone profile on classification responses (returns
  Arabic but tone-neutral). **BACKLOG**.
