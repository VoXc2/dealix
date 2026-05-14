# Source Passport — جواز المصدر

> Purpose: define the schema that binds every input entering Dealix to a verifiable origin, owner, allowed use, and retention rule. Without a Source Passport, an input cannot be ingested, scored, drafted from, or proven.

A Source Passport is the smallest unit of data clarity in Dealix. Every CSV, CRM export, manual list, partner feed, or licensed dataset must carry one. The passport is created at intake and travels with the data through every downstream workflow — ranking, drafting, governance, proof, value, capital.

## Schema — البنية

```json
{
  "source_id": "src_<ulid>",
  "source_type": "client_upload | crm_export | manual_entry | partner_data | licensed_dataset",
  "owner": "client | dealix | partner",
  "allowed_use": ["internal_analysis", "draft_only", "reporting", "scoring"],
  "contains_pii": true,
  "sensitivity": "low | medium | high",
  "ai_access_allowed": true,
  "external_use_allowed": false,
  "retention_policy": "project_duration | retainer_duration | anonymize_after_close | delete_after_close"
}
```

Field semantics:

- **source_id** — opaque identifier, generated at intake. Every downstream artifact (ranked account, draft, proof item, value entry, capital asset) carries this `source_id` as `source_ref`.
- **source_type** — one of five enumerated values. Anything else, including `scraped`, is rejected.
- **owner** — who legally controls the data. Most often `client`.
- **allowed_use** — a list, subset of the four use modes. Drafting outreach requires `draft_only`. Ranking requires `scoring`. Reports require `reporting`.
- **contains_pii** — boolean. If `true`, downstream actions inherit PII handling rules and middleware redaction.
- **sensitivity** — qualitative tier used by governance to choose between `ALLOW`, `ALLOW_WITH_REVIEW`, `REQUIRE_APPROVAL`, and `BLOCK`.
- **ai_access_allowed** — whether the data may be sent to any AI model for analysis or drafting. If `false`, only deterministic workflows may touch it.
- **external_use_allowed** — whether output derived from this source may leave Dealix systems (e.g., publish, share with a third party, include in a public case study).
- **retention_policy** — when the data must be deleted, anonymized, or retained.

## Allowed source types — الأنواع المقبولة

| source_type | Meaning | Example |
|-------------|---------|---------|
| `client_upload` | Client uploads a file they own | CSV of existing accounts |
| `crm_export` | Export from a CRM the client owns | HubSpot, Salesforce, Zoho export |
| `manual_entry` | Client types entries into the workspace | Hand-curated account list |
| `partner_data` | Data shared by an explicit partner with rights | Co-marketing partner list |
| `licensed_dataset` | A dataset Dealix or client has license to use | Industry registry under license |

Anything outside this list — including web scraping, social media harvests, leaked databases, and "found" lists — is refused at intake. This is enforced by the constitutional non-negotiable on scraping. See [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).

## Decision matrix — مصفوفة القرار

The passport feeds the runtime governance layer. The base matrix at intake is:

| Condition | Decision |
|-----------|----------|
| No passport attached | `BLOCK` — no ingestion without a passport |
| Unknown or unsupported `source_type` | `BLOCK` — only the five enumerated types are accepted |
| `contains_pii = true` AND `external_use_allowed = true` | `REQUIRE_APPROVAL` — explicit human approval before any external action |
| `contains_pii = true` AND `retention_policy = project_duration` | `ALLOW_WITH_REVIEW` — proceed, but flag for retention review at project close |
| `ai_access_allowed = false` | drafts and AI-derived analysis are disabled for this source |
| `external_use_allowed = false` | public proof and external sharing are disabled for derived artifacts |

Downstream layers may *narrow* the decision further (e.g., a draft destined for WhatsApp is downgraded to `DRAFT_ONLY` even if the passport allowed `draft_only`). Downstream layers never *widen* a decision. The passport sets the ceiling.

## Lifecycle — دورة الحياة

1. **Intake** — client provides input and declares passport fields. The system validates the declaration.
2. **Bind** — `source_id` is attached to the ingested data and inherited by every derived artifact as `source_ref`.
3. **Use** — every governance decision references the passport. Every draft, score, and proof item records the passport's `source_id`.
4. **Review** — the passport is shown in the workspace, in the Proof Pack section "Source Passports", and in the Value Ledger entries.
5. **Close** — at project or retainer close, the retention policy executes: anonymize, delete, or retain per declared rule.

## What a passport is not — ما ليس جواز المصدر

- It is not a consent record. Consent (e.g., WhatsApp opt-in) is a separate object tied to specific recipients.
- It is not a licensing contract. Licensing lives in legal documents; the passport encodes the operational interpretation.
- It is not optional metadata. It is the precondition for any AI or external action.

## Cross-references

- [Runtime Governance](../05_governance_os/RUNTIME_GOVERNANCE.md) — how `decide(action, context)` reads the passport.
- [Proof Pack Standard](../07_proof_os/PROOF_PACK_STANDARD.md) — section 4 is "Source Passports", listing every passport used.
- [Value Ledger](../08_value_os/VALUE_LEDGER.md) — every value entry carries a `source_ref` that traces back to a passport.
