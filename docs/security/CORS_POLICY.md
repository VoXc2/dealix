# CORS Policy

> Source of truth for production CORS. Implementation: `api/main.py:130-136`. Env var: `CORS_ORIGINS`.

## Production

Allowed origins (exact match, no wildcards):
```
https://dealix.sa
https://www.dealix.sa
https://dashboard.dealix.me
https://app.dealix.me        # reserved for future SPA
```

`CORS_ORIGINS` env in Railway (production):
```
CORS_ORIGINS=https://dealix.sa,https://www.dealix.sa,https://dashboard.dealix.me,https://app.dealix.me
```

### Configuration
- `allow_credentials=True` (required for Authorization header from dashboard)
- `allow_methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"]`
- `allow_headers=["Authorization","X-API-Key","X-Request-ID","Content-Type","Accept"]`
- Preflight cache: 600 seconds (browser default; do not increase without security review)

## Staging

```
CORS_ORIGINS=https://staging.dealix.sa,https://staging-dashboard.dealix.me,http://localhost:3000,http://localhost:8501
```

## Development

```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8501,http://127.0.0.1:3000
```

## Forbidden

- `*` (wildcard) — never, even in staging
- `null` origin — never (Postman / curl don't need CORS)
- Origins without explicit scheme (`dealix.sa` vs `https://dealix.sa`) — always include scheme
- HTTP origins on production — never (allow only HTTPS in production)

## Verification

After every CORS env change, run:
```bash
curl -i -X OPTIONS https://api.dealix.me/api/v1/pricing/plans \
  -H "Origin: https://dealix.sa" \
  -H "Access-Control-Request-Method: GET"
# Expect: HTTP 200 + Access-Control-Allow-Origin: https://dealix.sa

curl -i -X OPTIONS https://api.dealix.me/api/v1/pricing/plans \
  -H "Origin: https://evil.example.com" \
  -H "Access-Control-Request-Method: GET"
# Expect: HTTP 400 (or 403) — no Access-Control-Allow-Origin header
```

CI test scaffold: `tests/security/test_cors_policy.py` (to add) — asserts above behaviour against the running app.

## Adding a new origin

1. PR titled `security(cors): add <origin>`
2. Justify in PR description: business need, data classification touched, expiry (if temporary)
3. Approve: founder + CTO (two-eye rule)
4. Update this doc + Railway env on merge
5. Run verification curl above
