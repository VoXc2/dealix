# Escalation — Readiness

## Maturity checklist

| Dimension | Relevance | Verified |
|-----------|-----------|----------|
| observable | supporting | ☐ |
| governable | core | ☐ |
| evolvable | supporting | ☐ |
| measurable | supporting | ☐ |
| orchestrated | supporting | ☐ |
| workflow_native | supporting | ☐ |
| enterprise_safe | core | ☐ |
| agent_ready | supporting | ☐ |
| transformation_ready | supporting | ☐ |
| continuously_improving | supporting | ☐ |

## How you know you have arrived

- [ ] Every implementing module listed in `architecture.md` exists and imports cleanly.
- [ ] `tests/` for this system pass in CI.
- [ ] Telemetry in `observability.md` is emitting in a live environment.
- [ ] `rollback.md` procedure has been dry-run at least once.
- [ ] KPIs in `metrics.md` have live values, not placeholders.
- [ ] `risk_model.md` risk tier is reviewed and accepted by an owner.

Until all boxes are checked, this system is **scaffolded**, not **verified**.
