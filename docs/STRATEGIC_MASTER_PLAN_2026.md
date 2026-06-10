# Dealix — Strategic Master Plan (2026 H2 → 2027)

> Strategic plan for turning Dealix into the dominant Saudi Revenue
> Execution OS — covering positioning, business model, defensible
> moats, autonomous operation, distribution, GEO/AIO discoverability,
> and a 90-day → 12-month execution sequence.
>
> Grounded in real 2026 market signals (sources at the bottom).
> Respects every hard rule from the four prior prompts: no live
> sends/charges, no scraping, no cold WhatsApp, no fake data, no
> pricing changes without proof, Arabic primary.

## Part I — The Five Market Truths That Decide Strategy

These are not opinions. Each is sourced from 2026 research at the
end of this document.

1. **Saudi SaaS market is growing 14.63% CAGR through 2030**, driven
   explicitly by Vision 2030 manufacturing and digital sovereignty
   initiatives. The market doubled to $2.86B in 2024 and is on track
   to $6.49B by 2030.
2. **Data residency is no longer optional.** 70%+ of cloud-hosted
   SaaS in KSA already runs on local data centers (up from 20% in
   2020). Enterprises buying foreign tools without KSA-resident
   storage face procurement friction.
3. **PDPL enforcement is real.** SDAIA issued 48 sanction decisions
   in 2025 alone, with fines up to **5,000,000 SAR per breach**
   (doubled for repeat offenses) and **up to 2 years prison** for
   sensitive-data violations. Marketing without explicit opt-in is
   the most-punished category.
4. **The "blast 500 emails/week" model is dying.** Salesloft is
   architecturally obsolete in 2026 per industry analysis; buyers
   demand personalized, research-based outreach. Gong pricing
   ($1,360–$1,600/user/year + $5K–$50K platform fee + $15K–$65K
   implementation = $80K–$130K/year for 50 reps) prices it out of
   the Saudi SME market entirely.
5. **48% of B2B buyers now research vendors via AI tools** (ChatGPT,
   Perplexity, Gemini) before visiting a website. AI-referred
   sessions grew **527% YoY** in early 2025. Perplexity cites new
   content within 1–2 weeks; ChatGPT in 6–12 weeks.

## Part II — Why Dealix's Existing Architecture Is the Winning Shape

Read the truths above against what's already in the repo:

| 2026 Truth | Dealix's Existing Answer | Code Evidence |
|---|---|---|
| Vision 2030 SME push | Saudi-first positioning, Arabic-primary UX, 499 SAR pilot wedge | `docs/PRICING_STRATEGY.md`, `landing/index.html` |
| Data residency required | YAML matrix has `cross_border_restriction` service; KSA-resident storage in `definition_of_live` | `docs/registry/SERVICE_READINESS_MATRIX.yaml::services[id=cross_border_restriction]` |
| PDPL fines for marketing without consent | `assess_contactability` blocks cold WA; `consent_required_send` service in matrix; restricted-actions registry blocks `send_cold_whatsapp` / `auto_linkedin_dm` | `auto_client_acquisition/v3/compliance_os.py:37-39`, `auto_client_acquisition/v3/agents.py:66`, matrix `services[id=consent_required_send]` |
| Blast model is dead | Architecture is "draft → approve → send" only; `ApprovalGate` (Redis) for queueing | `dealix/governance/approvals.py:96-150`, `auto_client_acquisition/personal_operator/operator.py:308-346` |
| AI buyers research first | Service Activation Console at `/status.html` is bilingual, structured, honest, JSON-exportable — exactly what AI engines want to cite | `landing/status.html`, `landing/assets/js/service-console.js`, `landing/assets/data/service-readiness.json` |

**Strategic implication:** Dealix doesn't need to invent a new
position. The market is moving *toward* the architecture Dealix
already has. The job is to (a) get one paying customer to validate
willingness-to-pay, (b) deploy what's built, (c) compound
distribution — not to build more product.

## Part III — Defensible Moats, Ranked

