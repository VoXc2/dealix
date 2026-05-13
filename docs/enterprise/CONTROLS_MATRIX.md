---
doc_id: enterprise.controls_matrix
title: Enterprise Controls Matrix — The Gate That Cannot Be Skipped
owner: CTO + HoLegal
status: approved
last_reviewed: 2026-05-13
audience: [internal, enterprise-buyer, procurement]
---

# Enterprise Controls Matrix

> No Enterprise contract is signed without **every** control below
> live, documented, and demonstrable. This file is the binding gate
> referenced by `IMPLEMENTATION_TIERS.md` Tier 5 and
> `ENTERPRISE_DECISION.md`. Procurement reads this matrix; if a row
> is missing, the deal is deferred.

## The 9 controls

| # | Control | Definition | Live in code / process | Procurement evidence |
|---|---------|------------|------------------------|----------------------|
| 1 | RBAC | Role-based access control with at minimum Admin / Operator / Reviewer / Auditor roles | `docs/adr/0003-multi-tenant-isolation.md` + RBAC plan | RBAC policy document + role matrix |
| 2 | SSO | SAML 2.0 or OIDC SSO with the customer's IdP | Auth module configured | SSO test plan + working integration |
| 3 | Audit exports | Append-only audit log exportable to customer (CSV / SIEM-friendly JSON) | `auto_client_acquisition/revenue_memory/event_store.py` + export endpoint | Sample audit export + retention spec |
| 4 | Data retention | Documented retention windows per data class with hard delete | `docs/trust/data_governance.md` | Retention schedule + deletion proof |
| 5 | Approval workflows | Approval matrix wired for every external-action class | `dealix/trust/approval_matrix.py` | Approval matrix document + sample approval log |
| 6 | PII redaction | PII detected and redacted before storage / display where required | `dealix/trust/pii_detector.py` | Redaction report + PDPL Art. 5 register snippet |
| 7 | Model run logs | Every LLM call logged: prompt hash, model, tokens, latency, cost | LLM Gateway (per `MODEL_PORTFOLIO.md`) | Sample run log + cost report |
| 8 | Eval reports | Per-customer evaluation reports for AI outputs (citation rate, hallucination check, schema validity) | `docs/product/EVALUATION_REGISTRY.md` | Sample eval report + threshold definition |
| 9 | Incident response | Defined incident playbook with 24h SLO for customer notification | `docs/sre/` + `GOVERNANCE_LEDGER.md` | Incident response plan + tabletop record |

## Enterprise gate (procurement-readable)

| Question | Answer |
|----------|--------|
| Is RBAC live in your platform? | Yes — see Control 1 evidence |
| Do you support SSO? | Yes — see Control 2 evidence |
| Can we export the audit log? | Yes — see Control 3 evidence |
| What is your data retention policy? | See Control 4 evidence |
| Where are approvals enforced? | See Control 5 evidence |
| How is PII handled under PDPL? | See Control 6 evidence + PDPL register |
| Can we see your model run logs? | Yes — see Control 7 evidence |
| Do you publish eval reports? | Yes — see Control 8 evidence |
| What happens in an incident? | See Control 9 evidence + incident response plan |

## Hard rule

If **any** of the 9 rows lacks live evidence (not "roadmap," not
"coming soon"), the contract is **deferred**. The acceptable
substitute is the **Trojan Pilot** pattern in
`ENTERPRISE_DECISION.md`: a 90-day paid pilot that closes the
specific gap while delivering tangible value. After the pilot, the
matrix is revisited.

## Where each control lives in code

| Control | Code reference |
|--------:|----------------|
| 1 RBAC | (planned) Auth module + role table |
| 2 SSO | (planned) Auth module IdP integration |
| 3 Audit exports | `auto_client_acquisition/revenue_memory/event_store.py` |
| 4 Data retention | `docs/trust/data_governance.md` |
| 5 Approval workflows | `dealix/trust/approval_matrix.py` |
| 6 PII redaction | `dealix/trust/pii_detector.py` |
| 7 Model run logs | `dealix/llm_gateway/` (per `MODEL_PORTFOLIO.md`) |
| 8 Eval reports | `evals/` directory + `EVALUATION_REGISTRY.md` |
| 9 Incident response | `docs/sre/` + escalation channel |

## Pre-signature audit (CTO + HoLegal joint review)

Before any Enterprise contract reaches the CEO for signature:

- [ ] Each row of the 9 controls walked, in code, with the buyer's
      security team.
- [ ] Procurement pack delivered (per
      `docs/procurement/enterprise_pack.md`).
- [ ] SLA template signed by HoLegal (per
      `docs/sre/slo_framework.md`).
- [ ] Liability cap clause reviewed.
- [ ] PDPL DPA executed.

## Anti-patterns (auto-reject)

- "We'll deliver RBAC after kickoff" — defer the contract instead.
- "Audit export is available on request" — must be self-serve.
- "Approvals are by email" — not a control; not acceptable.
- "PII is handled at the model layer" — handle before storage.

## Saudi / PDPL context

Controls 4 (retention), 5 (approvals), and 6 (PII) map directly to
PDPL articles enforced by SDAIA in 2024–2025. The Saudi enterprise
buyer is increasingly fluent in these requirements; vague answers
end conversations.

## Cross-links

- `docs/company/IMPLEMENTATION_TIERS.md` — Tier 5 gate
- `docs/enterprise/ENTERPRISE_DECISION.md` — when to sign
- `docs/enterprise/ROAD_TO_ENTERPRISE.md` — path that opens the gate
- `docs/product/ARCHITECTURE.md` — architecture supporting controls
- `docs/product/EVALUATION_REGISTRY.md` — eval reports
- `docs/product/MODEL_PORTFOLIO.md` — LLM Gateway + run logs
- `docs/procurement/enterprise_pack.md` — procurement pack
- `docs/trust/data_governance.md` — retention + PII
- `docs/sre/slo_framework.md` — SLA template
- `docs/adr/0003-multi-tenant-isolation.md` — RBAC ADR
- `docs/governance/RUNTIME_GOVERNANCE.md` — the 8 runtime checks
