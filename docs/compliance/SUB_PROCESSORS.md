# Sub-processors — canonical list

This file is the **source of truth** for every entity that processes
Personal Data on Dealix's behalf. Adding a row triggers a 30-day
customer notification per `docs/legal/DPA.md` §9.

Last updated: 2026-05-12.

## Active sub-processors

| Sub-processor | Purpose | Country | Effective date | Status |
| --- | --- | --- | --- | --- |
| Railway | Application hosting | USA | 2026-04-23 | Active |
| Supabase | Postgres + RLS-protected docs | EU / USA | 2026-04-23 | Active |
| Anthropic | LLM inference (primary) | USA | 2026-04-23 | Active |
| OpenAI | LLM inference (fallback) | USA | 2026-04-23 | Active |
| Google (Gemini, Maps) | Optional LLM + place lookups | USA | 2026-04-23 | Active |
| Groq | Optional cheap LLM fallback | USA | 2026-04-23 | Active |
| Sentry | Error monitoring | USA | 2026-04-23 | Active |
| Resend | Transactional email | USA | 2026-04-23 | Active |
| Plain | Customer support tickets | UK | 2026-05-12 | Active |
| Knock | Multi-channel notifications | USA | 2026-05-12 | Active |
| BetterStack | Status page + heartbeats | EU | 2026-05-12 | Active |
| Portkey | LLM gateway + cost dashboard | USA | 2026-05-12 | Active |
| Tinybird | Embedded analytics (optional) | EU | 2026-05-12 | Active |
| Stripe | International card payments | USA | 2026-05-12 | Active |
| Moyasar | Saudi card payments | KSA | 2026-04-23 | Active |
| HubSpot | CRM integration (per-customer) | USA | 2026-04-23 | Active |
| Calendly | Public booking link | USA | 2026-04-23 | Active |
| Meta (WhatsApp Business Cloud) | Outbound + inbound messaging | USA / EU | 2026-04-23 | Active |
| Apollo.io | Lead enrichment (optional) | USA | 2026-05-12 | Active |
| Clearbit | Lead enrichment (optional) | USA | 2026-05-12 | Active |
| Wathq | Saudi commercial registry | KSA | 2026-05-12 | Active |
| WorkOS | Enterprise SSO (per-tenant) | USA | 2026-05-12 | Active |
| Lago | Usage metering (optional) | EU | 2026-05-12 | Active |
| Loops | Marketing automation (optional) | USA | 2026-05-12 | Active |
| Infisical | Secrets vault (optional) | USA | 2026-05-12 | Active |
| Inngest | Durable workflows (optional) | USA | 2026-05-12 | Active |
| Langfuse | LLM observability | EU | 2026-04-23 | Active |
| PagerDuty | On-call + incident comms | USA | 2026-05-12 | Active |
| PostHog | Product analytics + flags + surveys | USA | 2026-04-23 | Active |
| Voyage AI | Multilingual embeddings (RAG) | USA | 2026-05-22 | Active (optional) |
| Cohere | Multilingual embeddings + rerank (RAG) | Canada | 2026-05-22 | Active (optional) |
| Deepgram | Speech-to-text (voice) | USA | 2026-05-22 | Active (optional) |
| AssemblyAI | Speech-to-text fallback | USA | 2026-05-22 | Active (optional) |
| ElevenLabs | Text-to-speech (Arabic Khaliji) | USA | 2026-05-22 | Active (optional) |
| Cartesia | Text-to-speech fallback | USA | 2026-05-22 | Active (optional) |
| Vapi | Voice agent orchestration (SIP) | USA | 2026-05-22 | Active (optional) |
| Unifonic | Saudi SIP + SMS carrier | KSA | 2026-05-22 | Active (optional) |
| Nafath / Absher | Saudi national identity authentication | KSA | upon licence | Pending regulator |
| Yakeen (Elm) | Saudi identity verification | KSA | upon licence | Pending regulator |
| Tap Payments | Pan-GCC card payments | Kuwait | 2026-05-22 | Active (optional) |
| Tabby | BNPL (Saudi/UAE/Kuwait) | UAE | 2026-05-22 | Active (optional) |
| Tamara | BNPL (Saudi/UAE) | KSA | 2026-05-22 | Active (optional) |
| Salla | Saudi e-commerce orders sync | KSA | 2026-05-22 | Active (optional) |
| Zid | Saudi e-commerce orders sync | KSA | 2026-05-22 | Active (optional) |
| SAMA Open Banking | Account-information services | KSA | upon licence | Pending regulator |
| HyperDX | OTLP-native observability | USA | 2026-05-22 | Active (optional) |
| Highlight.io | Session replay | USA | 2026-05-22 | Active (optional) |
| Meilisearch | In-app full-text search | France | 2026-05-22 | Active (optional) |
| Memgraph | Knowledge graph (relationship modelling) | UK | 2026-05-22 | Active (optional) |
| Snyk | Daily vulnerability + container scan | Israel | 2026-05-22 | Active (optional) |
| Cloudflare Turnstile | Bot protection on public forms | USA | 2026-05-22 | Active (optional) |
| Lakera Guard | Prompt-injection defence (T6b) | Switzerland | 2026-06-11 | Active (optional) |
| Letta | Long-term agent memory store (T6b) | USA | 2026-06-11 | Active (optional) |
| Browserbase | Hosted browser runtime for Browser-Use / Computer Use (T6b) | USA | 2026-06-11 | Active (optional) |
| Etimad | Saudi government procurement portal (T6f) | KSA | 2026-06-11 | Active (optional) |
| Maroof | Saudi consumer-reputation directory (T6f) | KSA | 2026-06-11 | Active (optional) |
| Najiz | Saudi judicial commercial-risk snapshot (T6f) | KSA | 2026-06-11 | Active (optional) |
| Najm | Saudi auto-insurance vehicle history (T6f) | KSA | 2026-06-11 | Active (optional) |
| Tadawul | Saudi Stock Exchange listed-company data (T6f) | KSA | 2026-06-11 | Active (optional) |
| MISA | Saudi Ministry of Investment foreign-licence checks (T6f) | KSA | 2026-06-11 | Active (optional) |
| KNET | Kuwait national debit-card switch (T6f) | Kuwait | 2026-06-11 | Active (optional) |
| BENEFIT | Bahrain payment + national e-KYC (T6f) | Bahrain | 2026-06-11 | Active (optional) |
| Magnati | UAE merchant-acquiring AED (T6f) | UAE | 2026-06-11 | Active (optional) |

## Process for changes

1. Open a PR editing this file + `docs/sla.md` §8.
2. The CHANGELOG entry must mention the sub-processor change.
3. Customer notification emails fire from the Loops `sub_processor_added`
   event at PR merge.
4. The 30-day right-of-objection clock starts the day the email lands.

## Out of scope

Sub-processors used purely for internal collaboration (e.g. GitHub,
Slack, Notion) are listed in `docs/repo/internal_tools.md` (private).
They never see customer Personal Data.
