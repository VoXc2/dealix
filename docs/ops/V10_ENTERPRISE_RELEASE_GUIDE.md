# V10 Enterprise Release Guide (Dealix)

## What's in V10
- Enterprise readiness pack (8 docs)
- Observability plan
- Incident response runbook
- Data room V2 (11 docs)
- Demo pack (AR + EN)
- Master runner V10 (12 steps)

## How to use

### For investors / partners
- Send the data room link
- Reference `business/data-room/DATA_ROOM_INDEX.md`
- Send `business/enterprise/ENTERPRISE_BUYER_FAQ_AR.md` (or EN)

### For ops
- `python3 scripts/generate_health_snapshot.py` — daily health
- `python3 scripts/dealix_v10_run_all.py` — full check
- `python3 scripts/incident_report_template.py --severity P0 --summary "..."` — log incident

### For demos
- `python3 scripts/generate_demo_pack.py --lang both`
- Use `business/demo/DEALIX_DEMO_SCRIPT_AR.md` (or EN)
- After call: log in CRM, send one-pager, follow up within 48h

## Known limitations
- No 2FA / SSO yet
- Demo data still demo
- Connectors are stub (HubSpot, Google Places, WhatsApp, Email)
- Postgres migration not auto-run (V11)
