# Company Brain — Spec & Status

> No new tables added. The "Company Brain" is a logical composite over
> the existing schema. This doc maps the spec → existing models, and
> documents what's wired vs. what's not.

## Logical model

```
CompanyBrain[company_id] := {
  identity:       CompanyRecord
  prospects:      LeadRecord[]
  deals:          DealRecord[]
  meetings:       TaskRecord[type='meeting']
  service_session: ServiceSession (deploy branch — services router)
  proof_events:   ProofEvent[] (deploy branch — proof_ledger)
  invoices:       MoyasarInvoice / payments artifacts
  consent:        ConsentRecord / SuppressionRecord
  next_actions:   command-center/next-best-action + revenue-os/copilot/actions
  forbidden:      tone profile in CompanyRecord.tone_of_voice
  channels:       CompanyRecord.channel_plan
}
```

## Field-by-field map (verified on prod or local)

| Brain field | Source | Endpoint to read | Status |
| --- | --- | --- | --- |
| `company_name` | `CompanyRecord.name` | `POST /api/v1/companies/intake` returns id, fetch via internal | PROVEN_LIVE |
| `website` | `CompanyRecord.website` | same | PROVEN_LIVE |
| `sector` | `CompanyRecord.industry` | same | PROVEN_LIVE |
| `city` | `CompanyRecord.city` | same | PROVEN_LIVE |
| `offer` | `CompanyRecord.products` (or `target_customer_type`) | same | PROVEN_LIVE |
| `ICP` | `CompanyRecord.icp_profile` (auto-derived in intake) | same | PROVEN_LIVE |
| `language preference` | locale on inbound (auto-detected) | `POST /api/v1/prospect/inbound/*` | PROVEN_LOCAL |
| `tone preference` | `CompanyRecord.tone_of_voice` (default `professional_khaliji`) | intake | PROVEN_LIVE |
| `approved channels` | `CompanyRecord.channel_plan.auto_send_allowed` | intake | PROVEN_LIVE |
| `blocked channels` | `CompanyRecord.channel_plan.human_required` + `whatsapp_cold:"blocked"` | intake | PROVEN_LIVE |
| `consent records` | `ConsentRecord` + `SuppressionRecord` | `compliance/check-outreach` reads them | PROVEN_LOCAL |
| `current service` | `ServiceSession` (deploy branch) | `POST /api/v1/operator/service/start` | PROVEN_LIVE |
| `open decisions` | `command-center/snapshot.today_decisions` | `GET /api/v1/v3/command-center/snapshot` | PROVEN_LIVE |
| `proof summary` | `command-center/proof-pack` + `proof-ledger/customer/{id}/pack` | both endpoints | PROVEN_LIVE (deploy) / PROVEN_LOCAL |
| `past objections` | `objections/bank` (sector-keyed) | `GET /api/v1/objections/bank` | PROVEN_LIVE |
| `next best actions` | `command-center/next-best-action` + `revenue-os/copilot/actions` | both | PROVEN_LIVE |
| `forbidden claims` | tone in `personal-operator/messages/draft` (no "guaranteed" / "نضمن") | the draft endpoint | PROVEN_LIVE |

## What's NOT a single endpoint

There is no single `GET /api/v1/companies/{id}/brain` aggregator that
returns ALL fields together. The deploy branch composes them through
multiple routers. Whether to add a unified read endpoint is a UX call —
the data is already there.

**Recommendation:** if a unified brain read becomes necessary, add a
thin aggregator endpoint on the deploy branch that joins the above. Do
NOT create a new "brain" table — that would duplicate state and is
forbidden by the no-new-features rule.

## Gaps (BACKLOG)

1. No explicit `language_preference` column on `CompanyRecord` — the
   intake currently stores `languages: "ar,en"` as a comma-list. Could
   tighten to `language_preference ENUM('ar_sa','ar_msa','en','mixed')`.
2. No explicit `meetings` aggregator — tasks are keyed by type but not
   filterable as `meeting_history` from a single endpoint.
3. No HMAC signature on the proof pack response — see Service Tower
   matrix gap §2.
