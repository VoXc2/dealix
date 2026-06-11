# Founder War Room (Dealix)

## الهدف
غرفة واحدة، كل صباح. قرارات المؤسس اليومية على صفحة واحدة.

## المكوّنات
1. **Daily CEO moves** — أهم 5 مهام اليوم
2. **Revenue priorities** — أول 5 مراحل من قمع الاكتساب
3. **Risks** — أهم 4 مخاطر نشطة
4. **Operational constraints** — قواعد الحوكمة
5. **Assets to produce** — الأصول المطلوب إنتاجها
6. **Client pipeline pressure** — ضغط خط العميل الحالي

## الإيقاع
- **يومي:** CEO Brief (5 دقائق قراءة)
- **أسبوعي:** Weekly Operating Review
- **شهري:** Monthly Founder Review

## الأصول
- صفحة War Room على الموقع
- API: `/api/company-os/ceo-brief?format=md` (md|txt|json)
- سكربت: `scripts/generate_daily_ceo_brief.py`
- قالب: `business/reports/DAILY_CEO_BRIEF_TEMPLATE.md`
