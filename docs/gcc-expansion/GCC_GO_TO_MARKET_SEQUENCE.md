# GCC Go-to-Market Sequence

> Companion to `GCC_EXPANSION_THESIS.md` and `GCC_COUNTRY_PRIORITY_MAP.md`.
> This file describes **the order of operations**. The other two describe
> **the why** and **the where**. Together they form the Wave 19 GCC track.

## Step-by-Step Sequence

### Step 1 — Saudi proof (current)

- Land Invoice #1 in Saudi Arabia.
- Publish one verified Proof Pack (with client approval).
- Convert to one Governed Ops Retainer.
- Update `data/first_invoice_log.json` and
  `data/partner_outreach_log.json` honestly.

### Step 2 — Doctrinal readiness (parallel)

- Publish Open Doctrine repo (`open-doctrine/`).
- Publish `/api/v1/dealix-promise` and `/api/v1/doctrine` endpoints.
- Land doctrine tests in CI as non-bypassable gates.

### Step 3 — One anchor partner per priority country

- UAE: one named Big 4 / regulated-processor partner.
- Qatar: one named professional-services partner.
- Bahrain: one named fintech-adjacent partner.
- Register each in `data/anchor_partner_pipeline.json`.

### Step 4 — One co-sold pilot in country N+1

- Partner sources the lead.
- Dealix delivers the Revenue Intelligence Sprint.
- Proof Pack is country-of-delivery aware (data residency, language).
- Invoice in local currency or via partner.

### Step 5 — Productized country pack

Only after Step 4 succeeds for a country:

- Country-specific Trust Pack (residency, regulator references).
- Country-specific Outreach Pack (local language nuance).
- Country-specific pricing addendum (if material).

### Step 6 — Second co-sold pilot in same country

Repeat Step 4 in the same country to prove repeatability before opening
the next.

## Anti-Sequence — Things Forbidden Until Their Trigger

| Action                                        | Trigger                                      |
|-----------------------------------------------|----------------------------------------------|
| Hiring a country GM                           | After Step 6 in that country                 |
| Country-launch press / event                  | After Step 6 + client approval               |
| Multi-country pricing announcement            | After Step 6 in ≥ 2 countries                |
| Region-wide marketing campaign                | Never as a substitute for Step 4             |
| "GCC-wide partner program" branding           | After ≥ 2 partners have co-sold              |

## Verification Hooks

The verifier (`scripts/verify_all_dealix.py`) checks for the existence
of these documents and the Saudi-beachhead test. The actual sequence
events are tracked in:

- `data/anchor_partner_pipeline.json`
- `data/partner_outreach_log.json`
- `data/first_invoice_log.json`

Update those files only when the corresponding step is **actually** done.
