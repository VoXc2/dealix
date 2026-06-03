# نموذج Google Sheet — Dealix Level 1 Full Ops

هذا الملف **مصدر الحقيقة** لأسماء التبويبات والأعمدة والقيم. طبّقها حرفياً في الصف الأول من كل تبويب لتعمل الصيغ والسكربت.

---

## أسماء التبويبات (9 تبويبات)

| الترتيب | اسم التبويب | الغرض |
|--------|--------------|--------|
| 1 | `01_Lead_Intake` | ملخص حقول أو مرآة يدوية (اختياري) |
| 2 | `Form Responses 1` | ردود Google Form (افتراضي Google) |
| 3 | `02_Operating_Board` | صف واحد لكل lead + الحالات والكرت |
| 4 | `03_Diagnostic_Cards` | قوالب كروت (نسخ للعميل) |
| 5 | `04_Proof_Pack` | إثبات التسليم لكل عميل/فترة |
| 6 | `05_Outreach_Copy` | نصوص جاهزة (LinkedIn، واتساب، Pilot، إلخ) |
| 7 | `06_Service_Mapping` | شرط → خدمة → خطوة تالية |
| 8 | `07_Dashboard` | مؤشرات مجمّعة من اللوحة |
| 9 | `99_Dropdowns` | قوائم القيم الثابتة للتحقق من الصحة |

> **ملاحظة:** Google ينشئ `Form Responses 1` تلقائياً عند ربط الفورم. لا تغيّر اسمه إلا إذا عدّلت `FORM_RESPONSES_SHEET` في السكربت.

---

## `02_Operating_Board` — صف الرأس (العمود → المعنى)

استخدم **أسماء إنجليزية** للرأس لتبقى السكربتات مستقرة. المحتوى العربي يذهب في الخلايا أو في `diagnostic_card`.

**ترتيب إلزامي:** الصف الأول يجب أن يطابق ترتيب الأعمدة في `BOARD_COLUMN_ORDER` داخل [dealix_google_apps_script.gs](dealix_google_apps_script.gs) (نفس الترتيب أدناه).

| العمود | الوصف |
|--------|--------|
| `submitted_at` | وقت الإدخال |
| `lead_name` | الاسم |
| `company` | الشركة |
| `website` | الموقع |
| `sector` | القطاع |
| `city` | المدينة |
| `goal` | الهدف (عربي من الفورم) |
| `ideal_customer` | وصف العميل المثالي |
| `offer` | العرض الحالي |
| `contact_method` | واتساب / إيميل / غيره |
| `whatsapp_or_email` | قيمة التواصل |
| `has_list` | نعم / لا — هل يوجد قائمة |
| `business_type` | نوع النشاط |
| `source` | مصدر الـ lead (form، linkedin_manual، referral، x_post، wa_inbound، …) |
| `consent` | نعم / لا |
| `consent_source` | form_opt_in / wa_inbound / referral_intro / … |
| `meeting_status` | not_booked / requested / booked / completed |
| `diagnostic_status` | new / waiting_data / in_progress / sent |
| `pilot_status` | not_offered / offered / accepted / paid / declined |
| `proof_pack_status` | not_started / in_progress / delivered |
| `recommended_service` | من جدول التعيين |
| `next_step` | جملة تشغيلية واحدة |
| `diagnostic_card` | نص كامل للكرت |
| `owner` | المسؤول |
| `invoice_link` | اختياري |
| `last_touch_at` | اختياري |
| `notes` | حر |

**اختبار قبول لصف تجريبي:** `recommended_service` و `next_step` و `diagnostic_card` غير فارغة؛ `diagnostic_status = new`؛ `pilot_status = not_offered`؛ `proof_pack_status = not_started`.

---

## حالات إضافية (مرجع)

**meeting_status:** `not_booked` · `requested` · `booked` · `completed`

**diagnostic_status:** `new` · `waiting_data` · `in_progress` · `sent`

**pilot_status:** `not_offered` · `offered` · `accepted` · `paid` · `declined`

**proof_pack_status:** `not_started` · `in_progress` · `delivered`

---

## `03_Diagnostic_Cards` — عناوين الأقسام

قوالب نصية (Markdown أو نص عادي):

- Mini Diagnostic Card  
- Missing Data Card  
- Diagnostic Ready Card  
- Pilot Offer Card  
- Follow-up Card  
- Human Handoff Card  

مثال هيكل Mini Diagnostic (يولّده السكربت أو تنسخه يدوياً):

```
📊 Dealix Mini Diagnostic
الشركة: …
القطاع: …
الهدف: …
1. أفضل شريحة تبدأ بها: …
2. لماذا هذه الشريحة: …
3. 3 فرص مناسبة: …
4. رسالة عربية جاهزة: …
5. القناة المقترحة: …
6. مخاطرة يجب تجنبها: …
7. الخطوة القادمة: Pilot 499 لمدة 7 أيام.
```

