# أولويات P0 لجاهزية Enterprise — مستخرجة من خريطة الفجوات

**المصدر الرئيسي:** [docs/v10/DEALIX_CAPABILITY_GAP_MAP.md](../v10/DEALIX_CAPABILITY_GAP_MAP.md)  
**بوابات الإصدار:** [dealix/masters/release_readiness_checklist.md](../../dealix/masters/release_readiness_checklist.md)

هذا المستند **لا يستبدل** خريطة الفجوات؛ يحدد ترتيب التنفيذ المقترح لخدمة شركات تتوقع استمرارية وتدقيقاً وتعدد مستأجرين لاحقاً.

## ترتيب P0 المقترح (تراكمي)

| الأولوية | الطبقة | الوحدة المقترحة (من الخريطة) | لماذا للـ Enterprise |
|----------|--------|--------------------------------|----------------------|
| **P0-1** | Workflow OS | `auto_client_acquisition/workflow_os_v10/` — retry، idempotency، checkpoint | Pilot لا ينهار عند إعادة تشغيل الخادم؛ مطلوب لمصداقية التسليم |
| **P0-2** | AI Workforce | `auto_client_acquisition/ai_workforce_v10/` — Reviewer + Planner + ذاكرة ضمن حدود عميل | تقليل أخطاء الوكلاء؛ فصل مراجعة قبل ComplianceGuard؛ PDPL عبر حدود الذاكرة |
| **P0-3** | Platform | `auto_client_acquisition/platform_v10/` — عقود `tenant_contract` + `rls_contract` (بدون استبدال المكدس) | تمهيد multi-tenant وRLS دون كسر الإنتاج الحالي |
| **P0-4** | CRM / RevOps | `auto_client_acquisition/crm_v10/` (حسب الخريطة §3) | حسابات ولجان شراء وتسلسل مراحل — بعد الثبات في workflow |

## أساس موجود اليوم (لا يُعاد اختراعه)

- **عزل المستأجر على مستوى الطلب:** [api/middleware/tenant_isolation.py](../../api/middleware/tenant_isolation.py) (حقن `tenant_id` — يجب أن تلتزم به المستودعات).
- **تدقيق مسارات بيانات شخصية:** [api/middleware/http_stack.py](../../api/middleware/http_stack.py) (`AuditLogMiddleware` / PDPL Article 18 في التعليقات).
- **عقود منصة مرجعية (بدون استبدال المكدس):** [auto_client_acquisition/platform_v10/](../../auto_client_acquisition/platform_v10/) — `tenant` / `rls` / `storage` / `auth` كعقود Pydantic + Protocol؛ راجع `tests/test_platform_v10.py`.

## بوابات إثبات (Evidence gates) — مأخوذة من الخريطة

- **Workflow:** إعادة تشغيل أثناء Pilot لا تفقد الحالة؛ نفس `idempotency_key` لا يضاعف الأثر.
- **AI Workforce:** Reviewer بعد كل وكيل رئيسي وقبل ComplianceGuard؛ لا تسرّب ذاكرة عبر عملاء.
- **Platform:** العقود تُتحقق باختبارات وحدات دون فرض Postgres replacement.

## ربط checklist الإصدار

قبل ادّعاء «جاهزية enterprise» في العقود أو `no_overclaim`:

- اجتياز بنود **Security** و **Quality gates** و **Build & deploy** في [release_readiness_checklist.md](../../dealix/masters/release_readiness_checklist.md).
- أي ميزة جديدة حساسة: تسجيل في [dealix/registers/no_overclaim.yaml](../../dealix/registers/no_overclaim.yaml) مع حالة ومسار أدلة.

## ما يبقى مرحلة لاحقة (من نموذج التشغيل)

- Temporal أو بدائل workflows طويلة الأمد بالكامل (Phase E في الخريطة).
- OAuth وتكاملات خارجية «حقيقية» حسب قرار المؤسس §S6/S7.

## تجربة «الأفضل في السوق» مقابل الدين التقني

التمييز التجاري (سلّم خدمات، Proof، ثقة سعودية) يعمل بشكل أقوى عندما لا ينهار التشغيل تحت الضغط:

| طموح السوق | دين تقني يُغلق عبر P0 أعلاه |
|-------------|------------------------------|
| Pilot ومبيعات دون فقدان حالة | **P0-1** Workflow OS — checkpoints + idempotency |
| وكلاء أذكى دون تسرب بيانات | **P0-2** AI Workforce v10 — reviewer + حدود ذاكرة عميل |
| عدة شركات على منصة واحدة | **P0-3** عقود tenant + مسار RLS |
| لجان شراء وحسابات معقّدة | **P0-4** CRM v10 — بعد استقرار الـ workflow |

**الخلاصة:** الوثائق الاستراتيجية ([DEALIX_ROLE_SERVICE_LADDER_AR.md](DEALIX_ROLE_SERVICE_LADDER_AR.md)، [DEALIX_MARKET_DIFFERENTIATION_AR.md](DEALIX_MARKET_DIFFERENTIATION_AR.md)) تشرح *ماذا تبيع*؛ هذا القسم يربط *لماذا P0 ضروري لتحمّل ذلك البيع*.

## مراجع

- [ENTERPRISE_OFFER_POSITIONING_AR.md](ENTERPRISE_OFFER_POSITIONING_AR.md)
- [DEALIX_MASTER_OPERATING_MODEL_AR.md](DEALIX_MASTER_OPERATING_MODEL_AR.md)
- [DEALIX_ROLE_SERVICE_LADDER_AR.md](DEALIX_ROLE_SERVICE_LADDER_AR.md)
