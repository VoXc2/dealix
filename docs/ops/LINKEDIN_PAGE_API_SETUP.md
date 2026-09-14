# LinkedIn Company Page API Setup — one-time founder setup

One-time setup. ~20 minutes. Free (no LinkedIn paid plan required for organic posting).

This unlocks Dealix organization publishing via the official LinkedIn Posts API
(`POST https://api.linkedin.com/rest/posts`, current as of 2026-08 docs). It does
NOT authorize personal-profile automation, scraping, bot connections/DMs, or
auto-engagement — those remain blocked by `NO_LINKEDIN_AUTO` + `NO_SCRAPING`.

After this setup, the `dealix_linkedin_page` channel moves from
`OFFICIAL_API_OR_NATIVE_CONFIGURATION_REQUIRED` to API-canary, and exact publish
manifests can be executed under normal action-bound approval.

Source: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api

## What you need before you start

- A LinkedIn account that holds an **ADMINISTRATOR** (or CONTENT_ADMIN) role on
  the Dealix Company Page.
- Access to the LinkedIn Developer Portal (https://developer.linkedin.com/).
- 20 minutes + a channel to pass 3 secret values privately (never PR comments).

## Step-by-step

### 1. Create a LinkedIn app

Open: https://developer.linkedin.com/ → **Create app**.

- App name: **Dealix Publisher** (or equivalent).
- LinkedIn Page: select the Dealix Company Page.
- Upload logo, complete app details, check the legal agreement, **Create app**.
- Open the app → **Products** tab → request access to:
  - **Share on LinkedIn** (gives `w_member_social`),
  - **Sign In with LinkedIn using OpenID Connect** (gives `openid profile email`),
  - **Advertising API / Community Management** product surface that carries
    `w_organization_social` + `r_organization_social` for your region.
- Wait for product approval if LinkedIn puts the app in review (usually automatic
  for the basic share product; organization scopes may require verification).

### 2. Configure OAuth redirect

App → **Auth** tab:

- Add redirect URL: `http://localhost:8000/api/v1/integrations/linkedin/oauth/callback`
  (local canary only; production URL after deploy authority).
- Note the **Client ID** and **Client Secret** (keep private).

### 3. Mint the access token (run on your laptop)

Request scopes (minimum for Page publishing + read-back):

```
openid profile email w_organization_social r_organization_social
```

Authorization URL (open in browser, sign in as the Page admin):

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8000/api/v1/integrations/linkedin/oauth/callback&scope=openid%20profile%20email%20w_organization_social%20r_organization_social
```

Exchange the returned `code` (60s per exchange, single use):

```bash
curl -s -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d grant_type=authorization_code \
  -d code=RETURNED_CODE \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d redirect_uri=http://localhost:8000/api/v1/integrations/linkedin/oauth/callback
```

Keep the `access_token` private. Default lifetime is 60 days; record the expiry
date. (Refresh-token rotation for organization scopes follows the same endpoint
with `grant_type=refresh_token` once LinkedIn issues a refresh token for the app.)

### 4. Hand the values to Dealix (private channel only)

Pass exactly these three, e.g. WhatsApp to the founder directly, never in chat
logs or PRs:

1. `LINKEDIN_CLIENT_ID`
2. `LINKEDIN_CLIENT_SECRET`
3. `LINKEDIN_ACCESS_TOKEN` (+ its expiry date `LINKEDIN_TOKEN_EXPIRES_AT`)

Also confirm: **Dealix organization URN** (`urn:li:organization:{id}` — visible in
the Page admin URL or via Organization Lookup API).

### 5. Verification (run by Dealix, no publish)

```bash
curl -s https://api.linkedin.com/rest/posts \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Linkedin-Version: 202608" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  | head -c 300
```

Expected: HTTP 200 with post data (read-back via `r_organization_social`).
A DRAFT-mode canary post (`lifecycleState: DRAFT`) proves write scope without
publishing. First PUBLIC post always requires an exact publish manifest +
action-bound approval.

## What this does NOT unlock

- Founder personal profile automation (still manual-native only).
- Scraping, connection/DM bots, auto-like/comment (permanently blocked).
- Any publish without an approved immutable manifest (hash/account/time change =
  approval expires).

## After verification

Update `data/commercial/channel_readiness_registry.json` (`dealix_linkedin_page`
→ API canary evidence: token presence, scope, expiry, last canary, receipt) through
the normal tested PR path — never hand-edit production state.
