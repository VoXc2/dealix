# Dealix — Investor One-Pager

> **Stage:** pre-revenue (pre-customer #1 at time of writing)
> **Round:** pre-seed planned at customer #10 (~Q2 2026)
> **Round size:** 500K-1M SAR ($133K-$267K) seed angel; 5-10M SAR ($1.3M-$2.7M) institutional pre-seed
> **Use of funds:** team expansion (CS, eng, sales) + Saudi market saturation
> **Last updated:** 2026-05-13

---

## The Bet (one sentence)

**Saudi B2B will pay 2× the price of translated US tools for AI ops that is PDPL-native, ZATCA-compliant, and approval-first by design — because regulatory sovereignty matters more than feature parity in the Saudi enterprise procurement cycle.**

## The Market

- Saudi B2B SaaS market: ~$1B and growing 30%/year (per multiple reports; verify with most recent SDAIA/MoCI data)
- Pain: Saudi B2B companies cannot deploy US AI tools without PDPL DPA + Saudi data residency that don't exist
- Existing Saudi competitors: 1-2 partial Arabic CRM tools; no full-stack AI ops with our compliance depth
- TAM expansion: GCC ($5B) and MENA ($15B) markets accessible from Saudi base

## The Product

**Three engines (already built):**
1. **Lead Engine** — 5 data adapters (Google Maps/CSE/Hunter/Firecrawl/Wappalyzer) + Saudi sources (Chambers, SDAIA, MCI, ZATCA)
2. **Service Engine** — 7 AI services productized (S1-S7) with endpoint surface + landing page
3. **Trust Engine** — PDPL Articles 5/13/14/18/21/32 wired + ZATCA Phase 2 e-invoice + 24-hour breach notification SLA

**Seven revenue streams (all scaffolded):**
- R1 Managed Pilot (499 SAR), R2 SaaS (999-7,999 SAR/mo), R3 LaaS (25/150 SAR metered), R4 Sector Reports (1.5K-10K), R5 Bespoke AI (5K-25K), R6 White-Label (1K + 25% rev share), R7 Enterprise PMO (25K-100K/mo)

**Engineering state:**
- 120+ FastAPI routers, 300+ tests, 8 Alembic migrations
- Tenant theming end-to-end, ICP scoring, PDPL DSAR endpoints
- Live compliance status endpoint (computed from actual code state, not hardcoded badges)

## The Founder

**Sami Asiri** — solo founder, Saudi-native, technical (built the entire repo). Risk: solo until customer #10 hire trigger.

## The Plan (3 horizons)

| Horizon | Window | Goal | ARR |
|---------|--------|------|-----|
| H1 | Year 1 | 30 customers + first R7 enterprise | 1.5M SAR |
| H2 | Years 2-3 | 200 customers + UAE office | 18M SAR |
| H3 | Years 4-7 | 500+ customers GCC-wide + IPO-ready | 100M+ SAR |

## The Moat

1. **Saudi Sovereign Trust** — PDPL+ZATCA+SDAIA. 18-24 month gap for US competitors to close.
2. **Data Network Effects** — Each customer's anonymized signals improve the master Saudi B2B graph.
3. **Agency Channel Lock-in** — R6 White-Label customer agencies bring 200+ end-customers to Dealix. Switch costs are 6-12 months.

## The Ask

**Pre-seed (when triggered at customer #10):**
- **Amount:** 5-10M SAR ($1.3M-$2.7M)
- **Pre-money valuation:** 25-40M SAR
- **Use of funds:**
  - 60% — team (CS lead, 2 engineers, 1 senior sales)
  - 20% — Saudi market saturation (paid pilots, conferences, content)
  - 10% — compliance (DPO appointment, SDAIA registration, ISO 27001 audit prep)
  - 10% — runway buffer (18 months minimum)
- **What we don't take:** convertible notes, SAFE without cap, board control, founder-friendly clauses we don't fully understand

## Why This Round, Why Now

We close pre-seed when we have **10 paying customers** because:
1. Pre-customer #1 fundraises favor optionality over execution discipline
2. Customer #1-9 fundraises invite valuation games at the worst leverage
3. At customer #10 we have product-market evidence + retention data + ARR trajectory

## What We've Built (verifiable)

- **Repo:** `github.com/VoXc2/dealix` (admin access granted to serious diligence parties)
- **Live compliance posture:** `GET /api/v1/compliance/status` (returns real-time state, not screenshots)
- **Landing:** `dealix.me` with 60+ pages including:
  - `/services.html` — 7 productized AI services
  - `/bespoke-ai.html` — R5 intake form wired to API
  - `/vision.html` — 2026-2032 strategic plan
  - `/dpo.html` — PDPL Art. 32 disclosure

## Risks Diligence Should Ask About

1. **Solo founder risk** — mitigation: hiring path documented, angel funding bridges to CTO hire
2. **TAM concentration in Saudi** — mitigation: GCC expansion path Y3+, sovereignty moat travels
3. **PDPL framework changes** — mitigation: Dealix participates in SDAIA consultations; compliance team year 3
4. **Customer #1 still unachieved** — mitigation: founder commitment to 30-day kill switch documented in repo

## Why a Saudi Investor (vs international)

- Saudi LPs / family offices understand the sovereignty thesis without education
- Saudi network amplifies distribution faster than valuation premium
- Tadawul Nomu IPO path is real and well-trodden for Saudi B2B at our target ARR
- Vision 2030 alignment helps with SDAIA/Misk co-marketing later

## Comparison References (for valuation context)

- **Salla** — Saudi B2B e-commerce platform, $400M valuation 2023
- **Foodics** — Saudi B2B restaurant SaaS, $1B valuation 2024
- **Lean Technologies** — Saudi fintech API, $33M Series B 2024
- **HockeyStack** (US comparable) — $1.7M ARR → $10M Series A 2023

Dealix targets early Foodics-trajectory: 18M ARR by Year 3, 1B+ SAR valuation by Year 7.

## What This Document Is NOT

- Not a deck (this is the substance; deck visualizes it)
- Not legal advice (Saudi legal counsel reviews every term sheet)
- Not a forecast (these are commitments tied to kill-switches in repo)

## Next Step for Interested Investors

1. **Read the repo** — `github.com/VoXc2/dealix` (request access via dpo@dealix.me)
2. **Read v3-v7** of the strategic playbook at `/root/.claude/plans/go-lovely-gem.md`
3. **Schedule 60-min diligence call** — Sami discusses customer #1-#N current state
4. **Term sheet** sent only after first customer is paying AND mutual fit confirmed

We do not pitch into rooms. We work, then talk.
