# إدارة الصلاحيات — البوابة الآمنة فقط
## WhatsApp Permission Onboarding

> **الغرض:** يوضّح هذا المستند كيف تُطلب صلاحيات الوصول للبيانات من العميل وكيف تُمنح — حصرًا عبر البوابة الآمنة، بمبدأ أقل امتياز، دون أي طلب سر أو مفتاح في واتساب أو أي دردشة.  
> مرجع السكيمة: `schemas/client_permission.schema.json`.

---

## 1. القاعدة الذهبية — لا أسرار في واتساب

**ممنوع مطلقًا إرسال أو طلب ما يلي في واتساب أو أي دردشة:**

| ممنوع | البديل الصحيح |
|---|---|
| مفاتيح API (`sk-...`, `AKIA...`) | البوابة الآمنة فقط |
| كلمات المرور | البوابة الآمنة فقط |
| رموز المصادقة (`Bearer ...`) | البوابة الآمنة فقط |
| روابط Google Drive موقّعة | `portal://` مرجع يُصدر من البوابة |
| رقم الجوال الكامل | مُقنَّع (`+9665XXXX1234`) |

هذا الحظر يسري على: واتساب، الإيميل، السجلات، الـPrompts، الـJSONL، التقارير، وقضايا/تعليقات GitHub.  
مرجع: `AGENTS.md §2` (الخطوط الحمراء) و`§8` (قاعدة "لا أسرار").

---

## 2. كيف يُطلب الوصول للبيانات؟

### الخطوة 1: إخطار العميل في واتساب

```
القالب: permission_request_notice
─────────────────────────────────
"عشان نكمّل، نحتاج صلاحية «قراءة فقط» لمصدر بياناتك (CRM/جدول).
ما نطلب أبدًا كلمات مرور أو مفاتيح هنا في واتساب —
كل شيء عبر البوابة الآمنة بصلاحية محدودة وتنتهي تلقائيًا:
{portal_link_placeholder}"

خيارات:
  [1] أعطيت الصلاحية   → granted
  [2] ليش تحتاجونها؟   → explain_permission
  [3] ما أعرف — اقترح علي → dont_know_suggest
```

### الخطوة 2: العميل يفتح البوابة الآمنة

- البوابة تُصدر رابطًا منتهي الصلاحية (expiring link) + MFA
- العميل يختار مصدر البيانات من قائمة واضحة
- يمنح قراءة فقط لنطاق محدد وفترة محددة

### الخطوة 3: تسجيل الصلاحية

```json
{
  "id": "PRM-xxxx",
  "scope": "read_only_crm",
  "resource": "Leads sheet (last 90 days)",
  "granted": false,           // يتحول true بعد منح العميل
  "via": "secure_portal",     // دائمًا secure_portal
  "secret_ref": "portal://vault/company/resource",  // مرجع، لا القيمة
  "expires_at": "...",
  "least_privilege": true
}
```

---

## 3. نطاقات الصلاحية المتاحة (`scope`)

| النطاق | ما يسمح به | مثال |
|---|---|---|
| `read_only_crm` | قراءة بيانات CRM فقط | قائمة العملاء المحتملين |
| `read_only_sheet` | قراءة جدول بيانات محدد | جدول المبيعات Q2 |
| `read_only_inbox` | قراءة صندوق البريد (محدود) | متابعة لا ردّ عليها |
| `file_upload` | رفع ملف محدد | تقرير PDF |
| `report_view` | عرض تقارير Dealix | تقرير القيمة الأسبوعي |
| `none` | لا وصول | افتراضي ما لم يُمنح |

---

## 4. مبادئ أقل امتياز (Least Privilege)

1. **الحد الأدنى الضروري فقط:** لا نطلب وصولًا لن نستخدمه.
2. **صلاحية قراءة فقط:** لا كتابة، لا حذف، لا تعديل على بيانات العميل.
3. **انتهاء تلقائي:** كل صلاحية لها `expires_at` — لا صلاحية دائمة.
4. **مراجعة دورية:** `audit.reviewed_by` و`audit.revoked` محفوظان.
5. **سحب فوري:** يمكن للعميل سحب الصلاحية في أي وقت.

---

## 5. مثال حقيقي — PRM-0001 (TrainMe KSA)

```json
{
  "id": "PRM-0001",
  "company": "TrainMe KSA",
  "scope": "read_only_crm",
  "resource": "Leads sheet (last 90 days)",
  "granted": false,
  "via": "secure_portal",
  "secret_ref": "portal://vault/trainme/crm-readonly",
  "expires_at": "2026-06-17T10:20:00+03:00",
  "least_privilege": true,
  "risk_level": "medium"
}
```

الصلاحية لا تزال `granted: false` لأن العميل لم يكملها بعد في البوابة.

---

## 6. ماذا لو طلب العميل شرح السبب؟

تدفق `explain_permission` يُرسل رسالة شرح موجزة:
- ما البيانات التي نصل إليها بالضبط
- لماذا نحتاجها (تشخيص التسرب)
- أنها قراءة فقط ومؤقتة
- كيف يسحب الصلاحية في أي وقت

ثم يعود للخيارات الأصلية.

---

## مراجع

- `schemas/client_permission.schema.json`
- `data/whatsapp/permissions.jsonl` (مثال: PRM-0001)
- `data/whatsapp/flows.yaml` (تدفق: `permission_request`, `secure_portal_link`)
- `data/whatsapp/templates.yaml` (قالب: `permission_request_notice`)
- `company_os/governance/data_handling_checklist.md`
- `company_os/governance/pdpl_checklist.md`
- `AGENTS.md §2` و`§8`

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
