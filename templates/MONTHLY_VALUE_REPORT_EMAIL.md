# Monthly Value Report — {{ customer_name }} / تقرير القيمة الشهري

**Period / الفترة:** {{ period_start }} → {{ period_end }} ({{ month }})
**Engagement / المشروع:** {{ engagement_id }}
**Governance / الحوكمة:** {{ governance_decision }}

_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة_

---

## Executive Summary / الملخص التنفيذي

This month, your Managed Revenue Ops cycle produced **{{ proof_events_count }}** proof events,
blocked **{{ blocked_unsafe_actions_count }}** unsafe outreach attempts, and recorded value across
**{{ tier_count }}** evidence tiers.

خلال هذا الشهر أنتجت دورة Managed Revenue Ops عدد **{{ proof_events_count }}** حدث Proof،
وحجبت **{{ blocked_unsafe_actions_count }}** محاولات تواصل غير آمن، وسجلت القيمة عبر
**{{ tier_count }}** مستوى من مستويات الأدلة.

---

## Verified Value / القيمة المُتحقَّقة

{{ verified_lines }}

---

## Observed Value / القيمة المرصودة (داخل الـworkflow)

{{ observed_lines }}

---

## Estimated Value / القيمة التقديرية (نطاق غير قابل للادعاء خارجياً)

{{ estimated_lines }}

---

## Adoption / الاعتماد

| Metric / المقياس | Previous / السابق | Current / الحالي | Delta / التغير |
|---|---|---|---|
| Adoption Score | {{ adoption_prev }} | {{ adoption_curr }} | {{ adoption_delta }} |
| Tier / المستوى | — | {{ adoption_tier }} | — |

---

## Friction / الاحتكاك

- **Total events** / **عدد الأحداث:** {{ friction_total }}
- **Top 3 sources** / **أبرز 3 مصادر:** {{ friction_top_3 }}
- **Cost minutes** / **دقائق التكلفة:** {{ friction_cost }}

---

## Limitations / القيود

{{ limitations_list }}

---

## Recommended Next Steps / الخطوات التالية المُوصى بها

{{ next_steps }}

---

## Capital Assets Created This Month / الأصول الرأسمالية المُنشأة هذا الشهر

{{ capital_assets_list }}

---

**This report is a draft for founder approval before send / هذا التقرير مسودّة بانتظار موافقة المؤسس قبل الإرسال.**

— Dealix Team
