# متغيّر التسليم حسب القطاع — Delivery Variant by Sector

كيف تتخصّص مخرجات النظام العام لكل قطاع وقت التسليم. **كل متغيّر** يحمل:
`core_system` · `specialized_delivery_pack` · `required_inputs` · `acceptance_criteria`.
هذا هو **عقد التسليم** لأول سبرنت.

مصدر الحقيقة: `data/business_need_intelligence/delivery_variant_by_sector.yaml`.

---

## جدول المتغيّرات (14 قطاعًا)

| القطاع | النظام العام | أول Sprint | حزمة التسليم (مختصر) |
|--------|--------------|------------|------------------------|
| وكالات التسويق | followup_recovery_os | Campaign Lead Recovery | Campaign Lead Queue · First-Response Template · Follow-up Set · Weekly Recovery Report |
| شركات التدريب | followup_recovery_os | Enrollment Recovery | Enrollment Inquiry Queue · Student Status Model · Message Set · Weekly Recovery Report |
| العيادات | whatsapp_client_os | Clinic Appointment Flow | WhatsApp Intake Flow · Patient Journey Model · Reminder Set · Booking & No-show Report |
| العقار | followup_recovery_os | Property Lead Response | Property Lead Queue · Fast First-Response · Viewing Follow-up · Response-Time Report |
| الخدمات المهنية | proposal_proof_os | Proposal & Scope Proof | Scoped Proposal Template · Proof Sheet · Next-Step Block · Review Checklist |
| التوظيف | followup_recovery_os | Recruitment Follow-up | Candidate Pipeline · Follow-up Set · Interview Coordination · Weekly Status Report |
| SaaS / تقنية | whatsapp_client_os | Demo-to-Onboarding | Onboarding Flow · Activation Checklist · Post-Demo Follow-up · Activation Report |
| اللوجستيات | proposal_proof_os | Vendor Coordination | Vendor Register · Coordination Flow · SLA Tracking · Daily Operations Report |
| المطاعم / فروع | whatsapp_client_os | Customer Message Flow | Unified Message Flow · Complaint Triage · Quick-Reply · Weekly Experience Report |
| مزودو التعليم | revenue_os | Course Inquiry Routing | Inquiry Routing Rules · Readiness Tagging · Lead Capture Form · Source Report |
| الاستشارات | proposal_proof_os | Proposal & Scope Proof | Unified Proposal Template · Knowledge Library · Scope Model · Next-Step Block |
| التجزئة / FMCG | whatsapp_client_os | Customer Message Flow | Unified Message Flow · Complaint & Return Triage · Quick-Reply · Experience Report |
| الخدمات الصناعية | proposal_proof_os | Proposal & Scope Proof | Quote Template · Work-Order Follow-up · Delivery Status Model · Quote-to-Delivery Report |
| كثيفة المشتريات | proposal_proof_os | Vendor Coordination | Vendor & Contract Register · Purchase Request Flow · Performance Tracking · Performance Report |

---

## مبدأ "5 محرّكات، تخصيص بلا بناء جديد"

| المحرّك العام | متغيّرات متخصصة |
|----------------|------------------|
| Follow-up Recovery OS | Enrollment · Property Lead · Candidate Follow-up |
| WhatsApp Client OS | Clinic Flow · Real Estate Flow · Training Flow |
| Proposal & Proof OS | Consulting · Agency · B2B Services Proposal |
| Executive Command OS | Founder · Clinic Manager · Agency Owner Command |
| Revenue OS | Agency · Training · Real Estate Revenue OS |

---

## قاعدة القبول

لا يُعتمد متغيّر تسليم بدون **مدخلات مطلوبة** و**معايير قبول**. يتحقق من ذلك
`scripts/business_need_validate.py` لكل القطاعات الـ 14.
