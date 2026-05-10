# Frontend Tier-1 Audit — Baseline (Pre-Redesign)

**Date**: 2026-05-10
**Branch**: `claude/redesign-homepage-revenue-xrFlU`
**Plan**: `/root/.claude/plans/vivid-baking-quokka.md`

This document captures the baseline state of the Dealix landing site **before** the Tier-1 Revenue Command Center redesign so we can measure improvement post-execution.

---

## 1. Site inventory (46 HTML pages)

Pure static HTML+CSS+JS (no framework). All pages: `lang="ar" dir="rtl"`. Two top-level CSS files:
- `landing/styles.css` — base tokens (colors, typography, layout)
- `landing/assets/css/design-system.css` — 1,028 lines, `ds-` prefixed components, additive only

**7 Tier-1 conversion pages targeted by this redesign**:
| File | Lines | Role |
|---|---|---|
| `landing/index.html` | 812 | Homepage |
| `landing/customer-portal.html` | 603 | Operations console (8-section API contract) |
| `landing/diagnostic.html` | 529 | Free intake form (6 fields) |
| `landing/ai-team.html` | 378 | Engine deep-dive (kept as deep page) |
| `landing/proof.html` | 280 | Proof Pack page |
| `landing/trust-center.html` | 220 | Compliance & gates |
| `landing/pricing.html` | 211 | Pricing page (5 tiers today) |
| `landing/partners.html` | 206 | Partners (becomes Agency Partner) |

**39 secondary pages** stay as-is: launchpad, command-center, executive-command-center, autopilot, copilot, decisions, workflow, market-radar, simulator, verticals, pulse, academy, community, case-study, compare, founder, founder-leads, investor, marketers, pay-per-result, pilot-day-0, pilot-tracker, roi, start, status, styleguide, dealix-beast-power, dashboard, dealix-live-demo, diagnostic-real-estate, executive-command-center, launch-readiness, personal-operator, privacy, subprocessors, terms, trust, verticals, free-tools/lead-score-calculator.

---

## 2. Homepage (landing/index.html) — current state

**Title**: `Dealix — أوّل AI Operating Team لشركتك`

**Hero H1** (line 6 / line 156-160):
> «نظام تشغيل AI كامل لشركتك — قبل ما توظّف فريق»

**Hero subheadline** (~line 162):
> «Dealix يبني لشركتك أوّل AI Operating Team: Sales · Growth · Support · Ops · Executive. كلّ مدير ينفّذ قراره بضغطة واحدة عبر WhatsApp أو الجوّال — والنظام يجهّز، يصنّف، يصعّد، ويوثّق كلّ شيء بالأدلّة. صفر تواصل بارد · صفر سحب بيانات · صفر إرسال حيّ بدون موافقتك.»

**Hero primary CTA** (line ~164): `/launchpad.html` — «شوف الباقة المغلقة (Sprint + Partner) →»
**Hero secondary CTA**: `/diagnostic.html` — «أو ابدأ بالتشخيص المجّاني (٢ دقيقة)»

**Top navigation** (lines 90-150): **37 anchors and links** — wildly oversized for a Tier-1 conversion page.

```
#pillars · #for-who · #sectors · #how · #trust · /pricing · /roi · /case-study ·
/customer-portal · /command-center · /ai-team · /launchpad · /diagnostic ·
/diagnostic-real-estate · /start · /decisions · /free-tools/lead-score-calculator ·
/compare · /proof · /workflow · /investor · /dealix-beast-power · /styleguide ·
/autopilot · /market-radar · /copilot · /simulator · /verticals · /pulse ·
/academy · /community · /pay-per-result · /trust-center · /trust · /founder ·
/partners · /marketers · /status
```

**Section IDs in DOM** (must preserve as anchors): `#pillars`, `#for-who`, `#sectors`, `#how`, `#trust`, `#proof`, `#pricing`, `#faq`, `#pilot`, `#prospector*`, `#sector-*`, `#main`, `#top`, `#cta-form-title`, `#consentBanner`, `#year`, plus form field IDs and `#CLM-001..015`.

**Sections in scroll order**:
1. Announcement bar — pilot disclosure
2. Hero (H1 + sub + dual CTA + trust strip + anti-claim row)
3. Chat demo (Khaliji Saudi example) — gets pulled out of homepage in redesign
4. Prospector tool — gets pulled out
5. `#pillars` — 3 pillars
6. `#for-who` — 3 ICP
7. `#sectors` — tabs (SaaS / Banking / Enterprise / Distribution / Government)
8. `#how` — 7-step pipeline
9. `#trust` — PDPL + audit trail
10. `#pricing` — Starter / Growth / Scale / Enterprise
11. `#proof` — service matrix (32 services)
12. Partners placeholder strip
13. `#faq` — 10 questions
14. `#pilot` — demo form

---

## 3. Customer portal (landing/customer-portal.html) — 8-section contract

