# Dealix Release Notes — Wave 16 → 19+ Operational Closure
## ملاحظات الإصدارات — من الموجة ١٦ إلى الإغلاق التشغيلي ١٩+

> **Audience / الجمهور:** anchor partners · investors · CISOs · advisors. Internal too.
> **Range / النطاق:** PR #235, 8 commits, ~50 days of Claude-driven build.
> **Status / الحالة:** build-complete + waiting on 2 founder market actions.
> **Verifier / المُحقّق:** `python scripts/verify_all_dealix.py` reports 10 systems / 8 perfect / 2 honestly waiting.

This document is the single bilingual evidence pack you hand to anyone asking "what does Dealix actually do?". Every claim references a file, an endpoint, or a passing test. No marketing fluff.

هذه الوثيقة هي حزمة الأدلّة الثنائيّة اللغة التي تسلّمها لأي شخص يسأل "ماذا يفعل Dealix فعلًا؟". كل ادّعاء يُشير إلى ملف أو نقطة نهاية أو اختبار ناجح. لا تسويق فارغ.

---

## 0. The 8-commit chain · سلسلة الالتزامات الثمانية

| # | SHA | Theme | Files |
|---|---|---|---|
| 1 | `046d36b` | Wave 16 polish | warnings filter (passlib silenced), `/api/v1/founder/post-deploy-check`, daily-brief markdown emitter, WhatsApp drafter, 10 bilingual templates |
| 2 | `fbf1acc` | 2026-Q2 commercial reframe | 7-offer ladder → 3-offer ladder, 4,999 SAR/mo paid floor, Saudi B2B services sole beachhead |
| 3 | `208c804` | Wave 17 part-1 | `/api/v1/dealix-promise` public manifesto endpoint, `scripts/daily_routine.py`, anchor partner pipeline seed, 8 new tests |
| 4 | `3f381b2` | Wave 17 part-2 | 4 bilingual docs (Promise / Anchor Partner / 90-day Cadence / Continuous Routine) + `landing/promise.html` |
| 5 | `5e36628` | Wave 19 part-1 | GCC standardization pack + Capital Asset Library (15 strategic assets) + Open Doctrine framework + Funding pack + `/api/v1/doctrine` + `/api/v1/capital-assets/public` + `/api/v1/gcc-markets` |
| 6 | `62605af` | Wave 19 part-2 | GCC go-to-market sequence + USE_OF_FUNDS + HIRING_PLAN + open-doctrine ADOPTION_GUIDE |
| 7 | `0f3f253` | Wave 19 Recovery — CEO Completion Sprint | 4 honest CEO marker JSON files (counts=0 until founder acts) + master verifier `scripts/verify_all_dealix.py` + funding/open-doctrine remainder + 12 Recovery tests |
| 8 | (this commit) | Wave 19+ Operational Closure | `landing/verify.html` + `landing/dealix-os.html` + `scripts/post_merge_smoke.py` + Day-1 kit + smoke runbook + master verifier 10th system "Operational Closure" + README refresh + 3 closure tests |

Net diff across 8 commits: ~12,000 insertions / ~800 deletions / ~135 files changed. 195+ tests pass.

---

## 1. What this build delivers · ما يقدّمه هذا البناء

### 1.1 Doctrine made the brand · العقيدة أصبحت العلامة

Dealix's 11 non-negotiables are now a public, verifiable, machine-readable surface:

- **Public manifesto API:** `GET /api/v1/dealix-promise` — JSON of all 11 commitments, each tied to the `tests/test_no_*.py` file that enforces it.
- **Bilingual markdown render:** `GET /api/v1/dealix-promise/markdown`.
- **Public landing page:** `landing/promise.html`.
- **Canonical text:** `docs/THE_DEALIX_PROMISE.md` (~1,440 words bilingual) + `docs/00_constitution/NON_NEGOTIABLES.md`.

Any CISO, DPO, SAMA reviewer, or procurement officer can verify the perimeter in seconds:

