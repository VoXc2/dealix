# العربية

# موجز مجلس الإدارة الشهري — قالب

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead).

> قالب بإيقاع شهري يستند إلى نمط `auto_client_acquisition/value_os/monthly_report.py`. الحقول بين `{{ }}` تُملأ من بيانات مرصودة. هذا موجز قرار لمجلس الإدارة: أثر، مخاطرة، اتجاه — لا استخدام خام ولا وعد مضمون.

## 1. ترويسة الشهر

- العميل / الوحدة: `{{ tenant_name }}`
- نافذة القياس: `{{ month_label }}`
- أُعِدّ في: `{{ generated_at }}` — مراجَع بشرياً قبل العرض.

## 2. ملخّص تنفيذي

`{{ executive_summary }}` — ثلاث جمل: ما تحقّق، ما العائق، ما القرار القادم.

## 3. أثر الأعمال هذا الشهر

| المؤشّر | القيمة المرصودة | نافذة القياس | المصدر |
|---|---|---|---|
| ساعات موفَّرة | `{{ hours_saved }}` | الشهر | دفتر القيمة |
| عملاء مؤهَّلون | `{{ qualified_leads }}` | الشهر | خطّاف الإيراد |
| فرص مُثبتة بأدلة | `{{ evidenced_opportunities }}` | الشهر | حزمة الأدلة |
| التكلفة لكل نتيجة | `{{ cost_per_outcome }}` | الشهر | ملخّص التكلفة |
| معدّل التبنّي (تقديري) | `{{ adoption_rate }}` | الشهر | مركز القيادة |

## 4. الاتجاه

- اتجاه الساعات الموفَّرة (مدى التوقّع): `{{ hours_forecast_range }}` بمدى ثقة `{{ confidence_band }}`.
- اتجاه العملاء المؤهَّلين: `{{ leads_trend }}` — "الاتجاه المرصود يشير إلى" لا وعد.

## 5. المخاطر أمام مجلس الإدارة

| الخطر | الاحتمالية | الأثر (تقديري) | المالك | الإجراء |
|---|---|---|---|---|
| `{{ risk_1 }}` | `{{ likelihood_1 }}` | `{{ impact_1 }}` | `{{ risk_owner_1 }}` | `{{ action_1 }}` |
| `{{ risk_2 }}` | `{{ likelihood_2 }}` | `{{ impact_2 }}` | `{{ risk_owner_2 }}` | `{{ action_2 }}` |

## 6. القرارات المطلوبة

- `{{ decision_1 }}` — مرتبط بدليل: `{{ evidence_1 }}`.
- `{{ decision_2 }}` — مرتبط بدليل: `{{ evidence_2 }}`.

## 7. ملاحظة منهجية

كل رقم مرصود أو محسوب من بيانات حقيقية. الأرقام التقديرية والتوقّعات موسومة صراحةً مع مدى الثقة. لا يحوي هذا الموجز أي ادعاء مبيعات مضمونة.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

# Monthly Board Brief — Template

**Owner:** Executive Intelligence Layer Lead.

> A monthly-cadence template based on the pattern in `auto_client_acquisition/value_os/monthly_report.py`. Fields in `{{ }}` are filled from observed data. This is a decision brief for the board: impact, risk, trend — not raw usage and not a guaranteed promise.

## 1. Month header

- Customer / unit: `{{ tenant_name }}`
- Measurement window: `{{ month_label }}`
- Generated at: `{{ generated_at }}` — human-reviewed before presentation.

## 2. Executive summary

`{{ executive_summary }}` — three sentences: what was achieved, what is the blocker, what is the next decision.

## 3. Business impact this month

| Indicator | Observed value | Measurement window | Source |
|---|---|---|---|
| Hours saved | `{{ hours_saved }}` | Month | Value ledger |
| Qualified leads | `{{ qualified_leads }}` | Month | Revenue hook |
| Evidenced opportunities | `{{ evidenced_opportunities }}` | Month | Proof pack |
| Cost per outcome | `{{ cost_per_outcome }}` | Month | Cost summary |
| Adoption rate (estimated) | `{{ adoption_rate }}` | Month | Command Center |

## 4. Trend

- Hours-saved trend (forecast range): `{{ hours_forecast_range }}` with a `{{ confidence_band }}` confidence band.
- Qualified-leads trend: `{{ leads_trend }}` — "the observed trend points to", not a promise.

## 5. Risks before the board

| Risk | Likelihood | Impact (estimated) | Owner | Action |
|---|---|---|---|---|
| `{{ risk_1 }}` | `{{ likelihood_1 }}` | `{{ impact_1 }}` | `{{ risk_owner_1 }}` | `{{ action_1 }}` |
| `{{ risk_2 }}` | `{{ likelihood_2 }}` | `{{ impact_2 }}` | `{{ risk_owner_2 }}` | `{{ action_2 }}` |

## 6. Decisions required

- `{{ decision_1 }}` — tied to evidence: `{{ evidence_1 }}`.
- `{{ decision_2 }}` — tied to evidence: `{{ evidence_2 }}`.

## 7. Methodology note

Every number is observed or computed from real data. Estimated numbers and forecasts are labelled explicitly with a confidence range. This brief contains no guaranteed sales claim.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
