# Connector Env Vars — when you're ready to upgrade the machine

v1 ships without paid connectors (LLM-native). Add these env vars in Railway → Variables to unlock each connector.

---

## Google Custom Search API

**Purpose:** real-time web discovery of Saudi companies, press, job posts, partner pages.

| Env var | Where to get it | Notes |
|---------|-----------------|-------|
| `GOOGLE_SEARCH_API_KEY` | https://console.cloud.google.com/apis/credentials → Create API key | Enable "Custom Search API" on the project first |
| `GOOGLE_SEARCH_CX` | https://programmablesearchengine.google.com → Create engine → copy the "cx" ID | Configure to search the entire web, enable "Image search" off |

**Free tier:** 100 queries/day. Paid: $5 per 1K queries after that (up to 10K/day).

**Cost estimate for Dealix:** with 5-10 queries per lead and 20 leads/day → 100–200 queries/day → mostly within free tier.

---

## Wappalyzer API (technographics)

**Purpose:** detect which tools a target uses (HubSpot, Calendly, Shopify, Intercom, Meta Pixel, etc.) — the strongest intent signal.

| Env var | Where to get it |
|---------|-----------------|
| `WAPPALYZER_API_KEY` | https://www.wappalyzer.com/api/ |

**Pricing (as of 2026):** Free tier 50 URLs/day; paid plans start ~$100/mo for 1K URLs.

**Alternative free sources:**
- `BuiltWith.com` public pages (scrape sparingly, attribution required)
- `Wappalyzer Lite` browser extension for manual lookups
- Self-inspect HTML head/script tags for common tool signatures (Calendly, HubSpot, Shopify, WordPress, Meta Pixel)

---

## Apollo API

**Purpose:** find decision-makers by role + seniority + geography. Optional enrichment (email, phone) within plan.

| Env var | Where to get it |
|---------|-----------------|
| `APOLLO_API_KEY` | Apollo.io → Settings → API |

**Pricing:** Free tier limited; paid plans from $49/user/mo.

**Dealix pattern:** use People Search only (no email reveals) unless explicitly needed; stay within plan.

---

## Moyasar (already wired)

| Env var | Status |
|---------|--------|
| `MOYASAR_SECRET_KEY` | ⚠️ Sami to re-verify after KYC activation — see `MOYASAR_HOSTED_CHECKOUT.md` |
| `MOYASAR_WEBHOOK_SECRET` | ✅ Set in Railway |

---

## Optional: Saudi-specific sources

### CR (Commercial Registration) lookup
Public SP portal: https://www.mc.gov.sa/ar/eservices/Pages/ShowServiceDetails.aspx — manual lookup only (no public API). Use for validation, not bulk.

### Monsha'at / SME Authority
https://www.monshaat.gov.sa — public lists of SMEs that joined programs. Manual discovery.

### GOSI (public-sector contractor list)
Public contractor directory. Only use for B2G pathway.

### Wamda / MAGNiTT press
https://www.wamda.com , https://magnitt.com — public press and startup pages. Use `site:` queries via Google Custom Search.

---

## Setup order recommendation

1. **First week:** v1 LLM-native (no connectors) — validate product-market fit
2. **After 5 paying customers:** add `GOOGLE_SEARCH_API_KEY` + `GOOGLE_SEARCH_CX` (free tier covers you)
3. **After 10 customers:** add `WAPPALYZER_API_KEY` ($100/mo pays back with better targeting)
4. **After 20 customers or partner launch:** add `APOLLO_API_KEY` (when volume justifies)

Do not pay for connectors until v1 proves value.
