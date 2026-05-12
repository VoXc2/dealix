# PostHog — Event Schema & Funnel Setup

> Single source of truth for analytics events. Any new event must be added here **first**, then implemented.

## Account
- URL: https://app.posthog.com (US cloud) — confirmed for performance reasons; PII is minimised so cross-border is acceptable per PDPL with proper consent.
- Owner: founder
- Plan: Free (1M events/mo)

## Env Vars
```env
POSTHOG_API_KEY=phc_xxxxx
POSTHOG_HOST=https://us.i.posthog.com
```

Backend client: `api/deps.py::get_posthog_client()`.
Frontend snippet: `landing/posthog_snippet.html` (include on every page).

## Identification rules
- **Anonymous browse** → use auto-generated distinct_id (PostHog default)
- **Submitted demo form** → `posthog.identify(email_hash, { company, role })`
  - **Never** send raw email as distinct_id — use SHA-256 hex of lowercased email
- **Paying customer** → `posthog.identify(customer_id, { plan, signed_at })`

## Core funnel events

Names are **snake_case**, properties are JSON. Every event has `$insert_id` set server-side to allow idempotent replay.

### Landing & top-of-funnel
| Event | When | Properties |
|-------|------|------------|
| `page_view` | client auto | `path`, `referrer`, `utm_*` |
| `pricing_viewed` | landing/pricing.html load | `plan_visible[]` |
| `cta_clicked` | any CTA button | `cta_id`, `page` |
| `diagnostic_started` | diagnostic.html step 1 | `sector` |
| `diagnostic_completed` | diagnostic.html final step | `sector`, `score`, `archetype` |

### Demo & qualification
| Event | When | Properties |
|-------|------|------------|
| `demo_request_submitted` | server: POST /api/v1/public/demo-request returns 200 | `company_size`, `sector`, `source` |
| `demo_request_failed` | server: same endpoint returns 4xx/5xx | `reason` |
| `calendly_booked` | calendly webhook → /api/v1/webhooks/calendly | `slot_at`, `meeting_type` |

### Checkout (payments funnel)
| Event | When | Properties |
|-------|------|------------|
| `checkout_started` | client: pricing.html plan click | `plan`, `amount_sar` |
| `checkout_session_created` | server: POST /api/v1/checkout returns 200 | `plan`, `payment_id` |
| `checkout_redirected_to_moyasar` | client: window.location → moyasar | `payment_id` |
| `checkout_success` | server: webhook payment_paid → DB row | `plan`, `amount_sar`, `customer_id` |
| `checkout_failed` | server: webhook payment_failed | `plan`, `reason` |
| `checkout_refunded` | server: webhook payment_refunded | `plan`, `amount_sar` |

### Product usage (post-paid)
| Event | When | Properties |
|-------|------|------------|
| `dashboard_login` | server: successful /auth/login | `role` |
| `lead_imported` | server: import_leads.py | `count`, `source_type` |
| `lead_scored` | server: scoring pipeline | `priority`, `quality` |
| `approval_requested` | server: any A1/A2/A3 class output | `class`, `module` |
| `approval_decided` | server: human approval submitted | `decision`, `latency_sec` |

### Reliability
| Event | When | Properties |
|-------|------|------------|
| `webhook_received` | any /webhooks/* hit | `source`, `signature_valid` |
| `webhook_dlq_pushed` | dlq.push() | `queue`, `attempts`, `error_class` |
| `retention_job_completed` | scheduled job | `job`, `deleted_count` |
| `backup_completed` | hourly_backup.sh | `size_bytes`, `s3_uploaded` |

## Funnels to build (in PostHog UI)

### Funnel A — Landing → Pilot ($1)
1. `page_view (path=/)`
2. `pricing_viewed`
3. `checkout_started (plan=pilot_1sar)`
4. `checkout_session_created`
5. `checkout_success (plan=pilot_1sar)`

Target conversion: ≥ 2% landing → pilot

### Funnel B — Pilot → Paid plan
1. `checkout_success (plan=pilot_1sar)`
2. `dashboard_login`
3. `checkout_success (plan IN [starter, growth, scale])`

Target conversion: ≥ 25% pilot → paid within 14 days

### Funnel C — Demo → Calendly → Pilot
1. `demo_request_submitted`
2. `calendly_booked`
3. `checkout_success`

## Cohorts to build

- **Saudi enterprises** — `country == 'SA'` AND `company_size in ['51-200', '200+']`
- **Hot pilots** — submitted demo AND booked Calendly within 24h
- **At-risk paid** — `dashboard_login` not seen in 14 days

## Dashboards to pin

1. **Acquisition** — landing visits, source breakdown, top UTM combos
2. **Conversion** — Funnel A + B side-by-side
3. **Reliability** — webhook_dlq_pushed rate, error rate vs Sentry
4. **Revenue** — checkout_success count + sum(amount_sar) over time

## PII rules
- Never send raw `email`, `phone`, `national_id`, `card_*`
- Always hash: `sha256(email.lower())`
- IP capture: off (set `disable_session_recording=true`, `ip=None` server side)
- Geo: only country-level

## Schema enforcement
Add to CI: `tests/test_posthog_schema.py` parses this file and verifies every `posthog.capture(event=...)` in code matches a row above. Any new event without a doc entry fails CI.
