# Capital Ledger

Track **which capital** each project compounded. IDs: `C-###`.

## Capital types

```text
Service
Product
Knowledge
Trust
Market
```

## Minimum per project

```text
1 Trust Asset
+ 1 Knowledge أو Product Asset
```

Examples:

- **Trust:** anonymized proof pack, QA’d deliverable narrative
- **Knowledge:** playbook delta, objection, sector insight
- **Product:** script, internal tool, feature candidate shipped or specified

| ID | Project | Capital Type | Asset Created | Reusable? | Owner | Next Use |
|----|---------|--------------|---------------|-----------|-------|----------|
| C-001 | Lead Sprint A | Trust | anonymized proof pack | Yes | | sales deck |
| C-002 | Lead Sprint A | Product | import preview script | Yes | | all lead sprints |
| C-003 | Clinic Sprint | Knowledge | clinics playbook update | Yes | | clinic outreach |

**Parent model:** [`DEALIX_CAPITAL_MODEL.md`](../company/DEALIX_CAPITAL_MODEL.md).

## Graduation stage per row

Capital assets are not static—they **graduate through stages**. See [`../assets/ASSET_GRADUATION_SYSTEM.md`](../assets/ASSET_GRADUATION_SYSTEM.md) for the full stage definitions.

Each ledger row should note the asset's **current graduation stage**:

```text
Raw output
→ Reusable template
→ Standard asset
→ Productized asset
→ Market asset
```

A row is not "done" when the asset is created—it is tracked until the asset stops climbing. Note the stage in the `Next Use` column or as a parenthetical, e.g. `(Standard asset)`. An asset at **Market asset** stage is ready to hand to the distribution layer.

## Related

- [`../distribution/README.md`](../distribution/README.md) — distribution layer index.
- [`../distribution/CASE_STUDY_FACTORY.md`](../distribution/CASE_STUDY_FACTORY.md) — consumes Trust Assets that reach Market stage.
