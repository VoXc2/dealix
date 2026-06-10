# Dealix — تحديد أولويات الميزات

## المبدأ الأساسي

**الأولوية تحكمها البيانات، ليس الآراء.**

---

## إطار RICE/ICE

### RICE Score

```
RICE = (Reach × Impact × Confidence) / Effort
```

| المقياس | الوصف | الوزن |
|---------|-------|-------|
| **Reach** | عدد المستخدمين المتأثرين في الفترة | 0-100 |
| **Impact** | الأثر على الهدف (0.25 = 25%) | 0-1 |
| **Confidence** | مستوى الثقة في التقدير | 0-100% |
| **Effort** | جهد الفريق بالأشهر | 1-12 |

### ICE Score

```
ICE = (Impact × Confidence × Ease) / Risk
```

| المقياس | الوصف | الوزن |
|---------|-------|-------|
| **Impact** | الأثر على الإيراد/العميل | 1-10 |
| **Confidence** | الثقة في التقدير | 1-10 |
| **Ease** | سهولة التنفيذ | 1-10 |
| **Risk** | مستوى المخاطرة | 1-10 |

---

## عوامل إضافية

### Revenue Impact
- الإيراد المتوقع
- تأثير على margin
- تأثير على conversion rate

### Delivery Complexity
- الجهد الهندسي
- Dependencies
- Time to market

### Risk Level
- Technical risk
- Compliance risk
- Reputational risk

---

## تصنيف الأولويات

| الأولوية | النطاق | الإجراء |
|----------|--------|---------|
| **P0** | Launch blocker | Build now |
| **P1** | Revenue critical | Build next |
| **P2** | Scale enabler | Backlog |
| **P3** | Nice to have | Future |
| **P4** | Defer | Park |
| **P5** | Do not build | Reject |

---

## سجل الميزات

كل feature يجب أن يتضمن:

| الحقل | الوصف |
|-------|-------|
| **name** | اسم الـ feature |
| **user** | المستخدم المستهدف |
| **problem** | المشكلة التي تحلها |
| **outcome** | النتيجة المتوقعة |
| **revenue_impact** | الأثر على الإيراد |
| **risk** | مستوى المخاطرة |
| **effort** | الجهد المطلوب |
| **priority** | الأولوية (P0-P5) |
| **dependencies** | التبعيات |
| **acceptance_criteria** | معايير القبول |

---

## أمثلة

### Example 1: Approval Queue (P0)
```
name: Approval Queue
user: Founder
problem: رسائل ترسل بدون مراجعة
outcome: كل رسالة تمر عبر queue للموافقة
revenue_impact: High (prevents mistakes)
risk: Low
effort: 2 weeks
priority: P0
dependencies: None
acceptance_criteria:
  - Queue UI يعمل
  - Email notifications يعمل
  - Audit log موجود
```

### Example 2: WhatsApp Auto-send (P5)
```
name: WhatsApp Auto-send
user: Sales team
problem: إرسال يدوي يستغرق وقت
outcome: إرسال تلقائي
revenue_impact: Medium
risk: High (compliance)
effort: 4 weeks
priority: P5
reason: No consent flow, compliance risk too high
```

---

## مصادر Feedback

| المصدر | النوع | الأولوية |
|--------|-------|----------|
| Replies | Signal | High |
| Discovery calls | Insight | High |
| Proposal objections | Pain | High |
| Delivery blockers | Risk | Critical |
| Customer success reports | Usage | Medium |
| Renewal reasons | Value | High |
| Churn risks | Alert | Critical |
| Partner feedback | Signal | Medium |

---

## Process

1. **جمع**: تسجيل كل feedback في `data/product/feedback.jsonl`
2. **تحليل**: تقييم الأثر والترجيح
3. **تصنيف**: تعيين أولوية لكل feature
4. **مراجعة**: اجتماع أسبوعي للمراجعة
5. **اعتماد**: موافقة المؤسس على P0/P1
6. **تنفيذ**: إضافة للـ sprint

---

## Decision Rules

| الحالة | القرار |
|--------|--------|
| ICE > 70 | Build now |
| ICE 40-70 | Backlog |
| ICE < 40 | Do not build |
| Risk > 7 | Do not build |
| No customer signal | Do not build |

---

## _links

- Strategy: `PRODUCT_STRATEGY_AR.md`
- MVP Scope: `MVP_SCOPE_AR.md`
- What Not to Build: `WHAT_NOT_TO_BUILD_AR.md`
- Data: `data/product/features.jsonl`
