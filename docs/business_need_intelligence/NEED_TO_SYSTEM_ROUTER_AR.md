# موجّه الاحتياج → النظام — Need to System Router

يربط كل احتياج من الـ 15 بـ **نظام عام واحد (Core)** أساسي، وأنظمة عامة ثانوية
اختيارية، ثم بالنظام **المتخصص** المستخدم في التسليم.

مصدر الحقيقة: `data/business_need_intelligence/need_to_system_router.yaml`.

القاعدة الذهبية: **كل نظام متخصص يرجع إلى نظام عام واحد فقط.**

---

## 1. الأنظمة العامة الخمسة

| المعرّف | النظام | يملك الاحتياجات |
|---------|--------|------------------|
| `revenue_os` | Revenue Operating System | lead_capture, qualification, sales_execution, finance_visibility |
| `executive_command_os` | Executive Command OS | reporting, ai_governance, service_quality |
| `followup_recovery_os` | Follow-up Recovery OS | lead_response, follow_up, renewal |
| `whatsapp_client_os` | WhatsApp Client OS | customer_support, client_onboarding |
| `proposal_proof_os` | Proposal & Proof OS | proposal, delivery, knowledge |

---

## 2. جدول التوجيه (15 احتياجًا)

| # | الاحتياج | النظام العام الأساسي | عام ثانوي | النظام المتخصص |
|--:|----------|----------------------|-----------|----------------|
| 1 | lead_capture | revenue_os | whatsapp_client_os | Lead Qualification OS |
| 2 | lead_response | followup_recovery_os | whatsapp_client_os | Sector Lead Response OS |
| 3 | qualification | revenue_os | followup_recovery_os | Lead Qualification OS |
| 4 | follow_up | followup_recovery_os | — | Follow-up Recovery OS |
| 5 | sales_execution | revenue_os | proposal_proof_os | Revenue OS |
| 6 | proposal | proposal_proof_os | revenue_os | Proposal & Proof OS |
| 7 | customer_support | whatsapp_client_os | executive_command_os | Customer Support Triage OS |
| 8 | client_onboarding | whatsapp_client_os | proposal_proof_os | Client Onboarding OS |
| 9 | delivery | proposal_proof_os | executive_command_os | Delivery Operations OS |
| 10 | reporting | executive_command_os | revenue_os | Executive Command / KPI Reporting OS |
| 11 | renewal | followup_recovery_os | revenue_os | Renewal & Upsell OS |
| 12 | service_quality | executive_command_os | whatsapp_client_os | Service Quality OS |
| 13 | knowledge | proposal_proof_os | executive_command_os | Knowledge & Document OS |
| 14 | finance_visibility | revenue_os | executive_command_os | Finance & Unit Economics OS |
| 15 | ai_governance | executive_command_os | — | AI Team Governance OS |

---

## 3. الأنظمة المتخصصة (≈30) → النظام العام

### → revenue_os
Lead Qualification OS · Revenue OS (sector variants) · Finance & Unit Economics OS ·
Partner / Channel OS · Content Authority OS

### → followup_recovery_os
Follow-up Recovery OS (sector variants) · Marketing Campaign Follow-up OS ·
Real Estate Lead Response OS · Admissions / Enrollment OS · Recruitment Pipeline OS ·
Candidate Follow-up OS · Renewal & Upsell OS · Appointment Booking OS

### → whatsapp_client_os
WhatsApp Client OS (sector variants) · Customer Support Triage OS ·
Clinic Patient Journey OS · Client Onboarding OS

### → proposal_proof_os
Proposal & Proof OS (sector variants) · Delivery Operations OS · Vendor Management OS ·
Knowledge & Document OS · Pricing & Scope Control OS

### → executive_command_os
Executive Command OS (role variants) · KPI Reporting OS · AI Team Governance OS ·
Service Quality OS

---

## 4. مثال خامات أساسية تتخصص حسب القطاع

| النظام العام | التخصيص (أمثلة) |
|--------------|------------------|
| Follow-up Recovery OS | Enrollment Follow-up · Property Lead Follow-up · Candidate Follow-up |
| WhatsApp Client OS | Clinic WhatsApp Flow · Real Estate WhatsApp Flow · Training WhatsApp Flow |
| Proposal & Proof OS | Consulting Proposal · Agency Proposal · B2B Services Proposal |
| Executive Command OS | Founder Daily Command · Clinic Manager Command · Agency Owner Command |
| Revenue OS | Agency Revenue OS · Training Revenue OS · Real Estate Revenue OS |

> ملاحظة: لا نبني 30 نظامًا من الصفر. نبني 5 محرّكات ونخصّص مخرجاتها.