```bash
curl https://api.dealix.me/api/v1/dealix-promise | jq '.commitments | length'
# → 11
```

### 1.2 The doctrine extended to an open framework · الإطار المفتوح

The same 11 commitments are now also published as an open framework other AI ops shops can adopt:

- **Open framework API:** `GET /api/v1/doctrine` — separate from the Dealix-customer commitment.
- **Controls JSON:** `GET /api/v1/doctrine/controls`.
- **Bilingual markdown:** `GET /api/v1/doctrine/markdown`.
- **Repository:** `open-doctrine/` (9 files — README, GOVERNED_AI_OPS_DOCTRINE, 11_NON_NEGOTIABLES, CONTROL_MAPPING, IMPLEMENTATION_CHECKLIST, ADOPTION_GUIDE, CONTRIBUTING, LICENSE, SECURITY).
- **Positioning page:** `landing/dealix-os.html`.
- **License posture:** CC BY 4.0 for doctrine text · MIT for code examples · Dealix trademark reserved.
- **Strategic doc:** `docs/THE_DEALIX_OS_LICENSE.md`.

Dealix is the commercial reference implementation. Tiers 1-3 (awareness / alignment / compliance) are free in perpetuity; only Tier 4 (Dealix-certified review) is commercial.

### 1.3 The 3-offer ladder + Saudi beachhead · السلّم التجاري + القاعدة السعودية

The 2026-Q2 commercial reframe collapsed a 7-rung ladder to 3 rungs:

| Offer | Price | Cadence | Duration | Target |
|---|---|---|---|---|
| Strategic Diagnostic | 0 SAR | one-time | 1 working day | Saudi B2B services founder/COO |
| Governed Ops Retainer | **4,999 SAR / month** | per-month | 3-month minimum | B2B services 50–500 employees with PDPL/NDMO exposure |
| Revenue Intelligence Sprint | **25,000 SAR** | one-time | 30 days fixed | Companies needing 3-source merge + audit-ready governance |

- **Source of truth:** `auto_client_acquisition/service_catalog/registry.py`.
- **Public commercial map:** `GET /api/v1/commercial-map` + `/markdown`.
- **Pricing page:** `landing/pricing.html`.
- **Strategic rationale:** `docs/sales-kit/PRICING_REFRAME_2026Q2.md`.
- **Investor one-pager:** `docs/sales-kit/INVESTOR_ONE_PAGER.md`.

Banking, energy, healthcare, government, SaaS are handled exclusively as Custom AI engagements (≥ 50,000 SAR) negotiated founder-direct, NOT via the public ladder. For the next 90 days, the public ladder serves Saudi B2B services only.

### 1.4 The GCC standard positioning · التموضع كمعيار خليجي

Saudi remains the active beachhead. UAE / Qatar / Kuwait are documented as future markets with full regulatory mapping:

- **Public market intel:** `GET /api/v1/gcc-markets` — 4 markets × regulator × framework × articles × processor × invoicing × language × Dealix status (`active` | `pilot_ready` | `future_market`).
- **Bilingual markdown:** `GET /api/v1/gcc-markets/markdown`.
- **Strategy pack:** `docs/gcc-expansion/` — 8 files (THESIS, GOVERNED_AI_OPS_STANDARD, COUNTRY_PRIORITY_MAP, REGULATED_BUYER_MAP, PARTNER_ARCHETYPES, LOCALIZATION_MATRIX, RISK_AND_COMPLIANCE_NOTES, GO_TO_MARKET_SEQUENCE).
- **Constants module:** `auto_client_acquisition/governance_os/gcc_markets.py`.

`active_count == 1` is enforced by `tests/test_gcc_markets.py::test_saudi_is_the_only_active_market_today` — a second market cannot be promoted without an actual signed customer.

### 1.5 The Capital Asset Library · مكتبة الأصول الرأسماليّة

15 strategic Capital Assets are now indexed:

