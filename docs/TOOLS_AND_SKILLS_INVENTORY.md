# Tools & Skills Inventory

> Verified what's actually shipped and reachable.

## Core tools (this branch)

| Tool | Purpose | Required env | Safe mode | Live mode | Status | Test command |
| --- | --- | --- | --- | --- | --- | --- |
| `python -m uvicorn api.main:app` | run API locally | APP_ENV, APP_SECRET_KEY, DATABASE_URL | sandbox sqlite | Postgres prod | PROVEN_LOCAL | `python -m uvicorn api.main:app --port 8000` |
| `python -m pytest` | unit + integration tests | APP_ENV=test | always safe | n/a | PROVEN_LOCAL (516 pass) | `python -m pytest -q --no-cov` |
| `scripts/print_routes.py` | OpenAPI route dump | none | always safe | n/a | PROVEN_LOCAL (260 routes) | `python scripts/print_routes.py` |
| `scripts/smoke_inprocess.py` | ASGI in-process smoke | APP_ENV=test | always safe | n/a | PROVEN_LOCAL (6/6 200) | `python scripts/smoke_inprocess.py` |
| `scripts/smoke_local_api.py` | smoke a local server | port set | always safe | n/a | available | run after uvicorn |
| `scripts/staging_smoke.sh` | smoke a remote URL | BASE_URL | always safe | safe | PROVEN_LIVE (22/22 on prod) | `BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh` |
| `scripts/run_demo.py` | end-to-end pipeline demo | none | always safe | n/a | PROVEN_LOCAL | `python scripts/run_demo.py` |
| `scripts/seed_data.py` | seed demo records | DATABASE_URL | demo namespace | n/a | CODE_EXISTS_NOT_PROVEN | careful — review before running on prod |
| `scripts/seed_demo_data.py` | richer seed | DATABASE_URL | demo namespace | n/a | CODE_EXISTS_NOT_PROVEN | same |
| `scripts/seed_production_db.py` | named for prod | DATABASE_URL | uses real prod URL | dangerous if pointed at live DB | exists but **DO NOT run blindly** | inspect file before use |
| `scripts/smoke_test.sh` | bash smoke against domain | DOMAIN arg | always safe | safe | PROVEN_LOCAL | `bash scripts/smoke_test.sh dealix.me` |
| `scripts/smoke_staging.py` | python smoke (staging) | BASE_URL | always safe | safe | available | n/a |

## Tools claimed by spec but NOT in repo

| Tool | Reality | Substitute |
| --- | --- | --- |
| `scripts/full_acceptance.sh` | MISSING_OR_EMPTY | `python -m pytest` + `bash scripts/staging_smoke.sh` together cover the intent |
| `scripts/launch_readiness_check.py` | MISSING_OR_EMPTY | `GET /api/v1/personal-operator/launch-readiness` (live endpoint) |
| `scripts/repo_architecture_audit.py` | MISSING_OR_EMPTY | n/a |
| `scripts/forbidden_claims_audit.py` | MISSING_OR_EMPTY | grep `core/prompts/` for forbidden tokens manually |
| `dealix first-customer-flow` CLI | MISSING_OR_EMPTY | the curl chain in `FIRST_CUSTOMER_REALITY_REPORT.md` |
| `dealix invoice 499 cus_demo` CLI | MISSING_OR_EMPTY | `POST /api/v1/payments/manual-request` |

CLI exists at top-level `cli.py` (`ai-company` console script) and supports
demo + acceptance modes — but does NOT have `first-customer-flow` or
`invoice` subcommands.

## Business tools (deploy branch — verified live)

