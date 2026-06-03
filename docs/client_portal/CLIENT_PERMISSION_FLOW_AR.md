# تدفق صلاحيات العميل عبر البوابة

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2
> السكيمات المرجعية: `schemas/client_permission.schema.json` + `schemas/client_portal_permission.schema.json`
> المسار: `/client/permissions`

---

## 1. المبدأ: الصلاحيات عبر البوابة فقط

**لا تُمنح أي صلاحية وصول (CRM، جداول، بريد) عبر واتساب أو أي قناة أخرى.**

القاعدة في `client_permission.schema.json`:
```json
"via": { "enum": ["secure_portal"] }
```

هذا الحقل ثابت — لا قيمة أخرى مقبولة. أي صلاحية تُمنح خارج البوابة = **غير صالحة** ومرفوضة من النظام.

---

## 2. نوعا الصلاحية

### 2.1 صلاحية البوابة (Client Portal Permission)
تتحكم في **ما يمكن للعميل الوصول إليه داخل البوابة**:

| الحقل | الوصف |
|---|---|
| `id` | `CPP-XXXX` |
| `role` | `client_viewer` / `client_approver` / `client_uploader` |
| `allowed_routes` | قائمة المسارات المسموح بها (من التسعة) |
| `mfa_required` | `true` دائمًا |
| `expires_at` | انتهاء تلقائي |
| `least_privilege` | `true` دائمًا |
| `audit.granted_by` | من منح الصلاحية |
| `audit.revoked` | هل أُلغيت؟ |
| `audit.revoked_at` | وقت الإلغاء |

### 2.2 صلاحية الوصول للبيانات (Client Permission Grant)
تتحكم في **ما يمكن لـ Dealix الوصول إليه من بيانات العميل**:

| الحقل | الوصف |
|---|---|
| `id` | `PRM-XXXX` |
| `scope` | نوع الوصول: `read_only_crm` / `read_only_sheet` / `read_only_inbox` / `file_upload` / `report_view` / `none` |
| `resource` | اسم المورد المنطقي (مثل "Leads sheet Q2") — **لا URL مع token** |
| `granted` | هل وافق العميل؟ |
| `via` | دائمًا `secure_portal` |
| `secret_ref` | `portal://...` — **مرجع فقط، لا سر حقيقي** |
| `expires_at` | انتهاء الصلاحية |
| `risk_level` | `low` / `medium` / `high` / `critical` |
| `audit` | `granted_by`, `reviewed_by`, `revoked`, `revoked_at` |

---

## 3. تدفق منح الصلاحية خطوة بخطوة

```
[1] Dealix يُرسل رابط بوابة مؤقت → /client/permissions
            ↓ (magic_link_ref = portal://...)
[2] العميل يسجل الدخول + يتحقق بـ MFA
            ↓
[3] النظام يعرض طلب الصلاحية المحدد:
    - نوع الوصول: read_only_crm / read_only_sheet / ...
    - المورد: اسم منطقي فقط (مثل "Leads CRM — Q2 2026")
    - المدة: حتى expires_at
            ↓
[4] العميل يوافق (granted=true) أو يرفض (granted=false)
            ↓ إن وافق
[5] العميل يُدخل secret/token عبر نموذج مشفّر في البوابة
    → النظام يخزّن secret_ref = portal://secrets/...
    → لا قيمة السر في أي سجل أو ملف بيانات
            ↓
[6] Dealix يستخدم الصلاحية خلال المدة المحددة
    (scope=read_only → قراءة فقط، لا تعديل)
            ↓
[7] عند انتهاء expires_at أو إلغاء العميل:
    audit.revoked=true, audit.revoked_at=<timestamp>
    → الصلاحية غير صالحة فورًا
```

---

## 4. الأدوار داخل البوابة

| الدور | ما يستطيع فعله | المسارات المسموح بها |
|---|---|---|
| `client_viewer` | قراءة التقارير والأدلة | `/client/start`, `/client/proof-pack`, `/client/weekly-report` |
| `client_approver` | مراجعة وقبول العروض والدفع | `/client/start`, `/client/proposal`, `/client/proof-pack`, `/client/payment` |
| `client_uploader` | رفع الملفات والبيانات | `/client/start`, `/client/upload`, `/client/assessment` |

**ملاحظة:** يمكن للعميل الواحد أن يمتلك أدوارًا متعددة، لكن كل صلاحية تُمنح بشكل منفصل وموثّق.

---

## 5. مثال واقعي: Digital Rise Agency

| الحقل | القيمة |
|---|---|
| `id` | `CPP-1001` |
| `role` | `client_approver` |
| `allowed_routes` | `/client/start`, `/client/proposal`, `/client/proof-pack`, `/client/payment` |
| `mfa_required` | `true` |
| `expires_at` | 2026-06-10T12:00:00+03:00 |
| `audit.granted_by` | founder |
| `audit.revoked` | false |

---

## 6. قواعد التدقيق والإلغاء

- كل منح صلاحية يُسجَّل فورًا في `ai_action_ledger`.
- مراجعة دورية للصلاحيات النشطة كل أسبوع.
- إلغاء فوري عند:
  - انتهاء العقد مع العميل
  - طلب العميل
  - اشتباه أمني
  - انتهاء `expires_at` التلقائي

---

## 7. ما هو ممنوع قطعًا

- طلب أو استلام token/API key عبر واتساب أو بريد إلكتروني.
- تخزين أي سر في JSONL أو تقارير أو GitHub issues.
- منح صلاحية كتابة أو تعديل — الوصول دائمًا `read_only` في v1.
- تمديد صلاحية منتهية بدون موافقة موثّقة جديدة.

---

## الروابط المرجعية

- سكيمة صلاحية البوابة: `schemas/client_portal_permission.schema.json`
- سكيمة صلاحية البيانات: `schemas/client_permission.schema.json`
- سياسة البوابة الآمنة: [`SECURE_CLIENT_PORTAL_AR.md`](SECURE_CLIENT_PORTAL_AR.md)
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
