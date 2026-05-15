# Dealix AI Use Case Risk Classifier

كل use case داخل العميل **يجب أن يُصنّف** قبل التشغيل.

## مستويات المخاطر

### Low Risk

- تلخيص داخلي  
- محتوى **مسودة فقط** غير حساس  
- تقارير غير حساسة  

### Medium Risk

- مسودات مواجهة للعميل  
- تحليل يحتوي PII  
- توصيات تؤثر على قرارات  

### High Risk

- تواصل خارجي  
- قرارات مالية/امتثال  
- بيانات شخصية حساسة  
- سير عمل آلي ذو أثر مباشر  

### Forbidden / Not Supported

- أنظمة كشط (scraping)  
- أتمتة واتساب باردة  
- أتمتة لينكدإن  
- ادّعاءات مبيعات مضمونة  
- قرار بلا مصدر (source-less decisioning)  

## Use Case Card (مرجع JSON)

```json
{
  "use_case_id": "UC-001",
  "name": "Revenue account scoring",
  "department": "Sales",
  "data_sources": ["SRC-001"],
  "contains_pii": true,
  "risk_level": "medium",
  "human_oversight": "required",
  "external_action_allowed": false,
  "governance_decision": "DRAFT_ONLY",
  "proof_metric": "accounts_scored_and_prioritized"
}
```

## القواعد

- **No use case without risk classification.**  
- **No high-risk use case without governance review.**  
- **No external action without approval.**

## الكود

`auto_client_acquisition/responsible_ai_os/use_case_risk_classifier.py`
