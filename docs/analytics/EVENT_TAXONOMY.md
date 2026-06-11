# Event Taxonomy (Dealix)

```json
{
  "events": [
    {"name": "page_view", "props": ["path", "locale"]},
    {"name": "cta_click", "props": ["cta_id", "source_page"]},
    {"name": "sales_pack_download", "props": ["format"]},
    {"name": "ceo_brief_download", "props": ["format"]},
    {"name": "proposal_generated", "props": ["account_id", "offer"]},
    {"name": "lead_imported", "props": ["count"]},
    {"name": "draft_reviewed", "props": ["reviewer", "decision"]},
    {"name": "proof_report_generated", "props": ["account_id"]}
  ],
  "no_pii": true,
  "consent_required": false
}
```
