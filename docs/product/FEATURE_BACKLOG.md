# Feature Backlog

Rolling table from **delivery pain** → **build decision**. Deep log: [`../company/FEATURE_CANDIDATE_LOG.md`](../company/FEATURE_CANDIDATE_LOG.md).

## Backlog

| Feature | Source project | Service | Repeated? | Value | Risk reduction | Score | Decision |
|---------|----------------|---------|-----------|-------|----------------|------:|----------|
| Import preview | Lead Sprint · synthetic | Lead Intelligence | Yes | High | High | 92 | Build |
| Report section generator | Lead Sprint · client A | All | Yes | High | Medium | 88 | Build |
| WhatsApp auto-send | Client request X | Revenue | No | Med | Low | 30 | Do not build |

**Decision values:** Build / Backlog / Do not build / Template only / Script only.

Prioritization math: [`BUILD_DECISION.md`](BUILD_DECISION.md), [`FEATURE_PRIORITIZATION.md`](FEATURE_PRIORITIZATION.md).

## Rule

Every row needs **source project** or **ticket ID**—no orphan “nice ideas.”
