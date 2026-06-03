# Internal Dry Run Plan (Day 0)

**الهدف:** إثبات أن النظام يعمل داخليًا — بدون أي إرسال خارجي — قبل أي إطلاق حقيقي.

---

## شروط الدخول

- [x] `docs/launch/*` موجودة
- [x] `reports/launch/*` موجودة
- [x] سياسات السلامة موجودة (suppression، external content، agent permissions)
- [x] `scripts/checks/check_launch_readiness.py` يمر (hard gates)
- [ ] موافقة المؤسس على بدء Dry Run

## خطوات التشغيل

```bash
# 1) لقطة الحوكمة (تُظهر العناصر بانتظار الموافقة — تخرج بقيمة غير صفرية وهذا متوقّع)
python scripts/governance_check.py

# 2) فحص جاهزية الإطلاق + السكور
python scripts/checks/check_launch_readiness.py

# 3) توليد لوحات المراجعة الداخلية (لا إرسال)
python scripts/generate_outreach_queue.py
python scripts/generate_war_room.py
python scripts/revenue_scorecard.py
```

> ملاحظة: السكربتات الحالية تولّد مسودّات وتقارير **للمراجعة فقط**. لا يوجد أي مسار
> إرسال خارجي في هذا الوضع، وهذا مقصود.

## ماذا تراجع؟

```txt
reports/launch/LAUNCH_SCORECARD.md          ← السكور والأوزان
reports/launch/GO_NO_GO_DECISION.md         ← القرار الحالي
reports/founder/DAILY_SUPER_COMMAND.md      ← أمر المؤسس اليومي (قالب)
company_os/revenue/outreach_queue.json      ← المسودّات (pending_approval)
company_os/war_room/REVENUE_WAR_ROOM_TODAY.md
```

## معايير النجاح (Exit Criteria)

- [ ] hard gates في checker = PASS
- [ ] لا guaranteed claims في أي مسودّة
- [ ] لا contacts مُخترَعة (أدوار فقط، أو مصدر عام موثّق)
- [ ] كل مسودّة حالتها `pending_approval`
- [ ] لا أي استدعاء إرسال خارجي في السجلّات

## بعد النجاح

انتقل إلى تجهيز **Soft Launch** فقط بعد رفع السكور إلى ≥ 75 وبناء:
Account Packs تجريبية + Email Quality Gate تنفيذي + Mini Proposal Gate.

راجع `docs/launch/SOFT_LAUNCH_PLAN_AR.md`.
