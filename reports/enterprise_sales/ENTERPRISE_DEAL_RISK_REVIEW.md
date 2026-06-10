# Enterprise Deal Risk Review Report — تقرير مراجعة المخاطر

> **Generated:** 2026-06-03 · v0.1
> **Scope:** المخاطر في `data/enterprise_sales/deal_risks.jsonl`
> **Owner:** Sales Lead

---

## 1. ملخص الـ Pipeline Risk

| المؤشر | القيمة |
|--------|--------|
| **إجمالي المخاطر المفتوحة** | 7 |
| **مخاطر high** | 3 |
| **مخاطر medium** | 4 |
| **مخاطر low** | 0 |
| **حسابات متأثرة** | 3 من 3 (100%) |
| **مخاطر بحالة `open`** | 3 |
| **مخاطر بحالة `mitigating`** | 3 |
| **مخاطر بحالة `watching`** | 1 |

---

## 2. التوزيع حسب الفئة

| الفئة | العدد | high | medium | low |
|-------|-------|------|--------|-----|
| champion | 1 | 0 | 1 | 0 |
| economic_buyer | 1 | 1 | 0 | 0 |
| technical | 0 | 0 | 0 | 0 |
| security | 1 | 1 | 0 | 0 |
| procurement | 1 | 0 | 1 | 0 |
| timeline | 1 | 0 | 1 | 0 |
| budget | 1 | 0 | 1 | 0 |
| competitive | 1 | 1 | 0 | 0 |
| internal_change | 0 | 0 | 0 | 0 |

---

## 3. التوزيع حسب الحساب

| الحساب | عدد المخاطر | high | medium | low |
|--------|-------------|------|--------|-----|
| ACC-ENT-001 (industrial) | 3 | 1 | 2 | 0 |
| ACC-ENT-002 (healthcare) | 2 | 2 | 0 | 0 |
| ACC-ENT-003 (retail) | 2 | 0 | 2 | 0 |

---

## 4. التوزيع حسب المالك (Escalation Owner)

| المالك | عدد المخاطر |
|--------|-------------|
| Sales Lead | 3 |
| Sales Lead + Founder | 2 |
| Founder | 1 |
| Founder + Compliance Lead (العميل) | 1 |
| CS Lead + Sales Lead | 1 |
| **المجموع** | **8** (واحد يملكه 2) |

> **Founder هو المالك في 4 من 7 مخاطر (57%).** هذا متوقع لـ design-time — لا توجد صفقات متقدمة.

---

## 5. أهم 5 مخاطر (Top 5)

| # | الحساب | الفئة | الشدّة | Signal | المالك |
|---|--------|-------|--------|--------|--------|
| 1 | ACC-001 | competitive | high | "منافس سبقنا في 3 عروض مشابهة" | Sales Lead + Founder |
| 2 | ACC-002 | economic_buyer | high | "EB Family approval بطيء" | Sales Lead + Founder |
| 3 | ACC-002 | security | high | "حساسية بيانات المرضى" | Founder + Compliance Lead (العميل) |
| 4 | ACC-001 | champion | medium | "CRO جديد لم يستقر" | Sales Lead |
| 5 | ACC-001 | procurement | medium | "CISO/DPO سيُضيف بنود DPA جديدة" | Founder |

---

## 6. Severity Distribution

```
high    ████████████ 3 (43%)
medium  ████████████████ 4 (57%)
low     0
```

> **لا مخاطر low في الـ Pipeline الحالي. هذا منطقي design-time.**

---

## 7. Status Distribution

```
open        ████████████ 3 (43%)
mitigating  ████████████ 3 (43%)
watching    ████ 1 (14%)
```

> **نسبة `open` 43% تحتاج إلى تخفيض هذا الأسبوع.**

---

## 8. توصيات هذا الأسبوع

1. **حركة عاجلة:** ترتيب مكالمة Founder مع EB في ACC-002 خلال 48 ساعة.
2. **ACC-001 champion:** ترتيب 1:1 بين CRO والفFounder (Quick Win).
3. **ACC-002 security:** إرسال DPA موقّع مسبقًا لـ Compliance Lead هذا الأسبوع.
4. **تحديث JSONL:** Sales Lead يُحدّث status للحالات الثلاث المفتوحة بعد اجتماع يوم الإثنين.

---

## 9. KPIs (Placeholders)

| المؤشر | القيمة الحالية | الهدف (placeholder) |
|--------|----------------|---------------------|
| متوسط زمن إغلاق المخاطرة (open → closed) | tracked only | tracked |
| مخاطر high لكل صفقة | 1.0 | < 0.5 |
| مخاطر بحالة `open` > 14 يوم | 0 | 0 |
| مخاطر بدون `escalation_owner` | 0 | 0 |

---

## 10. خلاصة

- الـ Pipeline **3 حسابات نشطة** مع **7 مخاطر** و **3 منها high**.
- **كل الصفقات في Tier-1/2** — لا Tier-3.
- **نصف المخاطر (3/7) بحالة `mitigating`** — يوجد تقدم.
- **الـ ACC-002 (Healthcare) هو الأكثر مخاطرة** (2 high/2).
- **لا مخاطر بحالة `internal_change`** — هذا قد يكون فجوة (لم نرصدها بعد).

> **هذا التقرير يُعاد كل أسبوع. لا بدائل للقاعدة: «كل صفقة نشطة ≥ 1 risk item».**

---

> **آخر تحديث:** 2026-06-03 · v0.1