| # | Section | Source | Status |
|---|---|---|---|
| 1 | Operations اليوم (KPI grid) | DEMO data hard-coded | ✅ DEMO label visible |
| 2 | Journey timeline (12-state) | DEMO | ✅ |
| 3 | Radar اليومي (6 signal cards) | DEMO | ✅ |
| 4 | Daily Decisions queue (3 cards) | DEMO | ✅ |
| 5 | Digest weekly + monthly | DEMO | ✅ |
| 6 | Important decisions this week | DEMO | ✅ |
| 7 | Workflow map (10 cells) | static | ✅ |
| 8 | CTA section | static | ✅ |

**Constitutional**: `tests/test_customer_portal_live_full_ops.py` enforces `len(body["sections"]) == 8`.

**Today's Decision card**: NOT yet at top of page — currently buried inside section 4. Redesign adds new `#today-decision` hero strip ABOVE the ops grid.

**State pill**: ✅ Present at top (`<span class="state-pill state-pill--demo">DEMO MODE</span>`).

**Degraded banner**: ✅ Hidden by default (`#cp-degraded-banner`).

---

## 4. Pricing (landing/pricing.html) — current 5-tier ladder

| Tier | Price | Notes |
|---|---|---|
| Pilot | 1 ر.س / 7 days | Anchor (almost free) |
| Starter | 999 ر.س/mo | — |
| Growth | 2,999 ر.س/mo | — |
| Scale | 7,999 ر.س/mo | — |
| Enterprise | تواصل | — |

**Disclaimer block** (lines 71-78): contains "ضمانات Dealix" wording — needs renaming to "التزامات Dealix" (negation-safe).

**Sprint 499 SAR**: NOT visible on this page; lives only on `/launchpad.html`.

**Mini Diagnostic (Free)**: NOT a tier on this page; it's on `/diagnostic.html`.

**Partner / Executive Command Center 12,000 SAR**: NOT a tier on this page.

Redesign: 6-tier ladder with anchor-pricing pattern (Partner top, Mini Diagnostic bottom-left "ابدأ هنا").

---

## 5. Proof page (landing/proof.html)

**Title**: `Proof — كل ادعاء بدليل · Dealix`
**H1**: line ~88
**KPI strip**: 3 cells (CLM count, evidence_id count, hash chain status)
**Has L1-L5 ladder?**: ❌ NO. Currently flat. Redesign adds 5-step horizontal ladder.

---

## 6. Trust Center (landing/trust-center.html)

**Title**: `Compliance & Trust Center — Dealix`
**Frames as**: compliance bullets, NOT sales features.
**8 hard gates listed?**: Mentioned in copy but not as headline cards. Redesign reframes as 8 feature cards.

**⚠️ Allowlist note**: `trust-center.html` is **NOT** in the NEGATION allowlist for tokens `cold|scraping|blast`. Redesign avoids those tokens or adds allowlist entries.

---

## 7. Diagnostic (landing/diagnostic.html)

**6 fields**: company name, sector tier, team size, channels, main pain, budget range. ✅ Already minimal.

**Primary CTA**: form submit. ✅ Single primary.

**Trust strip near form**: ❌ Not yet. Redesign adds inline.

**Sector tiers listed**: T1 (agencies, B2B services, consulting), T2 (SaaS, e-commerce, real estate), T3 (healthcare, education, logistics).

---

## 8. Partners → Agency Partner

`landing/partners.html` (206 lines) — 3-tier program: Referral 10% / Certified 15% / Strategic 20%.

Redesign: new `landing/agency-partner.html` with refreshed positioning, `partners.html` becomes thin meta-refresh redirect.

---

## 9. Design System (landing/assets/css/design-system.css)

**1,028 lines, ds- prefixed, additive only.**

**Tokens (lines 19-116)**:
- Spacing: `--space-0..12` (0px → 128px, 8px grid)
- Typography: `--fs-2xs..5xl` (11px → clamp 42-62px)
- Motion: `--dur-instant..deliberate` (80ms → 480ms), 3 easing curves
- Z-index: `--z-base..toast` (1 → 2000)
- Container widths: `--container-narrow/base/wide/full` (720/980/1200/1400px)
- Surfaces: `--ds-surface-1/2/3` + borders + status colors + 5 action mode colors
- Focus ring: `--ds-focus-ring` (WCAG AA)
- Reduced-motion: gated globally (lines 119-138)

**Components ready for reuse (no need to invent)**:
ds-banner, ds-status, ds-mode, ds-pulse, ds-card (+ clickable variant), ds-grid (+ narrow/wide), ds-kpi, ds-feature (+ icon-side), ds-stat, ds-quote, ds-faq, ds-tabs, ds-breadcrumb, ds-footer, ds-eyebrow, ds-headline (+ hero), ds-lede, ds-btn (+ ghost/subtle/danger/sm/lg/block/icon), ds-link (+ quiet), ds-input, ds-skeleton (+ text/block/circle), ds-spinner (+ sm/lg), ds-glass, ds-toast, ds-skip-link, ds-focus-ring, ds-gate, ds-chip (+ accent/warn), ds-section, ds-list-clean, ds-divider, ds-container (+ full/base/narrow), ds-stack (+ xs/sm/md/lg/xl), ds-row, ds-hover-lift, ds-reveal, ds-code, ds-endpoint.