---

## `04_Proof_Pack` — رأس الأعمدة

`client` · `service` · `period` · `opportunities_created` · `drafts_created` · `followups_planned` · `partner_suggestions` · `risks_blocked` · `unsafe_channels_avoided` · `contacts_marked_needs_review` · `cold_whatsapp_blocked` · `messages_awaiting_approval` · `followups_awaiting_approval` · `meeting_drafts_awaiting_approval` · `potential_pipeline` · `confidence` · `assumptions` · `next_recommended_action`

عناوين أقسام للقالب: Client · Service · Period · What Was Created · What Was Protected · What Needs Approval · Revenue Impact Estimate · Next Recommended Action

---

## `05_Outreach_Copy` — عناوين رئيسية

LinkedIn Post · X Post · Agency Outreach · Company Outreach · Follow-up 24h · Pilot Offer · Proof Pack Delivery · Referral Ask

---

## `06_Service_Mapping`

| condition | recommended_service | service_description | deliverables | price | next_step | risk_policy |
|-----------|---------------------|---------------------|--------------|-------|-----------|-------------|
| goal = أبغى عملاء | Growth Starter | … | … | … | Mini Diagnostic ثم Pilot 499 | … |
| goal = أبغى اجتماعات | Meeting Sprint | … | … | … | رسائل + متابعة + agenda | … |
| goal = أبغى شراكات | Partnership Growth | … | … | … | شركاء محتملين + رسائل | … |
| has_list = نعم | Data to Revenue | … | … | … | تصنيف القائمة + رسائل | … |
| sector = وكالة/مسوق | Agency Partner Pilot | … | … | … | Diagnostic لعميل واحد | … |

---

## `07_Dashboard` — مؤشرات (صيغ تشير إلى `02_Operating_Board`)

المطلوب (12 مقياساً على الأقل):

Total leads · WhatsApp inbound · Forms submitted · Needs data · Diagnostics in progress · Diagnostics sent · Meetings requested · Pilots offered · Pilots accepted · Pilots paid · Proof Packs delivered · Revenue collected · Risks blocked

**ألوان الحالة (يدوية أو شرط تنسيق):**

- **Green:** 5+ leads/week + 2 diagnostics + 1 pilot  
- **Yellow:** 2–4 leads/week + 1 diagnostic  
- **Red:** 0 leads أو لا يوجد diagnostic  

> الصيغ الدقيقة تعتمد على نطاق بياناتك (مثلاً `COUNTIF` على عمود `source` و `diagnostic_status`). ضع نطاقاً ثابتاً مثل `02_Operating_Board!A2:Z500`.

---

## `99_Dropdowns`

صف عمودي أو جدول صغير لكل قائمة:

- `source_values`  
- `diagnostic_status_values`  
- `meeting_status_values`  
- `pilot_status_values`  
- `proof_pack_status_values`  
- `recommended_services`  
- `business_types`  
- `goals`  
- `channels`  
- `owners`  

---

## Google Form — أسئلة مقترحة (12 + موافقة)

1. الاسم الكامل  
2. اسم الشركة  
3. رابط الموقع (اختياري)  
4. القطاع  
5. المدينة  
6. ما هدفك الآن؟ (قائمة: أبغى عملاء / أبغى اجتماعات / أبغى شراكات)  
7. وصف العميل المثالي  
8. ماذا تقدّم للسوق اليوم؟ (عرض مختصر)  
9. أفضل طريقة للتواصل (واتساب / إيميل)  
10. رقم الواتساب أو الإيميل  
11. هل عندك قائمة عملاء محتملين؟ (نعم/لا)  
12. نوع النشاط (قائمة من `99_Dropdowns`)  
13. **الموافقة:** أوافق على التواصل وفق سياسة الخصوصية (إلزامي — نعم)

اربط عناوين أعمدة `Form Responses 1` بالترتيب أعلاه أو عدّل دالة المزامنة في السكربت لتطابق عناوينك الفعلية.

---

## أقل نسخة صحيحة (Level 1)

1. Google Form فيه أسئلة أساسية + موافقة  
2. Google Sheet فيه التبويبات المذكورة  
3. Apps Script: trigger + معالج + اختبار يدوي  
4. اللوحة فيها `diagnostic_card`  
5. Dashboard فيه المقاييس المطلوبة  
6. رابط WhatsApp صحيح  
7. نصوص Outreach و Pilot و Proof جاهزة في `05_Outreach_Copy` و `04_Proof_Pack`  
8. قائمة قبول + Evidence Pack
