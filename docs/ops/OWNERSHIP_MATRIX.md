# Dealix Ownership Matrix

This matrix defines default ownership for repository areas. Replace individual ownership with GitHub teams as the organization grows.

| Area | Path | Primary owner | Review focus |
|---|---|---|---|
| Repository governance | `.github/`, `Makefile`, `.env.example` | @VoXc2 | CI, security gates, environment contract, review workflow |
| Backend API | `api/`, `core/`, `db/` | @VoXc2 | Route behavior, data access, auth boundaries, OpenAPI contract |
| Agents and growth engine | `auto_client_acquisition/`, `autonomous_growth/` | @VoXc2 | Approval classes, deterministic execution, provider fallback, evidence |
| Integrations | `integrations/` | @VoXc2 | Credentials, retries, webhooks, idempotency, external API risk |
| Trust and compliance | `dealix/registers/`, `dealix/masters/` | @VoXc2 | PDPL posture, no-overclaim evidence, approval policy, auditability |
| Frontend | `apps/web/`, `landing/` | @VoXc2 | Public claims, API usage, browser-exposed variables, UX flows |
| Operations docs | `docs/ops/` | @VoXc2 | Launch readiness, incident response, release process, smoke tests |
| Architecture docs | `docs/architecture/` | @VoXc2 | System design, API policy, ADRs, gap audit |
| Scripts | `scripts/` | @VoXc2 | Safe defaults, idempotency, dependency footprint, production impact |

## Review rules

- Production-facing changes should update `CHANGELOG.md`.
- API changes should follow `docs/architecture/API_CONTRACT_POLICY.md`.
- Launch-facing changes should be checked against `docs/ops/PRODUCTION_READINESS_CHECKLIST.md`.
- Public claim changes should update or verify `dealix/registers/no_overclaim.yaml`.
- Spreadsheet/planning items should be reflected in `docs/ops/EXECUTION_BACKLOG.md`.

## Arabic summary

هذا الملف يوضح من يراجع كل جزء من الريبو وما الذي يجب التركيز عليه في المراجعة. الهدف تقليل التداخل وضمان أن كل تغيير إنتاجي له مالك واضح.
