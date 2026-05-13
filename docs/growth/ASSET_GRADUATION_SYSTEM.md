---
doc_id: growth.asset_graduation_system
title: Asset Graduation System — From Raw Output to Market Asset
owner: HoP
status: approved
last_reviewed: 2026-05-13
audience: [internal]
---

# Asset Graduation System

> Every deliverable Dealix produces can graduate through 5 stages. At
> each stage the asset becomes more reusable, more valuable, and less
> dependent on the founder. Without this system every project starts
> from zero. With this system every project compounds.

## The 5 graduation stages

| Stage | Name | What it looks like | Owner | Location |
|------:|------|--------------------|-------|----------|
| 1 | Raw Output | One-off deliverable produced for one customer | CSM | `clients/<codename>/` |
| 2 | Reusable Template | Sanitized + parameterized; another delivery can fill it in | HoCS | `docs/assets/templates/` or `templates/` |
| 3 | Standard Asset | Adopted across all deliveries of this service; part of the Dealix Standard | HoCS + CEO | `docs/_templates/` + `docs/quality/QUALITY_STANDARD.md` reference |
| 4 | Productized Asset | Code-backed, machine-generated when the workflow runs | CTO | `dealix/<module>/` (e.g. `dealix/reporting/`) |
| 5 | Market Asset | Public-facing artifact that earns the category (case study, benchmark, sample report) | CEO | `docs/assets/case_studies/`, website, Benchmark report |

## Example chain — Executive Report

| Stage | Concrete example |
|------:|------------------|
| 1 | Founder writes a weekly executive report for CLIENT-A by hand. |
| 2 | The report becomes a reusable template in `docs/assets/templates/executive_report_template.md`. |
| 3 | The template is named in the Dealix Standard #7 (Proof Delivered) and used across every delivery. |
| 4 | The template is replaced by `dealix/reporting/executive_report.py` — code generates the report from ledger inputs. |
| 5 | An anonymized sample executive report is published on the Dealix website and inside the Saudi AI Operations Benchmark. |

## Example chain — Sector Playbook

| Stage | Concrete example |
|------:|------------------|
| 1 | Notes from a B2B Services Sprint live in `clients/CODENAME/`. |
| 2 | Notes lifted into `docs/playbooks/b2b_services.md` as a draft. |
| 3 | Playbook references in `VERTICAL_PLAYBOOKS.md` and used in every B2B Services Sprint. |
| 4 | Playbook drives ICP scoring rules inside `auto_client_acquisition/icp_builder.py`. |
| 5 | Anonymized B2B Services case study published with measurable KPI deltas. |

## Graduation rules (binding)

| Movement | Trigger | Evidence required |
|----------|---------|-------------------|
| 1 → 2 | Asset used in 2 different customer projects | Template filed + 2 client references |
| 2 → 3 | Asset used in ≥ 5 projects with QA score ≥ 85 | Named in the Dealix Standard; reviewed by CEO |
| 3 → 4 | Manual production repeats ≥ 3× per month | Feature Candidate logged + approved per `FEATURE_PRIORITIZATION.md` |
| 4 → 5 | Code-backed asset stable for ≥ 90 days + customer permission obtained | Anonymized + HoLegal sign-off + published |

## Anti-patterns

- Skipping Stage 2 (rewriting the same Raw Output for 5 customers).
- Building Stage 4 software before Stage 3 (no customer paid for it).
- Publishing Stage 5 without anonymization (PDPL incident waiting to happen).
- Letting an asset stall at Stage 3 (it should keep moving or be retired).

## Cadence

- **Weekly** — `WEEKLY_OPERATING_REVIEW.md` Compounding section
  counts assets added per stage.
- **Monthly** — Operating Intelligence question 6 (per
  `OPERATING_INTELLIGENCE.md`) decides Stage 3 → 4 promotions.
- **Quarterly** — HoP audits the asset library; retires anything
  stale at Stage 2 or 3 with no use in 90 days.

## Saudi / PDPL note

Stage 5 publication requires HoLegal sign-off because anonymization
under PDPL is not a checkbox — it requires removal of any direct or
indirect identifiers (account names, sector tells, distinctive
metrics). When in doubt, asset stays at Stage 4.

## Cross-links

- `docs/company/COMPOUNDING_SYSTEM.md` — the 6 compounding assets per project
- `docs/company/IP_REGISTRY.md` — the IP catalog (Stage 3+ assets)
- `docs/company/OPERATING_INTELLIGENCE.md` — promotion ritual
- `docs/product/FEATURE_PRIORITIZATION.md` — Stage 3 → 4 trigger
- `docs/company/DEALIX_STANDARD.md` — Stage 3 home
- `docs/strategy/FROM_SERVICE_TO_STANDARD.md` — company-level 5-stage arc (parallel)
- `docs/strategy/AI_OPS_CATEGORY_METRICS.md` — Stage 5 Benchmark report
