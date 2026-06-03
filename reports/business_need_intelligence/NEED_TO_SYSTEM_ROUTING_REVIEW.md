# مراجعة توجيه الاحتياج → النظام — Routing Review
*مولّد آليًا: 2026-06-03 — المصدر: data/business_need_intelligence/*

> تقرير مولّد من `scripts/business_need_report.py`. لا تحرير يدوي.

## 1. توزيع الأنظمة المتخصصة على الأنظمة العامة

| النظام العام | عدد الأنظمة المتخصصة | عدد السبرنتات |
|--------------|---------------------:|--------------:|
| Revenue Operating System | 5 | 3 |
| Executive Command OS | 4 | 2 |
| Follow-up Recovery OS | 8 | 6 |
| WhatsApp Client OS | 4 | 3 |
| Proposal & Proof OS | 5 | 6 |

## 2. الاحتياجات الـ 15 وتوجيهها

| الاحتياج | أساسي | ثانوي | النظام المتخصص |
|----------|-------|-------|----------------|
| lead_capture | revenue_os | whatsapp_client_os | Lead Qualification OS |
| lead_response | followup_recovery_os | whatsapp_client_os | Sector Lead Response OS |
| qualification | revenue_os | followup_recovery_os | Lead Qualification OS |
| follow_up | followup_recovery_os | — | Follow-up Recovery OS |
| sales_execution | revenue_os | proposal_proof_os | Revenue OS |
| proposal | proposal_proof_os | revenue_os | Proposal & Proof OS |
| customer_support | whatsapp_client_os | executive_command_os | Customer Support Triage OS |
| client_onboarding | whatsapp_client_os | proposal_proof_os | Client Onboarding OS |
| delivery | proposal_proof_os | executive_command_os | Delivery Operations OS |
| reporting | executive_command_os | revenue_os | Executive Command / KPI Reporting OS |
| renewal | followup_recovery_os | revenue_os | Renewal & Upsell OS |
| service_quality | executive_command_os | whatsapp_client_os | Service Quality OS |
| knowledge | proposal_proof_os | executive_command_os | Knowledge & Document OS |
| finance_visibility | revenue_os | executive_command_os | Finance & Unit Economics OS |
| ai_governance | executive_command_os | — | AI Team Governance OS |

## 3. ملخص التغطية

- الاحتياجات: 15 / 15
- الأنظمة المتخصصة: 26
- السبرنتات: 20
- الأنظمة العامة المستخدمة في السبرنتات: 5 / 5
