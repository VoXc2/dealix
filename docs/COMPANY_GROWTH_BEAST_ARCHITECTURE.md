# Company Growth Beast — معمارية

## المكان في المنظومة

```
Experience (واجهة شركة بسيطة)
        ↓
company_growth_beast (مسودات + ترتيب + تقارير)
        ↓
V12 OS modes / V10 modules (growth_v10, sales_os, support_os, delivery, proof_ledger, compliance, executive, self_improvement, role_command_os, …)
```

## مبادئ

- **تحليل ذاتي (deterministic)** في هذه النسخة: بدون LLM داخل الحزمة لتبقى قابلة للاختبار والتدقيق.
- **Arabic-first**: الحقول العربية هي المرجع للعميل؛ الإنجليزية ثانوية في الـschemas حيث ينطبق.
- **Proof-first**: لا أرقام أو شهادات بدون أحداث proof وموافقة.
- **Service wrapper**: لا يكرر CRM أو الـinbox؛ يوجّه للمسارات الموجودة في الـAPI الجذرية عند الحاجة.

## الملفات

| جزء | مسار |
|-----|------|
| منطق الخدمة | `auto_client_acquisition/company_growth_beast/` |
| REST | `api/routers/company_growth_beast.py` |
| تحقق | `scripts/company_growth_beast_verify.sh` |

## تخزين الجلسة

`session_store.py` يحفظ في الذاكرة فقط لبيئة API long-running؛ للاختبار يُستدعى `reset_all()`.
