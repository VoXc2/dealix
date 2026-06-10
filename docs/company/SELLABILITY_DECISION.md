# Sellability Decision

A service can be sold **officially** only if gates and evidence below are satisfied. Otherwise use **Beta**, **Designed**, **Idea**, or **Blocked**—see states below.

## Required scores (official)

| Gate | Minimum |
|------|---------:|
| Offer readiness | ≥ 85 |
| Delivery readiness | ≥ 85 |
| Governance readiness | ≥ 90 (manual + verification) |
| Demo readiness | ≥ 85 |
| Sales readiness | ≥ 85 |

Numeric detail: [`SELLABILITY_POLICY.md`](SELLABILITY_POLICY.md), [`SERVICE_READINESS_MATRIX.md`](SERVICE_READINESS_MATRIX.md), `scripts/verify_service_readiness_matrix.py` / `verify_dealix_ready.py`.

## Required evidence (blueprint service)

- `offer.md`
- `scope.md`
- `intake.md`
- `delivery_checklist.md`
- `qa_checklist.md`
- `report_template.md` (or explicit report pattern in templates)
- `proof_pack_template.md` (or `proof_pack.md` per service folder)
- `sample_output.md` (or linked anonymized asset in `docs/assets/`)
- `upsell.md` (or explicit upsell path in offer/registry)

Verification: `scripts/verify_service_files.py`, `scripts/verify_proof_pack.py`.

## Decision states

| State | Meaning |
|-------|---------|
| **Official** | بعها بثقة — meets scores + evidence |
| **Beta** | بِع كـ pilot فقط — labeled expectations + pricing |
| **Designed** | لا تبعها؛ استخدمها في الحديث / roadmap |
| **Idea** | لا تعرضها كمنتج |
| **Blocked** | ممنوع — خطر أو غير جاهز (see [`DO_NOT_SELL_YET.md`](DO_NOT_SELL_YET.md)) |

## Decision record (template)

- Service ID:
- Evidence links:
- Scores:
- Risks:
- Owner:
- State chosen:
- Next action:
