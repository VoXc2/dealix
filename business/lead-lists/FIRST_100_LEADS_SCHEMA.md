# First 100 Leads Schema

```json
{
  "id": "lead-001",
  "account_name": "string",
  "segment": "marketing_agency | training | clinic | real_estate | logistics | partner",
  "city": "string",
  "source_type": "open_data | csv_import | manual_research | website_signal | referral",
  "source_url_or_note": "string (URL or quote)",
  "visible_signal": "string",
  "weakness_hypothesis": "string",
  "recommended_offer": "diagnostic_sprint | revenue_os | command_center | delivery_os | review_reputation | custom_enterprise | managed_retainer",
  "score": 0,
  "review_status": "not_started | draft_pending_human_review | approved | rejected",
  "next_action": "string",
  "owner": "Founder",
  "demo": true
}
```

## قواعد
- لا profile لشخص طبيعي
- لا رقم هاتف أو إيميل شخصي في الـ schema
- الـ source_url_or_note إلزامي
- demo=true إلزامي إذا ما عندنا lead حقيقي