A moat is something a competitor can't copy in 6 months. Ranked
strongest → weakest:

1. **Regulatory moat** — PDPL audit trail + KSA data residency.
   International tools take 12–18 months to build a localized
   compliance posture; by then Dealix has the customer references.
2. **Linguistic moat** — Saudi-executive Arabic register (Khaliji,
   not standard MSA). The chat demo on `landing/index.html:192-199`
   is already Khaliji-native. Translated tools sound foreign;
   Dealix sounds local.
3. **Trust moat (architectural)** — approval-first agent design.
   `SafeAgentRuntime.restricted_actions`, `ApprovalGate`, the 8-gate
   validator. Buyers afraid of an AI "going rogue" can read the code.
4. **Brand-honesty moat** — the Service Activation Console publicly
   shows "0 Live, 1 Pilot, 7 Partial, 24 Target." No competitor
   does this. It's a CONVERSION asset because it proves Dealix
   doesn't lie. AI engines also love structured honesty.
5. **Distribution moat (compounding)** — Saudi B2B agencies (sales
   consultants, marketing agencies, CRM implementers) become
   resellers/co-deliverers. Each onboarded agency = ongoing pipeline
   with no marketing spend. International tools rarely build deep
   Saudi agency channels.
6. **Data moat (over time)** — every Proof Pack delivered =
   structured ProofEvent rows. After 50+ events, Dealix can
   benchmark conversion rates, message lift, sector ROI in ways no
   foreign tool can match for KSA.

## Part IV — The Smartest Business Model

Built on the principle: *low-risk first dollar, expanding contract
value with proof, recurring with operational integration, defensible
with compliance*.

### IV.A The Pricing Ladder (Refined)

Current ladder vs recommended evolution. **No pricing changes
yet** — recommendations only, in line with the master prompt's
"don't change pricing" rule.

| Tier | Now | After 3 Proofs | After 10 Customers | Locks In |
|---|---:|---:|---:|---|
| Free Diagnostic | Free | Free | Free | Wedge — only marketing cost |
| Growth Starter Pilot | 499 SAR | 499 SAR (Pilot only) | retire as a SKU | First-payment friction reducer |
| Growth Starter | — | 990 SAR (one-shot) | 1,490 SAR | Post-proof first paid service |
| Data to Revenue | 1,500 SAR | 1,500 SAR | 2,500 SAR | One-shot data project |
| Executive Growth OS | 2,999 SAR/mo | 2,999 SAR/mo | 3,999 SAR/mo | Recurring core |
| Executive Growth OS Plus | — | 5,999 SAR/mo | 8,999 SAR/mo | Heavier delivery |
| Partnership Growth | 3,000–7,500 SAR | same | 5,000–12,000 SAR | Project-based |
| Full Control Tower | Custom | Custom | Custom (50K+ SAR/mo) | Enterprise anchor |

**Pricing logic:**
- Pilot 499 SAR is a *cost of customer acquisition*, not a profit
  product. Cap it at 5 paid pilots, then retire.
- Annual contract discount = 2 months free (saves CAC, locks
  retention).
- Compliance tier: any customer needing **DPO-shareable PDPL audit
  exports** pays a 30% premium. Compliance teams have budget;
  marketing teams don't.
- Outcome rider (optional): customers can opt into a 10% bonus on
  proven uplift (vs documented baseline) — only available after
  Executive Growth OS for 90+ days. Aligns incentives without
  promising guaranteed revenue.

### IV.B The Land/Expand Sequence

```
  Free Diagnostic          (week 0, 1 hour of founder time)
       ↓ converts ~30% in pilot pool
  Growth Starter 499 Pilot (week 1-2, manual delivery)
       ↓ proof pack delivered → ~50% expand
  Executive Growth OS      (week 4+, recurring)
       ↓ data trust + workflow integration → ~80% retention/yr
  Full Control Tower       (after 6+ months, custom)
```

