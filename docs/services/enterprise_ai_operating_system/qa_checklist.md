# QA Checklist

## Before every phase gate

- [ ] phase deliverables match the [`delivery_checklist.md`](delivery_checklist.md)
- [ ] no auto-send or auto-charge enabled (action mode is approval-required)
- [ ] hard gates intact: `no_live_send`, `no_live_charge`, `no_cold_whatsapp`, `no_linkedin_auto`, `no_scraping`, `no_blast`
- [ ] no fabricated proof or revenue figures (`no_fake_proof`, `no_fake_revenue`)
- [ ] forbidden terms absent from user-facing copy (e.g. guaranteed / نضمن)
- [ ] risk register updated with any new items
- [ ] gate sign-off recorded with date and approver

## Company Brain checks

- [ ] every answer carries a source citation
- [ ] PII handling and access controls documented
- [ ] knowledge sources have an owner and refresh cadence

## Agent checks

- [ ] all agent output is draft-first and routed to an approver
- [ ] append-only audit trail captures each draft and decision
- [ ] rollback path documented per agent

## Before handoff

- [ ] all 6 phase gates signed off
- [ ] dashboards verified against the value ledger
- [ ] governance policy pack delivered and acknowledged
- [ ] Scale Plan and retainer scope agreed in writing
