# Account Pack Output Contract — عقد مخرجات باقة الحساب

*التعريف الملزِم لكل حقل في باقة الحساب. المرجع الآلي: `schemas/account_intelligence_pack.schema.json`.*
*آخر تحديث: 2026-06-03*

> الفكرة الكبرى: لم نعد ننتج «إيميل draft». ننتج **ملف بيع كامل** لكل شركة.
> قبل: 400 email drafts → الآن: **400 Account Intelligence Packs**.

---

## الحقول (Fields)

| الحقل | النوع | إلزامي | ملاحظات |
|------|------|:------:|--------|
| `company_name` | string | ✅ | اسم الشركة |
| `website` | string\|null | — | عام أو null — لا يُختلق |
| `country`, `city` | string | ✅ | الدولة/المدينة |
| `sector`, `subsector` | string / string\|null | sector ✅ | القطاع والفرع |
| `services_detected` | string[] | — | من مصادر عامة (L1+) |
| `business_model_hint` | string\|null | — | تلميح نموذج العمل |
| `public_contact_channels` | string[] | ✅ | مراجع لـ contact_channels (قد تكون فارغة) |
| `phone_if_public` | string\|null | — | فقط إن وُجدت قناة هاتف عامة — لا يُخمَّن |
| `email_if_public` | string\|null | — | بريد عام (info@/sales@) — لا بريد شخصي مخمَّن |
| `contact_page_url` | string\|null | — | صفحة التواصل |
| `social_links` | string[] | — | روابط عامة |
| `google_business_hint` | string\|null | — | تلميح Google Business |
| `likely_decision_maker_role` | string | ✅ | **دور** لا اسم — يجب أن يطابق النظام |
| `secondary_contact_role` | string\|null | — | الدور البديل |
| `best_contact_route` | enum | ✅ | email/contact_form/phone/linkedin_public/social_dm/website_only/none_found |
| `buying_signal` | string\|null | — | إشارة شراء عامة |
| `signal_source` | string\|null | — | مصدر الإشارة |
| `likely_pain` | string | ✅ | الألم المحتمل (لغة احتمالية في L0/L1) |
| `recommended_system` | enum | ✅ | أحد الأنظمة الخمسة (slug) |
| `why_this_system` | string | ✅ | سبب اختيار النظام |
| `first_sprint_offer` | object | ✅ | {name, starter_price_sar, timeline_days, deliverables[]} |
| `proof_angle` | string\|null | — | زاوية الإثبات |
| `email_subject` | string | ✅ | بدون Re:/Fwd: مضلّل |
| `email_body` | string | ✅ | مخصّص، نظام واحد فقط، بلا ضمانات |
| `call_opener` | string\|null | — | افتتاحية الاتصال |
| `call_questions` | string[] | — | أسئلة الاكتشاف |
| `expected_objections` | object[] | — | [{objection, response}] |
| `mini_proposal_title` | string | ✅ | عنوان العرض المختصر |
| `mini_proposal_angle` | string\|null | — | زاوية العرض |
| `delivery_pack` | string[] | — | عناصر التسليم عند الفوز |
| `required_inputs` | string[] | ✅ | مدخلات الـ Sprint (≥1) |
| `risk_level` | enum | ✅ | low/medium/high |
| `evidence_level` | enum | ✅ | L0–L4 |
| `contact_confidence` | enum | — | CC0–CC3 |
| `score` | number\|null | — | نقاط التقييم (0–100) — يحسبها النموذج |
| `next_action` | enum | ✅ | الخطوة التالية |
| `owner` | enum | ✅ | founder/caller/agent/unassigned |
| `status` | enum | ✅ | حالة دورة الحياة |

---

## Status Model (دورة الحياة)

```txt
researched → contact_found → need_card_ready → draft_ready → quality_passed
→ top_100 → approved → sent → call_due → called → interested
→ mini_proposal_ready → proposal_sent → won → delivery_started → active
→ renewal_candidate
(فروع جانبية: lost · do_not_contact)
```

---

## القواعد الملزِمة (Contract Rules) — يفحصها المدقّق

```txt
1. recommended_system إلزامي ويطابق أحد الأنظمة الخمسة.
2. likely_decision_maker_role يطابق أدوار النظام (CONTACT_TARGETING_MATRIX_AR.md).
3. phone_if_public / email_if_public تُملأ فقط إن وُجدت قناة عامة مطابقة — لا اختلاق.
4. عند عدم وجود قناة: best_contact_route = none_found، ولا تُملأ حقول التواصل،
   ولا تصل الحالة إلى approved/sent (معالجة سلِسة لغياب التواصل).
5. في L0/L1: لغة احتمالية إلزامية، وممنوع أي ادعاء جازم.
6. ممنوع أي صياغة ضمان (نضمن/مضمون/100%/guarantee) في كل النسخ.
7. email_subject لا يبدأ بـ Re:/Fwd: مضلّل.
8. email_body لا يسرّب أسماء داخلية أو slugs أو أسماء ملفات.
9. كل باقة تبقى draft حتى موافقة المؤسس (approval gate).
```

التحقق: `python3 scripts/validate_account_intelligence.py` (17 فحصًا).
