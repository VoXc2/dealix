# Company Growth Beast — جدول أدلة

| ادعاء | دليل في الريبو | ملاحظة |
|--------|-----------------|--------|
| مسارات API موجودة | `api/routers/company_growth_beast.py` | جرب `/status` |
| منطق حتمي قابل للاختبار | `auto_client_acquisition/company_growth_beast/*.py` | بدون LLM |
| بوابات عدم الإرسال الحي | `command_center.blocked_actions` + `compliance_action` | مزدوج |
| عدم تزييف الإثبات | `proof_loop.no_fake_metrics` + سياسة العرض | لا أرقام وهمية |
| عربي أولاً | حقول `*_ar` و`language_primary` | — |
| حزمة تحقق | `scripts/company_growth_beast_verify.sh` | CI محلي |

املأ أعمدة «تشغيل إنتاج» و«عميل حقيقي» يدوياً بعد أول طلعة على `api.dealix.me`.
