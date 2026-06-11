# Delivery Automation Blueprint (Dealix)

## الفلسفة
التسليم ليس “نرسل داشبورد”. التسليم هو:
1. نظام تشغيل حقيقي عند العميل
2. Workflow مرئي وقابل للمراجعة
3. Proof report أسبوعي
4. توسعة مبنية على فجوة مرصودة

## المراحل (6 مراحل)
| # | Stage | Day Range | Risk |
|---|-------|-----------|------|
| 1 | Day 0 — Intake | 0–1 | خريطة أصحاب مصلحة غير واضحة |
| 2 | Workflow Map | 2–4 | محاولة أتمتة كل شيء |
| 3 | Command Center Setup | 5–8 | مؤشرات بدون owners |
| 4 | Automation Build | 9–14 | أتمتة قبل إثبات القيمة |
| 5 | Weekly Review | 15+ | تخطّي المراجعة |
| 6 | Expansion | 30+ | عرض توسعة بدون proof |

## الأتمتة
- Command Center URL حيّ
- تقرير أسبوعي مولّد (scripts/generate_weekly_command_report.py)
- سجل إثبات أسبوعي
- مسوّدة تقرير مراجعة شهرية للعميل

## الحوكمة
- لا توسعة قبل توقيع proof report من العميل
- لا أتمتة لقرار مالي أو قانوني بدون human-in-the-loop
- كل إجراء خارجي له audit log
