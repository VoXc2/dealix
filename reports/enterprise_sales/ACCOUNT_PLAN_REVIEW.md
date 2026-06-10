# Account Plan Review — مراجعة خطط الحسابات

> **Generated:** 2026-06-03 · v0.1
> **Scope:** TAPs في `data/enterprise_sales/accounts.jsonl`
> **Owner:** Sales Lead

---

## 1. ملخص الـ Completeness

| الحساب | الحقول Required مكتملة؟ | الفجوات |
|--------|--------------------------|---------|
| ACC-ENT-001 | ✅ جميع الـ 18 حقل | لا فجوات بنيوية. بعض الحقول placeholder (severity, urgency). |
| ACC-ENT-002 | ✅ جميع الـ 18 حقل | لا فجوات بنيوية. يتطلب Privacy/DPA detail. |
| ACC-ENT-003 | ✅ جميع الـ 18 حقل | 3 حقول placeholder (competitor names). |

> **جميع الحسابات الثلاثة حقّقت 100% من الحقول الـ Required في schema.**

---

## 2. مراجعات تفصيلية

### 2.1 ACC-ENT-001 (شركة_X_صناعية)

| البُعد | الحالة | ملاحظات |
|--------|--------|---------|
| **Company basics** | ✅ | sector=industrial، region=Dammam، public_listed |
| **Size bands** | ✅ | 5001-10000, 1-5B SAR |
| **Pain** | ✅ | primary_pain موثّق، severity=high |
| **Trigger** | ✅ | competitive_pressure، urgency=high |
| **Stakeholder Map** | ✅ | 4 stakeholders (STK-001..004) |
| **Champion/Economic Buyer hypotheses** | ✅ | مكتوبة كـ placeholders |
| **Technical/Legal Reviewer** | ✅ | placeholders |
| **First Offer** | ✅ | pilot, placeholder price band |
| **Pilot Scope** | ✅ | فريق + قناة + 8 أسابيع + 3 metrics |
| **Expansion Path** | ✅ | 3 stages |
| **Proof Needed** | ✅ | 4 عناصر |
| **Risks** | ✅ | 2 risks |
| **Next Action** | ✅ | مع owner و due_window |
| **Evidence Level** | ✅ | assumption (صحيح لـ design-time) |
| **Gaps** | — | لا أرقام قابلة للقياس (placeholder) — مقبول |

**التقييم:** **95% Complete.** ممتاز كنموذج. يحتاج فقط:
- Risk Mitigation detail (لكل risk).
- Specific Competitive names (لا تكشف هنا — placeholder كافية).

---

### 2.2 ACC-ENT-002 (ExampleCo KSA - Healthcare)

| البُعد | الحالة | ملاحظات |
|--------|--------|---------|
| **Company basics** | ✅ | healthcare, hospital_network, Riyadh |
| **Size bands** | ✅ | 1001-5000, 500M-1B |
| **Pain** | ✅ | primary_pain موثّق، severity=high |
| **Trigger** | ✅ | regulatory_pressure (NHIC + PDPL) |
| **Stakeholder Map** | ✅ | 5 stakeholders |
| **Champion/Economic Buyer hypotheses** | ✅ | placeholders |
| **Technical/Legal Reviewer** | ✅ | placeholders |
| **First Offer** | ✅ | diagnostic (بداية أصغر — حكمة) |
| **Pilot Scope** | ✅ | 6 أسابيع + 3 metrics |
| **Expansion Path** | ✅ | 2 stages |
| **Proof Needed** | ✅ | 3 عناصر (DPA, NHIC, anonymized reference) |
| **Risks** | ✅ | 2 risks |
| **Next Action** | ✅ | مع owner و due_window |
| **Evidence Level** | ✅ | assumption |
| **Gaps** | — | `recent_events` غير محدد — مقبول design-time |

