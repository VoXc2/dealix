# Lead Intelligence Sprint — Executive Report Skeleton / هيكل التقرير التنفيذي

Bilingual PDF + PPT, <= 18 slides. Compiled on Day 9. Delivered to Head of Sales + CEO.

## 1. Headline / العنوان
- AR + EN single-line outcome (e.g., "From 4,832 messy rows to 50 ranked Saudi accounts worth SAR 6.4M in addressable pipeline.").
- Project codename, vertical, sprint window.

## 2. Executive Summary (1 slide) / الملخص التنفيذي
- 3 bullets: scope delivered, headline KPI delta, recommended next 30 days.
- One number the CEO can repeat in the next board meeting.

## 3. Data Health / صحة البيانات
KPI rows (before vs after):
| KPI | Before | After | Delta | Method |
|---|---|---|---|---|
| Rows received | n | — | — | intake |
| Valid rows | n | n | +n | `data_quality_score.score_batch` |
| Source coverage % | % | % | % | provenance audit |
| Duplicate groups | n | n | -n | dedupe report |
| PII findings auto-redacted | n | 0 | -n | `dealix/trust/pii_detector.py` |

Visual: stacked bar (valid / quarantined / duplicates), provenance pie.

## 4. Scoring & Banding / التصنيف
| Band | Count | Median score | Notes |
|---|---|---|---|
| A | n | n | priority outreach this week |
| B | n | n | nurture 30-day cadence |
| C | n | n | qualify before any send |
| D | n | n | hold / re-verify source |

Visual: A/B/C/D heatmap by vertical and region.

## 5. Top 50 Accounts / أفضل 50 حساباً
- Table excerpt (top 10), full list in appendix CSV.
- Columns: company_name_ar, vertical, region, score, owner, next action.

## 6. Top 10 Next-Best-Actions / أفضل 10 إجراءات
- Bilingual outreach drafts with PDPL Art. 13/14 footer.
- Each draft tagged with: target persona, evidence level, approver role.

## 7. Pipeline Forecast / توقعات الأنابيب
- Addressable pipeline (SAR) at 100% qualification.
- Expected pipeline at observed conversion (sector benchmark).

## 8. Risks & Compliance Notes / المخاطر والامتثال
- Quarantined-row reasons.
- PDPL Art. 13/14 wording included in every draft (sample shown).
- Forbidden-claims auto-check result.

## 9. 30-Day Activation Plan / خطة 30 يوماً
- Week-by-week tasks, owners, expected outputs.
- Upsell path preview (see `upsell.md`).

## Recommended Visuals
- Heatmap (A/B/C/D x vertical).
- Funnel (rows -> valid -> scored -> top-50 -> top-10).
- Provenance pie chart.
- Pipeline waterfall (SAR).

## Cross-links
- Proof pack: `docs/services/lead_intelligence_sprint/proof_pack_template.md`
- Handoff agenda: `docs/services/lead_intelligence_sprint/handoff.md`
- Renewal pathways: `docs/services/lead_intelligence_sprint/upsell.md`
- ROI math: `docs/sales/roi_model_saudi.md`
- Delivery standard: `docs/strategy/dealix_delivery_standard_and_quality_system.md`
- Reporting module: `auto_client_acquisition/executive_reporting/`
