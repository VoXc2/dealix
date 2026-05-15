# العربية

# تقرير عائد الاستثمار — Company Brain — قالب

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead).

> قالب واقعي لتقرير عائد خدمة Company Brain (المعرفة المؤسسية). الحقول بين `{{ }}` تُملأ من بيانات مرصودة. لا رقم مفبرك. لا وعد مضمون.

## 1. الترويسة

- الخدمة: Company Brain — معرفة المؤسسة وذاكرتها.
- العميل / الوحدة: `{{ tenant_name }}`
- نافذة القياس: `{{ period_start }}` إلى `{{ period_end }}`
- أُعِدّ في: `{{ generated_at }}` — مراجَع بشرياً.

## 2. قصة العائد

تجعل Company Brain إجابات الفريق مدعومة بمصدر وقابلة للتتبّع. هذا التقرير يعرض أثر المعرفة على سرعة العمل وجودته، لا عدد الاستعلامات فقط.

## 3. الأثر المرصود

| المؤشّر | القيمة المرصودة | المصدر | ملاحظة |
|---|---|---|---|
| ساعات موفَّرة في البحث عن المعلومة | `{{ hours_saved }}` | دفتر القيمة | ضمن النافذة |
| إجابات حاملة لمصدر | `{{ sourced_answers }}` | محرّك الأدلة | مرصود |
| نسبة "أدلة غير كافية" بدل إجابة بلا مصدر | `{{ insufficient_evidence_rate }}` | طبقة المعرفة | مرصود |
| عمق الاستخدام عبر الفرق | `{{ usage_depth }}` | مركز القيادة | مرصود |
| التكلفة لكل إجابة | `{{ cost_per_answer }}` | ملخّص التكلفة | مرصود |

## 4. تقدير العائد

- التكلفة المرصودة للخدمة في النافذة: `{{ observed_cost }}`.
- القيمة التقديرية للوقت الموفَّر: `{{ estimated_time_value }}` (تقديري — معدّل ساعة معلن).
- نسبة العائد التقديرية: `{{ estimated_roi_ratio }}` (تقديري، ليس وعداً).

## 5. القراءة

`{{ narrative }}` — أين يدعم الدليل الأثر، وأين يبقى تقديرياً.

## 6. التوصية القادمة

`{{ recommendation }}` — مرتبطة بدليل: `{{ evidence_reference }}`.

## 7. حدود التقرير

الأرقام التقديرية موسومة "تقديري". لا يحوي التقرير بيانات تعريف شخصية. القيمة المعروضة تقديرية ما لم تُوصَف صراحةً كمرصودة.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

# ROI Report — Company Brain — Template

**Owner:** Executive Intelligence Layer Lead.

> A realistic ROI report template for the Company Brain service (enterprise knowledge). Fields in `{{ }}` are filled from observed data. No fabricated number. No guaranteed promise.

## 1. Header

- Service: Company Brain — enterprise knowledge and memory.
- Customer / unit: `{{ tenant_name }}`
- Measurement window: `{{ period_start }}` to `{{ period_end }}`
- Generated at: `{{ generated_at }}` — human-reviewed.

## 2. ROI story

Company Brain makes the team's answers source-backed and traceable. This report shows the impact of knowledge on work speed and quality, not just the query count.

## 3. Observed impact

| Indicator | Observed value | Source | Note |
|---|---|---|---|
| Hours saved searching for information | `{{ hours_saved }}` | Value ledger | Within the window |
| Answers carrying a source | `{{ sourced_answers }}` | Proof engine | Observed |
| Share of "insufficient evidence" instead of a sourceless answer | `{{ insufficient_evidence_rate }}` | Knowledge layer | Observed |
| Usage depth across teams | `{{ usage_depth }}` | Command Center | Observed |
| Cost per answer | `{{ cost_per_answer }}` | Cost summary | Observed |

## 4. ROI estimate

- Observed service cost in the window: `{{ observed_cost }}`.
- Estimated value of time saved: `{{ estimated_time_value }}` (estimated — stated hourly rate).
- Estimated ROI ratio: `{{ estimated_roi_ratio }}` (estimated, not a promise).

## 5. Reading

`{{ narrative }}` — where the evidence supports the impact, and where it remains an estimate.

## 6. Next recommendation

`{{ recommendation }}` — tied to evidence: `{{ evidence_reference }}`.

## 7. Report limits

Estimated numbers are labelled "estimated". The report contains no PII. A displayed value is an estimate unless explicitly described as observed.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
