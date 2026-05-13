---
title: Bilingual Operating Assets Index (Saudi GTM)
doc_id: W3.T20.bilingual-operating-assets
owner: HoP
status: draft
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: none
related: [W0.T00, W1.T01, W1.T02, W1.T05, W2.T03, W2.T04, W2.T08, W2.T09, W2.T12, W3.T06, W3.T07a, W3.T07b, W3.T07c, W3.T07d, W3.T15, W5.T28, W5.T30]
kpi:
  metric: bilingual_assets_in_freshness
  target: 100
  window: 90d
rice:
  reach: 30
  impact: 2
  confidence: 0.9
  effort: 1
  score: 54
---

# Bilingual Operating Assets Index (Saudi GTM)

## 1. Context

The Saudi GTM is bilingual by contract: every customer-facing, partner-facing, and procurement-facing artefact must exist in Arabic and English, and the Arabic version must be authoritative for the audience whose first language is Arabic (procurement, DPO, legal, executive). This index is the single canonical register of every bilingual asset produced under the 90-day Saudi GTM initiative. Owners use it to track freshness, parity, and accountability. Drift between EN and AR is treated as a Sev 3 hygiene issue and must be closed within 14 days; a delta older than 30 days marks the asset stale and blocks customer use until resynced.

This index covers Waves 1–3 and 5 artefacts. It does not duplicate the general repository localisation map; instead, it focuses on the GTM-critical assets created or refreshed for the Saudi initiative.

## 2. Audience

- Internal owners of each asset (writing, reviewing, publishing).
- Head of Product (HoP) as accountable owner of the index.
- Localization reviewers (Arabic fasīh fluency required).
- Partner enablement teams selecting which artefacts to share.
- Audit / compliance for evidence that customer-facing material is bilingual.

## 3. Decisions & Content

### 3.1 Freshness Status Definitions

- **Fresh:** EN and AR last reviewed within 30 days, content parity confirmed.
- **Drift:** EN and AR diverge in substance or `last_reviewed` differs by more than 14 days.
- **Stale:** Either version not reviewed in 30+ days; blocks customer-facing use until refreshed.
- **Missing:** AR or EN companion not yet authored.

### 3.2 Wave 1 — Discovery & Positioning

| Asset | EN path | AR path | Owner | Last reviewed | Freshness |
|---|---|---|---|---|---|
| Saudi ICP profile | `docs/go-to-market/icp_saudi.md` | `docs/go-to-market/icp_saudi.ar.md` | CRO | 2026-05-13 | Fresh |
| Saudi vertical positioning | `docs/go-to-market/saudi_vertical_positioning.md` | `docs/go-to-market/saudi_vertical_positioning.ar.md` | CRO | 2026-05-13 | Fresh |
| Saudi lead engine | `docs/product/saudi_lead_engine.md` | `docs/product/saudi_lead_engine.ar.md` | HoP | 2026-05-13 | Fresh |

### 3.3 Wave 2 — Commercial & Sales Enablement

| Asset | EN path | AR path | Owner | Last reviewed | Freshness |
|---|---|---|---|---|---|
| Saudi ROI model | `docs/sales/roi_model_saudi.md` | `docs/sales/roi_model_saudi.ar.md` | CRO | 2026-05-13 | Fresh |
| ROI deck outline | `docs/sales/roi_deck_outline.md` | `docs/sales/roi_deck_outline.ar.md` | CRO | 2026-05-13 | Fresh |
| Persona × value matrix | `docs/sales/persona_value_matrix.md` | `docs/sales/persona_value_matrix.ar.md` | CRO | 2026-05-13 | Fresh |
| Saudi pricing & packaging | `docs/pricing/pricing_packages_sa.md` | `docs/pricing/pricing_packages_sa.ar.md` | CRO | 2026-05-13 | Fresh |
| Value metrics catalogue | `docs/pricing/value_metrics.md` | `docs/pricing/value_metrics.ar.md` | HoP | 2026-05-13 | Fresh |
| Sales playbook (Saudi) | `docs/SALES_PLAYBOOK.md` | `docs/SALES_PLAYBOOK.ar.md` | CRO | 2026-05-13 | Fresh |

### 3.4 Wave 3 — Trust, Legal, Procurement, Partners

