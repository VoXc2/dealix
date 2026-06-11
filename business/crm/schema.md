# CRM Schema (Dealix)

## File: `business/_data/leads.json`
```json
{
  "accounts": [
    {
      "id": "acc-001",
      "name": "string",
      "segment": "marketing_agency | training | clinic | real_estate | logistics | consulting | b2b_services | retail",
      "city": "string",
      "sourceType": "open_data | csv_import | manual_research | website_signal | google_places | hubspot | whatsapp_business | referral",
      "sourceNote": "string (URL or quote)",
      "visibleSignal": "string",
      "weaknessHypothesis": "string",
      "recommendedOffer": "diagnostic_sprint | revenue_os | command_center | delivery_os | review_reputation | custom_enterprise | managed_retainer",
      "score": 0,
      "stage": "new | qualified | drafted | review | meeting | proposal | won | lost | retainer",
      "owner": "string",
      "reviewStatus": "draft_pending_human_review | approved | rejected | not_started",
      "demo": true,
      "createdAt": "YYYY-MM-DD",
      "nextAction": "string",
      "nextActionDate": "YYYY-MM-DD",
      "monthlyValue": 0,
      "setupValue": 0
    }
  ]
}
```

## File: `business/_data/outreach_review_queue.json`
```json
{
  "drafts": [
    {
      "draftId": "draft-001",
      "accountId": "acc-001",
      "language": "ar | en",
      "channel": "whatsapp | email | linkedin",
      "tone": "executive",
      "opener": "string",
      "followUp1": "string",
      "followUp2": "string",
      "reviewStatus": "draft_pending_human_review",
      "generatedAt": "YYYY-MM-DD",
      "reviewer": null,
      "reviewedAt": null,
      "rejectionReason": null
    }
  ]
}
```

## File: `business/_data/proposals.index.json`
```json
{
  "proposals": [
    {
      "id": "prop-001",
      "accountId": "acc-001",
      "offer": "revenue_os",
      "lang": "ar | en | both",
      "timeline": "21 days",
      "setupPrice": 0,
      "monthlyPrice": 0,
      "status": "draft | sent | accepted | rejected",
      "createdAt": "YYYY-MM-DD"
    }
  ]
}
```

## File: `business/_data/deals.ledger.json`
```json
{
  "deals": [
    {
      "id": "deal-001",
      "accountId": "acc-001",
      "status": "won | lost | open",
      "value": 0,
      "monthlyRecurring": 0,
      "closedAt": "YYYY-MM-DD",
      "reason": "string",
      "demo": true
    }
  ]
}
```
