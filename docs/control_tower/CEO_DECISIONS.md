# CEO Decisions — لوحة القرار (v2)

## أقسام مقترحة

1. CEO Decisions  
2. Revenue Health  
3. Delivery Health  
4. Productization Queue  
5. Governance Risk  
6. Proof Strength  
7. Capital Creation  
8. Client Expansion  
9. Unit Maturity  
10. Venture Signals  

## أمثلة قرارات تظهر للمراجعة

- Scale this offer.  
- Raise price here.  
- Stop this service.  
- Productize this manual step.  
- Offer retainer to this client.  
- Promote this unit.  
- Investigate this risk.  

### مثال JSON

```json
{
  "decision": "PRODUCTIZE",
  "target": "proof_report_generation",
  "reason": "Repeated 5 times, saves 3h/project, used across all sprints",
  "expected_impact": "delivery margin +12%",
  "priority": "high"
}
```

**محرك النقاط:** `intelligence_os/strategy_decision.py` · **الخوارزميات:** [`../intelligence/OPERATING_ALGORITHMS.md`](../intelligence/OPERATING_ALGORITHMS.md)

**قاعدة:** كل قرار تنفيذي خارجي يبقى **بموافقة** حسب الدستور.
