# Dealix Responsible AI Workflow

كل سير عمل يتبع سلسلة واحدة قابلة للتدقيق:

```
Business problem
→ Use case card
→ Data source passport
→ Risk classification
→ Governance decision
→ AI-assisted output
→ Human review
→ Approval if needed
→ Audit log
→ Proof event
→ Monthly report
```

## مثال: Revenue Intelligence

| المحور | المحتوى |
|--------|---------|
| Problem | فرص مبيعات مبعثرة |
| Use case | Account scoring + مسودات متابعة |
| Risk | Medium — قد توجد حقول اتصال / PII |
| Governance | Draft-only؛ لا إرسال خارجي من Dealix |
| Proof | حسابات مُصنّفة، ازدواجيات، فرص عليا، إجراءات غير آمنة محجوبة |

## القاعدة

لا تخطّي خطوة في السلسلة عندما يكون المخرج **موجهًا للعميل** أو **خارجيًا** أو يحتوي PII.

## الكود

`auto_client_acquisition/responsible_ai_os/use_case_risk_classifier.py` + طبقات `governance_os` و`proof_architecture_os`.
