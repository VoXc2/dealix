# Founder Max Ops Backlog — 50+ مهمة (تشغيل موسّع)

**الغرض:** فهرس تنفيذي لخطة «أقوى تشغيل» — مربوط بالمستودع وليس مقالات منفصلة.

**مصدر الحقيقة الآلي:** [`dealix/config/founder_max_ops_backlog.yaml`](../../dealix/config/founder_max_ops_backlog.yaml)

**الحالة:** `py -3 scripts/founder_comprehensive_plan_status.py --section backlog --json`

**العمود الفقري:** [FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md](FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md) · [FOUNDER_OPERATING_SYSTEM_AR.md](FOUNDER_OPERATING_SYSTEM_AR.md) · [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md)

---

## ملخص الأقسام

| قسم | المحور | عدد المهام |
|-----|--------|------------|
| A | استراتيجية وقرار أسبوعي | 6 |
| B | منتج وقيمة وأدلة | 8 |
| C | GTM 0→100 | 9 |
| D | إيقاع يومي/أسبوعي | 10 |
| E | PDPL وثقة | 6 |
| F | طاقة ومالية | 6 |
| G | مواد إقناع Full Ops | 9 |
| H | Frontend Ops | 10 |
| I | Backend وAPI | 10 |
| J | Dealix يخدم نفسه | 6 |

**المجموع:** 80 مهمة مرقّمة في YAML (توسيع الخطة الشاملة؛ حدّث `status` عند الإغلاق).

---

## حالات المهمة

| status | معنى |
|--------|------|
| `open` | لم يبدأ |
| `in_progress` | جزء منه موجود في المستودع |
| `done` | مغلق ومتحقق منه |
| `blocked` | معطّل ببوابة خارجية |
| `cancelled` | لم يعد ضمن النطاق |

---

## أوامر مرتبطة

```bash
# لقطة كاملة (قرار أسبوعي + مرحلة 0–5 + backlog)
py -3 scripts/founder_comprehensive_plan_status.py --json

# قرار أسبوع جديد
py -3 scripts/founder_weekly_decision_init.py

# Dogfooding War Room داخلي
py -3 scripts/founder_dogfooding_war_room_sync.py

# تحقق أسبوعي (محلي)
bash scripts/verify_founder_operating_system.sh
py -3 scripts/verify_commercial_launch_ready.py
```

---

## Dogfooding

[DEALIX_DOGFOODING_WAR_ROOM_AR.md](DEALIX_DOGFOODING_WAR_ROOM_AR.md) — معالم Dealix الداخلية في نفس غرفة الإيراد والأدلة.

---

## مواد إقناع

| أصل | مسار |
|-----|------|
| Executive Deck (مخطط شرائح) | [EXECUTIVE_DECK_OUTLINE_AR.md](../commercial/ops_client_pack/EXECUTIVE_DECK_OUTLINE_AR.md) |
| Runbook ديمو | [dealix_ops_runbook_ar.md](../commercial/ops_client_pack/dealix_ops_runbook_ar.md) |
| pptx (خارج Git اختياري) | انظر [ops_client_pack/README_AR.md](../commercial/ops_client_pack/README_AR.md) |

---

*آخر تحديث: 2026-05-18*
