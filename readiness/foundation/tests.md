# العربية

Owner: قائد المنصة (Platform Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة الأساس. هذه مواصفة بالكلمات، لا كود. كل اختبار يحدد ما يثبت السلوك وما الذي يوقف الدمج.

## اختبارات الجاهزية

### ت-1: ربط معرّف المستأجر

- **الهدف:** كل استعلام بيانات يحمل `tenant_id` ولا يتسرّب عبر المستأجرين.
- **الخطوات:** أنشئ مستأجرَين، اكتب سجلاً لكل منهما، استعلم بهوية كل مستأجر.
- **النتيجة المتوقعة:** كل مستأجر يرى سجله فقط.
- **معيار النجاح/الفشل:** أي تسرّب عبر المستأجرين = فشل يوقف الدمج.

### ت-2: المصادقة والجلسات

- **الهدف:** الجلسات تنتهي وتُبطَل كما هو محدد.
- **الخطوات:** سجّل دخولاً، انتظر انتهاء الجلسة، حاول استخدام الرمز المنتهي.
- **النتيجة المتوقعة:** الرمز المنتهي مرفوض.
- **معيار النجاح/الفشل:** قبول رمز منتهٍ = فشل.

### ت-3: فرض RBAC

- **الهدف:** الدور المحدود لا يصل إلى مسارات إدارية.
- **الخطوات:** استدعِ مسار `api/routers/admin.py` بدور غير إداري.
- **النتيجة المتوقعة:** رفض بصلاحية.
- **معيار النجاح/الفشل:** أي وصول غير مصرّح = فشل.

### ت-4: الأسرار والتشفير

- **الهدف:** لا تظهر الأسرار في السجلات أو الاستجابات.
- **الخطوات:** افحص سجلات `dealix/observability/` بعد عملية تستخدم سراً.
- **النتيجة المتوقعة:** السر محجوب.
- **معيار النجاح/الفشل:** ظهور سر = فشل.

### ت-5: تمرين الاستعادة (فجوة معروفة)

- **الهدف:** استعادة نسخة احتياطية إلى حالة سليمة بزمن مُسجَّل.
- **الخطوات:** خذ نسخة، احذف بيانات اختبارية، استعِد، تحقق من السلامة.
- **النتيجة المتوقعة:** بيانات مستعادة كاملة بزمن موثَّق.
- **معيار النجاح/الفشل:** غياب تمرين متحقَّق دوري = فجوة تُبقي الطبقة في نطاق تجربة عميل.

### ت-6: تمرين حذف مستأجر (فجوة معروفة)

- **الهدف:** حذف مستأجر يزيل بياناته من التخزين والفهارس.
- **الخطوات:** أنشئ مستأجراً، احذفه، افحص التخزين والفهارس.
- **النتيجة المتوقعة:** لا بقايا بيانات.
- **معيار النجاح/الفشل:** أي بقايا = فشل؛ غياب التمرين الدوري = فجوة.

## ما يوقف الدمج

أي فشل في ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج فوراً. ت-5 وت-6 فجوتان موثَّقتان تُبقيان الطبقة دون نطاق "جاهز للمؤسسات".

## روابط ذات صلة

- `readiness/foundation/readiness.md`
- `platform/foundation/tests.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Platform Lead

## Purpose

A readiness test specification for the Foundation layer. This is a spec in words, not code. Each test states what proves the behavior and what blocks a merge.

## Readiness tests

### T-1: Tenant ID binding

- **Goal:** every data query carries `tenant_id` and does not leak across tenants.
- **Steps:** create two tenants, write one record each, query as each tenant.
- **Expected result:** each tenant sees only its own record.
- **Pass/fail:** any cross-tenant leak = fail that blocks the merge.

### T-2: Authentication and sessions

- **Goal:** sessions expire and are invalidated as specified.
- **Steps:** log in, wait for expiry, attempt to use the expired token.
- **Expected result:** the expired token is rejected.
- **Pass/fail:** accepting an expired token = fail.

### T-3: RBAC enforcement

- **Goal:** a limited role cannot reach admin routes.
- **Steps:** call an `api/routers/admin.py` route with a non-admin role.
- **Expected result:** denied on permission.
- **Pass/fail:** any unauthorized access = fail.

### T-4: Secrets and encryption

- **Goal:** secrets do not appear in logs or responses.
- **Steps:** inspect `dealix/observability/` logs after an operation that uses a secret.
- **Expected result:** the secret is redacted.
- **Pass/fail:** any secret exposed = fail.

### T-5: Restore drill (known gap)

- **Goal:** restore a backup to a healthy state with recorded time.
- **Steps:** take a backup, delete test data, restore, verify integrity.
- **Expected result:** fully restored data with documented time.
- **Pass/fail:** absence of a periodic verified drill = a gap that keeps the layer in the client-pilot band.

### T-6: Tenant-deletion drill (known gap)

- **Goal:** deleting a tenant removes its data from storage and indexes.
- **Steps:** create a tenant, delete it, inspect storage and indexes.
- **Expected result:** no residual data.
- **Pass/fail:** any residue = fail; absence of a periodic drill = a gap.

## What blocks a merge

Any failure in T-1, T-2, T-3, or T-4 blocks the merge immediately. T-5 and T-6 are documented gaps that keep the layer below the enterprise-ready band.

## Related links

- `readiness/foundation/readiness.md`
- `platform/foundation/tests.md`

Estimated value is not Verified value.