**التقييم:** **90% Complete.** جيد جدًا. يحتاج:
- تحديد `recent_events` (آخر 3 أحداث موثّقة).
- توضيح من هو "CISO" في الرعاية الصحية (أحيانًا يكون Compliance Lead، ليس CISO تقليدي).
- Pilot metrics أدق (placeholder, لكن يفضّل ربطها بـ HEDIS أو KPIs صحية).

---

### 2.3 ACC-ENT-003 (شركة_Y_تجزئة)

| البُعد | الحالة | ملاحظات |
|--------|--------|---------|
| **Company basics** | ✅ | retail, fashion, Jeddah |
| **Size bands** | ✅ | 501-1000, 200M-1B |
| **Pain** | ✅ | primary_pain، severity=medium |
| **Trigger** | ✅ | growth_target، urgency=medium |
| **Stakeholder Map** | ⚠️ | فقط 3 stakeholders (المطلوب ≥ 4) |
| **Champion/Economic Buyer hypotheses** | ✅ | placeholders |
| **Technical/Legal Reviewer** | ✅ | placeholders |
| **First Offer** | ✅ | proof_of_value |
| **Pilot Scope** | ✅ | 4 أسابيع + 3 metrics |
| **Expansion Path** | ✅ | 2 stages |
| **Proof Needed** | ✅ | 3 عناصر |
| **Risks** | ✅ | 2 risks |
| **Next Action** | ✅ | مع owner و due_window |
| **Evidence Level** | ✅ | assumption |
| **Gaps** | — | Multi-threading منخفض (3/4 minimum) |

**التقييم:** **85% Complete.** جيد. يحتاج:
- إضافة ≥ 1 stakeholder آخر (Procurement أو Legal).
- توضيح Attribution model (مهم في retail).
- KPIs أكثر دقة (CAC, LTV, Attribution).

---

## 3. مقارنة شاملة

| المؤشر | ACC-001 | ACC-002 | ACC-003 |
|--------|---------|---------|---------|
| **% Complete** | 95% | 90% | 85% |
| **Evidence Level** | assumption | assumption | assumption |
| **Stage** | prospect | discovery | prospect |
| **Tier** | 1 | 1 | 2 |
| **Stakeholders** | 4 | 5 | 3 ⚠️ |
| **Risks** | 2 | 2 | 2 |
| **Next Action محددة** | ✅ | ✅ | ✅ |
| **Expansion Path** | 3 stages | 2 stages | 2 stages |

---

## 4. الفجوات الحرجة (Critical Gaps)

| الحساب | الفجوة | خطورة |
|--------|--------|-------|
| ACC-003 | Multi-Threading Index = 3 (أقل من 4) | high — لا proposal قبل 4 |
| ACC-002 | `recent_events` فارغ | medium — يُضعف trigger story |
| ACC-001 | Risk Mitigation plans مفقودة | medium |
| ACC-002 | Pilot metrics غير مرتبطة بـ HEDIS/KPIs صحية | low |
| ACC-003 | Attribution model غير محدد | medium |

---

## 5. التوصيات (هذا الأسبوع)

1. **ACC-003:** إضافة 2 stakeholders (Procurement + Legal) → Multi-Threading = 5.
2. **ACC-002:** توثيق آخر 3 أحداث (NHIC update، PDPL audit، إلخ) في `recent_events`.
3. **ACC-001:** إضافة Mitigation Plan لكل risk.
4. **كل الحسابات:** تحديد Reference anonymized واحد قابل للمشاركة (يحتاج Founder approval).

---

## 6. تقييم شامل

> **جودة البيانات:** مرتفعة نسبيًا. 3 حسابات مع 18 حقل لكلٍّ = 54 نقطة بيانات، معظمها placeholder صحيح.
>
> **Gap واحد حرج:** ACC-003 لا يستوفي Multi-threading Rule (4 stakeholders قبل proposal).
>
> **استعداد General لـ Pilot:** ACC-002 هو الأكثر جاهزية (في `pilot_scope`). ACC-001 و ACC-003 لا يزالان يحتاجان 1–2 أسبوع من العمل قبل بدء Pilot.

---

> **آخر تحديث:** 2026-06-03 · v0.1
