# Trust & Safety Charter

> Dealix's public, contract-grade commitments to customers, partners, and
> regulators. This charter is what we will sign — and what we will be held
> to. Aligned with Saudi PDPL, sector procurement norms, and Dealix's
> internal runtime governance.

## What we commit to (in plain language)

1. **No spam.** We never send outbound messages on a customer's behalf
   without their explicit, named approval.
2. **No unsourced PII.** We never use personal data we cannot trace to a
   registered, lawful source (`SOURCE_REGISTRY.md`).
3. **No fake proof.** Every claim of impact is backed by a Proof Pack with
   real inputs, real outputs, and named witnesses.
4. **No guaranteed claims.** We do not promise ROI, ranking, or revenue
   outcomes. Our copy and our agents are gated against guarantee language
   (`dealix/trust/forbidden_claims.py`).
5. **No source-less knowledge answers.** The Company Brain returns a cited
   answer or `"insufficient evidence"` — never a confident guess.
6. **Human approval for external actions.** Anything that leaves Dealix's
   perimeter — message sent, file published, API written — requires a
   named human approver per `dealix/trust/approval_matrix.py`.
7. **Audit logs for every customer-affecting action.** Read or write,
   internal or external — recorded with actor, action, target, and
   decision.
8. **Proof Packs on demand.** Any customer can request the Proof Pack for
   any deliverable; it will include inputs (redacted), outputs, prompt
   version, governance decisions, and approver names.

## Why this matters in Saudi Arabia

Procurement teams in regulated sectors — finance, healthcare, government,
energy — increasingly require documented AI governance from suppliers. The
charter is written to be usable verbatim in procurement responses and on
public Dealix surfaces.

## What we will not do

- We will not train any third-party model on customer data.
- We will not cross-border-transfer personal data without lawful basis
  per `docs/governance/PDPL_DATA_RULES.md` and the customer's DPA.
- We will not use a customer's data to benefit another customer.
- We will not deploy any autonomous agent at Autonomy Level 6
  (autonomous external action) — ever (per `RUNTIME_GOVERNANCE.md`).
- We will not ship a customer-facing AI output without (prompt version +
  schema + redaction status + QA score + risk) per
  `docs/ledgers/AI_RUN_LEDGER.md`.

## How we enforce each commitment

| Commitment | Enforcement |
|-----------|-------------|
| No spam | Approval Matrix; outreach drafts only — sends are customer-side |
| No unsourced PII | Source Registry gate (`AI_INFORMATION_GOVERNANCE.md`) + PII redaction |
| No fake proof | Proof Pack schema validator; inputs+outputs required (`QUALITY_AS_CODE.md`) |
| No guaranteed claims | `dealix/trust/forbidden_claims.py` runs on every output |
| No source-less answers | KnowledgeAgent hard rule + Ragas eval (`EVL-BRN-001`) |
| Human approval for external actions | `dealix/trust/approval_matrix.py` + `HUMAN_IN_THE_LOOP_MATRIX.md` |
| Audit logs | `dealix/trust/audit.py` + event store |
| Proof Packs on demand | `dealix/reporting/proof_pack.py` |

## How customers can verify

- Request the Proof Pack for any deliverable.
- Request an Information Governance review (`SOURCE_REGISTRY.md` + audit).
- Request a Promotion Gate report per `AGENT_LIFECYCLE_MANAGEMENT.md`.
- Submit a Data Subject Request per `PDPL_DATA_SUBJECT_REQUEST_SOP.md`.

## Incident commitment

If a personal data breach occurs, we notify the customer within 24 hours,
notify SDAIA and affected individuals within the 72-hour PDPL window
(`PDPL_BREACH_RESPONSE_PLAN.md`), and publish a post-incident summary.

## Where to find this charter

This file (source of truth); the public website (`landing/`) when Phase-1
marketing surfaces refresh; bundled into procurement responses and the
DPA (`DPA_DEALIX_FULL.md`).

## Cross-links

- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/AI_INFORMATION_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/PDPL_DATA_RULES.md`
- `/home/user/dealix/docs/governance/INCIDENT_RESPONSE.md`
- `/home/user/dealix/docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `/home/user/dealix/docs/product/QUALITY_AS_CODE.md`
- `/home/user/dealix/docs/PDPL_BREACH_RESPONSE_PLAN.md`
- `/home/user/dealix/docs/DPA_DEALIX_FULL.md`
- `/home/user/dealix/dealix/trust/forbidden_claims.py`
- `/home/user/dealix/dealix/trust/approval_matrix.py`
- `/home/user/dealix/dealix/trust/audit.py`
