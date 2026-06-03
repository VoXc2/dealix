# Dealix Business Packaging — Current State (Wave 4)

**Date:** 2026-05-07
**Audience:** founder + sales
**Note:** this is a **documentation-only** map of what's sellable today. NO pricing-page rewrite (existing tests confirm safe defaults).

---

## Six packaging tiers

| # | Package | Price (SAR) | Tier |
|---|---|---|---|
| 1 | Free AI Ops Diagnostic | 0 | Free |
| 2 | 7-Day Revenue Proof Sprint | 499 | Entry |
| 3 | Data-to-Revenue Pack | 1,500 | Sprint |
| 4 | Managed Revenue Ops | 2,999 – 4,999/mo | Subscription |
| 5 | Executive Command Center | 7,500 – 15,000/mo | Premium |
| 6 | Agency Partner OS | custom / rev-share | Partner |

---

## 1. Free AI Ops Diagnostic — 0 SAR

### Target customer
Saudi B2B owner curious about AI ops; not yet committed.

### Problem solved
"Where do I even start with AI for my company?" — gives them a 1-page sector-fit analysis in 24-48h.

### Existing modules powering it
- `auto_client_acquisition/diagnostic_workflow/` — 6-question intake
- `landing/diagnostic.html` + `landing/diagnostic-real-estate.html`
- `api/routers/customer_company_portal.py` (Slot-A view)
- `auto_client_acquisition/leadops_spine` (Wave 3) — captures the lead

### Deliverables
- 1-page diagnostic PDF with sector-specific KSA benchmarks
- Customer Portal access (DEMO state)

### Customer-visible portal sections
- `1_start_diagnostic` (default 8-section)
- `enriched_view.full_ops_score` (system status visible)

### Executive dashboard sections
- N/A (no active customer yet)

### Proof metrics
- Diagnostic intake completed (event: `diagnostic_created`)

### Manual actions
- Founder writes the 1-page report personally
- 30-min call with prospect

### Blocked actions
- No outreach without consent
- No automated follow-up

### Upsell path
- Diagnostic → 499 SAR Sprint (within 14 days)

### Readiness status
✅ LIVE

### What must NOT be claimed
- "We guarantee a result" (Article 8)
- "We will scrape your competitors" (NO_SCRAPING)

---

## 2. 7-Day Revenue Proof Sprint — 499 SAR

### Target customer
Saudi B2B owner who completed the diagnostic and wants a quick proof point.

### Problem solved
"Can Dealix actually move my pipeline?" — runs a 7-day controlled test with Proof Pack output.

### Existing modules
- `auto_client_acquisition/leadops_spine` — qualifies inbound leads
- `auto_client_acquisition/service_sessions` — runs the 7-day workflow
- `auto_client_acquisition/proof_ledger` — captures proof events
- `auto_client_acquisition/payment_ops` — invoice + manual confirmation (NO_LIVE_CHARGE)

### Deliverables
1. Lead Quality Audit
2. Pipeline Audit
3. Daily Decisions Briefs (7)
4. Initial Proof Pack
5. 30-day plan

### Portal sections
- All 8 + enriched_view.ops_summary + sequences + service_status

### Exec dashboard sections
- Today's 3 Decisions
- Sales Pipeline
- Proof Ledger

### Proof metrics
- proof_events_count ≥ 5
- payment_confirmed = true (manual evidence)

### Manual actions
- Founder confirms payment manually
- Founder approves every external draft

### Blocked actions
- No live WhatsApp send to customer's leads
- No automated outreach

### Upsell path
- Sprint → Data-to-Revenue Pack (1,500 SAR) OR Managed Revenue Ops

### Readiness status
✅ LIVE (all modules in Wave 3)

---

## 3. Data-to-Revenue Pack — 1,500 SAR

### Target customer
B2B owner who saw Sprint result and wants deeper data work.

### Problem solved
Lead enrichment + ICP mapping + sector benchmarks against their actual data.

### Existing modules
- `auto_client_acquisition/customer_brain` — builds per-customer snapshot
- `auto_client_acquisition/market_intelligence/` — sector_pulse + opportunity_feed
- `auto_client_acquisition/full_ops_contracts/` — canonical envelopes

### Deliverables
- ICP score + fit map for top 50 prospects
- Sector benchmark report (anonymized)
- Channel preference guide
- Compliance flags + risk register

### Portal sections
- enriched_view.full_ops_score + weaknesses_summary

### Exec dashboard sections
- Growth Radar
- Risk & Compliance
- Full-Ops Score

### Proof metrics
- Customer Brain snapshot built
- ≥ 3 opportunities in growth_radar

