# Dealix Definition of Done

Three "Done" checklists. Nothing is "done" without ticking every box on the
applicable list. Used by Engineering, Delivery, and Sales as the close-out
gate.

## Service Definition of Done

A service is **Sellable** (per `docs/company/SELLABILITY_POLICY.md`) only when:

- [ ] `offer.md` exists in `docs/services/<offer>/`
- [ ] `scope.md` exists (inclusions + exclusions + customer responsibilities)
- [ ] Intake file exists (`intake.md` / `process_intake.md` / `inbox_intake.md` / `document_request.md`)
- [ ] `data_request.md` exists
- [ ] `delivery_checklist.md` exists (day-by-day)
- [ ] `qa_checklist.md` exists (5 gates)
- [ ] `report_template.md` exists
- [ ] `proof_pack_template.md` exists
- [ ] `sample_output.md` exists (anonymized realistic example)
- [ ] `handoff.md` exists
- [ ] `upsell.md` exists
- [ ] SOW template exists in `templates/sow/`
- [ ] Backing OS module(s) at least at MVP per `docs/product/CAPABILITY_MATRIX.md`
- [ ] Governance check defined (forbidden actions + approval requirements)
- [ ] Demo runnable in ≤ 10 minutes (`demos/<offer>_demo.py`)
- [ ] Acceptance test passes against sample data
- [ ] Sales asset published (offer page in `docs/sales/offer_pages/`)

## Project Definition of Done

A paying project is **Closed** only when:

- [ ] All SOW deliverables delivered
- [ ] 5-gate QA all PASS (`clients/<codename>/delivery_approval.md`)
- [ ] Quality Score ≥ 80 (target ≥ 85)
- [ ] 0 Hard Fails triggered
- [ ] Governance events log complete (`clients/<codename>/governance_events.md`)
- [ ] PDPL Art. 13/14 honored on every outbound action
- [ ] Proof Pack delivered (`clients/<codename>/proof_pack.md`)
- [ ] Anonymized Proof Pack added to `docs/assets/proof_packs/`
- [ ] Handoff session completed (recorded)
- [ ] Next-step / renewal proposal drafted
- [ ] `POST_PROJECT_REVIEW.md` filed (`docs/company/COMPOUNDING_SYSTEM.md` Rule)
- [ ] At least 1 of: new template / playbook update / feature candidate / sales asset captured

A project that ships deliverables but fails the post-review filing is **NOT** closed internally — it stays in the founder's WIP queue until learning is captured.

## Feature Definition of Done

A code feature is **Production-Ready** only when:

- [ ] Implementation passes `py_compile` and `ruff` / `mypy`
- [ ] Pytest test added in `tests/test_<area>_*.py` (happy path + ≥ 1 negative path)
- [ ] Logging via `structlog` (no `print`, no f-strings in log calls)
- [ ] Error handling: raises typed exceptions; HTTPException at route boundary
- [ ] Audit event emitted to `event_store` if the action has a side-effect
- [ ] Pydantic output schema defined and validated
- [ ] PII check applied if any field could carry personal data
- [ ] LLM cost guard wired if model-backed (Phase 2: via `dealix/llm_gateway/`)
- [ ] Documentation: at minimum a docstring; for endpoints, an entry in `docs/product/API_SPEC.md`
- [ ] Backs ≥ 1 customer-visible Sellable service (Rule 5: no speculation)
- [ ] Either reduces delivery time, reduces a tracked risk, or improves output quality (and that improvement is named in the PR description)

## How to use this file

- **Engineering PRs**: PR description must explicitly state which of the Feature DoD boxes are ticked.
- **CS at project close**: opens `POST_PROJECT_REVIEW.md` and walks the Project DoD; CEO signs off only on a fully ticked list.
- **CRO before adding a service to the catalog**: walks the Service DoD; only Sellable services with all boxes ticked appear in `docs/company/SERVICE_REGISTRY.md` as Sellable.

## Owner & cadence

- **Owner**: HoP for Service DoD; HoCS for Project DoD; CTO for Feature DoD.
- **Audit**: quarterly the CEO samples 3 random items from each DoD and confirms compliance.

## Cross-links

- `docs/company/SELLABILITY_POLICY.md` — Service DoD authority
- `docs/company/COMPOUNDING_SYSTEM.md` — Project DoD authority
- `docs/company/DECISION_RULES.md` — Rule 5/6 → Feature DoD authority
- `docs/product/FEATURE_PRIORITIZATION.md` — how features earn a place in the backlog before reaching DoD
