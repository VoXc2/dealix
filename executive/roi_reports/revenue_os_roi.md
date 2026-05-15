# العربية

# تقرير عائد الاستثمار — Revenue OS — قالب

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead).

> قالب واقعي لتقرير عائد خدمة Revenue OS. الحقول بين `{{ }}` تُملأ من بيانات مرصودة عبر `auto_client_acquisition/value_os/value_ledger.py`. لا رقم مفبرك. لا وعد بمبيعات مضمونة.

## 1. الترويسة

- الخدمة: Revenue OS — ذكاء الإيراد.
- العميل / الوحدة: `{{ tenant_name }}`
- نافذة القياس: `{{ period_start }}` إلى `{{ period_end }}`
- أُعِدّ في: `{{ generated_at }}` — مراجَع بشرياً.

## 2. قصة العائد

تساعد Revenue OS فريق الإيراد على رؤية خط الأنابيب مبكراً وترتيب الفرص المؤهَّلة. هذا التقرير يعرض الأثر المرصود، لا الاستخدام الخام.

## 3. الأثر المرصود

| المؤشّر | القيمة المرصودة | المصدر | ملاحظة |
|---|---|---|---|
| عملاء مؤهَّلون | `{{ qualified_leads }}` | خطّاف الإيراد | مرصود |
| فرص مُثبتة بأدلة | `{{ evidenced_opportunities }}` | حزمة الأدلة | كل فرصة بدليل |
| ساعات موفَّرة في الفرز | `{{ hours_saved }}` | دفتر القيمة | ضمن النافذة |
| التكلفة لكل عميل مؤهَّل | `{{ cost_per_qualified_lead }}` | ملخّص التكلفة | مرصود |

## 4. تقدير العائد

- التكلفة المرصودة للخدمة في النافذة: `{{ observed_cost }}`.
- القيمة التقديرية للوقت الموفَّر: `{{ estimated_time_value }}` (تقديري — يعتمد على معدّل ساعة معلن).
- نسبة العائد التقديرية: `{{ estimated_roi_ratio }}` (تقديري، ليس وعداً).

## 5. القراءة

`{{ narrative }}` — ما الذي يدعمه الدليل، وما الذي ما زال تقديرياً.

## 6. التوصية القادمة

`{{ recommendation }}` — مرتبطة بدليل: `{{ evidence_reference }}`.

## 7. حدود التقرير

الأرقام التقديرية موسومة "تقديري". Dealix لا تَعِد بمبيعات مضمونة؛ تعرض فرصاً مُثبتة بأدلة. لا يحوي التقرير بيانات تعريف شخصية.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

# ROI Report — Revenue OS — Template

**Owner:** Executive Intelligence Layer Lead.

> A realistic ROI report template for the Revenue OS service. Fields in `{{ }}` are filled from observed data via `auto_client_acquisition/value_os/value_ledger.py`. No fabricated number. No guaranteed-sales promise.

## 1. Header

- Service: Revenue OS — revenue intelligence.
- Customer / unit: `{{ tenant_name }}`
- Measurement window: `{{ period_start }}` to `{{ period_end }}`
- Generated at: `{{ generated_at }}` — human-reviewed.

## 2. ROI story

Revenue OS helps the revenue team see the pipeline early and rank qualified opportunities. This report shows observed impact, not raw usage.

## 3. Observed impact

| Indicator | Observed value | Source | Note |
|---|---|---|---|
| Qualified leads | `{{ qualified_leads }}` | Revenue hook | Observed |
| Evidenced opportunities | `{{ evidenced_opportunities }}` | Proof pack | Each tied to evidence |
| Hours saved in triage | `{{ hours_saved }}` | Value ledger | Within the window |
| Cost per qualified lead | `{{ cost_per_qualified_lead }}` | Cost summary | Observed |

## 4. ROI estimate

- Observed service cost in the window: `{{ observed_cost }}`.
- Estimated value of time saved: `{{ estimated_time_value }}` (estimated — based on a stated hourly rate).
- Estimated ROI ratio: `{{ estimated_roi_ratio }}` (estimated, not a promise).

## 5. Reading

`{{ narrative }}` — what the evidence supports, and what is still an estimate.

## 6. Next recommendation

`{{ recommendation }}` — tied to evidence: `{{ evidence_reference }}`.

## 7. Report limits

Estimated numbers are labelled "estimated". Dealix promises no guaranteed sales; it presents evidenced opportunities. The report contains no PII.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
