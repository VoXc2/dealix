# Objection handling — the 12 questions every Saudi B2B buyer asks

> Every objection below has a one-paragraph honest answer + a link to
> the code path or doc that proves it. Read this once before any
> commercial call; never improvise on these — accuracy is the moat.

## 1. "How is your Arabic actually better than HubSpot's?"

We don't *translate* — we ship Saudi-Khaliji-tuned prompts in
`dealix/prompts/` (proposal, qualification, content_generator),
plus a 60-term commercial glossary (`dealix/agents/skills/handlers.py:
_GLOSSARY_AR_EN`) that the AR↔EN translator uses for invoices,
contracts, and CR lookups. The agents are *built* in Arabic; English
is the secondary path.

## 2. "Do you actually issue ZATCA Phase 2 invoices?"

Yes. `dealix/billing/invoice_pdf.py` renders a bilingual UBL-2.1-shaped
invoice with a TLV-encoded QR-code payload (5 mandatory tags) on every
post-payment webhook. The PDF is emailed via
`api/routers/pricing.py:_send_receipt_email_best_effort`. Live for
SAR via Moyasar today.

## 3. "Where does customer data live?"

By default: EU/US (Railway / RDS). Enterprise contracts ship to
KSA region (AWS me-central-1, STC Cloud) via the
`infra/terraform/live/prod/` module + `deploy/helm/dealix/` chart.
The migration runbook is `docs/ops/runbook_zero_to_prod.md`.

## 4. "What about PDPL?"

Enforced at write-time, not audited at quarter-end:
- Consent ledger: `auto_client_acquisition/compliance_os/`.
- DNC + contactability gate: `dealix/agents/skills/handlers.py:_sales_qualifier`.
- DSR API: `/api/v1/pdpl/dsr/{export,delete,portability}`.
- Quarterly ROPA generator: same compliance_os module.

## 5. "Pricing seems low — what's the catch?"

No catch. SAR 199 Pilot → 499 Growth → 999 Scale → 1999 Enterprise
per seat per month. Annual discount 17%. We make margin on LLM
metering (Lago), not on seat squeeze. The trial is 14-day no-card.

## 6. "Are you SOC 2 certified?"

SOC 2 Type I audit is in progress, target Q3 2026. Pre-audit posture
is documented in `docs/procurement/soc2_readiness.md` — every
Trust-Services-Criteria control maps to a code path. ISO 27001:2022
alignment doc is `docs/procurement/iso27001_mapping.md`.

## 7. "Lock-in?"

Zero. PDPL Article 22 portability + our DSR API (`/api/v1/pdpl/dsr/portability`)
gives you a full JSON export of your tenant any day. Audit logs
exportable to your S3 / Datadog / Splunk via
`dealix/audit/forward.py`. SDK published as `dealix-sdk` on PyPI + npm.

## 8. "We already use HubSpot / Salesforce / Outreach."

Co-existence, not replacement, on day 1:
- HubSpot bidirectional sync — `dealix/agents/skills/handlers_data.py:_crm_syncer`.
- Salesforce — REST + planned bidirectional in Q3.
- Outreach / Salesloft — we ingest opens/clicks via webhook, push
  cadence decisions back via API.

The honest comparison pages tell you exactly when we win and when
the incumbent wins: `landing/comparisons/*.html`.

## 9. "How do payments actually flow?"

Customer hits `/checkout.html` → POST `/api/v1/payment-ops/invoice-intent`
(T13a) → if `MOYASAR_SECRET_KEY` is set, redirect to Moyasar hosted
checkout. On webhook (`/api/v1/webhooks/moyasar`), the
`InvoiceRecord` is persisted, the customer gets a bilingual receipt
email with a signed PDF download link (T13b), and Lago metering +
Knock notification fire. Non-SAR currencies flow through Stripe.
GCC currencies (KWD / BHD / AED) flow through KNET / BENEFIT / Magnati
once merchant onboarding lands (`api/routers/billing_gcc.py`).

## 10. "Will you sue our previous vendor for our data?"

No. Customers retain ownership of their data; we are a processor
under PDPL Article 16 / GDPR Article 28. DPA template at
`docs/legal/DPA.md`.

## 11. "What if Anthropic / Moyasar / WorkOS goes down?"

Sub-processor list (`docs/compliance/SUB_PROCESSORS.md`) names every
upstream dependency with its SLA. Critical-path fallbacks:
- LLM router (`core/llm/router.py`) — multi-provider with cost cap.
- Email — Resend → SendGrid → SMTP fallback chain.
- Payment — Moyasar primary, Stripe international, manual bank
  transfer always available.
- Status page: status.dealix.me.

## 12. "What if you go out of business?"

Source escrow available on Enterprise contracts. The codebase is
deploy-ready via `deploy/docker-compose.prod.yml` or `deploy/helm/dealix/`;
the customer's IT can run the platform on their own infra
indefinitely. PDPL Article 22 export gives them their data
out anytime.
