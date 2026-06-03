# كيف تستخدم حزمة الاستخبارات اليوم — مبيعات · منتج · GTM · بنية

**آخر تحديث:** 2026-05-18 · **ابدأ من:** [MARKET_INTELLIGENCE_MASTER_INDEX_AR.md](MARKET_INTELLIGENCE_MASTER_INDEX_AR.md)

---

## صباح المؤسس (15 دقيقة)

| دقيقة | فعل | مرجع |
|-------|-----|-------|
| 0–5 | شغّل `run_founder_commercial_day` · اقرأ الموجز | FOUNDER_REVOPS |
| 5–8 | صفقة واحدة: هل Decision Passport مكتمل؟ | GOVERNED_AI |
| 8–12 | Motion A: 3 حسابات من seed | SAAS_MARKET § ICP |
| 12–15 | مسودة سوشال → موافقة (لا نشر تلقائي) | MASTER plan |

---

## قبل اجتماع اكتشاف (10 دقائق)

1. اقرأ [`POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md`](POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md) — فقرة 30 ثانية.
2. حضّر Sample Proof / Risk Score إن وُجد.
3. راجع Truth Matrix للتكاملات — لا تعد بـ HubSpot إن أحمر.
4. إن ذكر العميل PDPL: [`MARKET_INTELLIGENCE_OBJECTIONS_PDPL_AR.md`](MARKET_INTELLIGENCE_OBJECTIONS_PDPL_AR.md).

---

## بعد الاجتماع (5 دقائق)

```bash
py -3 scripts/founder_evening_evidence.py --append --company "اسم_الشركة" --event meeting_held
```

+ debrief: [`operations/founder_meeting_debrief_template.yaml`](operations/founder_meeting_debrief_template.yaml)

---

## عند إرسال عرض / RFP

| خطوة | وثيقة |
|------|--------|
| فقرة امتثام | PDPL_LEGAL §6 |
| ملحق تقني region | INFRA rubric YAML |
| أسئلة أمن | PROCUREMENT_FAQ |
| تسعير | DEALIX_REVOPS_PACKAGES |

---

## في المنتج (أسبوعي — CTO/مهندس)

| مهمة | مخرج |
|------|------|
| تحقق anti-waste tests | `pytest tests/test_commercial_doctrine.py -q` |
| مسارات personal data logged | `http_stack.py` prefixes |
| تحديث sub-processors إن تغيّر مزود | COMPLIANCE_CERTIFICATIONS + landing |
| region فعلي في rubric سجل §8 | INFRA |

---

## في GTM / محتوى (أسبوعي)

| قناة | زاوية | ممنوع |
|------|-------|-------|
| لينكد إن | Why Now + حوكمة | أرقام سوق دقيقة كادعاء |
| واتساب warm | مسودة يدوية | بارد |
| بريد | opt-out + DPA عند العميل | ادعاء «100% KSA hosting» |

**محتوى:** `dealix/config/social_content_queue.yaml` — queue للموافقة فقط.

---

## عند توقيع عميل (> 50K SAR)

- [ ] DPA checklist كامل
- [ ] ملحق INFRA مملوء
- [ ] DPIA إن قطاع منظّم
- [ ] تحديث `landing/sub-processors.html` إن لزم
- [ ] Pre-enterprise checklist في COMPLIANCE_CERTIFICATIONS

---

## مسار أسبوعي (جمعة)

| # | فعل |
|---|-----|
| 1 | `founder_weekly_scorecard.py` |
| 2 | مراجعة evidence CSV vs KPI import |
| 3 | تحديث واحد من: positioning / objections / procurement FAQ |
| 4 | Business Now: `/ar/business-now#strategy` |

---

## خريطة قرار «ماذا أقرأ؟»

```
سؤال العميل عن السوق؟     → SAAS_MARKET
سؤال PDPL؟                 → OBJECTIONS_PDPL + PDPL_LEGAL
سؤال أين البيانات؟         → INFRA + PROCUREMENT § hosting
سؤال AI يرسل لوحده؟        → GOVERNED_AI
تنظيم يومي؟                → هذا الملف § صباح
بريد بعد اجتماع؟           → EMAIL_TEMPLATES
ديمو؟                      → DEMO_SCRIPT
لماذا نخسر/نفوز؟           → CATEGORY_BATTLECARD
بعد الدفع؟                 → CUSTOMER_SUCCESS
```

## أوامر آلة

```powershell
py -3 scripts/market_intelligence_status.py
py -3 scripts/market_intelligence_status.py --json
# وثيقة الأسبوع + تذكير جمعة تلقائياً في:
powershell -File scripts/run_founder_commercial_day.ps1
```