- **Registry:** `auto_client_acquisition/capital_os/capital_asset_registry.py` (CAP-001 → CAP-015).
- **Schema:** `auto_client_acquisition/capital_os/capital_asset.py`.
- **Public API:** `GET /api/v1/capital-assets/public` (7 public-safe assets — file paths and commercial use omitted from the public view).
- **Admin API:** `GET /api/v1/capital-assets` (full 15-asset registry).
- **Generated index:** `capital-assets/CAPITAL_ASSET_INDEX.json` (from `scripts/generate_capital_asset_index.py`).
- **Library docs:** `capital-assets/` — 9 markdown files (LIBRARY, SCHEMA, TRUST/SALES/PRODUCT/DOCTRINE/PARTNER/INVESTOR/HIRING ASSETS).
- **Validator:** `scripts/validate_capital_assets.py` (schema integrity + file-path existence + non-negotiable id validity + public-asset commercial-sensitive-token canary).

Asset types: trust_asset, sales_asset, product_asset, doctrine_asset, proof_asset, partner_asset, investor_asset, hiring_asset, standard_asset, market_asset, revenue_ops_asset.

### 1.6 The founder operating routine · روتين تشغيل المؤسس

- **One-command morning ritual:** `python scripts/daily_routine.py` → consolidated bilingual brief at `data/daily_routine/YYYY-MM-DD.md`. 5 sections + 3 next actions. Idempotent.
- **Sunday strategic review:** `python scripts/weekly_ceo_review.py` → `data/weekly_ceo_review/YYYY-WW.md`. 6 sections + 3 decisions.
- **Day-1 kit:** `docs/ops/FOUNDER_DAY1_KIT.md` — the only doc to read after PR merge.
- **Post-merge smoke:** `python scripts/post_merge_smoke.py https://api.dealix.me` — 18 endpoint checks in ≤ 2 min.
- **Founder Command Center:** `landing/founder-command-center.html` — single-pane-of-glass with 12 status cards + top-3 next actions.
- **Public verify page:** `landing/verify.html` — share with any reviewer; live-fetches 4 public surfaces.
- **Continuous routine ops:** `docs/ops/CONTINUOUS_ROUTINE.md` — cron / Railway / mobile wiring.
- **90-day cadence:** `docs/ops/FOUNDER_90_DAY_CADENCE.md`.

### 1.7 The funding + hiring tracks · مسارا التمويل والتوظيف

- **Funding pack:** `docs/funding/` — 10 files (FUNDING_MEMO, INVESTOR_NARRATIVE, WHY_NOW_GCC_AI_OPS, DEALIX_MOAT_STACK, PRE_SEED_PITCH, SAFE_NOTE_TEMPLATE, CAPITAL_ASSET_TRACTION, USE_OF_FUNDS, HIRING_PLAN, INVESTOR_QA, FIRST_3_HIRES, HIRING_SCORECARDS).
- **Investor one-pager:** `docs/sales-kit/INVESTOR_ONE_PAGER.md`.
- **Three hires gated on revenue:** ≥ 50K SAR ARR → Hire #1 AI Ops Engineer; ≥ 100K SAR ARR → Hire #2 Delivery/RevOps Operator; ≥ 250K SAR ARR → Hire #3 Partnerships/GCC Growth Operator.
- **Anti-pattern:** no hiring before Invoice #2.

### 1.8 The partner channel · قناة الشركاء

- **Anchor partner outreach kit:** `docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md` — 3 archetypes (Big 4 advisory / SAMA-licensed processor / Saudi VC) with bilingual outreach drafts + 60-min meeting agendas + rev-share terms (20% / 12 months / 200K SAR cap).
- **Seeded pipeline:** `data/anchor_partner_pipeline.json` (committed despite gitignore — see `.gitignore` allowlist).
- **Outreach log:** `data/partner_outreach_log.json` (`outreach_sent_count: 0` until the founder actually sends).
- **Partner Covenant:** `docs/40_partners/PARTNER_COVENANT.md` (unchanged from prior waves).

---

