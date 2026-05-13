# Dealix Operating Flywheel

The compounding loop: every customer makes the next customer cheaper to
deliver, easier to close, and higher-margin.

```
Better Services
  → Better Delivery (Stage Machine + QA Engine)
  → Better Proof Packs
  → Better Case Studies (anonymized)
  → Better Sales (with proof, not promises)
  → More Customers
  → More Learning Captured (per COMPOUNDING_SYSTEM)
  → Better Product (features built from real repetition)
  → Better Services
```

## The flywheel rule

> Every project must improve the system. A project that delivers an output
> but produces no improvement to **services**, **delivery speed**, **product
> capability**, **playbooks**, **proof assets**, or **sales conversion** is
> operationally incomplete — even if the customer is satisfied and paid.

## Where the flywheel touches Dealix

| Flywheel step | Where it lives | How it accelerates |
|---------------|----------------|---------------------|
| Better Services | `docs/services/*` + `SERVICE_REGISTRY.md` | Each `POST_PROJECT_REVIEW.md` produces an offer/scope refinement |
| Better Delivery | `delivery_factory/stage_machine.py` + `qa_review.py` | New templates from each delivery shorten the next |
| Better Proof Packs | `dealix/reporting/proof_pack.py` + `docs/assets/proof_packs/` | Anonymized packs become sales weapons |
| Better Case Studies | `docs/assets/case_studies/` (post-customer permission) | Move conversions from 25% → 40% sprint-to-retainer |
| Better Sales | `docs/sales/sales_script.md` + `objection_handling.md` | Each closed deal teaches one new objection counter |
| More Customers | `verify_dealix_ready.py` SALES_UNLOCKED=true + outbound | First 25 customers seed everything |
| More Learning | `COMPOUNDING_SYSTEM.md` + `POST_PROJECT_REVIEW.md` | 6 assets per project, captured weekly |
| Better Product | `FEATURE_PRIORITIZATION.md` + `BUILD_DECISION.md` | Backlog items earn their place via repetition |

## Flywheel acceleration metrics (track monthly)

- Time-to-deliver same-service second customer vs first: target ≤ 80%.
- Sales-cycle length (days from lead to paid) for same-vertical second customer vs first: target ≤ 70%.
- Sprint → Retainer conversion rate: target 25% (Month 1) → 40% (Month 6).
- New templates / playbook updates per project: target ≥ 1.
- New feature candidates per 3 projects: target 1 promoted to backlog.

## Anti-flywheel patterns (block on sight)

- "Custom for this customer" without productizing it → next customer costs the same.
- "Skip the post-project review" → learning evaporates.
- "Don't update the playbook this time" → same mistake repeats.
- "Build a feature speculatively" → engineering capacity burned without paid demand.
- "Hide the Proof Pack inside the customer folder" → sales never re-uses it.

## What you should feel after 5 customers

- Quoting a new sprint takes < 30 minutes.
- Onboarding a new sprint customer takes < 1 business day.
- Generating an executive report takes 60% less time than the first one.
- You can name 5 specific things Dealix knows now that it didn't 3 months ago.

If you can't feel these, the flywheel isn't turning. Diagnose: which station broke?

## Owner & cadence
- **Owner**: CEO.
- **Cadence**: monthly retrospective; flywheel metrics in `WEEKLY_OPERATING_REVIEW.md`.

## Cross-links
- `docs/company/COMPOUNDING_SYSTEM.md`
- `docs/company/CLOSED_LOOP_EXECUTION.md`
- `docs/company/MATURITY_BOARD.md`
- `docs/strategy/dealix_maturity_and_verification.md`
