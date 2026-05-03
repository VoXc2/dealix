# Frontend — Reality Matrix

> Source: `landing/` directory served via `python -m http.server 8081`,
> last verified 2026-05-03. All 25 actual pages return 200 locally.

## Matrix

| Page | Local exists | Status | Spec required | Notes |
| --- | --- | --- | --- | --- |
| `index.html` | yes | PROVEN_LOCAL | yes | landing |
| `pricing.html` | yes | PROVEN_LOCAL | yes | 5+ tiers |
| `trust-center.html` | yes | PROVEN_LOCAL | yes | safety + PDPL |
| `command-center.html` | yes | PROVEN_LOCAL | yes | role/decisions concept |
| `pulse.html` | yes | PROVEN_LOCAL | n/a | |
| `roi.html` | yes | PROVEN_LOCAL | n/a | |
| `partners.html` | yes | PROVEN_LOCAL | n/a | |
| `verticals.html` | yes | PROVEN_LOCAL | n/a | |
| `pay-per-result.html` | yes | PROVEN_LOCAL | n/a | |
| `dashboard.html` | yes | PROVEN_LOCAL | n/a | |
| `personal-operator.html` | yes | PROVEN_LOCAL | n/a | |
| `autopilot.html` | yes | PROVEN_LOCAL | n/a | |
| `simulator.html` | yes | PROVEN_LOCAL | n/a | |
| `trust.html` | yes | PROVEN_LOCAL | n/a | |
| `founder.html` | yes | PROVEN_LOCAL | n/a | |
| `marketers.html` | yes | PROVEN_LOCAL | n/a | |
| `community.html` | yes | PROVEN_LOCAL | n/a | |
| `academy.html` | yes | PROVEN_LOCAL | n/a | |
| `customer-portal.html` | yes | PROVEN_LOCAL | n/a | |
| `copilot.html` | yes | PROVEN_LOCAL | n/a | |
| `market-radar.html` | yes | PROVEN_LOCAL | n/a | |
| `launch-readiness.html` | yes | PROVEN_LOCAL | n/a | |
| `status.html` | yes | PROVEN_LOCAL | n/a | |
| `case-study.html` | yes | PROVEN_LOCAL | n/a | |
| `services.html` | **NO** | **MISSING_OR_EMPTY** | yes | spec wanted; functional equivalent is `/api/v1/services/catalog` |
| `operator.html` | **NO** | **MISSING_OR_EMPTY** | yes | spec wanted; functional equivalent is `/api/v1/operator/chat/message` (deploy branch) |
| `proof-pack.html` | **NO** | **MISSING_OR_EMPTY** | yes | spec wanted; functional equivalent is `/api/v1/business/proof-pack/demo` |
| `support.html` | **NO** | **MISSING_OR_EMPTY** | yes | functional equivalent is `/api/v1/support/*` |
| `onboarding.html` | **NO** | **MISSING_OR_EMPTY** | yes | functional equivalent is `personal-operator/launch-readiness` |
| `role/sales.html`, `role/growth.html`, `role/ceo.html` | **NO** | **MISSING_OR_EMPTY** | yes | functional equivalent is `/api/v1/role-briefs/daily?role=*` |
| `client.html`, `brain.html` | **NO** | **MISSING_OR_EMPTY** | optional | |

## Broken-link audit

The deploy-branch `services_catalog` returns `cta_path` values referencing
pages that DO NOT exist in this local repo:

- `private-beta.html` → not in `landing/`
- `agency-partner.html` → not in `landing/`
- `growth-os.html` → not in `landing/`
- `support.html#contact` → page missing

These pages MAY exist in the deploy-branch `landing/` (which has
`landing/README.md` and probably more pages). On this branch
they would 404.

**Action:** either copy missing pages from the deploy branch, or change
`cta_path` values to existing pages (`pricing.html`, `partners.html`,
`trust-center.html`).

## API base configuration

- Production frontend (GitHub Pages or static host) should point to
  `https://api.dealix.me`.
- Local dev should default to `http://127.0.0.1:8000`.
- `landing/script.js` should expose a single `DEALIX_API_BASE` constant
  that can be overridden via `window.DEALIX_API_BASE` before script load.
- This was NOT independently audited in this session — **CODE_EXISTS_NOT_PROVEN**.

## CTAs verified

- `index.html` → contains links to `pricing.html` (works).
- Operator interaction is API-only on the deploy branch; no in-page chat
  UI on this branch.
- Diagnostic CTA → `private-beta.html` (404 on this branch).

## Status

| Concern | Status |
| --- | --- |
| Pages serve 200 | 25/25 PROVEN_LOCAL |
| Spec-claimed pages missing | 6 MISSING_OR_EMPTY (do not block first-customer flow if API-only) |
| API base configurability | CODE_EXISTS_NOT_PROVEN |
| Arabic readable | PROVEN_LOCAL |
| Broken cta_path links from API catalog | BLOCKER for self-serve UX (not blocker for sales-led first customer) |
