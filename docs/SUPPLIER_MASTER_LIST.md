# Supplier Master List — Dealix

**Status:** DRAFT — founder fills contract status + renewal dates
**Owner:** Sami (founder) · audit quarterly
**Last updated:** 2026-05-07
**Companion docs:** `docs/PRIVACY_PDPL_READINESS.md` (subprocessor list) · `landing/subprocessors.html` · Plan §23.5.9

> **Why this doc exists:** Without a single source of truth for vendors + renewal dates, surprise expiries (Hunter API key, Cloudflare cert, Moyasar onboarding) will block customer onboarding at the worst time. With it, founder Friday review surfaces 60-day-out renewals, no surprises.

---

## 1. The vendor table

Legend:
- **Service tier:** `infra` (downtime kills product) · `feature` (gets feature partly) · `ops` (internal-only)
- **PDPL:** `Y` if processes Saudi customer PII (must be in DPA chain) · `N` if not
- **Status:** `LIVE` (active subscription) · `READY` (account exists, not paid yet) · `PENDING` (signing up) · `NOT_NEEDED_YET` (deferred)
- **Renewal action SLA:** how many days before renewal to start vendor review

| # | Vendor | Service | Tier | PDPL | Status | Monthly cost (SAR) | Contract / API key | Primary contact | Renewal date | Renewal SLA |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Railway | Backend hosting (api.dealix.me) | infra | Y | LIVE | ~150 | env: RAILWAY_TOKEN | railway.com support | _TBD_ | 60 days |
| 2 | Cloudflare | DNS + CDN (dealix.me) | infra | Y (caches HTML) | LIVE | 0 (free) | dashboard.cloudflare.com | _TBD_ | _TBD_ | 30 days |
| 3 | GitHub | Source code + Pages (landing) | infra | N | LIVE | 0 (free public) | github.com/voxc2/dealix | _TBD_ | annual | 30 days |
| 4 | Anthropic | LLM API (Claude) | feature | Y (logs may include PII) | LIVE | variable (~50-200 SAR) | env: ANTHROPIC_API_KEY | console.anthropic.com | rolling | always-on |
| 5 | Groq | LLM API (fallback) | feature | Y | LIVE | usage-based | env: GROQ_API_KEY | console.groq.com | rolling | always-on |
| 6 | Hunter | Email enrichment | feature | Y (sub-processor) | NOT_LIVE_YET | $49 (~185 SAR) | env: HUNTER_API_KEY (P0.X) | hunter.io support | activation pending | 30 days from go-live |
| 7 | Moyasar | Payment gateway | infra | Y (financial) | NOT_LIVE_YET (sandbox only) | 2.75% per txn | merchant onboarding pending | moyasar.com support | n/a | always-on |
| 8 | Calendly | Demo scheduling | feature | Y (sched data) | NOT_LIVE_YET | $10-20/mo | env: CALENDLY_TOKEN (P0.4) | help.calendly.com | rolling | 30 days |
| 9 | HubSpot | Light CRM | feature | Y | NOT_NEEDED_YET (CRM v10 internal handles it) | $0 free tier | env: HUBSPOT_TOKEN (P0.3) | hubspot.com | rolling | 30 days |
| 10 | PostHog | Funnel analytics | feature | Y | NOT_LIVE_YET | $0 free tier | env: POSTHOG_KEY (P0.1) | posthog.com | rolling | 30 days |
| 11 | UptimeRobot | Status monitoring | ops | N | NOT_LIVE_YET | $0 free tier | dashboard.uptimerobot.com | uptimerobot.com | rolling | 30 days |
| 12 | Supabase | Postgres + Auth (some workflows) | infra | Y | depends on use | usage-based | env: SUPABASE_URL + KEY | supabase.com | rolling | always-on |
| 13 | Sentry | Error tracking | ops | N (no PII in stack traces) | _TBD_ | $0 free tier | sentry.io | _TBD_ | rolling | 30 days |
| 14 | Meta WhatsApp Business | WhatsApp Business API | infra | Y | NOT_APPROVED_YET | $0.05/conv | business.whatsapp.com pending | _TBD_ | rolling | always-on |
| 15 | Namecheap | Domain (dealix.me) | infra | N | LIVE | ~120/year | namecheap.com account | _TBD_ | _TBD_ (annual) | 60 days |
| 16 | Microsoft 365 / Google Workspace | Email + docs | ops | Y (employee email) | _TBD_ founder pick | $6-15/user/mo | _TBD_ | _TBD_ | annual | 30 days |
| 17 | Tavily / SerpAPI / Google Custom Search | Web search for radar | feature | N (no customer PII) | NOT_NEEDED_YET | $50-100/mo when activated | env vars | _TBD_ | rolling | 30 days |

