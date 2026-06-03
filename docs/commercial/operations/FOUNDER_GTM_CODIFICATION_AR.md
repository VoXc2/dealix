# ترميز GTM — أول 10 صفقات/محادثات

**الغرض:** تحويل حدس المؤسس إلى أنماط قابلة للتكرار قبل أي توظيف مبيعات (Phi / founder-led best practice).

---

## ماذا تُوثّق لكل صفقة

| حقل | سؤال |
|-----|------|
| trigger | ما الذي أثار المحادثة؟ |
| economic_buyer | من يوقّع/يدفع؟ |
| urgency | أين الإلحاح؟ |
| message_winner | أي جملة اشتغلت؟ |
| objection_primary | الاعتراض الأول |
| next_motion | A/B/C/D |

---

## أدوات

1. **بعد كل اجتماع:** `py -3 scripts/founder_meeting_debrief_init.py --company "..."` → `data/founder_debriefs/`
2. **أنماط مجمّعة:** عدّل [founder_gtm_codification_registry.yaml](founder_gtm_codification_registry.yaml)
3. **تقدّم:** `py -3 scripts/founder_comprehensive_plan_status.py --section gtm`

**هدف:** 10 debriefs مكتملة أو 10 patterns في الـ registry → verdict `READY`.

---

## ربط War Room

حدّث `war_room_status` و [DEALIX_REVENUE_WAR_ROOM_AR.md](../../ops/DEALIX_REVENUE_WAR_ROOM_AR.md) بعد كل خطوة.

---

*آخر تحديث: 2026-05-18*
