# خريطة احتياج القطاعات — Sector Need Map

لكل قطاع: أقوى 5 احتياجات، النظام العام الأساسي/الثانوي/التوسّعي، أفضل المشترين،
الإشارات، أول Sprint، زاوية الإيميل والاتصال، ومتغيّر التسليم.

مصدر الحقيقة: `data/business_need_intelligence/sector_need_map.yaml` (14 قطاعًا).

---

## ملخص القطاعات

| القطاع | أقوى الاحتياجات | النظام الأساسي | أول Sprint |
|--------|------------------|----------------|------------|
| وكالات التسويق | lead_response, follow_up, proposal, client_onboarding, reporting | followup_recovery_os | Campaign Lead Recovery |
| شركات التدريب | lead_response, follow_up, qualification, reporting, customer_support | followup_recovery_os | Enrollment Recovery |
| العيادات | lead_response, customer_support, client_onboarding, follow_up, service_quality | whatsapp_client_os | Clinic Appointment Flow |
| العقار | lead_response, follow_up, qualification, customer_support, proposal | followup_recovery_os | Property Lead Response |
| الخدمات المهنية | proposal, sales_execution, reporting, knowledge, delivery | proposal_proof_os | Proposal & Scope Proof |
| التوظيف | follow_up, lead_response, reporting, client_onboarding, proposal | followup_recovery_os | Recruitment Follow-up |
| SaaS / تقنية | client_onboarding, customer_support, renewal, sales_execution, reporting | whatsapp_client_os | Demo-to-Onboarding |
| اللوجستيات | delivery, reporting, service_quality, customer_support, follow_up | proposal_proof_os | Vendor Coordination |
| المطاعم / فروع | customer_support, service_quality, reporting, follow_up, renewal | whatsapp_client_os | Customer Message Flow |
| مزودو التعليم | lead_capture, qualification, lead_response, follow_up, reporting | revenue_os | Course Inquiry Routing |
| الاستشارات | proposal, knowledge, reporting, sales_execution, delivery | proposal_proof_os | Proposal & Scope Proof |
| التجزئة / FMCG | customer_support, service_quality, renewal, reporting, follow_up | whatsapp_client_os | Customer Message Flow |
| الخدمات الصناعية | proposal, delivery, lead_response, reporting, service_quality | proposal_proof_os | Proposal & Scope Proof |
| كثيفة المشتريات | delivery, reporting, sales_execution, service_quality, finance_visibility | proposal_proof_os | Vendor Coordination |

---

## تفصيل مختار (مع زوايا الرسائل)

### 1) وكالات التسويق
- **النظام:** أساسي `followup_recovery_os` · ثانوي `proposal_proof_os` · توسّع `revenue_os`
- **المشتري:** Founder / CEO · Managing Director · Account Director · Head of Growth
- **الإيميل:** "قيمة الحملة لا تضيع في الإعلان غالبًا؛ تضيع فيما يحدث بعد أول lead."
- **التسليم:** Campaign Lead Queue · First-Response Template · Post-Lead Follow-up Set · Weekly Recovery Report

### 2) شركات التدريب
- **النظام:** أساسي `followup_recovery_os` · ثانوي `whatsapp_client_os` · توسّع `executive_command_os`
- **المشتري:** Founder · Marketing Manager · Training Manager · Registration Lead
- **الإيميل:** "آخر متابعة لم تحدث قد تكون سبب ضياع تسجيل جاهز."
- **التسليم:** Enrollment Inquiry Queue · Student Status Model · Course Inquiry Message Set · Weekly Registration Recovery Report

### 3) العيادات
- **النظام:** أساسي `whatsapp_client_os` · ثانوي `followup_recovery_os` · توسّع `executive_command_os`
- **المشتري:** Owner · Clinic Manager · Front Desk Lead · Operations Manager
- **الإيميل:** "واتساب في العيادات ليس مجرد محادثة؛ هو بداية رحلة حجز ومتابعة وتصعيد."
- **التسليم:** WhatsApp Intake Flow · Patient Journey Model · Appointment Reminder Set · Booking & No-show Report

### 4) العقار
- **النظام:** أساسي `followup_recovery_os` · ثانوي `whatsapp_client_os` · توسّع `revenue_os`
- **الإيميل:** "في العقار، التأخير في الرد أو المتابعة قد يحوّل lead مهتمًا إلى فرصة ضائعة."

### 5) الخدمات المهنية / الاستشارات
- **النظام:** أساسي `proposal_proof_os`
- **الإيميل:** "العرض المقنع لا يحتاج كلامًا أكثر؛ يحتاج نطاقًا واضحًا ودليلًا وخطوة تالية."

> بقية القطاعات (التوظيف، SaaS، اللوجستيات، المطاعم، التعليم، التجزئة، الصناعة،
> المشتريات) مفصّلة بالكامل في ملف البيانات، بنفس الحقول: الاحتياجات، الأنظمة،
> المشترون، الإشارات، السبرنت، الزوايا، المدخلات، ومعايير القبول.
