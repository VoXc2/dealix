# Company Brain — Sales Page

**Layer:** L6 · Growth Machine
**Owner:** Head of Growth / Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [COMPANY_BRAIN_SALES_PAGE_AR.md](./COMPANY_BRAIN_SALES_PAGE_AR.md)

## Context
Company Brain is Dealix's knowledge-side offer: a governed, source-cited
internal assistant for companies whose pain is scattered documents and
inconsistent answers from staff. It directly implements the governance
stance set in `docs/AI_STACK_DECISIONS.md` and the service framing in
`docs/COMPANY_SERVICE_LADDER.md`. Removes the constraint of "ChatGPT
answers" — every answer in Company Brain is grounded in a known source
or returns "insufficient evidence".

## Headline

> **Turn scattered company knowledge into a source-cited internal
> assistant.**

## The Problem

- Documents live in 5+ places (Drive, email, WhatsApp, paper, shared
  laptops).
- New staff ask the same questions repeatedly.
- Senior people spend hours re-explaining policies.
- AI tools answer confidently from training data, not your data.
- No audit trail on what was answered to whom.

## What You Get (Deliverables)

1. **Document ingest** — controlled, classified, versioned.
2. **Index** — searchable, permissioned.
3. **RAG with citations** — every answer cites at least one source.
4. **"Insufficient evidence" mode** — no source = no answer.
5. **Knowledge gaps report** — questions asked but unanswered, ranked.
6. **Admin console basics** — upload, retire, re-index documents.
7. **Proof Pack** — usage, citation rate, gap report.

## Governance Rules

- **No source = no answer.** Hard constraint, not a setting.
- Sensitive documents tagged and access-controlled.
- Logs do not store full questions if they contain PII unless lawfully
  permitted; see `docs/ops/PDPL_RETENTION_POLICY.md`.
- Human-in-the-loop for any answer flagged as high-impact.
- Conforms to the trust stance in
  `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md`.

## KPIs Delivered

- Citation rate (target ≥ 95%).
- Insufficient-evidence rate (healthy 5–15%).
- Average answer time.
- Top 10 unanswered questions (gaps report).
- Document freshness (last reviewed).

## Timeline

Company Brain is delivered as a 4–8 week engagement, depending on
volume:

| Phase | Length |
|---|---|
| Document intake + classification | 1–2 weeks |
| Index + RAG build | 1–2 weeks |
| Citation + governance + admin | 1–2 weeks |
| QA, gaps report, handover | 1–2 weeks |

## Price

**SAR 20,000 – 60,000** depending on document volume, sensitivity, and
number of departments. 40% on kickoff, 40% on index live, 20% on
handover. Followed by Monthly Company Brain retainer.

## Who It's For

- Companies with ≥ 200 internal documents.
- Departments with frequent recurring questions (HR, ops, policy).
- Buyers: GM, COO, Head of Operations, Head of HR.

## CTA

> Book a 25-minute discovery call. If Company Brain fits, we will send
> a fixed-scope, milestone-paid proposal within 48 hours.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Document set + classifications | Indexed knowledge base | Delivery | Per engagement |
| Question logs | Gaps report | CSM | Monthly |
| Governance review | Updated permissions / retention | Compliance Owner | Monthly |

## Metrics

- **Citation rate** — % of answers with ≥ 1 valid citation.
- **Insufficient-evidence rate** — healthy band.
- **Active users / month**.
- **Retainer conversion** — % moving to Monthly Company Brain.

## Related

- `docs/AI_STACK_DECISIONS.md` — RAG / governance stance enforced here.
- `docs/COMPANY_SERVICE_LADDER.md` — Company Brain's place in the ladder.
- `docs/sales/ONE_PAGER.md` — short intro for buyers.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