Conversion targets at this stage of company maturity:
- Diagnostic → Pilot: 30% (1 of 3 founders take a paid step)
- Pilot → Recurring: 50% (proof pack quality dictates this)
- Recurring → Enterprise: 20% over 12 months

### IV.C Revenue Compounding Levers

Not just "sell more pilots" but the structural levers:

1. **Agency channel** — 30% rev share on Year 1, 20% Year 2. Each
   agency = passive pipeline.
2. **Co-delivery white-label** — Higher-end agencies deliver Dealix
   under their brand for 50% of contract value. Loses Dealix brand
   equity but unlocks accounts agencies own.
3. **Sector-templated bundles** — Real estate agency, SaaS, B2B
   manufacturing each get pre-templated 7-day pilots. Reduces
   delivery time from 7 days → 3 days = higher gross margin.
4. **Annual prepay** — 2 months free in exchange for 12-month
   commitment. Cash flow win + retention lock.
5. **Outcome rider** — 10% of proven uplift after 90 days. Adds
   ~15% to ACV when it triggers; aligns incentives.

### IV.D What NOT to Monetize (Yet)

Do not build a marketplace, partner directory, certification
program, or community SaaS. Each is a separate company. Founder
time is the bottleneck; spending it on these = no first paid pilot.

## Part V — "Smart Enough to Run with Just API Keys"

The user's vision: hand Dealix API keys (LLM provider + Postgres +
Redis + Moyasar test) and let it run intelligently. Here's the gap
between today and that:

### V.A What's Already Sufficient

- ✅ LLM router (multi-provider, fails gracefully) — `core/llm/router.py`
- ✅ Postgres + Redis + LLM-only deploy primitives — `Dockerfile`, `requirements.txt`
- ✅ Founder daily brief — `/api/v1/personal-operator/daily-brief`
- ✅ Approval queue (Redis) — `dealix/governance/approvals.py`
- ✅ Cold-WhatsApp / LinkedIn-DM static blocks — `compliance_os`, `SafeAgentRuntime`
- ✅ Service catalog source of truth — `SERVICE_READINESS_MATRIX.yaml`
- ✅ Live-action defaults off — `whatsapp_allow_live_send=False`
- ✅ Health endpoint with git SHA (this branch) — `api/routers/health.py`
- ✅ Service Activation Console — `landing/status.html`
- ✅ Read-only Self-Growth API — `/api/v1/self-growth/*`

### V.B What Must Exist for Founder-Walks-Away Mode

In priority order:

1. **Proof Event ledger** (Postgres table + writer + reader API).
   Schema: `event_id, tenant_id, service_id, event_type, payload,
   evidence_url, customer_visible, created_at, approved_by`.
   Without this, no Proof Pack is generative. *~4 hours of work,
   high leverage.*

2. **Self-driving daily brief that USES API keys.** Today's
   `/daily-brief` synthesizes from in-process state. Real version
   should:
   - Query last 24h ProofEvents
   - Query inbound queue
   - Run an LLM summarization with the founder-tone system prompt
   - Surface: top 3 decisions, pending approvals, risk flags
   *~6 hours.*

3. **Watchdog cron.** Hourly job that:
   - Probes `/health` (own service)
   - Probes that no `*_ALLOW_LIVE_*` flipped to True without ticket
   - Probes that no service in YAML moved to `live` without 8 gates
   - Slacks/emails the founder if any drift
   *~4 hours.*

