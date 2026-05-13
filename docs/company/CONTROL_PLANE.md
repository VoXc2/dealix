# Dealix Control Plane

> Reads the 8 Operating Ledgers and produces the 7 weekly answers the CEO
> needs to run the company.

## Inputs (8 ledgers)

`docs/ledgers/` — REQUEST · DECISION · CLIENT · DELIVERY · GOVERNANCE · PROOF · LEARNING · PRODUCT.

## Outputs (7 weekly answers)

The Control Plane is "queried" every Monday in the operating review:

1. **What services are sellable now?** → join Service Readiness Matrix + Client Ledger; output the 3 (or 5) services with > 0 closed customers and Readiness Score ≥ 85.
2. **What clients are ready for expansion?** → Client Ledger where Health ≥ 80 AND no active retainer; route to `RETAINER_DECISION.md`.
3. **What risks are repeating?** → Governance Ledger grouped by issue type; any type with > 2 occurrences in 30 days is a Friday QA-board agenda item.
4. **What proof assets can be turned into case studies?** → Proof Ledger where customer permission exists; route to `CASE_STUDY_FACTORY.md` *(when added)*.
5. **What feature should be built next?** → Product Ledger where score ≥ 80; route to next sprint per `BUILD_DECISION.md`.
6. **What service should be repriced?** → Cross-join Client Ledger (last 3 closes at full price, no push-back) with Pricing Decision triggers.
7. **What sector deserves a playbook?** → Client Ledger grouped by Sector; any sector with ≥ 3 paid projects gets a playbook in `docs/playbooks/<vertical>.md`.

## The Monday query

The CEO opens this doc, walks each of the 7 answers, and produces the 3
weekly decisions captured in `WEEKLY_OPERATING_REVIEW.md`.

Pseudocode (for the eventual product version):

```
def control_plane(week):
    sellable = service_readiness_matrix.where(status == "Sellable")
    expansions = client_ledger.where(health >= 80 and not active_retainer)
    repeating_risks = governance_ledger.group_by(issue).filter(count > 2, last_30d)
    case_candidates = proof_ledger.where(permission == "yes")
    build_next = product_ledger.where(score >= 80).top(1)
    reprice = client_ledger.recent_closes(3, no_pushback=True, same_service)
    playbook_targets = client_ledger.group_by(sector).filter(paid_count >= 3)
    return {
        "sellable": sellable,
        "expand": expansions,
        "risks_to_fix": repeating_risks,
        "case_studies": case_candidates,
        "build": build_next,
        "reprice": reprice,
        "new_playbooks": playbook_targets,
    }
```

## Phase 2 wiring

When ledgers move into the event store, the Control Plane becomes a real
endpoint: `GET /api/v1/control-plane/weekly` that returns the 7 answers as
structured JSON. Founder Command Center subscribes to it.

## Owner & cadence

- **Owner**: CEO.
- **Cadence**: Monday 09:00 weekly operating review.

## Cross-links

- `docs/company/OPERATING_LEDGER.md`
- `docs/ledgers/README.md`
- `docs/company/WEEKLY_OPERATING_REVIEW.md`
- `docs/company/FOUNDER_COMMAND_CENTER.md`
- `docs/company/DECISION_OPERATING_SYSTEM.md`
