# Market Production — Gap Matrix

Tracks every target artifact of the Market + Commercial layer and its status.
Legend: ✅ done · 🟡 partial · ⬜ planned · 🔒 protected (pre-existing, reused).

## Foundation (Phase 1)
| Artifact | Status |
|----------|--------|
| docs/gtm/MARKET_PRODUCTION_OS_AR.md | ✅ |
| docs/gtm/MARKET_PRODUCTION_SYSTEM_BOUNDARIES.md | ✅ |
| docs/gtm/MARKET_PRODUCTION_FILE_MAP.md | ✅ |
| docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md | ✅ |
| docs/gtm/FOUNDER_GTM_COMMAND_CENTER_AR.md | ✅ |
| docs/gtm/GTM_OPERATING_RHYTHM_AR.md | ✅ |
| docs/gtm/GTM_METRICS_AR.md | ✅ |
| reports/gtm/MARKET_PRODUCTION_GAP_MATRIX.md | ✅ |
| reports/gtm/DAILY_GTM_REPORT.md | ✅ |
| reports/gtm/WEEKLY_GTM_REVIEW.md | ✅ |

## Brand OS (Phase 2) — docs/brand/*
8 docs (identity, messaging house, visual, voice, claims policy, outbound system,
content rules, asset checklist) → ✅ on completion.

## Product Catalog & Offer (Phase 3)
9 docs (catalog, ladder, packaging, scope, deliverables, pricing guardrails,
discount, payment terms, quote approval) + schemas (product_offer, pricing_rule) +
data (product_catalog.yaml, pricing_rules.yaml) + 2 reports.

## ICP / Personas / Pain (Phase 4)
7 docs + schemas (icp, buyer_persona, pain_signal, offer_match) + data
(icp_segments, buyer_personas, pain_to_offer) + 2 reports.

## Sector Intelligence (Phase 5)
10 sector playbooks + data/sectors/sectors.yaml + 1 report.

## Signals & Prospect (Phase 6)
5 docs + prospect research OS + schemas (company_signal, job_signal, prospect) +
data (company_signals, job_signals, prospects, suppression) + 2 reports.

## Draft Factory (Phase 7)
6 docs + schema (outreach_draft) + data/outreach/drafts.jsonl + 3 reports.

## Deliverability / Compliance / Privacy (Phase 8)
9 outreach docs + 5 privacy docs + schemas (email_account, sending_batch,
suppression) + data + 6 reports.

## Content / Press / Partnership (Phase 9)
6 content + 7 press + 6 partnership docs + schemas (partner_opportunity,
content_asset) + data + 7 reports.

## Commercial Pipeline (Phase 10)
18 docs + schemas (opportunity, discovery_note, commercial_proposal,
commercial_proof_pack) + data (opportunities, discovery_notes, objections) + 4 reports.

## Tests (Phase 11)
10 pytest files + evals (2 docs + 2 data) + shared loader.

## Verification (Phase 12)
reports/gtm/CLAUDE_MARKET_COMMERCIAL_FINAL_REPORT.md + run logs.

> Live status of each file is reflected by its presence in the tree. This matrix is
> the checklist; the file map (`docs/gtm/MARKET_PRODUCTION_FILE_MAP.md`) is the index.