4. **Weekly self-improvement loop (Phase 18).** Sunday night job:
   - Reads weekly scorecard
   - Diffs vs last week
   - Drafts 3 specific improvement suggestions (page X needs CTA,
     service Y has stalled, partner Z hasn't replied)
   - Drops them in approval queue
   *~8 hours, depends on #1.*

5. **Founder command bus.** A single endpoint that accepts natural
   language ("draft a follow-up to ahmad@example.sa about the
   pilot offer") and returns a draft + queues approval. Uses
   existing LLM router. Never sends. *~6 hours.*

6. **Auto-billing reconciliation.** Moyasar webhook → match invoice
   → trigger CS handoff workflow → log ProofEvent. Manual until 3
   real proofs exist. *Build week 5+.*

7. **Multi-tenant readiness** (Phase 20 deferred). Postgres RLS +
   tenant_id on every table. Build only when 2nd customer asks
   about isolation guarantees. *Don't build before then.*

### V.C The "Just API Keys" Deployment Recipe

For the founder, this is the single page that should exist (not yet
written):

```
1. Provision: Postgres (Railway / Supabase) + Redis (Upstash) +
   LLM key (Groq is the cheapest route; Anthropic for quality work)
2. Set env vars: DATABASE_URL, REDIS_URL, GROQ_API_KEY,
   ANTHROPIC_API_KEY, MOYASAR_SECRET_KEY (test mode), DEALIX_FOUNDER_ID
3. Deploy via Railway → Dockerfile builds with GIT_SHA injected
4. Verify /health returns git_sha (this branch enables that)
5. Verify /api/v1/self-growth/service-activation returns 32 services
6. Open /status.html — should render bilingual cards
7. Open /api/v1/personal-operator/daily-brief — first daily brief
8. Done. Dealix is live in safe mode (no external sends, no charges).
```

This is an honest 30-minute deploy. *Document this as
`docs/QUICK_DEPLOY_API_KEYS_ONLY.md` — separate task, ~30 min.*

## Part VI — 90-Day Execution Plan (Real Calendar)

Each week has: target, owner, exit criterion, fallback if missed.
Built around the principle: **the only thing that matters in
weeks 1–6 is one paying customer with a Proof Pack.**

### Weeks 1–2: Deploy + first warm intros (founder + Claude)

| # | Action | Owner | Exit |
|---|---|---|---|
| 1 | Merge `claude/service-activation-console-IA2JK` → main | Founder | Branch on main |
| 2 | Railway redeploy from main | Founder | `/health` returns real `git_sha` |
| 3 | Verify `/api/v1/self-growth/*` returns 200 | Claude | All 3 endpoints 200 |
| 4 | Pick 5 warm intros (existing network only) | Founder | Names + emails recorded |
| 5 | Draft bilingual Diagnostic intake form | Claude | Form pasted into chat / Notion |
| 6 | Send 5 manual outreach (founder's own LinkedIn / WhatsApp) | Founder | 5 sent |
| 7 | Resolve 2 REVIEW_PENDING strings | Founder | `tests/test_landing_forbidden_claims.py` updated |

Fallback if week 2 ends with 0 replies: switch to ecosystem partner intros (next phase) and broaden to 10 warm targets.

### Weeks 3–4: First Diagnostic delivered + first paid Pilot

| # | Action | Owner | Exit |
|---|---|---|---|
| 8 | Run free Diagnostic on 1–2 respondents | Founder + Claude | Diagnostic doc delivered (PDF or Notion link) |
| 9 | Convert 1 to Growth Starter Pilot 499 SAR | Founder | Verbal + written commit |
| 10 | Manual Moyasar invoice via `dealix/payments/moyasar.py:39-67` | Founder | Invoice link sent |
| 11 | Payment received | Customer | Moyasar dashboard confirms |
| 12 | Build first ProofEvent ledger table (V.B #1) | Claude | DB migration shipped |
| 13 | Record paid event as first ProofEvent | Founder | Row exists in DB |

Fallback: if Diagnostic doesn't convert, run with 2 more
respondents in parallel. Diagnostic-to-pilot rate of 30% means need
3-4 to land 1.

### Weeks 5–6: Deliver Pilot + first Proof Pack

| # | Action | Owner | Exit |
|---|---|---|---|
| 14 | Deliver 10 opportunities (per `growth_starter` bundle YAML) | Founder | 10 records in customer's possession |
| 15 | Draft Arabic outreach for 5 opportunities | Claude | Drafts in approval queue |
| 16 | Customer approves drafts | Customer | Approvals captured |
| 17 | Founder sends manually (no live channel automation) | Founder | Sent records |
| 18 | Compose first Proof Pack from ProofEvents | Claude | PDF/markdown delivered |
| 19 | Customer reviews + signs proof | Customer | Sign-off recorded |

Fallback: if pilot stalls, deliver partial proof + offer 50% refund
per existing `roi.html` policy. Better to refund than to fake.

### Weeks 7–8: Expansion + first agency conversation

| # | Action | Owner | Exit |
|---|---|---|---|
| 20 | Pitch Executive Growth OS to pilot customer | Founder | Yes/no in writing |
| 21 | Identify 5 candidate Saudi B2B agencies | Founder | List recorded |
| 22 | Send 5 partner-pitch drafts | Founder | 5 sent |
| 23 | Take 1–2 agency intro calls | Founder | Calls held |
| 24 | Draft agency partnership terms (30% Y1) | Claude | Term sheet |

Fallback if pilot doesn't expand: do a *post-mortem with the
customer* (live transcript), turn it into the next pilot's playbook.

### Weeks 9–12: Compounding + Phase F begins

| # | Action | Owner | Exit |
|---|---|---|---|
| 25 | Land 2nd paid customer (different sector) | Founder | Paid |
| 26 | Build Self-Growth Phase 8 (content draft engine) | Claude | Wired into existing ApprovalGate |
| 27 | Publish Service Activation Console externally with real proofs | Founder | Updated `/status.html` showing pilot=2 |
| 28 | First agency partner signs MoU | Founder | MoU in writing |
| 29 | Start GEO content cadence (1 Arabic + 1 English page per week) | Claude + Founder | Pages live, indexed by Perplexity within 2 weeks |
| 30 | First weekly self-improvement loop runs in production | Claude | Suggestions in approval queue |

**End-of-90 targets:**
- ≥2 paying customers (1 must be on a recurring SKU)
- ≥1 agency partner with signed MoU
- ≥3 ProofEvents recorded with customer sign-off
- /status.html shows ≥1 service flipped from Partial → Live
  (lead_intake_whatsapp is the candidate after OTel + abuse test)
- AI search visibility: at least 1 Perplexity citation for "Saudi
  Revenue Execution OS" or "بديل HubSpot عربي"

## Part VII — Distribution Playbook (Multi-Channel, No Spam)

Five channels, none rely on cold outreach. Listed by leverage ratio
(highest first):

### Channel 1 — Founder warm intros (highest conversion, lowest scale)

- **Method:** Direct LinkedIn + WhatsApp (existing connections
  only). Each intro ends with "want a free 1-hour Diagnostic?"
- **Cost:** 2 hours/week of founder time
- **Conversion:** 30% → paid pilot
- **Volume cap:** ~50 founders/year
- **Fit for:** Phase 1 (months 1–4)

### Channel 2 — Inbound from Service Activation Console + GEO

- **Method:** `/status.html` and core landing pages get cited by AI
  engines. Visitors who arrive via AI are pre-qualified.
- **Why it works:** Per 2026 data, AI-referred sessions convert
  better than organic search. Dealix's structured, honest console
  is exactly what AI cites.
- **Cost:** 1 founder hour/week + Claude content drafts
- **Conversion:** 5–10% of AI-referred visitors → Diagnostic request
- **Volume:** Scales with content cadence
- **Fit for:** Phase 2 (months 4–12), compounds over time

### Channel 3 — Agency partner motion

- **Method:** 5 warm pitches to Saudi B2B agencies (marketing,
  CRM implementers, sales consultants). Offer 30% Year 1 rev share.
- **Why it works:** Agencies sell to the same SMEs Dealix targets,
  see customer signals first, and don't compete on product.
- **Cost:** 4 founder hours/week (pitch + onboarding)
- **Conversion:** 1 in 5 agencies signs; each signed agency = 2–3
  customers/quarter
- **Compounding:** Each new agency adds another ongoing channel
- **Fit for:** Phase 2 onward

### Channel 4 — Vision 2030 / SDAIA-aligned content

- **Method:** Long-form Arabic content on PDPL compliance, Saudi
  data sovereignty, Vision 2030 SME tech adoption. Each piece links
  to relevant Service Activation Console entries.
- **Why it works:** Government-adjacent buyers search for these
  topics. Content matched to SDAIA enforcement updates ranks fast.
- **Cost:** 1 piece/week, ~3 hours of Claude + founder review
- **Conversion:** Long lead time (6+ months) but builds authority
- **Fit for:** Continuous, starting month 3

### Channel 5 — Honest comparison pages

- **Method:** "HubSpot Alternative for Saudi B2B," "Gong vs Dealix,"
  "When Salesloft is the wrong tool for KSA." Each page lists honest
  tradeoffs (Dealix is NOT for 50-rep enterprise sales floors).
- **Why it works:** Comparison pages capture high-intent buyers.
  Honesty about boundaries builds trust.
- **Cost:** 2–3 hours per page
- **Conversion:** 3–5% of comparison visitors → Diagnostic
- **Fit for:** Continuous, starting month 4

### Channels NOT to Build

- ❌ Cold WhatsApp blasts (PDPL fine = up to 5M SAR)
- ❌ LinkedIn automation (terms violation; tools are dying anyway)
- ❌ Purchased lead lists (low quality + PDPL risk)
- ❌ Paid Google Ads (don't pay to acquire until 5 unit-economics
  proven via cheaper channels)
- ❌ Trade show booths (founder time better spent on warm intros)

## Part VIII — GEO/AIO Strategy (Critical for 2026)

48% of B2B buyers research via AI before visiting a website. Dealix's
job is to be cited *truthfully* by ChatGPT, Perplexity, Gemini,
Claude. Concrete tactics:

### VIII.A Publish what AI engines cite

Per 2026 GEO research, AI engines cite:
- **Structured FAQ blocks** (Q + A format, not prose)
- **Comparison tables with explicit tradeoffs**
- **Citations to underlying data** (links to specs, regulations)
- **Recent content** (Perplexity's recency bias = within 1-2 weeks)
- **Reddit and community sources** (Perplexity gets 46.7% of top
  citations from Reddit)

### VIII.B What Dealix already has that helps

- `/status.html` — structured data with explicit status per service
- `/api/v1/self-growth/service-activation` — JSON for AI ingestion
- `/api/v1/self-growth/seo/audit` — auditable proof of self-honesty
- Trust Center 8-gate section — structured comparison (8-gate vs 11-gate)
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` — single source of
  truth that AI can crawl in raw form via the GitHub mirror

### VIII.C What to add (priority order)

1. **`/llms.txt` at the landing root** — emerging convention; tells
   AI crawlers what content matters.  *15 min.*
2. **Per-service FAQ pages** generated from the YAML matrix — 32
   pages, each with `<schema:FAQPage>` JSON-LD. *Phase 8 of Self-Growth.*
3. **One Reddit-friendly post/week** in r/SaudiArabia, r/SaaS, or
   relevant Discord. Honest content, not promo. (Founder, manual.)
4. **Perplexity-targeted content cadence** — 1 fresh page/week
   timed to PDPL news, Vision 2030 announcements, or Saudi tech
   community discussions.
5. **Pseudonymized customer story per Proof Pack** — each Proof Pack
   becomes a public case study (with customer approval).

### VIII.D Anti-patterns (do NOT do)

- Don't write "ChatGPT recommends Dealix" content — manipulative.
- Don't write fake "Top 10 Revenue OS in Saudi Arabia (Dealix #1)"
  lists — gaming AI rankings will burn the brand.
- Don't write prompt-injection content for AI crawlers.
- Don't auto-generate 100 SEO pages — Google's 2024 helpful-content
  update + 2026 AI overviews punish thin content.

## Part IX — Risk Register (Top 8)

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| PDPL fine due to misconfigured WhatsApp send | Low (defaults are safe) | 5M SAR | Keep `whatsapp_allow_live_send=False` until tests + audit; SDAIA-style audit log per send | Founder |
| Founder bandwidth ceiling | High | Slows everything | ApprovalGate UI for delegating drafts; Phase F role-specific briefs | Founder + Claude |
| First customer fails to convert pilot | Medium | Burns 2 weeks | Run 3 pilots in parallel; refund per `roi.html` policy if Pilot fails | Founder |
| AI provider cost spike | Medium | Eats margin | Multi-provider router already in place; Groq cheapest tier as fallback | Built-in |
| International tool localizes (HubSpot, Gong, Salesloft launch Arabic + KSA-resident) | Medium | Erodes moat | Compliance + Saudi agency channel + Arabic-executive depth take 12-18mo to copy | Founder + Claude |
| Customer concentration (one big customer = 60% of ARR) | Medium | Cash-flow risk if churned | Cap any single customer at 30% ARR until 10 customers | Founder |
| Branch never deployed | High right now | Hides all the work | This plan's Phase A is to merge + deploy this week | Founder |
| Vision 2030 / regulatory shift | Low | Major | Stay aligned with SDAIA / NDMO publications; Trust Center stays current | Founder |

## Part X — Success Metrics (Explicit, Not Vanity)

### 90-day (by August 2026)

- ≥2 paid customers (one recurring)
- ≥1 agency partner MoU signed
- /api/v1/self-growth/* live in production with real `git_sha`
- 0 PDPL violations
- 1 service flipped Live in the YAML with passing 8 gates
- ≥3 ProofEvent rows with customer sign-off
- ≥1 case study published (anonymized OK)

### 6-month (by November 2026)

- 5+ paying customers
- 1 agency partner delivering Dealix at scale
- 30K+ SAR/month recurring revenue (10x current)
- 5+ Live services in YAML
- AI search citations across Perplexity for ≥1 of {"Saudi B2B
  revenue OS", "بديل HubSpot عربي", "WhatsApp leads compliance KSA"}
- ≥10 ProofEvent rows
- Founder works ≤30h/week on delivery (Dealix automates the rest)

### 12-month (by May 2027)

- 25+ paying customers OR 3 enterprise contracts (>50K SAR/year each)
- 3+ agency partners delivering
- 100K+ SAR/month recurring
- ≥10 Live services in YAML (33% of catalog)
- Established as the default answer for "Saudi Revenue OS" in AI
  search
- 1 written customer testimonial per quarter
- Founder spends ≥50% of time on strategy, not delivery
- Multi-tenant ready (Postgres RLS shipped)

### Anti-metrics (do NOT chase)

- ❌ Number of registered users (vanity)
- ❌ Number of WhatsApp messages sent (could be unsafe)
- ❌ Number of leads "generated" without specific source
- ❌ Number of services in YAML "Live" without 8 gates
- ❌ Sign-up funnel optimization before 5 paying customers exist

## Part XI — Hard Rules (Inviolable)

These remain in force regardless of who is acting. Same set as in
the previous closure plan — codified so they survive plan iterations.

- ❌ Do NOT flip `whatsapp_allow_live_send=True`.
- ❌ Do NOT add `MOYASAR_ALLOW_LIVE_CHARGE` or any new `*_ALLOW_LIVE_*` flag without:
  (a) tests proving safe failure modes, (b) audit log on every action, (c) founder approval recorded in writing.
- ❌ Do NOT enable Gmail live send.
- ❌ Do NOT change pricing — keep 499 SAR Pilot until 3+ proofs exist.
- ❌ Do NOT add LinkedIn automation, scraping, or cold WhatsApp paths.
- ❌ Do NOT mark any service Live without an explicit `gates:` block in the YAML matrix and tests on disk.
- ❌ Do NOT silently rephrase the 2 REVIEW_PENDING marketing strings — those are founder decisions.
- ❌ Do NOT add 23 self-growth modules at once. Phase-by-phase only.
- ❌ Do NOT publish customer stories without written consent.
- ❌ Do NOT chase "Top 10 Tools" content gaming AI rankings.

## Part XII — Founder Decisions This Plan Surfaces

Same as the prior plan, plus three new ones from this strategic
analysis:

| # | Decision | Effect |
|---|---|---|
| Existing B1 | `roi.html` "نضمن استرجاع 100%" — keep / qualify / rephrase | Unblocks forbidden-claims sweep |
| Existing B2 | `academy.html` "Cold Email Pro" course title | Same |
| Existing B3 | Pick next 1–3 pages for full OG copy | Shrinks ADVISORY_EXEMPT |
| Existing B4 | Pick search/keyword data source | Unblocks Phase 4 |
| Existing B5 | Authorize Phase D (7 safety tests) | Flips closure verdict cells from `not_runnable` to real |
| **NEW S1** | Approve Pilot retirement at customer #6 → Growth Starter at 990 SAR | Locks pricing evolution |
| **NEW S2** | Authorize agency partner outreach (5 names) at 30% rev share Y1 | Unlocks Channel 3 |
| **NEW S3** | Approve outcome-rider experiment after first Executive Growth OS recurring customer hits month 3 | Tests outcome-aligned pricing |
| **NEW S4** | Decide Compliance-tier premium (+30% for DPO-shareable PDPL exports) | Captures procurement budget |
| **NEW S5** | Pick the FIRST service to flip Live (recommendation: `lead_intake_whatsapp` after OTel + abuse-boundary test) | Validates the 8-gate process publicly |

## Part XIII — Final Synthesis (One Paragraph)

Dealix's market position in 2026 is structurally strong: the
"systems of agents" shift, PDPL enforcement, AI-driven buyer
research, and Vision 2030 SaaS spend all favor a Saudi-first,
compliance-native, approval-required, Arabic-executive product —
which is exactly what's already built on this branch. The bottleneck
is not product; it's (a) deployment, (b) one paying customer with a
real Proof Pack, (c) one agency partner. The 90-day plan in Part VI
is the smallest path to all three. The pricing ladder in Part IV.A
holds at current levels until 3 proofs exist. The "smart enough to
run with API keys" gap is closable in ~30 hours of focused work
across V.B priorities 1–6, but should be sequenced *after* the first
paying customer — earlier than that, the founder is the smartest
agent and any automation is premature. Defensibility comes not from
features but from the regulatory + linguistic + architectural moats
listed in Part III, which compound automatically as Dealix delivers
real Proof Packs to real Saudi customers.

## Sources (2026 market research grounding this plan)

- [Saudi Arabia SaaS Market Size & Outlook 2030 — TechSci](https://www.techsciresearch.com/news/8653-saudi-arabia-software-as-a-service-saas-market.html)
- [Saudi PDPL Compliance Guide 2026 — SecureLink](https://www.securelink.sa/blogs/saudi-personal-data-protection-law-compliance-guide-2026/)
- [Saudi PDPL First Anniversary, amendments and enforcement — IAPP](https://iapp.org/news/a/saudi-pdpl-s-first-anniversary-amendments-enforcement-and-ongoing-developments)
- [Revenue AI in 2026: The Definitive Market Landscape — Warmly](https://www.warmly.ai/p/blog/revenue-ai-market-landscape-2026)
- [Best AI Sales Tools 2026: Outreach vs Salesloft vs Apollo vs Gong](https://www.techno-pulse.com/2026/04/best-ai-sales-tools-in-2026-outreach-vs.html)
- [Generative Engine Optimization (GEO) — The 2026 SaaS Playbook](https://llmclicks.ai/blog/generative-engine-optimization-geo-saas/)
- [GEO Statistics 2026 — Digital Agency Network](https://digitalagencynetwork.com/generative-engine-optimization-statistics/)
- [Best B2B SaaS Partner Programs 2026 — PartnerStack](https://partnerstack.com/articles/10-star-b2b-saas-partner-programs-in-the-partnerstack-network-for-2026)
- [Best B2B Referral Software for SaaS 2026 — Cello](https://cello.so/7-best-b2b-referral-software-2026-guide/)