## 2. CEO completion verifier · مُحقّق اكتمال الشركة

The honest measure of where the company stands, distinct from build state:

```bash
python scripts/verify_all_dealix.py
```

Reports 10 systems on a 1-5 scale. Build-complete systems (1-8) score 5/5 once shipped. Market-motion systems (9-10) cap at 3/5 until the founder takes irreversible action.

Current state at the end of Wave 19+ Closure:

| # | System | Score |
|---|---|---|
| 1 | Doctrine (Dealix Promise + 11 Non-Negotiables) | 5/5 |
| 2 | Offer Ladder (3 offers + INVESTOR_ONE_PAGER + reframe doc) | 5/5 |
| 3 | GCC Standardization Pack | 5/5 |
| 4 | Capital Asset Library | 5/5 |
| 5 | Open Governed AI Ops Doctrine | 5/5 |
| 6 | Funding + Hiring Pack | 5/5 |
| 7 | Founder Command Center | 5/5 |
| 8 | Operational Closure (Day-1 Kit) | 5/5 |
| 9 | **Partner Motion** | **3/5** ← gated on 1 founder outreach |
| 10 | **First Invoice Motion** | **3/5** ← gated on Invoice #1 |

`ceo_complete = false` — by design. The marker files at `data/partner_outreach_log.json` and `data/first_invoice_log.json` refuse to claim outreach or invoices that have not actually happened. This is the moat.

---

## 3. What flips when the founder acts · ما الذي يتغيّر مع فعل المؤسس

### Action A — Send 1 anchor partner outreach (Partner Motion → 5/5)

