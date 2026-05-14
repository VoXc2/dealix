# Value Ledger — سجل القيمة

> Purpose: define the four-tier classification (Estimated, Observed, Verified, Client-Confirmed) that governs every value claim Dealix makes — internally, in proposals, and publicly. The Value Ledger is the layer that prevents Dealix from drifting into the "guaranteed sales outcomes" failure mode that the non-negotiables refuse.

A value claim is any number, percentage, multiple, or money figure that Dealix attributes to its work. Every such claim has a *tier* and a *source_ref*. Claims without both are blocked by governance. See [Runtime Governance](../05_governance_os/RUNTIME_GOVERNANCE.md).

## The four tiers — الطبقات الأربع

### 1. Estimated — تقديري

- **Definition:** a model-derived range produced by Dealix scoring, ranking, or simulation. Reflects what *could* happen given inputs and assumptions. Carries explicit uncertainty.
- **Required fields:**

```json
{
  "tier": "estimated",
  "value_range": {"low": 0, "high": 0, "unit": "SAR | accounts | %"},
  "assumptions": ["..."],
  "model_version": "ranker_vX.Y",
  "source_ref": "src_<ulid>",
  "computed_at": "<iso8601>"
}
```

- **External use:** **never**. Estimated values are internal-only. They may appear in proposals as a *modeled range with assumptions*, never as a claim.

### 2. Observed — مُلاحَظ

- **Definition:** a number measured inside Dealix workflows. Example: "120 accounts imported, 17 duplicates detected, 8 unsafe phrases redacted". The measurement happens at runtime, not in the world outside Dealix.
- **Required fields:**

```json
{
  "tier": "observed",
  "metric": "imported_accounts | duplicates_detected | drafts_generated | blocks_triggered",
  "value": 0,
  "unit": "count | % | seconds",
  "measured_in": "workflow_id",
  "source_ref": "src_<ulid>",
  "measured_at": "<iso8601>"
}
```

- **External use:** allowed in **internal reports and Proof Packs at tiers ≥ internal_learning**. Not yet a claim about client business outcomes. Wording is constrained: "Dealix observed X" — not "we generated X for the client".

### 3. Verified — مُتحقَّق

- **Definition:** a number cross-checked against client data outside Dealix. Example: a revenue lift cross-checked against the client's CRM closed-won records, or a meeting count cross-checked against the client's calendar export.
- **Required fields:**

```json
{
  "tier": "verified",
  "metric": "revenue_attributed | meetings_booked | accepted_drafts",
  "value": 0,
  "unit": "SAR | count | %",
  "verification_source": "client_crm_export | client_calendar_export | client_finance_record",
  "source_ref": "src_<ulid>",
  "verified_at": "<iso8601>",
  "anonymizable": true
}
```

- **External use:** allowed in **anonymized case studies and sales conversations**, subject to passport `external_use_allowed = true` on the verification source and the Proof Pack being in tier **case candidate** or **sales support**. See [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).

### 4. Client-Confirmed — مُعتمَد من العميل

- **Definition:** a Verified entry that the client has signed off on for named external use. This is the only tier that may be referenced as a *named* case study with the client's logo.
- **Required fields:**

```json
{
  "tier": "client_confirmed",
  "metric": "revenue_attributed | meetings_booked | accepted_drafts",
  "value": 0,
  "unit": "SAR | count | %",
  "verification_source": "...",
  "source_ref": "src_<ulid>",
  "client_confirmation_ref": "approval_<ulid>",
  "approver_identity": "name + role",
  "approved_at": "<iso8601>"
}
```

- **External use:** allowed as a **named case study**, subject to the standard governance gate on `publish.proof`.

## Tier progression — التدرّج

Tiers progress in one direction: Estimated → Observed → Verified → Client-Confirmed. They never regress, and a higher tier never invalidates a lower one — it supersedes it for the same metric.

```
Estimated         (model says it could be X)
  ↓ measurement inside Dealix
Observed          (Dealix workflows observed X)
  ↓ cross-check with client data outside Dealix
Verified          (cross-checked, anonymizable use)
  ↓ explicit client sign-off
Client-Confirmed  (named external use)
```

## The bilingual disclaimer — التنبيه

Every artifact that surfaces a value figure must carry the disclaimer in both languages when the figure is below Client-Confirmed:

> **Estimated value is not Verified value.**
>
> **القيمة التقديرية ليست قيمة مُتحقَّقة.**

The disclaimer is not decorative. It is part of the constitutional refusal to make guaranteed claims. See [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).

## Failure modes the Value Ledger blocks

- **Estimated promoted as Verified** — drafts that present a modeled range as a delivered outcome are downgraded by governance to `REDACT`.
- **Verified used externally without anonymization** — publish actions require either an anonymizable Verified entry or a Client-Confirmed entry.
- **Client-Confirmed without an approver identity** — entries missing `approver_identity` are rejected at intake.
- **Any tier without a `source_ref`** — rejected by `decide(action, context)`.

## Where Value Ledger entries appear

- **Proof Pack section 10 (Value Metrics).** Each project's pack lists every Value Ledger entry created in scope.
- **Monthly value report.** Retainer clients receive a monthly value report that summarizes entries by tier.
- **Sales material.** Only Verified (anonymized) and Client-Confirmed entries may appear in external sales material.

## Cross-references

- [Proof Pack Standard](../07_proof_os/PROOF_PACK_STANDARD.md) — section 10 is the Value Metrics section.
- [Source Passport](../04_data_os/SOURCE_PASSPORT.md) — every Value Ledger entry traces back to a passport.
- [Runtime Governance](../05_governance_os/RUNTIME_GOVERNANCE.md) — `decide(action, context)` consults Value Ledger tier before any external value claim.
