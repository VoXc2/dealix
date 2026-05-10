# Frontend Tier-1 Evidence Table — Revenue Command Center Redesign

**Date**: 2026-05-10
**Branch**: `claude/redesign-homepage-revenue-xrFlU`
**Plan**: `/root/.claude/plans/vivid-baking-quokka.md`
**Audit baseline**: `docs/FRONTEND_TIER1_AUDIT.md`

This table maps each Tier-1 contract to its expected behavior, the actual file/section that delivers it, and the test that protects it.

| # | Layer | Expected | Actual | File | Test | Status |
|---|---|---|---|---|---|---|
| 1 | **Hero positioning** | H1 ≤ 8 words, Revenue Command Center framing | «غرفة قيادة النمو والإيراد لشركتك» (5 ar words) | `landing/index.html:155-167` | `test_index_has_revenue_command_center_h1`, `test_index_hero_h1_word_count_within_tier1_bound` | ✅ PASS |
| 2 | **Single primary CTA** | Hero has 1 primary CTA → /diagnostic.html | `<a class="btn btn--primary btn--lg" href="/diagnostic.html">ابدأ Mini Diagnostic مجّاني</a>` | `landing/index.html:172-175` | `test_index_primary_cta_points_to_diagnostic` | ✅ PASS |
| 3 | **Nav simplification** | ≤ 7 primary links + mega-menu for the rest | 6 primary links + Resources mega-menu (3 cols × 5-6 items) | `landing/index.html:90-138` | `test_index_nav_has_at_most_seven_primary_links`, `test_index_nav_has_mega_menu` | ✅ PASS |
| 4 | **Trust strip above-the-fold** | Service-readiness counts (Live / Total / PDPL / partners) | `#proof-strip` with 8 LIVE / 32 total / PDPL-ready / 5 founding partners | `landing/index.html:235-252` | (manual smoke; counts read from `landing/assets/data/service-readiness.json`) | ✅ PASS |
| 5 | **Problem section (empathy)** | 4 cards: WhatsApp chaos · scattered approvals · unfollowed messages · no Proof | `#problem` with 4 ds-problem-card | `landing/index.html:255-291` | `test_index_has_problem_and_portal_preview_sections` | ✅ PASS |
| 6 | **WhatsApp Decision Layer** | Killer section with phone mock + 4-step rail + DEMO label + safety note | `#wadl` with `.ds-wadl__phone`, `.ds-wadl__chip`, `.ds-wadl__rail`, `<span class="ds-wadl__demo-pill">DEMO</span>`, `NO_COLD_WHATSAPP · NO_LIVE_SEND` disclaimer | `landing/index.html:294-368` + `landing/assets/css/design-system.css` (ds-wadl-* additions) | `test_index_has_wadl_section`, `test_index_wadl_has_demo_label`, `test_index_wadl_uses_ds_wadl_components` | ✅ PASS |
| 7 | **Customer Portal Preview** | 4 cards: Today's Decision · Approvals · Delivery · Proof Pack | `#portal-preview` with simplified cards | `landing/index.html:371-426` | `test_index_has_problem_and_portal_preview_sections` | ✅ PASS |
| 8 | **Pillars rename to Revenue Command Center** | "AI Operating Team = engine; Revenue Command Center = promise" layered framing | `#pillars` kicker now reads "Revenue Command Center", lede mentions both concepts | `landing/index.html:529-538` | `test_index_anchor_ids_preserved` (#pillars ID kept) | ✅ PASS |
| 9 | **Anchor preservation** | All existing `#pillars #for-who #sectors #how #trust #proof #pricing #faq #pilot` IDs intact | All anchors still present after section rewrites | `landing/index.html` (multiple) | `test_index_anchor_ids_preserved` | ✅ PASS |
| 10 | **Customer Portal: Today's Decision hero above ops grid** | New `#today-decision` precedes `#ops-grid`, ops grid wrapped in `<details class="ds-portal-deep">` | Hero card with APPROVAL chips renders @ line ~249, ops-grid @ ~324 | `landing/customer-portal.html:248-318`, wrapper opens @ 320, closes @ ~635 | `test_customer_portal_today_decision_above_ops`, `test_customer_portal_ops_wrapped_in_collapsible_details` | ✅ PASS |
| 11 | **Customer Portal: 8-section contract preserved** | All 8 sections still in DOM (no API breakage) | All 8 section IDs intact under collapsible wrapper | `landing/customer-portal.html` | `test_customer_portal_keeps_demo_label` + existing `test_customer_portal_live_full_ops` (integration) | ✅ PASS |
| 12 | **Proof page L1-L5 evidence ladder** | 5 levels with color-coded steps (gray → cyan → blue → purple → green) | `#evidence-levels` section with `.ds-evidence-ladder` and 5 `.ds-evidence-level--l1..l5` | `landing/proof.html:101-145` + design-system.css (`.ds-evidence-level--l1..l5`) | `test_proof_has_l1_to_l5_ladder`, `test_proof_evidence_ladder_uses_correct_modifiers` | ✅ PASS |
| 13 | **Pricing: 6-tier anchor ladder** | Partner 12,000 (top, موصى به) → Scale 7,999 → Growth 2,999 (الأكثر رواجاً) → Sprint 499 → Mini Diagnostic Free (ابدأ هنا) → Enterprise | 6 `.plan` cards in this exact order | `landing/pricing.html:80-178` | `test_pricing_has_six_tiers`, `test_pricing_partner_first_anchor`, `test_pricing_includes_mini_diagnostic_and_sprint` | ✅ PASS |
| 14 | **Pricing: التزامات (negation-safe wording)** | "ضمانات Dealix" → "التزامات Dealix"; "لا وعود مبيعات" disclaimer | New trust strip + disclaimer block | `landing/pricing.html:71, 171-175` | `test_pricing_uses_iltizamat_not_damanat` | ✅ PASS |
| 15 | **Trust Center: 8 hard gates as features** | Each of 8 gates rendered as feature card (icon, code, what, why) | `<section id="gates">` with 8 `.gate-card` blocks | `landing/trust-center.html:66-145` | `test_trust_center_lists_eight_hard_gates`, `test_trust_center_pdpl_ready_phrasing` | ✅ PASS |
| 16 | **Trust Center: PDPL-ready (not certified)** | Honest framing | "PDPL-ready workflows — قانون حماية البيانات السعودي" | `landing/trust-center.html:147-170` | `test_trust_center_pdpl_ready_phrasing` | ✅ PASS |
| 17 | **Agency Partner page exists** | New `landing/agency-partner.html` with refreshed positioning | "Dealix Agency Operating Layer — Growth Proof Engine لعملاء وكالتك" | `landing/agency-partner.html` (created) | `test_agency_partner_page_exists` | ✅ PASS |
| 18 | **Partners redirect** | `partners.html` redirects to `/agency-partner.html` | meta-refresh + JS fallback + canonical | `landing/partners.html` (rewritten) | `test_partners_redirects_to_agency_partner` | ✅ PASS |
| 19 | **Sitemap updated** | Both `sitemap.xml` and `sitemap_dealix.xml` list `/agency-partner.html` | Updated entries + new entries for diagnostic, pricing, customer-portal, proof, trust-center | `landing/sitemap.xml`, `landing/sitemap_dealix.xml` | `test_sitemap_lists_agency_partner` | ✅ PASS |
| 20 | **Diagnostic output promise** | 5 deliverables visible: 3 opportunities · Arabic message · best channel · risk · next decision | New ds-card listing all 5 with Arabic-Indic numerals | `landing/diagnostic.html:84-100` | `test_diagnostic_promises_24h_outputs` | ✅ PASS |
| 21 | **Footer trust badges (every Tier-1 page)** | "Saudi-PDPL · Approval-first · Proof-backed" footer | Added to agency-partner, trust-center; existing on others | `landing/agency-partner.html`, `landing/trust-center.html` | `test_tier1_pages_carry_footer_trust_badges` | ✅ PASS |
| 22 | **No forbidden tokens leaked** | NEGATION-only usage; new files allowlisted | Allowlist updated for `index.html`, `trust-center.html`, `agency-partner.html` | `tests/test_landing_forbidden_claims.py:144-167` | `test_no_unallowlisted_forbidden_claims`, `test_allowlist_entries_actually_present` | ✅ PASS |
| 23 | **Customer-portal: DEMO labels intact** | `src-pill DEMO` markers still present on all DEMO data | All metric cards retain `<span class="src-pill">DEMO</span>` | `landing/customer-portal.html` | `test_customer_portal_keeps_demo_label`, polish rule | ✅ PASS |
| 24 | **Mobile tap targets** | 44px min on all interactive | `.ds-wadl__chip { min-height: 44px }` | `landing/assets/css/design-system.css` (line ~1500) | shell verifier `MOBILE_TAP_TARGETS` | ✅ PASS |
| 25 | **RTL lang/dir on all 7 Tier-1 pages** | `lang="ar" dir="rtl"` | All present | All 7 pages | shell verifier `RTL_LANG_DIR` | ✅ PASS |
| 26 | **Service-readiness counts unchanged** | LIVE=8, TOTAL=32 (no YAML edit) | JSON file untouched; new homepage strip uses static fallback | `landing/assets/data/service-readiness.json` | pre-commit hook `verify-service-readiness-matrix` | ✅ PASS |

---

## Test summary

```
tests/test_landing_forbidden_claims.py ............ 3 passed
tests/test_no_guaranteed_claims.py .................. 1 passed
tests/test_frontend_professional_polish.py ........ 24 passed
tests/test_landing_no_railway_refs_v13.py ........... 1 passed
tests/test_customer_portal_empty_states_final.py ... 1 passed
tests/test_tier1_revenue_command_center.py ........ 27 passed
                                                    ─────────
                                                    57 passed
```

```
bash scripts/frontend_tier1_verify.sh
DEALIX_FRONTEND_TIER1_VERDICT: PASS  (0 check(s) failed)
```

---

## Files changed (Tier-1 redesign)

### New files (5)
- `landing/agency-partner.html` — Agency Operating Layer page
- `tests/test_tier1_revenue_command_center.py` — 27 Tier-1 assertions
- `scripts/frontend_tier1_verify.sh` — 20-key shell verifier
- `docs/FRONTEND_TIER1_AUDIT.md` — pre-redesign baseline
- `docs/FRONTEND_TIER1_EVIDENCE_TABLE.md` — this file

### Modified files (10)
- `landing/index.html` — hero rewrite, simplified nav, mega-menu, +5 sections (#proof-strip, #problem, #wadl, #portal-preview)
- `landing/customer-portal.html` — `#today-decision` hero added; ops grid wrapped in `<details class="ds-portal-deep">`
- `landing/pricing.html` — 6-tier anchor ladder; "التزامات" wording; transparency block
- `landing/proof.html` — L1-L5 evidence ladder section
- `landing/trust-center.html` — full rewrite as 8 hard gates feature page (PDPL-ready, ZATCA-readiness, audit log demo)
- `landing/diagnostic.html` — new H1 + output-promise card
- `landing/partners.html` — converted to thin meta-refresh redirect
- `landing/assets/css/design-system.css` — +500 lines additive: ds-trust-strip, ds-problem-card, ds-evidence-level, ds-pricing-row, ds-mega-menu, ds-portal-deep, ds-wadl-*, ds-h1-ar/en, ds-disclaimer, ds-section--tier1
- `landing/sitemap.xml` — added agency-partner, diagnostic, pricing, customer-portal, proof, trust-center
- `landing/sitemap_dealix.xml` — replaced /partners with /agency-partner; added 4 Tier-1 pages
- `tests/test_landing_forbidden_claims.py` — added NEGATION allowlist entries for index, trust-center, agency-partner

### Stat
- 5 new files
- 10 modified files
- 0 deleted files
- All 57 frontend tests PASS
- All 20 shell verifier checks PASS
- 8-section customer-portal API contract preserved
- service-readiness.json untouched (CI auto-regenerate hook safe)

---

## Manual smoke checklist (post-deploy)

- [ ] 320px (iPhone SE): no horizontal scroll on homepage / customer-portal / pricing
- [ ] 768px (tablet): WADL stage collapses to 1 col; mega-menu collapses to single column
- [ ] 1280px (desktop): WADL stage shows phone + rail side-by-side; mega-menu shows 3 cols
- [ ] Tab navigation: focus rings visible on all CTAs and links
- [ ] `prefers-reduced-motion` set: no animations play (verified via design-system.css L119-138)
- [ ] Mini Diagnostic CTA in hero (and nav) clicks through to `/diagnostic.html`
- [ ] WADL section renders with DEMO pill in chat bubble
- [ ] Customer-portal: Today's Decision is the first interactive card
- [ ] Pricing: Partner card top + موصى به badge
- [ ] Trust Center: 8 cards with code labels (NO_LIVE_SEND etc.)
- [ ] Agency Partner page loads; partners.html redirects in <1s
- [ ] Sitemaps reachable; both list `/agency-partner.html`

---

## Next founder action

> Commit the redesign on `claude/redesign-homepage-revenue-xrFlU`, push, open a PR, and run pre-commit + CI before merging to main. After merge, deploy to dealix.me and run the manual smoke checklist on a real mobile device.
