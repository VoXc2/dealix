# Value Realization System

> Every project must produce **at least one measurable value category**
> AND **one next-value opportunity**. Otherwise the project shipped but
> Dealix didn't compound.

## The 5 value categories

1. **Revenue Value** — leads ranked, pipeline created, opportunities clarified, conversion lifted.
2. **Time Value** — hours saved, manual steps reduced, response time improved.
3. **Quality Value** — fewer errors, better consistency, cleaner data, sharper reports.
4. **Risk Value** — PII protected, approvals logged, unsafe actions blocked, audit complete.
5. **Knowledge Value** — faster answers, source-backed responses, fewer repeated questions to the team.

## Value Ledger (canonical)

Lives at `docs/ledgers/VALUE_LEDGER.md`:

```markdown
| ID | Client | Service | Value Type | Metric | Baseline | Result | Evidence | Next Value |
|----|--------|---------|------------|--------|----------|--------|----------|-----------|
| V-001 | BFSI-A1 | Lead Intelligence | Revenue | ranked accounts | 0 | 50 | proof_pack_a1 | Pilot Conversion |
| V-002 | LOG-B2 | Quick Win | Time | manual hours/week | 6 | 1 | runbook + audit | Monthly AI Ops |
| V-003 | HEALTH-C3 | Company Brain | Knowledge | answers with citation % | n/a | 96% | eval report | Policy Assistant |
```

Rule: a Proof Pack without a Value Ledger entry is incomplete.

## Closure rule (binding)

Before marking a project CLOSED:

- [ ] At least 1 value category measured (numeric before/after).
- [ ] At least 1 next-value opportunity named (which capability to lift next).
- [ ] Value Ledger entry written.
- [ ] Linked to a Proof Pack file.
- [ ] Customer agreed on the measurement method (in writing).

## Capability ↔ Value Map

Per `docs/company/CAPABILITY_OPERATING_MODEL.md`:

| Capability | Primary Value |
|------------|---------------|
| Revenue | Revenue Value |
| Customer | Time + Quality Value |
| Operations | Time + Quality Value |
| Knowledge | Knowledge Value |
| Data | Quality + Risk Value |
| Governance | Risk Value |
| Reporting | Quality + Time Value |

## Why measurement matters

A customer who can't restate the value Dealix delivered in 1 sentence will not renew. A value not measured is a value not retained.

## Owner & cadence
- **Owner**: HoCS files each entry; CEO reviews monthly.
- **Cadence**: every project, mandatory.

## Cross-links
- `docs/ledgers/README.md` — Value Ledger template
- `docs/company/COMPOUNDING_SYSTEM.md`
- `docs/company/CAPABILITY_OPERATING_MODEL.md`
- `dealix/reporting/proof_pack.py` — code-side Proof Pack model
