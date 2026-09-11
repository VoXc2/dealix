# Dealix Open-Source Adoption Registry V1

Purpose: use open-source components only when they strengthen the canonical Company Machine. Do not create parallel CRM, scheduler, Company Brain, approval authority, or proof systems.

| Project | Role | Decision | Integration boundary |
|---|---|---|---|
| PostHog | product/web analytics, funnels, experiments | ADOPT_EXISTING | `posthog-js` already exists in `apps/web`. Prefer the current SDK/cloud-free-tier path initially; PostHog explicitly describes self-hosting as an advanced/hobby deployment with extra operational burden. |
| Sentry | error/performance telemetry | ADOPT_EXISTING_SDK_ONLY | Already in `apps/web`; keep SDK optional by env and correlate release SHA. Self-hosted Sentry is FSL-1.1-Apache-2.0, so do not treat the server as unrestricted OSS. |
| OpenTelemetry | vendor-neutral traces/metrics/logs | ADOPT_INCREMENTALLY | Use as observability transport across API/agents; do not replace business Proof Ledger. |
| Lighthouse CI | performance/SEO/accessibility regression | ADOPT_DEV_TOOL | Run against canary/public URLs as a release-quality gate; never infer release identity from Lighthouse success. |
| Pa11y | accessibility regression | ADOPT_DEV_TOOL | Public conversion pages only; fail on material WCAG regressions after baseline tuning. |
| Lychee | broken-link checker | ADOPT_DEV_TOOL | Crawl owned public docs/site links in verification jobs. |
| Uptime Kuma | self-hosted uptime/status probes | ADOPT_VPS_OPTIONAL | Monitor public endpoints and self-host canaries; uptime is not Production Green. |
| React Email | transactional/permissioned email templates | ADOPT_WHEN_EMAIL_SURFACE_MOVES | Template layer only; send remains action-bound. |
| listmonk | newsletters/permissioned lists | HOLD | Useful only after consent/list-management requirements exist; never use for cold blasting. |
| Umami | analytics | DO_NOT_DUPLICATE | PostHog already owns conversion analytics. |
| GrowthBook | experiments/feature flags | HOLD | PostHog can cover current experiment needs; avoid duplicate control plane. |
| Formbricks | surveys | HOLD | Adopt only after a real survey/NPS workflow justifies another service. |

## Admission rule

Before adding any repository/service: verify license, maintenance activity, security posture, data boundary, resource cost, canonical owner, rollback, and whether an existing Dealix component already owns the capability. New software is not progress by itself.

