# Scope

## Included

- ICP analysis and lead-machine design
- lead scoring and data enrichment model
- outbound strategy and Arabic sales messaging library
- WhatsApp and Email follow-up workflows, draft-first with approval points
- CRM pipeline build and AI-assisted follow-up cadence
- executive revenue dashboard
- monthly Proof Pack and ROI report during the retainer

## Excluded

- scraping or bulk data harvesting from any source
- cold WhatsApp outreach
- LinkedIn automation
- automatic external sending without explicit client approval
- bulk blasts to unconsented lists
- guaranteed meeting, conversion or sales counts
- CRM licenses or third-party tool fees (billed by the client)

## Action Mode

`approval_required`. Every external-facing message is generated as a draft and
sent only after the client approves it. Hard gates enforced: `no_live_send`,
`no_live_charge`, `no_cold_whatsapp`, `no_linkedin_auto`, `no_scraping`,
`no_fake_proof`, `no_fake_revenue`, `no_blast`.

See also: [`offer.md`](offer.md) · [`delivery_checklist.md`](delivery_checklist.md)
