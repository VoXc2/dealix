# سجل القيمة القابضة لوثائق Dealix (Holding Value Registry)

**الغرض:** تصنيف أهم الوثائق كأصول قابضة. **EvidenceLevel** يتبع [ASSET_EVIDENCE_LEVELS_AR.md](ASSET_EVIDENCE_LEVELS_AR.md). **LastUsed / UsageCount** يُحدَّثان من [`../../data/docs_asset_usage_log.json`](../../data/docs_asset_usage_log.json) و[MONTHLY_ASSET_COUNCIL_AR.md](MONTHLY_ASSET_COUNCIL_AR.md).

**قاعدة:** **High score + low evidence = activation priority** — انظر [_generated/asset_activation_priorities.json](_generated/asset_activation_priorities.json).

**قاعدة القيمة:** لا رفع درجات Revenue/Partner/Investor من غير استخدام مسجّل ([ASSET_USAGE_GOVERNANCE_AR.md](ASSET_USAGE_GOVERNANCE_AR.md)).

| الأصل | النوع | Revenue | Trust | Delivery | Partner | Investor | Holding | الحالة | Owner | ReviewCadence | Audience | PublicationBoundary | LastUsed | EvidenceLevel | UsageCount | NextAction |
|--------|--------|:-------:|:-----:|:--------:|:-------:|:--------:|:-------:|--------|-------|---------------|----------|---------------------|----------|---------------|:----------:|------------|
| HOLDING_DOCS_HUB_AR.md | Strategy / Navigation | 3 | 4 | 5 | 4 | 5 | 5 | CANONICAL | Founder | Monthly | Founder / Eng | Internal-only | TBD | L2 | 0 | Internal council + hub review |
| DEALIX_EXECUTION_WAVES_AR.md | Execution | 4 | 4 | 5 | 4 | 5 | 5 | CANONICAL | Founder | Monthly | Founder / Investor | Investor-safe | TBD | L2 | 0 | Use in investor motion |
| DOCS_CANONICAL_REGISTRY_AR.md | Governance | 2 | 5 | 5 | 4 | 5 | 5 | CANONICAL | Founder | Monthly | Founder / Ops | Partner-safe | TBD | L2 | 0 | Reference in partner tech call |
| HOLDING_OFFER_MATRIX_AR.md | Commercial / Holding | 5 | 3 | 4 | 5 | 5 | 5 | CANONICAL | Founder | Monthly | Sales / Partner | Partner-safe | 2026-05-14 | L4 | 1 | Follow up in 48h; book meeting → raise to L5 |
| PROOF_DEMO_PACK_5_CLIENTS_AR.md | Revenue / Prove | 5 | 3 | 5 | 4 | 4 | 4 | ACTIVE | Founder / Delivery | Monthly | Sales / Client | Client-facing | 2026-05-14 | L4 | 1 | Use in meeting if booked; client path next |
| RETAINER_PILOT_MINI_AR.md | MRR / Deliver | 5 | 3 | 5 | 3 | 4 | 4 | ACTIVE | Founder | Monthly | Client / Ops | Client-facing | TBD | L2 | 0 | Attach after proof demo |
| BU4_TRUST_ACTIVATION_GATE_AR.md | Trust / Enterprise | 3 | 5 | 4 | 5 | 4 | 5 | ACTIVE | Founder / Trust | Quarterly | Enterprise / Partner | Partner-safe | 2026-05-14 | L4 | 1 | Position as trust gate in partner thread; meeting → L5 |
| IP_LICENSE_OUTLINE_AR.md | Partner / License | 4 | 4 | 3 | 5 | 5 | 5 | ACTIVE | Founder | Quarterly | Partner / Legal | Partner-safe | TBD | L2 | 0 | Use in partner discussion |
| docs_top_level_snapshot.json | Memory Index | 1 | 3 | 5 | 2 | 4 | 5 | GENERATED | CI / Founder | Monthly | Eng | Internal-only | TBD | L2 | 0 | CI + monthly snapshot |
| DOCS_ARCHIVE_POLICY_AR.md | Govern | 2 | 5 | 4 | 3 | 4 | 5 | CANONICAL | Founder | Quarterly | Ops | Internal-only | TBD | L2 | 0 | Council review |
| DOCS_PUBLICATION_BOUNDARY_AR.md | Govern | 3 | 5 | 4 | 5 | 5 | 5 | CANONICAL | Founder | Quarterly | All | Internal-only | TBD | L2 | 0 | Pre-flight external send |

**ملاحظة:** `generate_holding_value_summary.py` يولّد [holding_value_summary.json](_generated/holding_value_summary.json) و[asset_activation_priorities.json](_generated/asset_activation_priorities.json).
