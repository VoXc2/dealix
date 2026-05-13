# Dealix Compounding System

> **Rule**: every project must make Dealix stronger. A project is not
> "closed" internally until it has produced the 6 compounding assets below.

## The 6 assets every project must produce

1. **Client Outcome** — the delivered work (reports, dashboards, workflows, assistants).
2. **Proof Asset** — anonymized Proof Pack added to `docs/assets/proof_packs/`.
3. **Template** — any reusable scope/intake/report/draft pattern that emerged.
4. **Playbook Update** — sector or use-case learning written to `docs/playbooks/<vertical>.md`.
5. **Product Feature Candidate** — manual step that repeated ≥ 2 times, logged in `docs/product/FEATURE_PRIORITIZATION.md`.
6. **Sales Asset** — anonymized case study, before/after example, or objection response added to `docs/assets/sales/`.

## Closure rule

```
Project marked CLOSED only when:
  ✓ Client Outcome delivered
  ✓ Proof Pack written (Stage 7)
  ✓ POST_PROJECT_REVIEW.md filed
  ✓ At least 1 compounding asset captured in docs/assets/
```

Otherwise the project remains in stage "Prove" — the founder's WIP queue stays heavy until learning is captured.

## Asset library layout

```
docs/assets/
  reports/                # sample executive reports per service
  proof_packs/            # anonymized Proof Ledger entries
  sales/                  # before/after, objections, anonymized case studies
  templates/              # reusable scope / intake / draft templates
  playbooks/              # vertical playbooks (also in docs/playbooks/)
  demos/                  # demo scripts and walkthroughs
  case_studies/           # public-grade case studies
```

## Project-side files (per project)

For each paying customer, create a directory `clients/<client_codename>/` containing:

- `DELIVERY_COMMAND.md` — owner, status, blockers, pending decisions, next action.
- `governance_events.md` — every Governance OS decision (PII found, claim caught, approval granted/denied).
- `delivery_approval.md` — the 5-gate QA checklist with PASS/FAIL.
- `proof_pack.md` — Stage-7 evidence (mirrors `proof_pack_template.md`).
- `POST_PROJECT_REVIEW.md` — captures the 6 compounding assets at close.

## Post-project review template

```markdown
# Post Project Review — <client_codename>
- Service:
- Date closed:

## 1. Client Outcome
What we delivered + KPI moved + customer feedback rating.

## 2. Proof Pack reference
docs/assets/proof_packs/<entry>.md

## 3. Template extracted
Path of new / improved template.

## 4. Playbook update
Sector playbook(s) touched + what was learned.

## 5. Feature Candidate
Manual step that repeated (and link to `docs/product/FEATURE_PRIORITIZATION.md`).

## 6. Sales Asset
What new sales asset was created from this work.

## Retainer opportunity
Yes / No → if yes, recommended offer + expected SAR/mo.

## Anti-patterns observed
Anything that almost broke the project — to inform Rule 5/6 of Decision Rules.
```

## Why this matters

- Two customers with the same service shouldn't cost 2× the effort. With this system, the 2nd customer costs ~70% of the 1st, the 5th costs ~40%.
- Sales gets stronger with every delivery because Sales Assets compound.
- Engineering builds the right features because Feature Candidates are evidence-based, not speculative.
- Playbooks become a moat that competitors cannot easily copy.

## Owner & cadence

- **Owner**: HoCS owns project closure; HoP curates the asset library.
- **Cadence**: every project, no exceptions. Monthly retro reviews assets created vs delivered.

## Cross-links

- `docs/company/DEALIX_OPERATING_KERNEL.md` — Learning Engine
- `docs/company/DECISION_RULES.md` — Rule 5/6 (build after repetition / services become products)
- `docs/strategy/dealix_maturity_and_verification.md` — "Build only after repetition"
- `docs/product/FEATURE_PRIORITIZATION.md` — where feature candidates are scored
