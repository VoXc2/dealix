# Dealix Compliance-by-Design & Trust Operations

> Dealix does not bolt on compliance at the end. The product and the service are built so compliance, proof, and audit are **part of execution itself**.

Layer 21 consolidated doctrine. Typed surfaces in `auto_client_acquisition/compliance_trust_os/`.

## 1. Trust Operations Model

```
Discover → Classify → Govern → Approve → Execute → Log → Prove → Review → Improve
```

## 2. Six principles

1. No invisible AI.
2. No unknown data.
3. No unowned agent.
4. No unsupported claim.
5. No external action without approval.
6. No compliance theater.

## 3. Compliance Architecture (modules)

`compliance_trust_os/`:
- source_passport_v2
- pii_classifier
- allowed_use_checker
- claim_compliance
- approval_engine
- audit_trail
- incident_response
- compliance_report
- compliance_dashboard

## 4. Source Passport v2

Extends the standard passport with `collection_context` and `deletion_required_after`.

## 5. AI Agent Compliance

Each agent inside `Agent Registry`; MVP autonomy 0–3 only.

## 6. Trust Artifacts (per engagement)

Source Passport, Governance Decision Log, AI Run Ledger, Approval Records, QA Results, Proof Pack, Blocked Risk Events, Incident Log.

## 7. Compliance Report (12 sections)

Data sources used, Source Passport status, PII detected, Redactions applied, AI runs logged, Governance decisions, Approvals requested, Approvals completed, External actions blocked/approved, Claims supported by proof, Incidents, Recommendations.

## 8. Claim Compliance

Forbidden: guaranteed sales, "strongest AI", unverified results. Allowed: ranking opportunities, measuring impact, producing reviewable outputs, lowering risks, Proof Pack.

Status: UNSUPPORTED → block, ESTIMATED → caveat, OBSERVED → in Proof Pack, VERIFIED → case-safe summary with permission.

## 9. Incident Response v2

Types: PII exposure, unsupported claim, source misuse, wrong client data, unapproved external action, hallucinated answer, partner violation, agent tool misuse. Flow: detect → contain → assign → assess → notify → correct → log → add rule/test/checklist.

## 10. Regulatory readiness mindset

AI inventory, use case classification, data source tracking, human oversight, audit trail, risk assessment, incident response, proof of governance.

## 11. Saudi Compliance Layer

PDPL-aware data handling, Arabic claim safety, WhatsApp boundary, human approval, source transparency, bilingual compliance report, client data responsibility statement.

## 12. Compliance Metrics

% sources with passport, % AI runs logged, % outputs with governance status, % external actions approved, PII flags, redactions, blocked actions, incidents by severity, time to resolve. Thresholds: < 100% AI run logging → no enterprise; < 100% passport coverage → no scale; any unapproved external action → incident review.

## 13. Compliance as sales advantage

> We do not put AI on unclear data. Every source has a passport, every output has a governance status, every claim has proof.

## 14. The closing sentence

> Dealix wins when the client never has to ask "is this safe?" — because the system itself proves safety via sources, approvals, ledgers, Proof, and clear limits before any expansion.