**To be added by this redesign** (Phase 10):
- `.ds-wadl` family (WhatsApp Decision Layer)
- `.ds-evidence-level` (L1-L5 step indicator)
- `.ds-pricing-row` (anchored tier with badge)
- `.ds-trust-strip` (horizontal trust chips bar)
- `.ds-problem-card` (variant of ds-feature, red-tinted)
- `.ds-mega-menu` (dropdown nav)
- `.ds-portal-deep` (collapsible <details> wrapper for ops grid)

---

## 10. Test gates baseline (PASS)

```
tests/test_landing_forbidden_claims.py ........... 3 passed
tests/test_no_guaranteed_claims.py ................. 1 passed
tests/test_frontend_professional_polish.py ....... 24 passed
tests/test_landing_no_railway_refs_v13.py .......... 1 passed
tests/test_customer_portal_empty_states_final.py ... passed
```

**Baseline verdict**: 28 frontend-scan tests PASS. Redesign must keep them PASS + add new Tier-1 assertions.

(The `test_customer_portal_live_full_ops.py` and `test_customer_portal_backward_compatibility.py` failures observed during baseline run are integration tests that require the FastAPI app to be running; they are not HTML-scan tests and are out of scope for this Tier-1 frontend redesign.)

---

## 11. Service-readiness baseline (locked, do not touch)

`landing/assets/data/service-readiness.json`:
```
counts: { live: 8, pilot: 0, partial: 0, target: 24, blocked: 0, backlog: 0, total: 32 }
```

This file is auto-regenerated by pre-commit hook from `docs/registry/SERVICE_READINESS_MATRIX.yaml`. Touching the YAML triggers JSON regen and CI block-on-diff.

The new homepage trust strip (`#proof-strip`) reads these counts via `script.js` fetch — never hard-coded, fallback static if no-JS.

---

## 12. Forbidden tokens baseline

From `tests/test_landing_forbidden_claims.py`:
- Arabic: `نضمن`, `مضمون`
- English: `guaranteed`, `blast`, `scrape`, `scraping`, `cold whatsapp/outreach/email/messaging`
- NEGATION context only allowed when file is in the explicit allowlist.

**Allowlisted files** (NEGATION usage permitted): founder, academy, roi, trust, privacy, subprocessors, styleguide, ai-team, start, diagnostic, founder-leads, pilot-day-0, compare, diagnostic-real-estate, status.

**NOT in allowlist** — must avoid forbidden tokens entirely (or add allowlist entry):
- `landing/index.html` (homepage) — must use Arabic phrasing where possible
- `landing/trust-center.html` — must describe gates in Arabic
- `landing/pricing.html` — disclaimer wording uses "التزامات" not "ضمانات"
- `landing/proof.html` — describe evidence levels without forbidden English tokens
- `landing/customer-portal.html` — already clean
- `landing/agency-partner.html` (new file) — write clean from start

---

## 13. Conversion funnel (post-redesign target)

```
Homepage hero → Mini Diagnostic CTA (Free)
            │
            ↓
   /diagnostic.html → 6-field form → 24h plan delivery
            │
            ↓
       Sprint 499 ر.س (7 days) → Proof Pack L3+
            │
            ↓
       Growth OS 2,999 ر.س/mo (recurring) → Customer Portal access
            │
            ↓
       Scale OS 7,999 / Partner ECC 12,000 / Enterprise (custom)
```

Each step has a single primary CTA. Each card has trust cues nearby. Pricing transparent at every hop.

---

## 14. Next steps

Proceed in this order (Phase 10 first as it's foundational):
1. **Phase 10** — Design system additions (`.ds-wadl`, `.ds-evidence-level`, `.ds-pricing-row`, `.ds-trust-strip`, `.ds-problem-card`, `.ds-mega-menu`, `.ds-portal-deep`).
2. **Phase 1** — Nav simplification (touches all 7 conversion pages).
3. **Phase 9** — Agency Partner page + redirect + sitemap.
4. **Phase 8** — Diagnostic polish (light).
5. **Phase 7** — Trust Center reframe (8 gates as features).
6. **Phase 5** — Proof L1-L5 ladder.
7. **Phase 6** — Pricing 6-tier anchor.
8. **Phase 4** — Customer Portal Today's Decision hero.
9. **Phases 2 + 3** — Homepage restructure + WADL section (heaviest, last).
10. **Phase 11** — Tier-1 pytest assertions.
11. **Phase 12** — `scripts/frontend_tier1_verify.sh`.
12. **Phase 13** — Evidence table.
13. **Phase 14** — Final run + commit + push.
