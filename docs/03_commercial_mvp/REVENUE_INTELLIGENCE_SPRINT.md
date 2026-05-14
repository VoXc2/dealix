# Revenue Intelligence Sprint — سبرنت ذكاء الإيرادات

> Purpose: the productized first paid offer in the Dealix ladder. A fixed-scope engagement that produces ranked accounts, governed drafts, proof, and a capital asset — without scraping, without cold WhatsApp, without guarantees. Cross-link: [COMPANY_SERVICE_LADDER.md](../COMPANY_SERVICE_LADDER.md).

## Who it's for — لمن

Saudi B2B operators with:

- An existing customer list, CRM export, or manual account list (real signal, not scraped lists).
- A named workflow owner on the client side (sales lead, growth lead, or founder).
- A willingness to approve every external action explicitly.

Typical fit: marketing agencies, B2B services firms, consulting practices, sector-specialist studios.

ليس مناسباً: من يطلب lead-gen بالحجم، من يطلب ضمانات مبيعات، من لا يملك مالكاً واضحاً للسير العملي.

## Problem — المشكلة

The buyer has accounts and contacts but cannot tell which to prioritize, cannot draft bilingual outreach at quality, cannot defend claims publicly, and cannot prove value to an executive committee. The buyer does not need more tools. The buyer needs *one governed motion* end-to-end.

## Inputs required — المدخلات

The sprint cannot start without inputs that carry a [Source Passport](../04_data_os/SOURCE_PASSPORT.md). Accepted input types:

- **CSV upload** — owned by the client, with `source_type=client_upload`.
- **CRM export** — owned by the client, with `source_type=crm_export`.
- **Manual list** — entered by the client in the workspace, with `source_type=manual_entry`.

Each input declares: owner, allowed use, PII flag, sensitivity, retention policy. Inputs without a passport are rejected at intake; inputs with `source_type=scraped` are refused as a constitutional violation. See [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).

## Deliverables — المخرجات

Every sprint delivers, in fixed scope:

- **10 ranked accounts** — scored by a transparent rubric (fit, signal strength, governance risk).
- **Draft pack (Arabic + English)** — outreach drafts marked `draft_only` until the client approves each one explicitly.
- **Governance decisions log** — every action and its decision (ALLOW / DRAFT_ONLY / REQUIRE_APPROVAL / REDACT / BLOCK / etc.). See [RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md).
- **Proof Pack** — the 14-section artifact with a computed proof score. See [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).
- **Capital asset** — at least one reusable asset added to the [Capital Ledger](../09_capital_os/CAPITAL_LEDGER.md).

## Scope boundaries — حدود النطاق

- Duration: a fixed sprint window (declared at contract).
- Account count: exactly 10 ranked accounts in the deliverable. More accounts ranked internally only if data quality permits.
- Workflows: one primary workflow per sprint (e.g., outbound revival of dormant accounts), with one named owner on the client side.
- Channels: drafts only. The client decides whether and when to send.

## Exclusions — الاستثناءات

The sprint **does not** include any of:

- Scraping or list purchase from non-licensed sources.
- Cold WhatsApp outreach.
- LinkedIn automation of any kind.
- Guaranteed sales outcomes or fixed conversion promises.
- Source-less knowledge answers (the workspace returns "source required" instead).

These are not negotiable scope items. They are constitutional refusals. See [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).

## Proof metrics — مقاييس الإثبات

Every sprint reports, at minimum:

- **DQ score** — data quality score on the ingested input.
- **Top-10 ranking** — the ranked list with score components per account.
- **Drafts generated** — count and language coverage.
- **Unsafe actions blocked** — count of governance events of kind `BLOCK` or `REDACT`.
- **Observed value** — measured inside Dealix workflows; not externally claimable until Verified. See [VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md).

These metrics roll into the Proof Pack and feed the proof score.

## Price logic — منطق التسعير

The sprint price is a function of three variables, declared in the proposal:

```
price = base_scope_price
      * data_complexity_multiplier
      * governance_depth_multiplier
```

- **Base scope price** — the published price for a standard sprint (10 ranked accounts, one workflow, one owner).
- **Data complexity multiplier** — higher when inputs span multiple sources, languages, or sensitivity tiers.
- **Governance depth multiplier** — higher when the client requires additional approval gates, redaction depth, or external-use review.

There is no per-lead pricing. There is no success-fee pricing tied to closed deals. Both create incentives that conflict with the non-negotiables.

## Retainer path — المسار إلى الـ retainer

The sprint is a one-time engagement. The path to a monthly **RevOps OS retainer** is gated, not automatic. The gate opens only when:

```
proof_score        >= 80
AND adoption_score >= 70
AND workflow_owner_present
AND governance_risk_controlled
```

See [ADOPTION_SCORE.md](../12_adoption_os/ADOPTION_SCORE.md) for the RetainerReadiness gate. Below the gate, the recommendation is a second sprint or a focused remediation engagement, not a retainer.

## Why this offer is the first rung

The sprint is fixed-scope, fixed-price, governed, and produces both proof and capital. It is the smallest engagement that demonstrates the full Dealix operating loop — data clarity, governance, AI assistance, approval, proof, value, capital. Every later offer in the [service ladder](../COMPANY_SERVICE_LADDER.md) is unlocked only by evidence from this rung.
