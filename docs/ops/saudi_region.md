# Saudi region — deployment runbook

When a customer's procurement requires that all PDPL-scoped data is
processed inside the Kingdom, this runbook moves the production stack
into a Saudi region. It does not replace `docs/ops/incident_response.md`
or `docs/sla.md`; it adds region-specific steps to the existing playbook.

## When this runbook applies

- An enterprise contract clause names a Saudi data-residency requirement.
- A regulator (CITC, SDAIA) requests evidence of in-Kingdom processing.
- A government tender (RFQ) requires Saudi-hosted infrastructure.

## Target architecture (1 line)

Replace Railway-hosted Postgres + Redis with **STC Cloud** *or*
**Mobily Cloud** *or* **AWS me-central-1 (Bahrain*** *region — Saudi
equivalence approved on a per-customer basis)*.

> AWS me-central-1 is physically in Bahrain. Some procurement teams
> accept it as Saudi-equivalent under the GCC data treaty; others
> require strictly in-Kingdom (STC / Mobily). Confirm per contract.

## Step-by-step migration

### 1. Decision gate (founder)

- Pick the target provider (STC / Mobily / AWS).
- Confirm sub-processor list update in `docs/sla.md` §8.
- Schedule the cutover window (Sun 02:00–04:00 Riyadh per maintenance
  policy).
- Notify affected customers ≥ 48 h in advance.

### 2. Provision (Platform)

- Apply Terraform overlay `infra/terraform/regions/saudi.tf` (TBD; this
  file lands when we first execute a migration).
- Provision Postgres 16 + Redis 7 in the target region.
- Mirror the existing Cerbos PDP container.
- Allocate a status page region: BetterStack monitor named
  `dealix-prod-sa`.

### 3. Data migration

- Snapshot prod Postgres via `scripts/infra/backup_pg.sh`.
- Restore the snapshot into the Saudi region via
  `scripts/infra/dr_restore_drill.sh DR_TARGET_DSN=...`.
- Set up logical replication from old → new for the cutover window so
  the gap is minutes, not hours.

### 4. DNS cutover

- Cloudflare `api.dealix.me` points at the Saudi region's load balancer
  via Terraform; TTL is reduced to 60s 24 h ahead of the cutover.
- BetterStack monitors hit both regions for 7 days post-cutover.

### 5. Compliance evidence

- Update `docs/compliance/CONTROLS.md` CC9.1 sub-processor list.
- Update `docs/sla.md` §8 with the new region row.
- Pull the latest `landing/trust/index.html` so the "Saudi region" pill
  on the trust page reflects the new state.
- Email the affected customers with the cutover confirmation.

### 6. Decommission

- Keep the old region read-only for 30 days as a fallback.
- After 30 days, run `terraform destroy` against the old region's
  workspace.

## Rollback

- Cloudflare DNS flip back to the old region (60s TTL).
- Replication direction reversed for any data written during the gap.
- Customer comms within 30 min.

## Sub-processor list — Saudi target

| Sub-processor | Purpose | Residency |
| --- | --- | --- |
| STC Cloud / Mobily Cloud / AWS me-central-1 | Postgres + Redis + object storage | Saudi Arabia / Bahrain (per-customer) |
| Existing entries (Anthropic, OpenAI, Resend, etc.) | unchanged | unchanged |

## Open items (founder)

- [ ] Pick the default provider (STC vs Mobily vs AWS me-central-1).
- [ ] Sign the relevant cloud-provider DPA.
- [ ] Source-control the Terraform overlay above (`saudi.tf`).
- [ ] Confirm that Anthropic / OpenAI per-customer routing complies
      with the customer's policy (we may need to disable certain
      models per-tenant).