---

## 2. PDPL sub-processor disclosure

Per `landing/subprocessors.html`, ALL vendors with PDPL=Y must:

1. Have a written DPA / sub-processing agreement on file (or vendor's standard SCC)
2. Be listed on `landing/subprocessors.html` publicly
3. Be reviewed quarterly for breach reports / regulatory changes

**Action when adding a new PDPL=Y vendor:**

1. Sign vendor's DPA (or counter-sign Dealix's DPA template — lawyer reviews)
2. Add row to this file
3. Update `landing/subprocessors.html` within 7 days
4. Notify all existing customers via WhatsApp + email of new sub-processor (PDPL transparency)
5. Lawyer review for cross-border data transfer (if vendor stores outside KSA — most US/EU vendors do)

---

## 3. Vendor risk classification

### Tier-1 (downtime = customer-visible problem within 1 hour)

- Railway (api.dealix.me)
- Cloudflare (DNS)
- Anthropic (Claude API for narrative generation)

**Mitigation:** dual provider for LLMs (Anthropic + Groq fallback), Cloudflare alternative ready (Bunny CDN), Railway alternative documented (Render / Fly.io).

### Tier-2 (downtime = degraded feature, but product still usable)

- Hunter (lead enrichment falls back to manual)
- Moyasar (bank transfer fallback for payments)
- Calendly (manual booking via WhatsApp)
- Meta WhatsApp Business (manual personal WhatsApp covers up to customer #3)

**Mitigation:** documented fallback per vendor in Tier-2 (manual workaround).

### Tier-3 (downtime = internal annoyance, no customer impact)

- PostHog (analytics gap, no fix needed)
- UptimeRobot (status page goes stale)
- Sentry (errors logged elsewhere)

**Mitigation:** none required short-term.

---

## 4. Vendor onboarding checklist (when adding a new vendor)

1. Identify need (which gap does this vendor close?)
2. Cost estimate vs alternative
3. PDPL classification (Y/N)
4. If PDPL=Y: lawyer reviews vendor DPA before signup
5. Add row to this file (status=PENDING)
6. Sign + activate
7. Update `landing/subprocessors.html` if PDPL=Y
8. Update env vars in deployment (Railway / local)
9. Status → LIVE, set renewal SLA reminder

---

## 5. Vendor offboarding checklist (when terminating a vendor)

1. Confirm no active customer dependency (search code for env var references)
2. Export any vendor-stored data Dealix needs
3. Notify customers if PDPL=Y removed (transparency)
4. Cancel subscription
5. Rotate any related API keys / secrets
6. Update `landing/subprocessors.html` (remove)
7. Update this file (status=OFFBOARDED + date)

---

## 6. Friday review — 5 minutes

Every Friday, scan this file for:

1. Any vendor with renewal date <60 days out + status not yet LIVE → schedule onboarding
2. Any LIVE vendor where last quarterly review was >90 days → re-audit
3. Any cost line >2× expected → investigate billing

If 2+ items flagged → 30-min deep dive same week.

---

## 7. Quarterly compliance audit

Once per quarter:

- Verify each PDPL=Y vendor's DPA still in force
- Verify each PDPL=Y vendor hasn't had public breach (search vendor name + "breach" / "data leak")
- Verify costs match billing actuals
- Update this file's "Last updated" date

---

## 8. Hard rules

- ❌ Never add a vendor without PDPL classification first
- ❌ Never store PDPL=Y vendor credentials outside env vars / secrets manager
- ❌ Never skip lawyer review on a PDPL=Y vendor's DPA before signup
- ❌ Never let renewal lapse on Tier-1 vendor
- ❌ Never share vendor credentials in WhatsApp / Slack / email plaintext
- ✅ Always update this file within 7 days of any vendor change
- ✅ Always update `landing/subprocessors.html` for PDPL=Y changes
- ✅ Always notify customers of new sub-processors before going live
- ✅ Always document Tier-1/Tier-2 vendor fallback procedures
