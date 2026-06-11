# KPI & Finance Control (Dealix)

## المؤشرات الأساسية
| Metric | Cadence | Target | Status |
|--------|---------|--------|--------|
| MRR (SAR) | monthly | 250,000 | watch |
| Active Retainers | monthly | 12 | on track |
| Proposal → Close % | monthly | 35 | watch |
| Drafts Pending Review | daily | 0 | off track |
| Follow-ups Due Today | daily | 5 | on track |
| Proof Items Logged | monthly | 20 | watch |

## قواعد التحكم
1. **off_track** → incident صغير + مالك + تاريخ إصلاح
2. **watch** → متابعة أسبوعية
3. **on_track** → استمر بنفس الإيقاع

## مصادر البيانات
- `scripts/generate_daily_ceo_brief.py`
- `business/_data/deals.ledger.json`
- `business/conversion/CONVERSION_SCORECARD.md`
- `business/_data/outreach_review_queue.json`

## ما لا نقيسه (عن قصد)
- عدد المتابعين (vanity)
- عدد الزيارات (vanity)
- عدد الـ "نقرات" على الإعلانات (vanity)

## ما نقيسه (الفلوس والحركة)
- MRR شهري
- Setup revenue
- Proposal conversion
- Client retention
- Expansion revenue per account
