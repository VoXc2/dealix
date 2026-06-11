# Session Security Plan (Dealix)

## Cookie attributes
- HttpOnly: true
- Secure: true (production)
- SameSite: Lax
- Path: /
- Max-Age: 3600 (1 hour) for admin, 86400 for marketing pages

## CSRF
- All POST/PUT/DELETE require `X-Requested-With: XMLHttpRequest`
- Or use a CSRF token in form

## Idle timeout
- Admin: 60 minutes
- Marketing: 8 hours

## Logout
- Always call `/api/auth/logout` to clear server-side state
- Clear cookie on client

## Penetration test (recommended)
- Run annually
- Test for: session fixation, CSRF, XSS, SQLi, IDOR
