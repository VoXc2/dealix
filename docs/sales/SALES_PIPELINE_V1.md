# Sales Pipeline v1

## Stages

1. Targeted  
2. Researched  
3. Contact Drafted  
4. Contacted Manually  
5. Discovery Booked  
6. Diagnostic Proposed  
7. Diagnostic Paid  
8. Sprint Proposed  
9. Sprint Paid  
10. Pilot Proposed  
11. Retainer Won  
12. Lost / Nurture  

## Required fields

- company_name  
- sector  
- city  
- pain_hypothesis  
- offer_fit  
- source  
- relationship_status  
- next_action  
- owner  
- last_touch  
- compliance_status  

## Rules

```text
Any lead without source or next_action = not ready.
Any external touch = manual, consented, and reviewable.
```

See also: [`CRM_PIPELINE_SCHEMA.md`](../growth/CRM_PIPELINE_SCHEMA.md), [`SALES_PLAYBOOK.md`](SALES_PLAYBOOK.md).
