# MVP APIs (Target Shape)

REST-style targets for the core spine (paths may be prefixed under `/api/v1` in product).

```text
POST /data/import-preview
POST /data/quality-score
POST /governance/check
POST /revenue/score-accounts
POST /revenue/draft-pack
POST /reporting/proof-pack
POST /delivery/qa-score
POST /capital/assets
GET  /founder/command-center
```

## Principle

Every response should support:

```text
result
risk_status
governance_status
audit_event_id (when persisted)
next_action
```

See [`MANAGEMENT_API_SPEC.md`](MANAGEMENT_API_SPEC.md).
