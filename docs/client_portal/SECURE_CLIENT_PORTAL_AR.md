# البوابة الآمنة للعملاء — المفهوم والمسارات والأمن

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2

---

## 1. ما هي البوابة الآمنة؟

البوابة الآمنة (`Secure Client Portal`) هي القناة **الوحيدة المعتمدة** لتبادل الملفات، والأسرار، وصلاحيات الوصول، ومراجعة العروض والأدلة، وتسليم الدفع بين Dealix والعميل.

**القاعدة الذهبية:** كل ما هو سري أو حساس — ملفات، روابط، مفاتيح وصول، عروض نهائية، روابط دفع — يأتي **فقط عبر البوابة**، لا واتساب ولا بريد إلكتروني عام ولا رسائل مباشرة.

---

## 2. لماذا البوابة وليست واتساب؟

| السبب | البوابة الآمنة | واتساب |
|---|---|---|
| الأسرار والمفاتيح | محمية بـ `secret_ref=portal://` | **محظور** — أي سر في واتساب ينتهك الثوابت |
| الملفات الحساسة | رفع آمن + فحص + PII check | **غير آمن** — نسخ واتساب غير مشفرة بما يكفي |
| موافقة العرض | تدفق رسمي + توقيع المؤسس | **لا سعر نهائي** عبر واتساب |
| رابط الدفع | يُنشأ في البوابة فقط، يتطلب موافقة | **محظور** إرسال رابط دفع بلا موافقة |
| السجل الأمني | كل جلسة مُسجَّلة (audit trail) | لا سجل موحّد |
| انتهاء الصلاحية | روابط منتهية الصلاحية تلقائيًا | لا تنتهي صلاحية الرسائل |

---

## 3. مسارات البوابة (Portal Routes)

| المسار | الهدف | مستوى الصلاحية |
|---|---|---|
| `/client/start` | دخول العميل وتعريفه بالنظام | L1 — Observe |
| `/client/assessment` | إكمال تقييم جاهزية الإيراد | L1 — Observe |
| `/client/permissions` | منح صلاحيات القراءة (CRM، جداول) | L4 — Act with Approval |
| `/client/upload` | رفع ملفات البيانات بأمان | L3 — Draft |
| `/client/proposal` | مراجعة العرض والسعر (غير نهائي حتى موافقة المؤسس) | L4 — Act with Approval |
| `/client/proof-pack` | مراجعة Proof Pack وأدلة الإثبات | L1 — Observe |
| `/client/payment` | خطوة الدفع — لا إرسال تلقائي | L5 — High-Risk / موافقة المؤسس |
| `/client/onboarding` | checklist الإعداد والانطلاق | L2 — Advise |
| `/client/weekly-report` | استلام تقرير القيمة الأسبوعي | L1 — Observe |

---

## 4. دورة الجلسة (Session Lifecycle)

يعتمد النظام على سكيمة `client_portal_session.schema.json`:

| الحقل | القيمة / الوصف |
|---|---|
| `id` | `CPS-XXXX` — معرّف فريد |
| `route` | أحد المسارات التسعة أعلاه |
| `magic_link_ref` | `portal://links/...` — مرجع فقط، لا رابط حي في البيانات |
| `mfa_verified` | التحقق بخطوتين — إلزامي قبل أي مسار L4/L5 |
| `least_privilege` | `true` دائمًا — أقل صلاحية ممكنة |
| `expires_at` | انتهاء تلقائي (لا روابط أبدية) |
| `status` | `issued → active → expired/revoked/completed` |
| `ip_country` | للتحقق من إقامة البيانات في السعودية (بدون تخزين IP كامل) |

**مثال واقعي:** جلسة Digital Rise Agency (CPS-1001) — مسار `/client/proposal`، MFA مُتحقَّق، تنتهي خلال 24 ساعة، من السعودية.

---

## 5. ضمانات الأمن

### 5.1 التحقق المزدوج (MFA)
كل مسار يتطلب L4 أو أعلى يستلزم `mfa_verified=true` قبل أي إجراء.

### 5.2 أقل امتياز (Least Privilege)
- كل جلسة تُفتح لمسار واحد فقط.
- لا صلاحيات إضافية إلا بمنح صريح موثّق في `client_portal_permission.schema.json`.
- الأدوار المتاحة: `client_viewer` | `client_approver` | `client_uploader`.

### 5.3 إقامة البيانات في السعودية
- جميع البيانات تُعالَج وتُخزَّن داخل السعودية (`ip_country=SA`).
- متوافق مع نظام حماية البيانات الشخصية PDPL/SDAIA.
- مرجع: [`company_os/governance/pdpl_checklist.md`](../../company_os/governance/pdpl_checklist.md)

### 5.4 روابط منتهية الصلاحية
- كل `magic_link_ref` ينتهي تلقائيًا (24 ساعة افتراضيًا، قابل للتقليص).
- لا رابط مفتوح أو أبدي.
- الروابط المُلغاة لا تُعاد تفعيلها.

### 5.5 سجل التدقيق (Audit Trail)
- كل جلسة وكل إجراء مُسجَّل في `ai_action_ledger`.
- `granted_by`, `revoked`, `revoked_at` موثّقة في كل سجل صلاحية.

### 5.6 قاعدة "لا أسرار"
- لا مفاتيح API، لا كلمات مرور، لا tokens في أي ملف بيانات أو سجل أو تقرير.
- كل سر يُخزَّن بـ `secret_ref = portal://...` (مرجع، لا قيمة).

---

## 6. ما يجب الانتباه إليه

- لا تُرسل رابط بوابة عبر واتساب أو بريد غير مشفر.
- لا تُعيد استخدام رابط منتهي الصلاحية.
- لا تمنح صلاحيات أعلى من الحاجة.
- إلغاء الصلاحية فوري عند انتهاء الارتباط مع العميل.
- لا تخزّن `ip_country` كعنوان IP كامل.

---

## 7. الاستجابة للحوادث

عند اشتباه بخرق:
1. إلغاء الجلسة فورًا (`status → revoked`).
2. إخطار المؤسس خلال ساعة.
3. إخطار SDAIA خلال 72 ساعة (حسب PDPL).
4. مراجعة [`company_os/governance/pdpl_checklist.md`](../../company_os/governance/pdpl_checklist.md) و[`data_handling_checklist.md`](../../company_os/governance/data_handling_checklist.md).

---

## الروابط المرجعية

- سكيمة الجلسة: `schemas/client_portal_session.schema.json`
- سكيمة صلاحية البوابة: `schemas/client_portal_permission.schema.json`
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)
- خصوصية البيانات: [`company_os/governance/pdpl_checklist.md`](../../company_os/governance/pdpl_checklist.md)
- التعامل مع البيانات: [`company_os/governance/data_handling_checklist.md`](../../company_os/governance/data_handling_checklist.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
