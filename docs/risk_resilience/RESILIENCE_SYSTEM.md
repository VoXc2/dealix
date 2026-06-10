# Resilience System

Dealix تُصمَّم لتحمّل صدمات تشغيلية شائعة:

1. **Client incident** — Detect → Contain → Notify → Correct → Log → Update rule/test/checklist  
2. **Model provider change** — LLM gateway · router · fallback · prompt registry · cost guard  
3. **Partner violation** — Suspend · audit · إخطار عملاء إن لزم · تحديث تدريب شركاء  
4. **Market slowdown** — تشخيصات · retainers · حوكمة enterprise · انضباط تكلفة  
5. **Governance failure** — إيقاف إجراءات خارجية · مراجعة حادث · سياسة · اختبار انحدار · Trust Pack  

**الكود:** `RESILIENCE_SHOCK_TYPES` · `governance_failure_playbook_steps` — `risk_resilience_os/resilience_playbooks.py`  
**حوادث العميل:** `CLIENT_INCIDENT_PHASES` — `risk_resilience_os/incident_response.py`

**صعود:** [`RISK_REGISTER.md`](RISK_REGISTER.md)
