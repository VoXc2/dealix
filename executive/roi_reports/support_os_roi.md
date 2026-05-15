# العربية

# تقرير عائد الاستثمار — Support OS — قالب

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead).

> قالب واقعي لتقرير عائد خدمة Support OS. الحقول بين `{{ }}` تُملأ من بيانات مرصودة عبر `auto_client_acquisition/value_os/value_ledger.py`. لا رقم مفبرك. لا وعد بنتيجة مضمونة.

## 1. الترويسة

- الخدمة: Support OS — تشغيل الدعم.
- العميل / الوحدة: `{{ tenant_name }}`
- نافذة القياس: `{{ period_start }}` إلى `{{ period_end }}`
- أُعِدّ في: `{{ generated_at }}` — مراجَع بشرياً.

## 2. قصة العائد

تختصر Support OS زمن الردّ الأول وترفع نسبة الردود المدعومة بمصدر. هذا التقرير يعرض الأثر المرصود على عمل فريق الدعم، لا عدد الرسائل فقط.

## 3. الأثر المرصود

| المؤشّر | القيمة المرصودة | المصدر | ملاحظة |
|---|---|---|---|
| ساعات موفَّرة في معالجة التذاكر | `{{ hours_saved }}` | دفتر القيمة | ضمن النافذة |
| تذاكر مُحلّة بمساعدة الخدمة | `{{ assisted_tickets }}` | دفتر القيمة | مرصود |
| نسبة الردود الحاملة لمصدر | `{{ sourced_reply_rate }}` | محرّك الأدلة | مرصود |
| احتكاك مُزال | `{{ friction_removed }}` | سجل الاحتكاك | مرصود |
| التكلفة لكل تذكرة مُعالَجة | `{{ cost_per_ticket }}` | ملخّص التكلفة | مرصود |

## 4. تقدير العائد

- التكلفة المرصودة للخدمة في النافذة: `{{ observed_cost }}`.
- القيمة التقديرية للوقت الموفَّر: `{{ estimated_time_value }}` (تقديري — معدّل ساعة معلن).
- نسبة العائد التقديرية: `{{ estimated_roi_ratio }}` (تقديري، ليس وعداً).

## 5. القراءة

`{{ narrative }}` — أين الأثر مدعوم بدليل، وأين هو تقديري.

## 6. التوصية القادمة

`{{ recommendation }}` — مرتبطة بدليل: `{{ evidence_reference }}`.

## 7. حدود التقرير

الأرقام التقديرية موسومة "تقديري". لا تُرسِل Dealix رسائل خارجية نيابة عن العميل دون موافقته الصريحة. لا يحوي التقرير بيانات تعريف شخصية.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

# ROI Report — Support OS — Template

**Owner:** Executive Intelligence Layer Lead.

> A realistic ROI report template for the Support OS service. Fields in `{{ }}` are filled from observed data via `auto_client_acquisition/value_os/value_ledger.py`. No fabricated number. No guaranteed-outcome promise.

## 1. Header

- Service: Support OS — support operations.
- Customer / unit: `{{ tenant_name }}`
- Measurement window: `{{ period_start }}` to `{{ period_end }}`
- Generated at: `{{ generated_at }}` — human-reviewed.

## 2. ROI story

Support OS shortens first-response time and raises the share of replies backed by a source. This report shows the observed impact on the support team's work, not just the message count.

## 3. Observed impact

| Indicator | Observed value | Source | Note |
|---|---|---|---|
| Hours saved in ticket handling | `{{ hours_saved }}` | Value ledger | Within the window |
| Tickets resolved with service assistance | `{{ assisted_tickets }}` | Value ledger | Observed |
| Share of replies carrying a source | `{{ sourced_reply_rate }}` | Proof engine | Observed |
| Friction removed | `{{ friction_removed }}` | Friction log | Observed |
| Cost per handled ticket | `{{ cost_per_ticket }}` | Cost summary | Observed |

## 4. ROI estimate

- Observed service cost in the window: `{{ observed_cost }}`.
- Estimated value of time saved: `{{ estimated_time_value }}` (estimated — stated hourly rate).
- Estimated ROI ratio: `{{ estimated_roi_ratio }}` (estimated, not a promise).

## 5. Reading

`{{ narrative }}` — where the impact is evidence-backed, and where it is an estimate.

## 6. Next recommendation

`{{ recommendation }}` — tied to evidence: `{{ evidence_reference }}`.

## 7. Report limits

Estimated numbers are labelled "estimated". Dealix sends no external messages on the customer's behalf without their explicit consent. The report contains no PII.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
