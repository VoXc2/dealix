# Role Briefs Operating Model

> Source: deploy-branch `GET /api/v1/role-briefs/daily?role=*` and
> `GET /api/v1/role-briefs/roles`.

## Roles registered live (8)

```
ceo, sales_manager, growth_manager, revops, customer_success,
agency_partner, finance, compliance
```

(Verified from `/api/v1/role-briefs/roles` 2026-05-03.)

## Per-role contract (target)

Every brief is expected to expose:

| Field | Source today | Status |
| --- | --- | --- |
| `summary` | top of brief response | PROVEN_LIVE |
| `top_decisions[≤3]` | `top_decisions` array | PROVEN_LIVE for ceo/growth_manager/customer_success/compliance/revops |
| `why_now` | per-decision `why_now_ar` | PROVEN_LIVE |
| `recommended_action` | per-decision `recommended_action_ar` | PROVEN_LIVE |
| `risk` | per-decision `risk_ar` | PROVEN_LIVE |
| `proof_impact` | per-decision `proof_impact_sar` | CODE_EXISTS_NOT_PROVEN — not all roles populate it |
| `pending_approvals` | linked to `approvals/pending` | CODE_EXISTS_NOT_PROVEN |
| `next_step` | per-decision `next_step_ar` | PROVEN_LIVE |
| `max_buttons=3` | UI contract | enforced client-side; no server check |
| `action_modes` | `suggest_only / draft_only / approval_required / approved_execute / blocked` | PROVEN_LOCAL via classifier; not enforced inside role brief response |
| `language_ar/en` | `text_ar` / `text_en` | PROVEN_LIVE for ar |

## Per-role status

| Role | HTTP status | Notes |
| --- | --- | --- |
| `ceo` | 200 | clean |
| `growth_manager` | 200 | clean — best-shaped brief on prod today |
| `revops` | 200 | clean |
| `customer_success` | 200 | clean |
| `agency_partner` | not exercised | CODE_EXISTS_NOT_PROVEN |
| `finance` | 200 | clean |
| `compliance` | 200 | clean |
| `sales_manager` | **200 with `_errors` payload** | **BLOCKER** — `column deals.hubspot_deal_id does not exist` (Postgres schema drift) |

The spec asked for `marketing_manager` and `finance_manager`. The
deploy-branch registry uses `growth_manager` and `finance`. **Role-name
alias** at the deploy branch is the cleanest fix:

```python
# api/routers/role_briefs.py — alias map
ROLE_ALIASES = {
    "marketing_manager": "growth_manager",
    "finance_manager":   "finance",
}
```

## Tests planned (BACKLOG until deploy branch is editable here)

```
tests/test_role_briefs_contract.py
- iterate 8 roles
- assert top_decisions length ≤ 3
- assert each top_decision has why_now / recommended_action / risk / next_step
- assert no decision text contains a "guaranteed" claim
- assert response is reachable
```

These tests should land on the deploy branch as part of the same merge
that fixes the schema drift.