1. Open `docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md` → pick one archetype + one named company.
2. Send the bilingual draft from a personal account. No automation. No cold blast (non-negotiable #2 + #3).
3. Append entry to `data/partner_outreach_log.json`. Increment `outreach_sent_count` to 1.

### Action B — Issue Invoice #1 (First Invoice Motion → 5/5)

1. Qualified buyer accepts the proposal.
2. Follow `docs/ops/FIRST_INVOICE_UNLOCK.md` — 8-action cascade, Capital Asset registration is action #1.
3. Run `scripts/moyasar_live_cutover.py` then `scripts/zatca_preflight.py`.
4. Issue invoice via Moyasar (founder approval logged per non-negotiable #8).
5. Append entry to `data/first_invoice_log.json`.

When both flip → `ceo_complete: true`.

---

## 4. Test inventory · جرد الاختبارات

195+ tests passing across:

- **Doctrine guards (19 tests):** `tests/test_no_*.py` — every non-negotiable enforced.
- **Article 13 compliance:** `tests/test_article_13_compliance.py` — Wave 4 architecture not in production code.
- **Wave 17 endpoints:** `tests/test_dealix_promise.py` (5) + `tests/test_daily_routine.py` (3).
- **Wave 18 endpoints:** `tests/test_founder_command_center.py` (6) + `tests/test_weekly_ceo_review.py` (4) + `tests/test_post_deploy_check.py` (6).
- **Wave 19 endpoints:** `tests/test_doctrine_endpoint.py` (7) + `tests/test_capital_assets_endpoint.py` (8) + `tests/test_gcc_markets.py` (7).
- **Wave 19 doc-pack integrity:** `tests/test_wave19_doc_pack_integrity.py` (10).
- **Wave 19 Recovery Sprint:** `tests/test_wave19_recovery_sprint.py` (12).
- **Wave 19+ Closure:** `tests/test_post_merge_smoke.py` + `tests/test_landing_verify_page.py` + `tests/test_landing_dealix_os_page.py`.
- **Reframe + landing wiring:** `tests/test_service_catalog.py` (8) + `tests/test_commercial_map.py` (10) + `tests/test_checkout_pages.py` + `tests/test_tier1_revenue_command_center.py` + `tests/test_customer_safe_product_language.py`.

---

## 5. Public endpoint inventory · جرد نقاط النهاية العامّة

8 public + 4 admin-gated surfaces that constitute Dealix's public interface:

**Public (no admin key):**
- `GET /healthz`
- `GET /api/v1/dealix-promise` + `/markdown`
- `GET /api/v1/doctrine` + `/controls` + `/markdown`
- `GET /api/v1/commercial-map` + `/markdown`
- `GET /api/v1/gcc-markets` + `/markdown`
- `GET /api/v1/capital-assets/public` + `/markdown`
- `GET /api/v1/founder/launch-status/public`
- `GET /api/v1/founder/command-center/public`

**Admin-gated (X-Admin-API-Key required):**
- `GET /api/v1/founder/command-center`
- `GET /api/v1/founder/post-deploy-check`
- `GET /api/v1/founder/launch-status`
- `GET /api/v1/capital-assets`

---

## 6. Doctrine guards reaffirmed · إعادة تأكيد الحماية

The 11 non-negotiables remain enforced. Every customer-facing markdown ends with the bilingual disclaimer. The marker files at `data/*.json` refuse to claim market state that has not happened. No live charge, no live send, no autonomous outreach, no fake claims, no project closure without Proof Pack + Capital Asset. The full canonical text is at `docs/00_constitution/NON_NEGOTIABLES.md` and the public manifestation is at `docs/THE_DEALIX_PROMISE.md`.

---

## 7. What's deliberately NOT in this release · ما هو خارج النطاق عمدًا

- No Wave 20. The user explicitly locked: do not start Wave 20 before (a) one partner meeting OR (b) one invoice conversation OR (c) one strong market objection.
- No live Moyasar charges (founder-flipped only — `scripts/moyasar_live_cutover.py` ready).
- No ZATCA Phase 2 automation (Day-30+ via `scripts/zatca_preflight.py`).
- No Postgres migration of JSONL ledgers (Q2 keeps JSONL).
- No hiring (gated on revenue per `docs/funding/FIRST_3_HIRES.md`).
- No public GitHub OSS repo for `open-doctrine/` until after the first partner conversation.
- No new sectors (banking, energy, healthcare, government, SaaS) — Saudi B2B services beachhead for 90 days.
- No marketplace, white-label, paid ads.

---

## 8. Verification block · كتلة التحقّق

```bash
# 1. Pre-merge readiness (build state only)
bash scripts/pr235_merge_readiness.sh

# 2. Master verifier (build + market motion)
python scripts/verify_all_dealix.py

# 3. Post-merge smoke (after Railway deploys main)
python scripts/post_merge_smoke.py https://api.dealix.me

# 4. Public verify page (share with any reviewer)
open https://dealix.me/verify.html

# 5. Verify the doctrine externally
curl https://api.dealix.me/api/v1/dealix-promise | jq '.commitments | length'
curl https://api.dealix.me/api/v1/doctrine | jq '.non_negotiables_count'
curl https://api.dealix.me/api/v1/commercial-map | jq '.registry_count'
curl https://api.dealix.me/api/v1/gcc-markets | jq '.active_count'
```

---

## 9. Single-sentence summary · ملخّص في جملة واحدة

**Dealix shipped 8 commits across Waves 16-19+: it polished the production runtime, collapsed a 7-offer ladder to a focused 3-offer ladder anchored on a 4,999 SAR/month paid floor, made the 11 non-negotiables a public verifiable surface, opened the same 11 as a free framework (CC BY 4.0 doctrine + MIT code) so other GCC shops adopt Dealix as the de-facto governed-AI-ops standard, registered 15 strategic Capital Assets as a visible compounding inventory, prepared evidence-first funding + revenue-gated hiring tracks, shipped a single-pane-of-glass Founder Command Center + daily/weekly cadence orchestrators, mapped Saudi/UAE/Qatar/Kuwait regulatory posture without overclaiming, and finished with an operational closure layer that compresses the founder's Day-1 friction to ≤ 30 minutes — leaving exactly two remaining motions both gated on founder market action, with marker files that refuse to lie until both have actually happened.**

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
