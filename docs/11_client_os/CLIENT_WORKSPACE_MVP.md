# Client Workspace MVP — مساحة عمل العميل

> Purpose: define the unified workspace endpoint a Dealix client sees, the 10 panels it exposes, the deterministic next-action priority, and the null-safety rules that prevent missing upstream data from breaking the experience.

The Client Workspace is the single page a workflow owner at a client company opens to understand the state of their Dealix engagement. It is unified by design: one endpoint, one response, ten panels. It avoids the failure mode of "ten separate dashboards no one operates".

## The endpoint — نقطة النهاية

```
GET /api/v1/customer-portal/{handle}/workspace
```

The handle identifies the client tenant. The endpoint is tenant-scoped via the existing `api/middleware/tenant_isolation.py`. Cross-tenant reads are rejected at middleware before any panel logic runs.

## The 10 panels — اللوحات العشر

The response carries ten panels, each with its own data shape and a `status_badge` (e.g., `green`, `amber`, `red`, `null`). Panels:

1. **capability_score** — the client's current Dealix capability score, summarizing data clarity, workflow ownership, and governance maturity.
2. **data_readiness** — counts of Source Passports by status (active, expired, missing). See [SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md).
3. **governance_status** — current count of governance decisions by type (`ALLOW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `ESCALATE`) in the active window. See [RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md).
4. **ranked_opportunities** — the top-N ranked accounts from the latest sprint or retainer cycle, each with score components.
5. **draft_packs_pending_approval** — count and list of drafts in `DRAFT_ONLY` or `REQUIRE_APPROVAL` state awaiting the workflow owner.
6. **proof_timeline** — recent Proof Pack assemblies, with proof score and tier. See [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).
7. **adoption_score** — the current adoption score, tier, and drivers. See [ADOPTION_SCORE.md](../12_adoption_os/ADOPTION_SCORE.md).
8. **friction_summary** — count of friction events by kind (e.g., `missing_source_passport`, `missing_proof_pack`, `approval_overdue`).
9. **latest_monthly_value_report** — pointer to the latest monthly value report (retainer clients only) with summary counts by Value Ledger tier. See [VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md).
10. **next_action** — exactly one recommended next step for the workflow owner, computed deterministically (see below).

Each panel returns at minimum:

```json
{
  "status_badge": "green | amber | red | null",
  "summary": "1 short line",
  "data": { /* panel-specific */ }
}
```

The badge is always one of the four values. Badge selection is deterministic given the underlying data — two reads at the same moment from the same tenant return the same badges.

## Deterministic next_action priority — أولوية الإجراء التالي

The `next_action` panel never offers more than one action and never decides probabilistically. It applies a fixed priority order and returns the first match:

```
governance_block   > approval_pending > stale_draft > adoption_push > capability_gap
```

Mapping:

- **governance_block** — there is at least one open governance event of kind `BLOCK` or `ESCALATE` the client must resolve (e.g., attach a Source Passport to a stalled intake).
- **approval_pending** — there is at least one draft in `REQUIRE_APPROVAL` waiting for the workflow owner.
- **stale_draft** — there is a `DRAFT_ONLY` pack older than the configured staleness window with no approver action.
- **adoption_push** — adoption score is below the next tier threshold and a specific driver would move it.
- **capability_gap** — capability score has a specific gap (e.g., no named workflow owner, no Source Passport on a recent input) that the client can close in-workspace.

If none of the above apply, `next_action` returns `null` with a quiet summary ("nothing pending"). It does not invent work to look busy.

## Null-safety and friction events — الأمان عند نقص البيانات

Some panels depend on upstream artifacts (Proof Packs, Source Passports, scoring outputs) that may not exist yet for a new client. The workspace is **defensive**:

- If an upstream artifact is missing, the panel returns `data = null`, `status_badge = "null"`, and `summary` describes the missing dependency in one short line.
- The workspace also emits a `friction_log` event of the appropriate kind so the issue is visible in the operator review:

| Missing upstream | Friction event kind |
|------------------|---------------------|
| No Source Passport on a recent input | `missing_source_passport` |
| No Proof Pack at expected milestone | `missing_proof_pack` |
| No workflow owner registered | `missing_workflow_owner` |
| No adoption signal in current window | `missing_adoption_signal` |
| No governance decision log for an action | `missing_governance_trace` |

Null panels never throw, never block the response, and never invent placeholder data. A missing panel is treated as information ("the upstream did not produce this yet") and recorded for follow-up.

## Tenant isolation — العزل بين العملاء

The workspace is tenant-scoped. Isolation is enforced by `api/middleware/tenant_isolation.py`, which:

- Resolves `{handle}` to a tenant identity from an authenticated session.
- Rejects any read whose query path would cross tenant boundaries.
- Strips any panel field that, if leaked, would expose another tenant's data.

This middleware is the single boundary. Panel code is written assuming tenant isolation has already been applied.

## What the workspace is not — ما ليست هذه المساحة

- It is not a CRM. The workspace does not own contact records or pipeline stages; it surfaces Dealix outputs for client review.
- It is not a chat surface. Approvals, redactions, and decisions are explicit actions, not free-form messages.
- It is not infinite. Ten panels is the cap. New capabilities replace or merge panels rather than appending an eleventh.

## Cross-references

- [Source Passport](../04_data_os/SOURCE_PASSPORT.md), [Runtime Governance](../05_governance_os/RUNTIME_GOVERNANCE.md), [Proof Pack Standard](../07_proof_os/PROOF_PACK_STANDARD.md), [Value Ledger](../08_value_os/VALUE_LEDGER.md), [Adoption Score](../12_adoption_os/ADOPTION_SCORE.md).
- [Architecture Layer Map](../ARCHITECTURE_LAYER_MAP.md) — the `client_os` wrapper composes existing portal, inbox, and customer-success folders.
