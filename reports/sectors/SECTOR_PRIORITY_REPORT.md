# SECTOR PRIORITY REPORT — Dealix GTM

> Source of truth: `data/sectors/sectors.yaml` (10 sectors) · Ladder: `data/commercial/product_catalog.yaml` · IDs: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`
> Status as of: 2026-06-03 · Owner: GTM / Founder
> This is a **template report**. It ranks the 10 ICP sectors so outreach effort lands where revenue is most defensible.

---

## 1) Scope & method

`data/sectors/sectors.yaml` does **not** yet carry an explicit `priority` field per row. Until that field lands, this report derives a transparent priority from the canonical signals that *do* exist in the repo, so the ranking is reproducible and auditable:

1. **Deal economics — `first_offer`** (ladder level → entry deal size, from `product_catalog.yaml`):
   `DLX-L1` 1,500–5,000 ر.س · `DLX-L2` 8,000–18,000 · `DLX-L3` 18,000–35,000. Higher entry value = higher revenue per won deal.
2. **`pricing_sensitivity`** (`low` > `medium` > `high`): `low` closes nearer to value with less discounting → higher priority.
3. **Strategic anchor / authoring order** in `sectors.yaml`: `marketing_agencies` is row 1 and the only sector with a pre-written, validated playbook — treated as the flagship beachhead.

> Tiebreak rationale aligns with the prospect-score rubric (`payment_ability` 15, `buying_signal` 20 in `MARKET_PRODUCTION_NAMING_CONVENTIONS.md`): we weight payment ability (proxied by deal size + low price sensitivity) and clarity of buying triggers.
>
> **Action when `priority` is added to `sectors.yaml`:** replace the derived `Priority` column below with the canonical field and re-sort. No other section needs to change.

### Scoring sketch (derived, not canonical)
- first_offer: L3 = 3 pts · L2 = 2 pts · L1 = 1 pt
- pricing_sensitivity: low = +2 · medium = +1 · high = 0
- anchor bonus: flagship beachhead = +1
- Higher total = higher focus priority. Ties broken by `sectors.yaml` row order.

---

## 2) Priority ranking (derived)

| # | Sector (`id`) | Arabic | First offer | Pricing sens. | Derived score | Tier |
|---|---------------|--------|-------------|---------------|---------------|------|
| 1 | `logistics_companies` | شركات اللوجستيك | DLX-L3 | low | 5 | P0 — Lead |
| 2 | `local_saas` | شركات SaaS المحلية | DLX-L3 | low | 5 | P0 — Lead |
| 3 | `real_estate_teams` | فرق العقار | DLX-L2 | low | 4 | P1 — Core |
| 4 | `professional_services` | الخدمات المهنية | DLX-L1 | low | 3 | P1 — Core |
| 5 | `marketing_agencies` | وكالات التسويق | DLX-L1 | medium | 2 (+1 anchor) | P1 — Core (anchor) |
| 6 | `recruitment_agencies` | وكالات التوظيف | DLX-L2 | medium | 3 | P1 — Core |
| 7 | `training_companies` | شركات التدريب | DLX-L1 | medium | 2 | P2 — Expand |
| 8 | `education_providers` | مزوّدو التعليم | DLX-L1 | medium | 2 | P2 — Expand |
| 9 | `clinics` | العيادات | DLX-L1 | medium | 2 | P2 — Expand |
| 10 | `restaurant_groups` | مجموعات المطاعم | DLX-L1 | medium | 2 | P2 — Expand |

> Note on row 5 (`marketing_agencies`): base derived score is 2, but it carries the **anchor bonus** as the validated flagship sector with an existing playbook and the cleanest operational story (lead_leakage + follow_up_chaos). It is sequenced as a Core anchor for proof generation even though raw deal size is L1.

---

## 3) Playbook delivery status

| Sector (`id`) | Playbook path | Status | First offer | First workflow |
|---------------|---------------|--------|-------------|----------------|
| `marketing_agencies` | `docs/sectors/MARKETING_AGENCIES_AR.md` | Ready | DLX-L1 | Revenue Leakage Diagnostic |
| `training_companies` | `docs/sectors/TRAINING_COMPANIES_AR.md` | Ready | DLX-L1 | Revenue Leakage Diagnostic |
| `clinics` | `docs/sectors/CLINICS_AR.md` | Ready | DLX-L1 | Revenue Leakage Diagnostic |
| `real_estate_teams` | `docs/sectors/REAL_ESTATE_TEAMS_AR.md` | Ready | DLX-L2 | Follow-up Recovery Workflow |
| `recruitment_agencies` | `docs/sectors/RECRUITMENT_AGENCIES_AR.md` | Ready | DLX-L2 | Follow-up Recovery Workflow |
| `professional_services` | `docs/sectors/PROFESSIONAL_SERVICES_AR.md` | Ready | DLX-L1 | Revenue Leakage Diagnostic |
| `education_providers` | `docs/sectors/EDUCATION_PROVIDERS_AR.md` | Ready | DLX-L1 | Revenue Leakage Diagnostic |
| `logistics_companies` | `docs/sectors/LOGISTICS_COMPANIES_AR.md` | Ready | DLX-L3 | AI Revenue Ops Starter |
| `restaurant_groups` | `docs/sectors/RESTAURANT_GROUPS_AR.md` | Ready | DLX-L1 | Revenue Leakage Diagnostic |
| `local_saas` | `docs/sectors/LOCAL_SAAS_AR.md` | Ready | DLX-L3 | AI Revenue Ops Starter |

All 10 playbooks follow the same 17-section structure and inherit the canonical defaults: `dry_run=true`, `approval_required=true`, `send_enabled=false`; WhatsApp post-reply only; 250 drafts/day with sending gated.

---

## 4) Recommended focus order

**Phase 1 — Lead (high deal value, low price sensitivity):**
`logistics_companies` → `local_saas`. Entry at DLX-L3 (18,000–35,000 ر.س) means one won deal funds outreach for the tier; the buyer (`operations_manager` / `founder_owner`) closes on operational rigor, not discount. Longer cycles, so start the pipeline first.

**Phase 2 — Core (fast proof + strong economics):**
`real_estate_teams` → `recruitment_agencies` (both DLX-L2, high-volume follow-up pain) → `professional_services` (DLX-L1, low price sensitivity, proposal_delay) → `marketing_agencies` (validated anchor; fastest, cleanest case-study generator to seed Proof Packs).

**Phase 3 — Expand (volume, seasonal, medium price sensitivity):**
`training_companies` and `education_providers` (time to nearest admissions/registration season) → `clinics` (data-handling guardrails: operational data only, no patient PII) → `restaurant_groups` (B2B events/catering arm only).

### Sequencing guidance
- Run **Phase 1 pipeline early** (long cycles) while harvesting **Phase 2 proof fast** (short DLX-L1/L2 deliverables) to build the Proof Pack with placeholder examples only.
- Honor `do_not_target` per sector before any outreach; never cold-WhatsApp; floor personalization at **P1**.
- Re-rank this table the moment a canonical `priority` field is added to `sectors.yaml`.

---

## 5) Open items
- [ ] Add explicit `priority` integer field to each row in `data/sectors/sectors.yaml`, then swap it into §2.
- [ ] Attach per-sector pipeline counts + win-rate once live data exists (`reports/` data sources).
- [ ] Review `clinics` data-handling scope with founder before any outreach (no patient PII; operational data only).
