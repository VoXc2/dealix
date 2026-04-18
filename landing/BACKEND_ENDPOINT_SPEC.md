# Backend Endpoint Required — `/api/v1/public/demo-request`

> **For:** backend subagent · **Consumer:** `landing/index.html` form submit · **Priority:** required before production launch

---

## Summary

The Dealix landing page form (`#demoForm`) POSTs demo/pilot requests to a public endpoint. This endpoint must be provisioned on the Dealix backend (FastAPI under `backend/`).

**Method:** `POST`
**Path:** `/api/v1/public/demo-request`
**Auth:** none (public). Rate-limited + honeypot + CORS restricted.

---

## Request body (JSON)

```json
{
  "name":    "string (required, 2-120 chars)",
  "company": "string (required, 2-160 chars)",
  "sector":  "enum: saas|banking|enterprise|distribution|government|other",
  "size":    "enum: 1-20|21-100|101-500|501-2000|2000+ (optional)",
  "phone":   "string (required; Saudi format: +?966?5XXXXXXXX or 05XXXXXXXX)",
  "email":   "string (required, RFC-5322)",
  "message": "string (optional, ≤ 2000 chars)",
  "source":  "string (optional, defaults to 'landing')",
  "ref":     "string (optional; document.referrer)",
  "consent": "boolean (required; must be true — PDPL)",
  "ts":      "ISO 8601 UTC timestamp (optional; client-supplied, server should ignore for records)"
}
```

### Ignored fields (honeypot)

If any of these are populated, **silently drop the request** (return 200 without side-effects):

- `website` — hidden honeypot field

---

## Response

### Success (200)

```json
{
  "ok": true,
  "id": "req_01HQ3...",
  "message": "Request received"
}
```

### Validation error (400)

```json
{
  "ok": false,
  "error": "validation",
  "fields": { "email": "invalid format" }
}
```

### Rate limit (429)

```json
{ "ok": false, "error": "rate_limited", "retry_after_seconds": 60 }
```

---

## Server-side requirements

1. **Validate** all fields with Pydantic (reject if missing required).
2. **Normalize phone** to E.164 (`+9665XXXXXXXX`) before storage.
3. **Persist** to `demo_requests` table with: `id, created_at, name, company, sector, size, phone_e164, email, message, source, ref, consent, ip_hash, ua_hash`.
4. **Consent audit:** store consent boolean + timestamp + IP hash (PDPL evidence). Do **not** store raw IP.
5. **Rate limit:** 3 requests per IP per 10 min; 10 per IP per day. Respond 429 on breach.
6. **Notify** on new request:
   - Send email/WhatsApp to `sami.assiri11@gmail.com` with the payload.
   - Create internal task/ticket.
7. **CORS:** allow only the production landing origin + localhost for dev. Reject others with 403.
8. **Honeypot:** if `website` populated, return 200 immediately without persisting or notifying (silent drop).
9. **Logging:** structured log with `correlation_id` for every request (audit trail matches `audit_trail` service).
10. **PDPL:** `POST /api/v1/public/demo-request` must be listed in the consent record as a purpose.

---

## Example FastAPI stub

```python
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
import hashlib, re, uuid, datetime as dt

router = APIRouter(prefix="/api/v1/public", tags=["public"])

SAUDI_PHONE = re.compile(r"^(?:\+?966|0)?5\d{8}$")

class DemoRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    company: str = Field(min_length=2, max_length=160)
    sector: str
    size: str | None = None
    phone: str
    email: EmailStr
    message: str | None = Field(default=None, max_length=2000)
    source: str = "landing"
    ref: str | None = None
    consent: bool
    ts: str | None = None
    website: str | None = None  # honeypot

    @validator("phone")
    def _phone(cls, v):
        digits = re.sub(r"[^\d+]", "", v)
        if not SAUDI_PHONE.match(digits):
            raise ValueError("phone_format")
        if digits.startswith("0"):
            digits = "+966" + digits[1:]
        elif digits.startswith("5"):
            digits = "+966" + digits
        elif not digits.startswith("+"):
            digits = "+" + digits
        return digits

    @validator("consent")
    def _consent(cls, v):
        if not v:
            raise ValueError("consent_required")
        return v

@router.post("/demo-request")
async def demo_request(payload: DemoRequest, request: Request):
    # Honeypot: silent drop
    if payload.website:
        return {"ok": True, "id": "drop"}

    # rate_limit_check(request.client.host)  # TODO: Redis/in-mem check

    ip = request.client.host or ""
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]
    ua_hash = hashlib.sha256((request.headers.get("user-agent","")).encode()).hexdigest()[:16]

    rid = "req_" + uuid.uuid4().hex[:12]
    # persist(...)
    # notify_sami(payload)
    return {"ok": True, "id": rid, "message": "Request received"}
```

---

## Testing

- **Happy path:** valid SAUDI phone + all required fields → 200 + id.
- **Invalid phone:** `+971501234567` → 400 `phone_format`.
- **Missing consent:** `consent=false` → 400 `consent_required`.
- **Honeypot triggered:** `website="spam"` → 200 but `id="drop"`, no DB record.
- **Rate limit:** 4th request within 10 min from same IP → 429.
- **CORS:** request from `https://evil.com` → 403.

---

## Dashboard surface (for ops)

Admin view at `/admin/demo-requests` (auth required) showing list + filters by sector, size, created_at. Each row links to create a Pilot opportunity.
