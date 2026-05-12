# Vendor cost sheet — what to pay first

> For every env var in `.env.example`, this sheet lists: the vendor
> URL, the *minimum* monthly cost at pilot scale (1–5 paying customers),
> the cost at scale-to-50, and whether the feature ships inert without
> the key. Use this to decide what to wire up *before* you take your
> first paying customer.

Legend:
- **Pilot** = 1–5 paying customers, < SAR 50k MRR.
- **Scale** = 50 paying customers, SAR 250k–500k MRR.
- **Inert?** = does the feature still work without this key? "Yes" means
  the platform degrades gracefully; "No" means the feature is broken
  without it.

## Critical for first revenue (wire these in week 1)

| Env var | Vendor | Pilot $/mo | Scale $/mo | Inert? |
| --- | --- | --- | --- | --- |
| `MOYASAR_SECRET_KEY` | https://moyasar.com | 0 (per-tx fee 2.5% + 1 SAR) | same | Yes — manual bank-transfer fallback |
| `ANTHROPIC_API_KEY` | https://anthropic.com | $30 | $400 | Yes — handlers degrade to deterministic rules |
| `RESEND_API_KEY` | https://resend.com | $0 (3k emails free) | $20 (50k emails) | Yes — SMTP / SendGrid fallback |
| `JWT_SECRET_KEY` | self-managed | — | — | No — auth needs a secret |
| `DATABASE_URL` | RDS / Neon / Supabase | $25 (small Postgres) | $200 (medium + replica) | No — required |
| `REDIS_URL` | Upstash / Railway | $0 (free tier) | $25 | Yes — degrades to in-process counters |
| `APP_URL` | your domain | — | — | No — emails need this to build links |

**Week-1 minimum:** ~$55/month, plus the per-transaction Moyasar fee.

## Trust gates (wire these before signing your first enterprise)

| Env var | Vendor | Pilot $/mo | Scale $/mo | Inert? |
| --- | --- | --- | --- | --- |
| `SENTRY_DSN` | https://sentry.io | $0 (free tier) | $26 (Team) | Yes |
| `WORKOS_API_KEY` + `WORKOS_CLIENT_ID` | https://workos.com | $0 (first 1M users free for SSO) | $0 | Yes — manual user invite path |
| `POSTHOG_API_KEY` | https://posthog.com | $0 (1M events free) | $0–450 | Yes |
| `BETTERSTACK_HEARTBEAT_URL` | https://betterstack.com | $0 (free tier) | $24 | Yes — falls back to internal /api/v1/status |
| `KNOCK_API_KEY` | https://knock.app | $0 (1k recipients free) | $99 | Yes — falls back to Resend |
| `PLAIN_API_KEY` | https://plain.com | $0 (free tier) | $79 | Yes — falls back to Resend |

**Trust-gate add:** ~$80/month at pilot scale. Enables SSO, error
tracking, multi-channel notifications, support ticketing.

## LLM cost binding (wire when you cross 10 paying customers)

| Env var | Vendor | Pilot $/mo | Scale $/mo | Inert? |
| --- | --- | --- | --- | --- |
| `PORTKEY_API_KEY` | https://portkey.ai | $0 (10k requests free) | $99 | Yes — direct SDK route |
| `LANGFUSE_PUBLIC_KEY` + `LANGFUSE_SECRET_KEY` | https://langfuse.com | $0 (50k traces free) | $59 | Yes — local logs |
| `LAGO_API_KEY` | https://getlago.com | $0 (self-host) | $0–$200 | Yes — no metering without it |

## Saudi-government APIs (wire only when a paying customer asks)

These all require a Saudi licence / partner agreement. Don't pay
for any of them until you have a customer using the feature.

| Env var | Vendor | Issuance time | Cost | Inert? |
| --- | --- | --- | --- | --- |
| `WATHQ_API_KEY` | https://wathq.sa | 1–4 weeks (Saudi Business Center) | per-call | Yes |
| `ETIMAD_API_KEY` | https://etimad.sa | months (partner agreement) | tiered | Yes |
| `MAROOF_API_KEY` | https://maroof.sa | weeks | tiered | Yes |
| `NAJIZ_API_KEY` | https://najiz.sa | partner-only | per-call | Yes |
| `TADAWUL_API_KEY` | https://saudiexchange.sa | data-feed contract | tiered | Yes |
| `MISA_API_KEY` | https://misa.gov.sa | restricted partner | per-call | Yes |
| `NAFATH_API_KEY` | https://nafath.sa | SDAIA-issued | volume-tiered | Yes |
| `YAKEEN_API_KEY` | https://yakeen.elm.sa | restricted | per-call | Yes |

## International / GCC payments (wire as you expand)

| Env var | Vendor | Pilot $/mo | Scale $/mo | Inert? |
| --- | --- | --- | --- | --- |
| `STRIPE_API_KEY` | https://stripe.com | per-tx (2.9% + $0.30) | same | Yes |
| `KNET_TRANPORTAL_ID` + `KNET_RESOURCE_KEY` | KNET (Kuwait) | merchant agreement | per-tx | Yes |
| `BENEFIT_API_KEY` | BENEFIT (Bahrain) | merchant agreement | per-tx | Yes |
| `MAGNATI_API_KEY` | Magnati (UAE) | merchant agreement | per-tx | Yes |
| `TABBY_API_KEY` | https://tabby.ai | merchant agreement | per-tx | Yes |
| `TAMARA_API_KEY` | https://tamara.co | merchant agreement | per-tx | Yes |
| `TAP_API_KEY` | https://tap.company | merchant agreement | per-tx | Yes |

## Advanced AI (wire after first 5 paying customers)

| Env var | Vendor | Pilot $/mo | Scale $/mo | Inert? |
| --- | --- | --- | --- | --- |
| `OPENAI_API_KEY` | https://platform.openai.com | $20 | $300 | Yes |
| `VOYAGE_API_KEY` | https://voyageai.com | $0 (50M tokens free) | $50 | Yes |
| `COHERE_API_KEY` | https://cohere.com | $0 (rate-limited free) | $100 | Yes |
| `LAKERA_API_KEY` | https://lakera.ai | $0 (free trial) | $99+ | Yes |
| `LETTA_URL` | https://letta.com | $0 (self-host) | $0+ | Yes |

## Founder rule

**Don't pay for a vendor before a paying customer needs it.** The
inert-by-default design means every feature degrades gracefully —
ship the trial flow first, then turn on keys one by one as customers
ask for the capability they back.

Week-1 spend to launch: **< $100/month** (Moyasar + Anthropic +
Resend + Postgres + Redis).