### Manual actions
- Founder reviews benchmark data before delivery

### Readiness status
✅ LIVE

---

## 4. Managed Revenue Ops — 2,999 – 4,999 SAR/month

### Target customer
SMB with 5-50 employees, growing pipeline.

### Problem solved
"We need a fractional growth/sales/CSM team" — Dealix runs the operating layer.

### Existing modules
- All Wave 3 + Wave 4 layers
- `auto_client_acquisition/approval_center` (per-channel policies)
- `auto_client_acquisition/whatsapp_decision_bot` (internal admin)
- `auto_client_acquisition/full_ops_radar` (Full-Ops Score weekly)

### Deliverables
- Daily Decisions queue (`/decisions.html`)
- Weekly executive pack
- Monthly KPI report
- Manual outreach drafts (founder-approved)
- Proof Pack with ≥ 50 events/month

### Portal sections
All 8 + every enriched_view key (Wave 3 + Wave 4)

### Exec dashboard sections
All 15 sections of `/executive-command-center.html`

### Proof metrics
- KPI commitment: +20% lift baseline
- ≥ 100 proof events/month
- Full-Ops Score ≥ 75 maintained

### Manual actions
- Founder/CSM approves all external sends
- Founder reviews weekly pack
- Manual payment confirmation via Moyasar dashboard

### Blocked actions
- LinkedIn automation (NO_LINKEDIN_AUTO)
- Cold WhatsApp (NO_COLD_WHATSAPP)
- Any blast (NO_BLAST)

### Upsell path
- Managed → Executive Command Center after 3 months proof

### Readiness status
✅ LIVE (Wave 4 unlocks the full Exec Command Center for premium pricing)

### What must NOT be claimed
- Guaranteed revenue (Article 8)
- Replacing the team (Dealix REPLACES first 3 hires only — not the whole team)

---

## 5. Executive Command Center — 7,500 – 15,000 SAR/month

### Target customer
Founder/CEO who needs daily visibility but has no time for dashboards.

### Problem solved
"I need ONE screen that tells me what to do today and where I'm bleeding."

### Existing modules
- `auto_client_acquisition/executive_command_center/` (Wave 4 — 15 sections)
- `auto_client_acquisition/full_ops_radar/` (score + weakness radar)
- `auto_client_acquisition/unified_operating_graph/` (cross-layer view)
- `auto_client_acquisition/whatsapp_decision_bot/` (admin commands)
- `landing/executive-command-center.html` + JS (4-state UX)

### Deliverables
- Live Executive Command Center (read-model, daily refresh)
- Saudi-Arabic WhatsApp decision bot (admin-only, never customer outbound)
- Weekly executive call (60 min)
- Monthly business review with founder

### Portal sections
All Wave 3 + Wave 4 keys + executive_command_link

### Exec dashboard sections
All 15 sections live with real data

### Proof metrics
- Full-Ops Score ≥ 90 ("Full Ops Ready")
- All 15 ECC sections populated
- Weekly Pipeline Audit shipped on time
- Customer NPS recorded monthly

### Manual actions
- Weekly 60-min executive call with founder
- WhatsApp Decision Bot escalations approved within 24h

### Blocked actions
- (Same as Tier 4)

### Readiness status
✅ LIVE (Wave 4 enables this tier — `/api/v1/executive-command-center/*` + frontend)

### What must NOT be claimed
- "AI replaces the CEO" (it doesn't — it briefs the CEO)
- "Predictive revenue forecasts guaranteed" (NO_FAKE_FORECAST)

---

## 6. Agency Partner OS — custom / rev-share

### Target customer
Saudi/MENA marketing agency with 5+ B2B clients.

### Problem solved
"How do I scale my agency without hiring 10 more analysts?"

### Existing modules
- `api/routers/partnership_os` (existing, optional)
- All other Wave 3 + Wave 4 layers
- Multi-tenant separation (currently single-tenant — multi-tenant RLS deferred until customer #2)

### Deliverables
- Custom (per-agency)
- Rev-share starting after first proof customer

### Readiness status
🟡 DEFERRED — multi-tenant RLS not yet built (Article 11). Activate when first agency partnership signs.

### What must NOT be claimed
- "Manage 100 customers from day 1" (multi-tenant not built yet)

---

## Cross-package rules

- Every tier respects the 8 hard gates
- Every external action is approval-required
- Every package includes a Customer Portal view + Executive Command Center preview
- Every package surfaces Full-Ops Score
- Every package operates in Arabic primary, English secondary
- Pricing on `/pricing.html` is **NOT changed** by Wave 4 — Phase 14 is doc-only
