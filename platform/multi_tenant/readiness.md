# العربية

## جاهزية تعدد المستأجرين — الطبقة الأولى

Owner: قائد المنصة (Platform Lead)

### قائمة الجاهزية

- [x] كل صف أعمال يحمل عمود `tenant_id` إلزاميًّا ومفهرسًا.
- [x] كل ملف وذاكرة ومحادثة مُقيَّد بـ `tenant_id`.
- [x] إنشاء مستأجر جديد خلال أقل من 5 دقائق عبر `api/routers/auth.py`.
- [x] استخراج `tenant_id` في كل طلب عبر `api/security/auth_deps.py`.
- [x] حذف مستأجر مُقيَّد بـ `tenant_id` المستهدف فقط.
- [x] قيود التدقيق التاريخية محفوظة بعد حذف المستأجر.
- [ ] تمرين حذف مستأجر كامل موثَّق دوريًا يثبت صفر أثر على الآخرين.
- [ ] تنبيه آلي قيد التشغيل على أي صف بـ `tenant_id` غير متطابق في نتائج الاستعلامات.

### المقاييس

- نسبة الجداول الحاملة لـ `tenant_id`: 100%.
- زمن إنشاء المستأجر: أقل من 5 دقائق.
- عدد حالات عبور الحدود المكتشَفة: هدف صفر.
- عدد المستأجرين الآخرين المتأثرين بأي حذف: يجب أن يكون صفرًا.
- نسبة عمليات الحذف الموثَّقة بموافقة: 100%.

### خطاطيف المراقبة

- تتبّع كل طلب مع `tenant_id` عبر `dealix/observability/otel.py`.
- قيود تدقيق إنشاء/تعديل/حذف المستأجر عبر `dealix/trust/audit.py`.
- تتبّع التكلفة لكل مستأجر عبر `dealix/observability/cost_tracker.py`.
- تنبيه على أي صف بـ `tenant_id` غير متطابق وعلى أي حذف يمسّ خارج المستأجر المستهدف.

### قواعد الحوكمة

- لا صف أو ملف أو محادثة بدون `tenant_id`.
- إنشاء أو حذف مستأجر إجراء بتصنيف A2 على الأقل ويتطلب موافقة موثَّقة.
- تصدير بيانات S3 يتطلب موافقة A3.
- لا تنفّذ المنصة إجراءات خارجية موجَّهة للعملاء بدون موافقة المستأجر.

### إجراء التراجع

1. إلغاء إنشاء مستأجر خاطئ بتعطيله ثم حذفه وفق `tenant_deletion.md`.
2. خلال فترة سماح الحذف: إعادة التفعيل تلغي الحذف.
3. بعد الحذف النهائي: استرجاع من آخر لقطة يومية ضمن نافذة RPO إلى بيئة معزولة.
4. التحقق من سلامة باقي المستأجرين وتسجيل التراجع كقيد تدقيق.

### درجة الجاهزية الحالية

**الدرجة: 76 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Multi-Tenancy Readiness — Layer 1

Owner: Platform Lead

### Readiness checklist

- [x] Every business row carries a mandatory, indexed `tenant_id` column.
- [x] Every file, memory, and conversation is scoped to `tenant_id`.
- [x] A new tenant is created in under 5 minutes via `api/routers/auth.py`.
- [x] `tenant_id` is extracted on every request via `api/security/auth_deps.py`.
- [x] Tenant deletion is scoped to the target `tenant_id` only.
- [x] Historical audit entries are retained after tenant deletion.
- [ ] A periodically documented full tenant-deletion drill proving zero impact on others.
- [ ] A live automated alert on any row with a mismatched `tenant_id` in query results.

### Metrics

- Tables carrying `tenant_id`: 100%.
- Tenant creation time: under 5 minutes.
- Count of detected boundary crossings: target zero.
- Count of other tenants affected by any deletion: must be zero.
- Ratio of deletions documented with an approval: 100%.

### Observability hooks

- Every request traced with `tenant_id` via `dealix/observability/otel.py`.
- Audit entries for tenant creation/modification/deletion via `dealix/trust/audit.py`.
- Per-tenant cost tracking via `dealix/observability/cost_tracker.py`.
- Alert on any row with a mismatched `tenant_id` and on any deletion touching outside the target tenant.

### Governance rules

- No row, file, or conversation without a `tenant_id`.
- Tenant creation or deletion is an A2-class action at minimum and requires a documented approval.
- S3 data export requires an A3 approval.
- The platform does not perform external customer-facing actions without tenant approval.

### Rollback procedure

1. Undo a wrongly created tenant by deactivating then deleting it per `tenant_deletion.md`.
2. During the deletion grace period: reactivation cancels the deletion.
3. After final deletion: restore from the last daily snapshot within the RPO window into an isolated environment.
4. Verify the integrity of remaining tenants and record the rollback as an audit entry.

### Current readiness score

**Score: 76 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
