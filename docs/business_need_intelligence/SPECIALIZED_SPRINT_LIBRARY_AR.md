# مكتبة السبرنتات المتخصصة — Specialized Sprint Library

20 سبرنتًا قابلًا للبيع والتسليم. **كل سبرنت يرجع إلى نظام عام واحد** ويحمل
مخرجات + مدخلات مطلوبة + معايير قبول.

مصدر الحقيقة: `data/business_need_intelligence/specialized_sprint_library.yaml`.

---

## الجدول الكامل (20 سبرنت)

| # | Sprint | النظام العام | القطاع | الاحتياج | المدة (يوم) |
|--:|--------|--------------|--------|----------|------------:|
| 1 | Enrollment Recovery Sprint | followup_recovery_os | training | follow_up | 7 |
| 2 | Property Lead Response Sprint | followup_recovery_os | real_estate | lead_response | 7 |
| 3 | Clinic Appointment Flow Sprint | whatsapp_client_os | clinics | customer_support | 7 |
| 4 | Proposal & Scope Proof Sprint | proposal_proof_os | professional | proposal | 7 |
| 5 | Campaign Lead Recovery Sprint | followup_recovery_os | agencies | lead_response | 7 |
| 6 | Demo-to-Onboarding Sprint | proposal_proof_os | saas | client_onboarding | 10 |
| 7 | Recruitment Follow-up Sprint | followup_recovery_os | recruitment | follow_up | 7 |
| 8 | Support Triage Sprint | whatsapp_client_os | saas | customer_support | 7 |
| 9 | Customer Message Flow Sprint | whatsapp_client_os | restaurants | customer_support | 7 |
| 10 | Renewal Recovery Sprint | followup_recovery_os | saas | renewal | 7 |
| 11 | Executive Daily Command Sprint | executive_command_os | professional | reporting | 7 |
| 12 | Agency Client Onboarding Sprint | proposal_proof_os | agencies | client_onboarding | 10 |
| 13 | Course Inquiry Routing Sprint | revenue_os | education | qualification | 7 |
| 14 | No-show Follow-up Sprint | followup_recovery_os | clinics | follow_up | 7 |
| 15 | Vendor Coordination Sprint | proposal_proof_os | logistics | delivery | 10 |
| 16 | Service Quality Review Sprint | executive_command_os | restaurants | service_quality | 7 |
| 17 | Partner Pipeline Sprint | revenue_os | professional | sales_execution | 10 |
| 18 | Content-to-Lead Sprint | revenue_os | consulting | lead_capture | 10 |
| 19 | Pricing & Scope Control Sprint | proposal_proof_os | consulting | sales_execution | 7 |
| 20 | Knowledge Reuse Sprint | proposal_proof_os | consulting | knowledge | 10 |

---

## بنية كل سبرنت

كل سبرنت في ملف البيانات يحمل:

```yaml
id, name_ar, name_en
core_system        # واحد من الخمسة
sector, need
duration_days
deliverables[]        # المخرجات الملموسة
required_inputs[]     # المدخلات المطلوبة من العميل
acceptance_criteria[] # معايير القبول
email_angle, call_angle
upsell_path           # نظام عام للتوسّع لاحقًا
```

---

## مثال مكتمل: 7-Day Enrollment Recovery Sprint

- **النظام العام:** `followup_recovery_os` — القطاع: التدريب — الاحتياج: follow_up
- **المخرجات:** طابور استفسارات التسجيل · نموذج حالة الطالب · مجموعة رسائل متابعة
  للدورات · تقرير استرجاع تسجيل أسبوعي
- **المدخلات المطلوبة:** قائمة البرامج · قناة استقبال الاستفسارات · أمثلة رسائل حالية
- **معايير القبول:** كل استفسار له حالة وخطوة تالية · زمن أول رد مقاس قبل/بعد ·
  تقرير استرجاع يُسلَّم في نهاية السبرنت
- **التوسّع:** `executive_command_os`

> القاعدة: لا يُعتمد أي سبرنت بدون مخرجات ومدخلات ومعايير قبول واضحة. يتحقق من ذلك
> `scripts/business_need_validate.py`.
