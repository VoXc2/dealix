# Trust Operations Model

```text
Discover → Classify → Govern → Approve → Execute → Log → Prove → Review → Improve
```

- **Discover:** بيانات، workflow، agent، model، قناة.  
- **Classify:** PII؟ مصدر؟ داخلي/خارجي؟ claim؟  
- **Govern:** تطبيق قرارات سياسة وقت التشغيل (انظر أدناه).  
- **Approve:** أي إجراء خارجي أو مخرج حساس.  
- **Execute:** AI يساعد، الإنسان يقرر.  
- **Log:** audit event لكل تشغيل وقرار وموافقة.  
- **Prove:** Proof Pack لكل مشروع.  
- **Review:** مخاطر، حوادث، قيمة، تبني.  
- **Improve:** risk → rule / test / checklist.

## قرارات الحوكمة (vocabulary في الكود)

`ALLOW` · `ALLOW_WITH_REVIEW` · `DRAFT_ONLY` · `REQUIRE_APPROVAL` · `REDACT` · `BLOCK` · `ESCALATE` — `GovernanceDecision` في `compliance_trust_os/approval_engine.py`.

**صعود:** [`COMPLIANCE_ARCHITECTURE.md`](COMPLIANCE_ARCHITECTURE.md)