| Tool | Endpoint | Status |
| --- | --- | --- |
| Mini Diagnostic | `POST /api/v1/operator/service/start {bundle_id:"free_diagnostic"}` | PROVEN_LIVE |
| Service recommender | `POST /api/v1/operator/chat/message` (10/14 tests) | PROVEN_LIVE w/ 4 misses |
| Role brief generator | `GET /api/v1/role-briefs/daily?role=*` (5/8 roles work) | PARTIAL — sales_manager BLOCKER |
| Proof Pack generator | `POST /api/v1/customers/{id}/proof-pack`, `POST /api/v1/command-center/proof-pack`, `GET /api/v1/proof-ledger/{customer,partner,session}/.../pack` | PROVEN_LIVE |
| Invoice / manual fallback | `POST /api/v1/payments/manual-request` | PROVEN_LOCAL |
| Prospect stage machine | `POST /api/v1/leads`, `POST /api/v1/deals`, `PATCH /api/v1/deals/{id}` | PROVEN_LOCAL |
| Customer brain (composite) | several routers — see COMPANY_BRAIN_SPEC_AND_STATUS.md | PROVEN_LIVE (parts) |
| Support bot | `POST /api/v1/support/classify`, `GET /api/v1/support/sla` | PROVEN_LIVE |
| WhatsApp brief preview | `GET /api/v1/whatsapp/brief?role=*` | partial (3/8 BLOCKER) |
| Compliance gate | `POST /api/v1/compliance/check-outreach`, `…/campaign-risk`, `…/contactability` | campaign-risk live; check-outreach BLOCKER on prod |

## External integrations

| Integration | Purpose | Required env | Default mode | Live mode | Status |
| --- | --- | --- | --- | --- | --- |
| Moyasar | hosted invoices | `MOYASAR_SECRET_KEY`, `MOYASAR_WEBHOOK_SECRET` | not configured → manual bank-transfer fallback | live charge after secret | PROVEN_LIVE (webhook 401), PROVEN_LOCAL (manual fallback) |
| Meta WhatsApp Cloud | inbound webhook + (gated) outbound | `WHATSAPP_VERIFY_TOKEN`, `WHATSAPP_APP_SECRET`, `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_ALLOW_LIVE_SEND` | inbound only; outbound BLOCKED | live send after explicit gate flip | PROVEN_LIVE (gate enforced) |
| Gmail | drafts only by default | `GMAIL_CLIENT_ID`, `GMAIL_REFRESH_TOKEN`, `GMAIL_SENDER_EMAIL` | not configured → blocked | drafts after OAuth | PROVEN_LIVE (blocked) |
| Google Search | enrichment | `GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_CX` | absent → fallback | live | PROVEN_LIVE (fallback works) |
| LLM providers (Groq / Anthropic / OpenAI) | reasoning | one of the keys | absent → rule-based fallback | live with key | PROVEN_LIVE (groq active on prod) |
| Railway | hosting | platform | always live | live | PROVEN_LIVE |
| GitHub Pages | landing | platform | always live | live | not directly probed here |

## PDF / Proof libraries

| Lib | Used for | Required | Status |
| --- | --- | --- | --- |
| `jinja2` | template rendering | declared in deps tree (transitively via fastapi) | available |
| `reportlab` / `weasyprint` | PDF rendering | NOT in `requirements.txt` | MISSING_OR_EMPTY → proof packs are Markdown today |
| stdlib `hmac` + `hashlib` | signing | always available | available — but proof-pack response does not currently include the HMAC signature (see Service Tower §gap 2) |

## Skills the system actually has, verified

- Detect Arabic/English in text (rule-based)
- Classify intent into `want_more_customers`, `has_list`,
  `cold_whatsapp_request`, `want_partnerships` (deploy branch)
- Score lead fit (ICP)
- Suggest service bundle
- Generate Khaliji Arabic message drafts
- Block live external action by default
- Run a full prospect → cash → proof-pack flow without external send

## Skills the system does NOT yet have (BACKLOG)

- HMAC-signed proof PDFs
- Multi-turn intake form on operator chat (currently single-shot)
- Saudi-Arabic-aware cold-WhatsApp purchased-list intent classifier (3 fails)
- `first-customer-flow` CLI alias
