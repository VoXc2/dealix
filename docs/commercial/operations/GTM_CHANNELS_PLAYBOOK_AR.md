# قنوات GTM — السعودية (warm فقط)

**مرتبط بـ:** [GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md](../GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md) · `dealix/config/gtm_abm_wave1.yaml`

---

## ماتريس القنوات

| القناة | متى | الحد اليومي | أداة Dealix |
|--------|-----|-------------|-------------|
| `linkedin_manual` | warm · تعليق ثم DM بموافقة | ضمن 10 لمسات | War Room مسودة |
| `email_warm` | مقدمة أو رد سابق | 5 متابعات | `/approvals` |
| `partner_intro` | شريك CRM/وكالة | 1 محادثة شريك | [PARTNER_ONBOARDING_KIT_AR.md](PARTNER_ONBOARDING_KIT_AR.md) |
| `inbound` | نموذج / Calendly | فوري | `/dealix-diagnostic` |
| `phone_task` | علاقة قائمة | حسب الحاجة | يدوي — لا تسجيل آلي |

## ممنوع (دائماً)

- `cold_whatsapp` · `linkedin_auto_send` · `scraping`

## تسلسل لمسة واحدة (Motion A)

1. طبقة Proof 1–2 ([PROOF_STACK_ORDER_AR.md](PROOF_STACK_ORDER_AR.md))
2. مسودة — موافقة
3. `message_sent_manual` في CSV
4. متابعة 48–72h → `reply_received` أو `closed_lost`

## إعلانات مدفوعة

**بوابة:** لا LinkedIn Ads / Google قبل **3** `discovery_completed` أو `demo_booked` من موجة 1 (حقيقية، غير template).

بعد البوابة: محتوى مرجعي + landing واحد — ليس بديل المحادثة.
