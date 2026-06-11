# V7 CRM Sync Architecture (Dealix)

## Modes
1. **Local JSON** (default) — `business/_data/*.json`
2. **CSV export** — `scripts/export_crm_csv.py`
3. **HubSpot sync** (planned) — OAuth, read-only, owner-side
4. **Salesforce sync** (future) — same pattern

## Field mapping
| Dealix | HubSpot | Salesforce |
|--------|---------|------------|
| account.id | contact.id | Contact.Id |
| account.name | contact.firstname + lastname | Contact.Name |
| account.segment | contact.industry | Contact.Industry |
| account.score | contact.deal_score__c | Custom |
| account.stage | deal.stage | Opportunity.StageName |
| account.reviewStatus | contact.review_status__c | Custom |
| account.sourceNote | contact.source_note__c | Custom |
| account.demo | contact.is_demo__c | Custom |

## Sync direction
- **Outbound** (Dealix → CRM): only on approve, only on demand
- **Inbound** (CRM → Dealix): via OAuth, only deals the founder owns
- No two-way sync for first version

## Safety
- Sync requires explicit `--sync` flag
- Sync writes audit log
- Sync never overrides local data without confirmation
