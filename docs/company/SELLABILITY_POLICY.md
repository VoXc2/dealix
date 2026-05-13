# Dealix Sellability Policy

> **Binding policy**. Sales and CS must apply this policy to every prospect
> conversation. CEO + CRO sign-off required on any exception.

## A service may be sold OFFICIALLY only if ALL of these are true

1. Offer Readiness score ≥ 85
2. Delivery Readiness score ≥ 85
3. Governance Readiness score ≥ 90 (higher bar — governance is non-negotiable)
4. Demo Readiness score ≥ 85
5. Sales Readiness score ≥ 85
6. QA checklist exists in `docs/services/<offer>/qa_checklist.md`
7. Proof Pack template exists in `docs/services/<offer>/proof_pack_template.md`
8. Sales / offer page exists in `docs/sales/offer_pages/` or `docs/services/<offer>/offer.md`
9. Scope is explicit and exclusions are written
10. No forbidden action (per `docs/governance/FORBIDDEN_ACTIONS.md`) is part of the service

## Beta services

A service scoring 70–84 may be offered ONLY as a **pilot** with:

- explicit "pilot" / "first-in-market" framing in writing
- max 1–2 customers in pilot at a time
- documented pilot success criteria
- discounted or capped price (typically half the eventual list)
- written agreement that scope may shift during pilot

Beta services **do not** appear in the customer-facing offer pages, in marketing materials, or in cold outreach. They are offered by referral only.

## Not-ready services

A service scoring below 70 cannot be:
- sold
- advertised
- promised
- referenced as available "soon" (avoid creating false expectations)

## Current sellable services (as of last `verify_dealix_ready.py` run)

1. **Lead Intelligence Sprint** — SAR 9,500 (10 days)
2. **AI Quick Win Sprint** — SAR 12,000 (7 days)
3. **Company Brain Sprint** — SAR 20,000 (21 days)

See `docs/company/SERVICE_READINESS_MATRIX.md` for the live status of every catalog item.

## Decision tree

```
Prospect interested in X
  ↓
Is X in Service Readiness Matrix as Sellable?
  ├─ YES → quote from SOW template, normal motion
  └─ NO →
       ├─ Is X Beta? → offer pilot with explicit framing
       ├─ Is X Designed? → offer paid discovery instead
       └─ Is X Idea/Not Ready? → polite no, recommend a Sellable alternative
```

## Enforcement

- **Sales**: SOWs may only be sent for Sellable services. Beta requires CRO sign-off + a pilot agreement variant.
- **Marketing**: offer pages and landing pages refer only to Sellable services.
- **CS**: pilot conversations follow the pilot template, never the SOW template.

## Owner & cadence

- **Owner**: CEO + CRO.
- **Refresh**: weekly (mirrors Service Readiness Matrix).
- **Exceptions**: any deviation requires CEO + CRO co-sign captured in the project file.

## Cross-links

- `DEALIX_READINESS.md`
- `docs/company/SERVICE_READINESS_MATRIX.md`
- `docs/company/DECISION_RULES.md`
- `docs/company/EVIDENCE_SYSTEM.md`
- `docs/governance/FORBIDDEN_ACTIONS.md`