| Asset | EN path | AR path | Owner | Last reviewed | Freshness |
|---|---|---|---|---|---|
| Saudi partner program | `docs/partnerships/partner_program_sa.md` | `docs/partnerships/partner_program_sa.ar.md` | CRO | 2026-05-13 | Fresh |
| Security overview | `docs/trust/security_overview.md` | `docs/trust/security_overview.ar.md` | HoLegal | 2026-05-13 | Fresh |
| Data governance | `docs/trust/data_governance.md` | `docs/trust/data_governance.ar.md` | HoLegal | 2026-05-13 | Fresh |
| Incident response | `docs/trust/incident_response.md` | `docs/trust/incident_response.ar.md` | HoLegal | 2026-05-13 | Fresh |
| Access control | `docs/trust/access_control.md` | `docs/trust/access_control.ar.md` | CTO | 2026-05-13 | Fresh |
| Enterprise procurement pack | `docs/procurement/enterprise_pack.md` | `docs/procurement/enterprise_pack.ar.md` | HoLegal | 2026-05-13 | Fresh |

### 3.5 Wave 5 — Expansion & Launch

| Asset | EN path | AR path | Owner | Last reviewed | Freshness |
|---|---|---|---|---|---|
| Expansion playbook | `docs/playbooks/expansion_playbook.md` | `docs/playbooks/expansion_playbook.ar.md` | CRO | TBD | Missing (Wave 5) |
| Launch checklist | `docs/launch/launch_checklist.md` | `docs/launch/launch_checklist.ar.md` | HoP | TBD | Missing (Wave 5) |

### 3.6 EN-Only Reference Assets (Not Bilingual)

These assets are deliberately EN-only because their audience is internal English-speaking operators (engineering, finance, executive). They are linked here for completeness so reviewers do not mistake their lack of AR companion as a freshness issue.

- `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md` — internal strategy master.
- `docs/strategy/competitive_landscape_sa.md` — internal competitive analysis.
- `docs/localization/bilingual_operating_assets.md` — this document.
- `docs/legal/enterprise_risk_register.md` — internal legal/finance risk register.

### 3.7 AR-Authoring Standards

- **Register:** فصحى رسمية (formal modern standard Arabic), suitable for procurement, DPO, legal, and executive audiences. Colloquial registers are not used.
- **Terminology:** terminology consistency is enforced through a glossary maintained alongside this index (placeholder: `docs/localization/glossary_ar.md`, planned). When a technical term has both an Arabic and an English form in active use (e.g., "API", "SLA"), the form that is recognisable to a Saudi enterprise reader is preferred and the alternative is footnoted on first occurrence.
- **Numerals:** Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩) preferred in legal and financial documents; Western digits (0123456789) acceptable in technical documents where parity with EN is the priority.
- **Dates:** Hijri date primary in legal documents, with Gregorian in parentheses; Gregorian primary in technical and operational documents.
- **Currency:** "ريال سعوديّ (SAR)" on first occurrence per document, then "SAR" thereafter is acceptable.
- **Right-to-left rendering:** all AR documents must render correctly in RTL across the surfaces where they are consumed (Markdown viewers, PDF exports, partner-portal HTML).

### 3.8 Review and Sign-Off Workflow

1. Author produces EN first, signed off by the owner.
2. Author or translator produces AR within 5 working days.
3. AR is reviewed by a fasīh-fluent reviewer (HoLegal for legal docs, HoP/CRO for commercial).
4. Both versions are committed in the same change set; `last_reviewed` is updated.
5. The owner files the change in this index and updates the freshness column.
6. Any change to EN automatically opens a 14-day ticket against AR to maintain parity.

### 3.9 Drift Detection (Operational)

A lightweight CI check is planned (`scripts/check_bilingual_freshness.py`, backlog) that compares `last_reviewed` dates between EN and AR companions and flags items where the gap exceeds 14 days. Until automation is in place, this index is manually reviewed weekly by HoP.

## 4. KPIs

- **Primary:** 100% of bilingual assets in "Fresh" status across a rolling 90-day window.
- Zero customer-facing documents shipped without AR companion.
- Mean drift-to-resync time ≤ 14 days.

## 5. Dependencies

- Continued availability of fasīh-fluent reviewers.
- Glossary publication (planned).
- CI freshness check (backlog).
- Wave 5 asset completion to clear "Missing" rows.

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Every asset listed in §§3.2–3.5.
- Risk register: `docs/legal/enterprise_risk_register.md`

## 7. Owner & Review Cadence

- Owner: Head of Product (HoP).
- Weekly index review during the 90-day GTM window; bi-weekly thereafter.

## 8. Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-13 | Initial index covering Waves 1–3 + Wave 5 placeholders | HoP |
