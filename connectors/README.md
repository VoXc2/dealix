# Connectors (Dealix)

## Status
| Connector | Status | Demo? | Notes |
|-----------|--------|-------|-------|
| CSV import | Functional | yes | local file |
| Manual research | Functional | yes | founder-supplied |
| Website signal | Functional | yes | local file |
| Open data (SA) | Plan | yes | public aggregate only |
| HubSpot | Stub | no | needs OAuth review |
| Google Places | Stub | no | needs API key |
| WhatsApp Business | Stub | no | needs template approval |
| Email | Stub | no | needs SMTP/API key |

## Run
```bash
python3 connectors/csv_connector.py --file data/imports/sample_leads.csv --demo
python3 connectors/manual_research_connector.py --file data/imports/sample_leads.csv --demo
python3 connectors/website_signal_analyzer.py --file data/imports/sample_website_text.txt --demo
```

## Safety
- All connectors carry `human_review_required=True`
- All carry `auto_send_allowed=False`
- All write a source-audit report
