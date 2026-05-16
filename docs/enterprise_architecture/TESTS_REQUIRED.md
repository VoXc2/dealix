# Tests Required — عقود الحماية في الكود

تحويل فلسفة Dealix إلى **اختبارات تمنع الانحراف** (regression على السياسات).

## قائمة الاختبارات (الاسم المستهدف → التنفيذ في الريبو)

| الاختبار | الغرض | ملف / ملاحظة |
|----------|--------|----------------|
| `test_no_source_passport_no_ai` | لا AI على بيانات بلا جواز صالح | `tests/test_no_source_passport_no_ai.py` |
| `test_pii_external_requires_approval` | PII + استخدام خارجي يتطلب مسار موافقة | `tests/test_pii_external_requires_approval.py` |
| `test_no_cold_whatsapp` | لا واتساب بارد | `tests/test_no_cold_whatsapp.py` |
| `test_no_linkedin_automation` | لا أتمتة لينكدإن | `tests/test_no_linkedin_automation.py` |
| `test_no_scraping_engine` | لا محرك كشط كمصدر تشغيل | `tests/test_no_scraping_engine.py` |
| `test_no_guaranteed_claims` | لا ادّعاءات ضمان وهمية | `tests/test_no_guaranteed_claims.py` |
| `test_output_requires_governance_status` | مخرجات حساسة تتطلب حالة حوكمة / جواز قرار | `tests/test_output_requires_governance_status.py` |
| `test_proof_pack_required` | اكتمال أقسام Proof Pack | `tests/test_proof_pack_required.py` |
| `test_agent_autonomy_mvp_limit` | سقف الاستقلالية في الـ MVP | `tests/test_agent_autonomy_mvp_limit.py` |
| `test_case_study_requires_verified_value` | دراسة حالة تتطلب verified + إذن | `tests/test_case_study_requires_verified_value.py` |

## اختبارات موجودة مسبقًا (لا تكرر المنطق)

- `tests/test_no_source_no_answer.py` — سياسة المعرفة بدون مصادر.
- `tests/` يحتوي اختبار قفل repo يمنع ظهور سلسلة استخراج بيانات LinkedIn الممنوعة في أيّ ملف متتبَّع (راجع مجلّد الاختبارات لاسم الملف الدقيق).
- `tests/test_proof_architecture_os.py` — proof score و case study.
- `tests/test_risk_resilience_os.py` — `claim_may_appear_in_case_study`.

## تشغيل سريع

```bash
APP_ENV=test pytest tests/test_no_source_passport_no_ai.py tests/test_pii_external_requires_approval.py tests/test_no_cold_whatsapp.py tests/test_no_linkedin_automation.py tests/test_no_scraping_engine.py tests/test_no_guaranteed_claims.py tests/test_output_requires_governance_status.py tests/test_proof_pack_required.py tests/test_agent_autonomy_mvp_limit.py tests/test_case_study_requires_verified_value.py -q --no-cov
```
