# Dealix Dependency Strategy

This document explains which libraries are worth adding and when. The goal is to increase reliability, observability, security, and revenue impact without bloating production or breaking deploys.

## Principle

Do not add a dependency just because it is useful in general. Add it only when it directly improves one of these:

- Production reliability.
- Security or supply-chain visibility.
- Revenue conversion or sales operations.
- Compliance evidence or auditability.
- Developer speed without production risk.

## Recommended optional dependency groups

### Observability

Add when production traffic is active and errors/costs need better traceability.

Recommended libraries:

- `sentry-sdk[fastapi]` for error capture.
- `opentelemetry-api`, `opentelemetry-sdk` for traces.
- `opentelemetry-instrumentation-fastapi` for FastAPI instrumentation.
- `opentelemetry-instrumentation-httpx` for outbound HTTP calls.
- `opentelemetry-instrumentation-sqlalchemy` for database spans.
- `prometheus-client` for metrics export.

### Security and supply chain

Add to CI/dev environments first, not runtime containers unless needed.

Recommended libraries/tools:

- `pip-audit` for dependency vulnerability checks.
- `cyclonedx-bom` for SBOM export.
- `detect-secrets` for secret scanning baseline.
- `bandit[toml]` for Python static security checks.

### Evals and quality

Add when measuring AI output quality, matching, scoring, and regression behavior.

Recommended libraries:

- `jsonschema` for structured output validation.
- `rapidfuzz` for Arabic/English fuzzy matching.
- `scikit-learn` for scoring/evaluation baselines.
- `pandas` for offline analysis and reporting.

### Documentation

Add when publishing internal or public documentation as a site.

Recommended libraries:

- `mkdocs`
- `mkdocs-material`

## Current recommendation

Keep core production dependencies lean. Add optional groups incrementally through PRs after CI is green and the live domain is stable.

Suggested order:

1. Security/dev tooling.
2. Observability.
3. Evals.
4. Docs site.

## Acceptance criteria before adding a dependency

- [ ] It has a clear owner.
- [ ] It has a clear runtime or dev-only scope.
- [ ] It has a direct value case.
- [ ] It does not duplicate an existing library.
- [ ] It is covered by dependency review or inventory.
- [ ] It does not expose credentials or personal data.

## Arabic summary

لا تضف مكتبات عشوائية. أضفها فقط إذا حسنت الإنتاج، الأمن، الإيرادات، الامتثال، أو سرعة التطوير. الأفضل فصلها كمجموعات اختيارية: observability، security، evals، docs.
