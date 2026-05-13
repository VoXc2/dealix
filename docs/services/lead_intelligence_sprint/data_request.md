# Lead Intelligence Sprint — Data Request / طلب البيانات

Send this packet to the customer on Day 0 (before kickoff). All CSV/Excel inputs must be encrypted at rest and transferred through the sealed-credentials vault.

## Required columns (must be present) / الأعمدة المطلوبة

| Column / العمود | Type | Notes |
|---|---|---|
| `company_name_ar` | string | Arabic legal/trading name. Required. |
| `vertical` | enum | bfsi / retail_ecomm / healthcare / logistics / education / gov_b2g |
| `region` | enum | Saudi region code (RUH / JED / DMM / MAK / MED / etc.) |
| `source` | string | Provenance label per row (e.g., `cr_lookup_2026Q1`, `event_riyadh_expo`, `partner_referral_x`). **No row without a source.** |
| `updated_at` | ISO 8601 | Last refresh date. Drives freshness scoring. |

## Recommended columns / مفضّل

`company_name_en`, `commercial_registration` (10 digits), `vat_number` (15 digits, starts with 3), `headcount`, `annual_revenue_sar`, `domain`, `triggers` (csv tags), `industry_sub_segment`.

## Optional columns / اختياري

`email`, `phone` (Saudi mobile preferred), `linkedin_url`, `notes_ar`, `last_interaction_at`, `existing_relationship` (yes/no/unknown).

## Provenance rules / قواعد المصدر

1. Every row must declare a `source`. Rows without a verifiable source are quarantined (not scored).
2. The customer must provide a written **lawful basis statement** (PDPL Art. 5) per source class — contract / legitimate interest / public records.
3. Sources that violate Saudi PDPL (scraped LinkedIn data, leaked databases, paid lists without DPA) are auto-rejected at intake.
4. PDPL Art. 13/14 notice text must accompany every contact mention before outreach drafts are generated.

## Volume & cadence / الحجم والإيقاع

- Up to **5,000 rows** included in base price.
- Overage tier: SAR 0.80 per row beyond 5,000 (capped at 20,000).
- One refresh batch allowed during the 10-day sprint (no rolling updates).

## Drop-off format / تسليم البيانات

- UTF-8 CSV or `.xlsx` workbook, one sheet per vertical.
- File name: `<customer>_<vertical>_<YYYYMMDD>.csv`.
- Upload through the sealed vault; do NOT email.

## Cross-links

- Intake questions: `docs/services/lead_intelligence_sprint/intake.md`
- PII rules: `dealix/trust/pii_detector.py`
- Saudi entity normalizer: `auto_client_acquisition/customer_data_plane/`
- PDPL readiness: `docs/PRIVACY_PDPL_READINESS.md`
- Persona-value matrix: `docs/sales/persona_value_matrix.md`
