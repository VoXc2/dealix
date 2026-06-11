# Lead Source Connectors Spec (Dealix)

| Connector | Auto-Send | Inputs | Outputs | Required env | Status |
|-----------|-----------|--------|---------|--------------|--------|
| CSV import | No | local CSV | normalized leads | — | Implemented |
| Manual research | No | structured note | lead record | — | Implemented |
| Website signal (local file) | No | saved HTML/text | signal summary | — | Implemented |
| Open Data SA | No | public dataset URL | segment hypothesis | — | Implemented |
| Google Places | No | place id | public surface | GOOGLE_PLACES_API_KEY | Plan only |
| HubSpot CRM | No | portal id | deal sync | HUBSPOT_PRIVATE_APP_TOKEN | Plan only |
| WhatsApp Business | No | approved template id | send queue | WHATSAPP_BUSINESS_TOKEN | Plan only |
| Referral | No | written consent | lead record | — | Implemented |

## Universal rules
- No auto-send. Always draft first.
- Source note required for every lead.
- Rate-limit aware.
- Token rotation quarterly.
- No private data scraping.
