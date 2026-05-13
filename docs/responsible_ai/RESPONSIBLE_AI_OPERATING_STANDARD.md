# Dealix Responsible AI Operating Standard (D-RAIOS)

> Dealix wins because it makes AI **commercially responsible**: clear, governed, documented, measurable, and operable inside companies without chaos.

Layer 25 consolidated doctrine. Typed surfaces in `auto_client_acquisition/responsible_ai_os/`.

## 1. Definition

A practical operating standard for deploying AI inside companies with: clear data sources, human oversight, runtime governance, audit logs, proof of value, continuous improvement.

## 2. Seven pillars

1. **Data Sovereignty** — Source Passport + allowed use + PII + retention + AI access.
2. **Human Oversight** — AI prepares, humans approve, system logs.
3. **Runtime Governance** — ALLOW / DRAFT_ONLY / REQUIRE_APPROVAL / REDACT / BLOCK / ESCALATE.
4. **Explainability & Auditability** — model route, prompt version, source IDs, decision, QA, audit event per run.
5. **Proof of Value** — Proof Pack per engagement; no claim without proof.
6. **Operating Cadence** — weekly review, monthly value report, quarterly capability review.
7. **Continuous Improvement** — every incident → rule/test/checklist; every friction → product candidate.

## 3. AI Use Case Risk Classifier

- **Low Risk:** internal summarization, draft-only content, non-sensitive reporting.
- **Medium Risk:** customer-facing drafts, PII-containing analysis, decision-affecting recommendations.
- **High Risk:** external outreach, financial/compliance decisions, sensitive personal data, automated impactful workflows.
- **Forbidden:** scraping, cold WhatsApp, LinkedIn automation, guaranteed sales claims, source-less decisioning.

## 4. Use Case Card

```json
{
  "use_case_id": "UC-001",
  "name": "Revenue account scoring",
  "department": "Sales",
  "data_sources": ["SRC-001"],
  "contains_pii": true,
  "risk_level": "medium",
  "human_oversight": "required",
  "external_action_allowed": false,
  "governance_decision": "DRAFT_ONLY",
  "proof_metric": "accounts_scored_and_prioritized"
}
```

## 5. AI Inventory

Per client: use case, department, owner, data sources, agent/model used, risk level, approval path, audit status, proof metric, status.

## 6. Responsible AI Trust Pack

13 sections including "What Dealix refuses to build". Lifts Dealix from vendor to trusted operating partner.

## 7. Saudi Responsible AI Positioning

Dealix builds responsible operations on top of national infrastructure. Position: HUMAIN provides infrastructure/models; Dealix provides responsible operations/workflows/governance/proof.

## 8. Responsible AI Score (7 dimensions, total 100)

| Dimension | Weight |
| --- | ---: |
| Source clarity | 15 |
| Data sensitivity handling | 15 |
| Human oversight | 15 |
| Governance decision coverage | 15 |
| Auditability | 15 |
| Proof of value | 15 |
| Incident readiness | 10 |

Tiers: 85+ ready, 70–84 ready with controls, 55–69 governance review required, <55 do not deploy.

Typed: `responsible_ai_os.responsible_ai_score.compute_responsible_ai_score()`.

## 9. AI Literacy Layer

Modules: AI for Executives, AI for Sales Operators, AI Governance Basics, Data Readiness for AI, Responsible AI Outreach, Company Brain Usage.

## 10. Compliance-to-Product Loop

Need source clarity → Source Passport Panel. Need AI visibility → AI Run Ledger. Need human review → Approval Center. Need proof → Proof Timeline. Need governance reporting → Compliance Report. Need education → Academy module. Need audit → Audit Export.

> Compliance friction is product signal.

## 11. The closing sentence

> Dealix wins when Responsible AI is the product itself — not a marketing promise, but a system of sources, approvals, ledgers, Proof, and education that lets companies use AI confidently with sustained value.
