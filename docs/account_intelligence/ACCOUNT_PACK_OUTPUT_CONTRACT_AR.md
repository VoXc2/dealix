# Account Pack Output Contract — عقد مخرج الباقة

العقد الرسمي لكل Account Pack. المرجع التنفيذي: `schemas/account_intelligence_pack.schema.json`.

---

## 1. الحقول

| الحقل | النوع | ملاحظات |
|-------|------|---------|
| `pack_id` | string | `AP-000001` |
| `generated_at` / `run_date` | string | وقت/تاريخ التشغيل |
| `company_name` | string | اسم الشركة |
| `website` | string\|null | الموقع |
| `country` / `city` | string | الدولة/المدينة |
| `sector` / `subsector` | string | القطاع/الفرعي |
| `services_detected` | string[] | خدمات مكتشفة |
| `business_model_hint` | string | إشارة نموذج العمل |
| `public_contact_channels` | string[] | قنوات عامة (قد تكون فارغة) |
| `phone_if_public` | string\|null | **null إن لم يكن عامًا — لا اختراع** |
| `email_if_public` | string\|null | **null إن لم يكن عامًا — لا اختراع** |
| `contact_page_url` | string\|null | صفحة التواصل إن وُجدت |
| `social_links` | string[] | روابط عامة |
| `google_business_hint` | string\|null | إشارة نشاط تجاري عام |
| `likely_decision_maker_role` | string | الدور الأنسب |
| `secondary_contact_role` | string | الدور الثانوي |
| `best_contact_route` | enum | contact_form · public_social · public_email · public_phone · role_based_outreach · founder_provided |
| `contact_confidence` | enum | C0…C4 |
| `buying_signal` / `signal_source` | string | الإشارة ومصدرها |
| `likely_pain` | string | الألم المحتمل (لغة احتمالية في L0/L1) |
| `recommended_system` | enum | **نظام واحد فقط** من الخمسة |
| `why_this_system` | string | لماذا هذا النظام |
| `first_sprint_offer` | string | أول Sprint |
| `proof_angle` | string | زاوية الإثبات |
| `email_subject` / `email_body` | string | مسودة الإيميل |
| `call_opener` | string | افتتاحية الاتصال |
| `call_questions` | string[] | ≥ 3 أسئلة |
| `expected_objections` | object[] | `{objection, response}` |
| `mini_proposal_title` / `mini_proposal_angle` | string | عنوان وزاوية العرض |
| `delivery_pack` | string[] | حزمة التسليم |
| `required_inputs` | string[] | مدخلات مطلوبة |
| `acceptance_criteria` | string[] | معايير القبول |
| `risk_level` | enum | low · medium · high |
| `evidence_level` | enum | L0…L4 |
| `cash_priority_score` | int 0–100 | أولوية الكاش |
| `account_score` | int 0–100 | درجة Top-100 |
| `next_action` | string | الخطوة التالية |
| `owner` | string | المالك (founder) |
| `status` | enum | new…won/lost/nurture/suppressed |
| `do_not_contact` | bool | قائمة المنع |
| `missing_contact` | bool | لا قناة عامة → role-based |

---

## 2. قاعدة التواصل الذهبية

> إذا لم يوجد رقم/إيميل عام:
> `phone_if_public = null` · `email_if_public = null`
> `best_contact_route = contact_form / public_social / role_based_outreach`
> `missing_contact = true`

**لا يُطلب أبدًا اختراع جهة اتصال**، ولا يُعتبر غياب القناة سببًا للرفض — بل لاكتشاف تواصل بشري.

---

## 3. التحقق

`validate_account_intelligence.py` يرفض أي Pack:
- ينقصه حقل مطلوب أو يخالف نوعًا/enum/نمطًا.
- يحوي قيمة هاتف/إيميل في الـseed (اختراع).
- يخالف بوابة الإيميل أو لغة الدليل أو يحوي ادعاءً مضمونًا.

---

*Version 1.0 — المصدر الرسمي: schemas/account_intelligence_pack.schema.json*
