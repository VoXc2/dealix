# Dealix Evidence System

> **Rule:** No service, feature, gate, or delivery is marked "ready" without
> evidence. "I think we're ready" is not allowed. Every readiness claim must
> point to an artifact.

## 1. The 8 evidence types

| # | Evidence type | Proves | Stored in |
|---|---------------|--------|-----------|
| 1 | Strategy evidence | Positioning + ICP + Market clear | `docs/company/`, `docs/strategy/` |
| 2 | Offer evidence | Service is sellable | `docs/services/<offer>/offer.md`, `templates/sow/` |
| 3 | Delivery evidence | We can deliver without improvisation | `docs/delivery/`, `docs/services/<offer>/delivery_checklist.md` |
| 4 | Product evidence | The repo supports delivery | `auto_client_acquisition/*/*.py`, `dealix/*/*.py` |
| 5 | Governance evidence | The service is safe | `docs/governance/`, `dealix/trust/*` |
| 6 | Demo evidence | The customer can see the result | `demos/`, `docs/services/<offer>/sample_output.md` |
| 7 | Sales evidence | We can close | `docs/sales/`, `templates/outbound_messages.md` |
| 8 | Proof evidence | We can prove impact after delivery | Proof Ledger entries + `docs/services/<offer>/proof_pack_template.md` |

## 2. The readiness rule (binding)

A service is **Official** only when all of the following exist:

- Service Readiness Score ≥ 85 (per `docs/quality/SERVICE_READINESS_SCORE.md`)
- Governance Score ≥ 90
- Demo runs end-to-end in ≤ 10 minutes
- Proof pack template present
- QA checklist present
- Sales page present
- Sample executive output present
- Backing product module(s) at least at MVP

A service that does not meet all of the above is **Beta** (single-pilot only)
or **Not Ready** (must not be sold).

## 3. Single source of truth

- **Readiness scorecard**: `DEALIX_READINESS.md` (repo root) — refreshed weekly.
- **Service matrix**: `docs/company/SERVICE_READINESS_MATRIX.md` — every catalog item with status.
- **Capability matrix**: `docs/product/CAPABILITY_MATRIX.md` — capability ↔ module ↔ MVP state.
- **Sellability policy**: `docs/company/SELLABILITY_POLICY.md` — binding rule for what we can sell.
- **Founder Command Center**: `docs/company/FOUNDER_COMMAND_CENTER.md` — daily action view.

## 4. Verification automation

```bash
python scripts/verify_dealix_ready.py    # 11-gate readiness check
python scripts/verify_full_mvp_ready.py  # orchestrates all 5 verifiers
python scripts/verify_company_ready.py   # core readiness (Gate 0–7 subset)
```

If any mandatory gate (0/1/2/4/5/6) fails, sales is blocked.

## 5. Owner & cadence

- **Owner**: CEO.
- **Refresh**: weekly in operating cadence (W5.T30).
- **Escalation**: any evidence gap on a "Sellable" service is a Monday-review blocker.
