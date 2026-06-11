# Production Auth Requirements (Dealix)

## Must have before production
1. `DEALIX_ADMIN_TOKEN` set (32+ chars)
2. `DEALIX_ADMIN_PASSWORD` set (16+ chars)
3. `NEXT_PUBLIC_DEMO_MODE=false`
4. HTTPS enabled
5. Secure cookies (HttpOnly, Secure, SameSite)
6. CSRF protection on all POST routes

## Recommended
1. Rate limiting on `/api/auth/*`
2. IP allowlist for `/crm/*`, `/war-room/*`
3. Audit log on every admin access
4. Auto-logout after 60 min idle
5. 2FA for founder

## Out of V6 scope
- SSO (SAML, OAuth)
- 2FA
- IP allowlist (planned for V7)
