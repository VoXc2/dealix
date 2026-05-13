# Enterprise Decision

> When to say yes to a big logo. When to say "not yet". Enterprise without
> readiness will burn the company.

## Hard gate (all must be true to sign an Enterprise contract)

- [ ] 10+ paid Sprints completed.
- [ ] 3+ active retainers.
- [ ] Average Quality Score ≥ 90 across the last 10 deliveries.
- [ ] Zero major governance incidents in the last 6 months.
- [ ] At least 3 published / publishable case studies.
- [ ] Audit-log export endpoint live (or 30-day commit to deliver).
- [ ] Role-based access control designed (`docs/adr/0003-multi-tenant-isolation.md` + RBAC plan).
- [ ] SLA template signed by HoLegal (per `docs/sre/slo_framework.md` Enterprise tier).
- [ ] Data handling + retention policy adopted (per `docs/trust/data_governance.md`).
- [ ] Procurement pack ready (`docs/procurement/enterprise_pack.md`).
- [ ] Dedicated project manager capacity available.

If any of the above is missing, the Enterprise contract is **deferred** until the gate is closed. Offer a Pilot Conversion Sprint or a 90-day pilot retainer in the interim.

## Enterprise opportunity classification

| Signal | Action |
|--------|--------|
| Customer asks for "everything" upfront | Slow down. Diagnose first (SAR 25K Readiness). |
| Customer requests SLA / DPA / RFP response | Procurement pack (`docs/procurement/enterprise_pack.md`). |
| Customer demands custom data residency | Sovereign tier per pricing packages — only if Enterprise gates pass. |
| Customer wants in-Kingdom dedicated VPC | Phase 4 capability — defer or partner-deliver. |
| Customer requests BYOK / customer-managed keys | Phase 4 — defer. |

## The "Trojan Pilot" pattern (acceptable substitute when gate fails)

Offer a 90-day paid pilot covering a single workflow (one pillar), at SAR 60–150K. This:
- Tests the customer's seriousness.
- Builds a Proof Pack inside the customer's environment.
- Earns the right to negotiate the Enterprise contract from strength, not aspiration.
- Closes a gap (e.g., audit-log export) while delivering tangible value.

## Enterprise commercial floor

- Setup: ≥ SAR 85,000.
- Recurring: ≥ SAR 35,000 / month.
- Term: ≥ 12 months.
- Cancellation: 60-day notice, pro-rated.
- Liability cap: 1× annual fees.
- Procurement-ready security questionnaire (≥ 50 standard responses pre-filled).

## Anti-patterns (auto-reject)

- "Build us our own AI" without a defined business problem.
- Demand to sign before discovery.
- Refusal to acknowledge PDPL.
- Request to bypass approval matrix.
- Multi-year contract at deep discount (Rule 3 on pricing: confidence over urgency).

## Owner & cadence

- **Owner**: CEO + CTO + HoLegal triumvirate. No single person signs an Enterprise contract.
- **Cadence**: Enterprise opportunities reviewed weekly in the operating cadence; quarterly enterprise pipeline review.

## Cross-links
- `docs/procurement/enterprise_pack.md` — procurement readiness
- `docs/sre/slo_framework.md` — SLA design
- `docs/trust/data_governance.md` — DPA + residency
- `docs/adr/0003-multi-tenant-isolation.md` — RBAC architecture
- `docs/strategy/dealix_maturity_and_verification.md` — Maturity Level 5
