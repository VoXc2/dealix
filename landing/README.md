# Dealix Frontend — Saudi Revenue Command Experience

Static HTML pages that make up the Dealix public website + product UI.

## Architecture

**Approach:** Static HTML with shared CSS + JS modules. No build pipeline.
We stay static until the first Proof Pack is shipped; Next.js migration
comes after.

**Why static:** SEO ✅, fast loading ✅, GitHub Pages compatible ✅,
Arabic-first works without bundler tooling.

## Layout

```
landing/
├── *.html                    25+ pages (homepage, services, command-center, etc.)
├── styles.css                Legacy v2 CSS — DO NOT modify lightly
├── script.js                 Legacy v2 JS — theme, posthog, demo form
├── posthog_snippet.html      Analytics loader
├── components/               (PR-FE-1) Shared HTML partials
│   ├── nav.html              Top navigation (loaded on every page)
│   └── footer.html           Footer (loaded on every page)
└── assets/                   (PR-FE-1) Modular CSS + JS
    ├── css/
    │   ├── base.css          Design tokens (navy/emerald/gold/amber/blue-trust)
    │   ├── components.css    Reusable UI (nav, footer, hero, bundle-card, ...)
    │   ├── cards.css         10 decision-card types
    │   └── responsive.css    Mobile / tablet / print / a11y helpers
    └── js/
        ├── api.js            Typed API client w/ fallback (DealixAPI global)
        ├── analytics.js      PostHog event taxonomy (DealixAnalytics global)
        └── components-loader.js   Injects components/*.html partials at runtime
```

## Page list

### PR-LAUNCH-FINAL (live wiring on top of design system)
- `proof-pack.html` reads from `/api/v1/proof-ledger/customer/{id}/pack`
  when `?customer_id=X` is in the URL. Falls back to demo otherwise.
- `command-center.html` shows live `Daily Ops history` + `Cost summary` +
  `Unsafe-actions blocked` widgets via `assets/js/command-center-widgets.js`.

### PR-FE-1 (new pages, full ops scaffolding)
- `companies.html` — للشركات
- `services.html` — Service Tower (5 bundles only)
- `private-beta.html` — Pilot 499 sales page
- `growth-os.html` — Executive Growth OS subscription
- `agency-partner.html` — Agency Partner Portal landing (demo data)
- `operator.html` — Dealix AI Operator (intent → service)
- `targeting.html` — Targeting OS (safe sources)
- `proof-pack.html` — Proof Pack sample (trust converter)
- `support.html` — Tier-1 Support (SLA + bot + ticket)

### Existing (refresh deferred to PR-FE-5/6)
- `index.html`, `command-center.html`, `pricing.html`, `marketers.html`,
  `partners.html`, `trust-center.html`, `trust.html`, `dashboard.html`,
  `market-radar.html`, `simulator.html`, `roi.html`, `case-study.html`,
  `pay-per-result.html`, `customer-portal.html`, `personal-operator.html`,
  `academy.html`, `community.html`, `verticals.html`, `pulse.html`,
  `status.html`, `founder.html`, `launch-readiness.html`

## How to add a new page

1. Copy any of the PR-FE-1 pages as a starting point.
2. Set the `<title>`, `<meta name="description">`, `<link rel="canonical">`,
   and OG tags.
3. Add `<div data-include="components/nav.html"></div>` at the top of `<body>`.
4. Add `<div data-include="components/footer.html"></div>` before the closing
   `</body>`.
5. Import the new CSS modules:
   ```html
   <link rel="stylesheet" href="styles.css">
   <link rel="stylesheet" href="assets/css/base.css">
   <link rel="stylesheet" href="assets/css/components.css">
   <link rel="stylesheet" href="assets/css/cards.css">
   <link rel="stylesheet" href="assets/css/responsive.css">
   ```
6. Import the JS modules at the end of `<body>`:
   ```html
   <script src="assets/js/api.js"></script>
   <script src="assets/js/analytics.js"></script>
   <script src="assets/js/components-loader.js"></script>
   <script>
     if (window.DealixAnalytics) DealixAnalytics.pageView('your-page');
   </script>
   ```
7. Add the file to `IN_SCOPE_FILES` in
   `scripts/forbidden_claims_audit.py`.
8. Add a link to the new page in `components/nav.html` and `components/footer.html`.

## Forbidden marketing claims (enforced by CI)

The `scripts/forbidden_claims_audit.py` blocks any page that contains the
following without an adjacent negative-context marker (لا / ✗ / forbidden / ...):

- نضمن / guaranteed
- scrape / scraping / نسحب البيانات
- auto-dm / auto dm / رسائل آلية
- cold whatsapp / واتساب بارد
- إرسال جماعي / mass send
- 100% automation / أتمتة كاملة

If you must mention one of these (e.g., "Dealix لا يستخدم scraping"),
ensure the line also contains a negative marker.

## Required per page

Every audited page must include:
- `<html lang="ar" dir="rtl">`
- `<meta name="description">` and `<link rel="canonical">`
- A link to `support.html` (or be the support page)
- A link to `trust-center.html` or `trust.html` (or be a trust page)
- A "Pilot" or "Diagnostic" CTA

Both shared partials (`nav.html` + `footer.html`) already satisfy the
support/trust link requirements.

## Local preview

```bash
cd landing
python -m http.server 8080
# open http://localhost:8080/index.html
```

The `data-include` partials require fetch to work, so always serve via
HTTP — not file://.

## Backend integration

API base URL is auto-detected:
1. `window.DEALIX_API_BASE_URL` (set inline)
2. `localStorage('dealix_api_base')`
3. `window.DEALIX_API_BASE` (legacy)
4. `https://api.dealix.me` (production)
5. `http://localhost:8000` (when on localhost)

When the API is unreachable, pages SHOULD render demo data inside a
`.dx-demo-banner` so the UX never breaks.

## Related plans

The Frontend Product System plan lives at
`/root/.claude/plans/eager-plotting-quiche.md` and covers PRs FE-1 → FE-6.

## Verification

```bash
# Architecture audit
python scripts/repo_architecture_audit.py

# Forbidden claims (frontend)
python scripts/forbidden_claims_audit.py

# Full launch readiness
python scripts/launch_readiness_check.py

# Architecture tests
pytest tests/architecture/ -q --no-cov
```
