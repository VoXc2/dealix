# قائمة مراجعة أسبوعية/ربع سنوية — حزمة استخبارات السوق

**المدة:** أسبوعياً 20 دقيقة (جمعة) · ربع سنوياً 60 دقيقة  
**آخر تحديث:** 2026-05-18

---

## أسبوعي (كل جمعة)

### سوق وتموضع
- [ ] هل رسالة Why Now ما زالت صحيحة؟ ([POSITIONING](POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md))
- [ ] هل ICP Motion A محدّث في seed CSV؟
- [ ] اعتراض جديد هذا الأسبوع → [OBJECTIONS](MARKET_INTELLIGENCE_OBJECTIONS_PDPL_AR.md)

### تشغيل مؤسس
- [ ] `founder_weekly_scorecard.py` منفّذ
- [ ] evidence CSV vs KPI import متسقان
- [ ] 3+ لمسات Motion A أو تعديل خطة الأسبوع القادم

### محتوى
- [ ] منشورات الأسبوع **موافق عليها** ([CONTENT_GTM](MARKET_INTELLIGENCE_CONTENT_GTM_AR.md))
- [ ] لا ادعاء إقامة/PDPL مخالف للواقع

### منتج/امتثال
- [ ] أي تغيير sub-processor → تحديث landing + COMPLIANCE_CERTIFICATIONS
- [ ] `pytest tests/test_commercial_doctrine.py -q` إن لمسنا حوكمة

---

## شهري

- [ ] مراجعة سلم العروض ([REVOPS_PACKAGES](DEALIX_REVOPS_PACKAGES_AR.md))
- [ ] تحديث واحد في PROCUREMENT_FAQ إن ورد سؤال RFP جديد
- [ ] Business Now: هل ركيزة تجارية تغيّرت؟

---

## ربع سنوي

### سوق
- [ ] تحديث أرقام SaaS من **مصدر واحد** ([SAAS_MARKET](MARKET_INTELLIGENCE_SAUDI_SAAS_MARKET_AR.md))
- [ ] مراجعة [FOUNDER_GTM_BENCHMARKS](operations/FOUNDER_GTM_BENCHMARKS_AR.md)

### قانوني/بنية
- [ ] [PDPL_LEGAL](MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md) — فجوات G1–G5
- [ ] INFRA rubric §11 سجل region مؤكد
- [ ] [CLOUD_CROSS_BORDER](MARKET_INTELLIGENCE_CLOUD_CROSS_BORDER_AR.md) إن تغيّر مزود

### شركاء/مستثمر
- [ ] [INVESTOR_PARTNER](MARKET_INTELLIGENCE_INVESTOR_PARTNER_AR.md) — data room محدّث
- [ ] EN summary للشركاء الدوليين

---

## مخرجات المراجعة (سجّل في evidence أو weekly note)

```yaml
review_date: YYYY-MM-DD
type: weekly | monthly | quarterly
market_signal_change: null | "<ملاحظة>"
icp_adjustment: null | "<ملاحظة>"
legal_gap_closed: []
infra_region_confirmed: "<region or pending>"
content_posts_approved: N
next_week_focus: "<Motion A | Proof | Paid gate>"
```

---

## أوامر سريعة

```powershell
py -3 scripts/founder_weekly_scorecard.py
py -3 scripts/commercial_value_map_status.py
```
