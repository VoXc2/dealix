# PostHog — Marketing & Revenue Attribution Contract

> Canonical analytics contract for Dealix marketing and commercial attribution.
> Business truth comes from Revenue Mesh / evidence state. Analytics may observe it; analytics must never promote a state by itself.

## Current activation truth — 2026-08-28

- The connected PostHog project exists, but the current project reports no captured events in the last 30 days.
- Snippet onboarding is not complete.
- Therefore no acquisition/conversion dashboard is currently evidence-backed.
- Do not infer zero traffic or zero buyer interest from an inactive analytics pipeline.

## Commercial authority

Current buying path:

`Free Mini Diagnostic -> Qualified Discovery -> customer-specific quote -> 30-Day Revenue Command Pilot -> Proof -> Stop/Expand/Recurring`

Retired analytics concepts must not return:
- no `$1 pilot` funnel;
- no public checkout funnel;
- no `starter/growth/scale` public tiers;
- no fixed public pilot amount;
- no `checkout_success == verified revenue` shortcut.

## Privacy / data-minimization boundary

Before production activation, verify the actual data-flow, hosting region, consent/notice, retention, transfer basis and customer-specific obligations.

Client-side analytics must not send raw:
- email;
- phone;
- national ID;
- message body;
- form free text;
- secret/token;
- customer confidential data.

Anonymous browsing stays anonymous. Session recording is disabled by default for the public marketing surface. Person identification is not required for marketing attribution.

## Layer A — anonymous marketing telemetry

These events describe interaction, not commercial truth.

| Event | When | Minimum non-PII properties |
|---|---|---|
| `$pageview` | SDK page load | current URL, referrer (SDK) |
| `cta_clicked` | reviewed CTA click | `cta_id`, `page`, `destination`, `utm_*` when present |
| `qualified_visit` | only after an explicit, documented qualification rule; never every pageview | `source`, `channel`, `page`, `rule_version` |
| `diagnostic_start` | first real interaction with the Mini Diagnostic | `source`, `channel`, `page`, optional non-PII segment |
| `diagnostic_submit` | Mini Diagnostic accepted | `source`, `channel`, optional non-PII segment, `diagnostic_id` |

`qualified_visit` is intentionally not automatic. Bot filtering, visit depth, or an approved qualification rule must be defined before emitting it.

## Layer B — evidence-backed commercial events

These events are emitted only from the canonical evidence/revenue state or a verified adapter. A browser click cannot create them.

| Event | Truth requirement | Required references |
|---|---|---|
| `real_interaction` | real two-way/in-person/inbound interaction evidence | `evidence_id`, `source`, `channel` |
| `verified_relationship` | relationship promotion passed Truth Firewall | `relationship_id`, `evidence_id`, `provenance` |
| `qualified_problem` | qualified buyer problem with source/evidence | `opportunity_id`, `relationship_id`, `evidence_id` |
| `discovery_booked` | booking/commitment evidence | `opportunity_id`, `evidence_id`, `source` |
| `discovery_completed` | actual completed discovery evidence | `opportunity_id`, `evidence_id` |
| `proposal_sent` | actual delivery/send receipt, not a draft | `opportunity_id`, `proposal_id`, `delivery_evidence_id` |
| `pilot_agreed` | customer agreement evidence | `opportunity_id`, `agreement_evidence_id` |
| `payment_verified` | verified payment evidence | `opportunity_id`, `payment_evidence_id`, `amount_sar` |
| `delivery_proof` | customer delivery/outcome proof | `opportunity_id`, `proof_id` |
| `referral` | verified referral event | `relationship_id`, `evidence_id` |
| `expansion` | verified expansion/renewal agreement | `opportunity_id`, `evidence_id` |

## Truth invariants

- `pageview != qualified_visit`
- `directory_record != real_interaction`
- `research != verified_relationship`
- `draft != proposal_sent`
- `provider_accepted != delivered`
- `invoice != payment_verified`
- `synthetic_demo != delivery_proof`
- `analytics_event != authority_to_change_revenue_state`

## Attribution dimensions

Use only when known and source-bound:
- `source`
- `channel`
- `campaign`
- `content`
- `event_name`
- `language`
- `page`
- `offer`
- `account_scope_id` (pseudonymous/internal identifier only)
- `opportunity_id`
- `evidence_id`

UTM convention:

`utm_source / utm_medium / utm_campaign / utm_content / utm_term`

Event campaigns should use stable identifiers such as `big5_2026_aug`, `leap_2026`, `deepfest_2026`, not ad-hoc prose.

## Canonical funnels

### Funnel A — Discover -> Diagnostic
1. `qualified_visit`
2. `diagnostic_start`
3. `diagnostic_submit`

### Funnel B — Relationship -> Discovery
1. `real_interaction`
2. `verified_relationship`
3. `qualified_problem`
4. `discovery_booked`
5. `discovery_completed`

### Funnel C — Discovery -> Verified money
1. `discovery_completed`
2. `proposal_sent`
3. `pilot_agreed`
4. `payment_verified`

### Funnel D — Proof -> Compounding distribution
1. `payment_verified`
2. `delivery_proof`
3. `referral` and/or `expansion`

## Dashboard activation gate

Do not create/pin a production acquisition dashboard until:
1. `$pageview` or equivalent public telemetry is observed in PostHog;
2. at least `cta_clicked` and diagnostic events are observed from the intended public origin;
3. test/internal traffic can be identified and excluded;
4. source/UTM properties are verified from captured schema;
5. business events remain server/evidence-backed.

Once active, dashboard order is:
1. Public acquisition and CTA movement.
2. Diagnostic funnel.
3. Relationship/discovery funnel.
4. Discovery-to-payment funnel.
5. Proof/referral/expansion.

North Star remains `FIRST VERIFIED PAID DEALIX PILOT`; analytics does not redefine revenue truth.
