# قالب الجر — Dealix Traction Template (AR)

> **القالب الرسمي لعرض traction في data room.** كل رقم موثّق أو
> مُصنَّف TBD. لا fake traction، لا inflated claims.

**الحالة:** مسودة — Phase 1 من Agent #16
**التاريخ:** 2026-06-03

---

## 1. ملاحظة دائمة

> **قاعدة الأرقام:** كل رقم في هذا القالب يأتي مع **Evidence Level** (L0–L5)
> و**مصدر**. لو غاب أي منهما ⇒ حقل `TBD — evidence pending`.

## 2. مقاييس الإيرادات (Revenue Metrics)

| المقياس | القيمة | Evidence Level | المصدر | التاريخ |
| --- | --- | --- | --- | --- |
| عدد العملاء الدافعين | TBD | | | |
| MRR (شهري متكرر) | TBD SAR | | Moyasar dashboard | |
| ARR (سنوي متكرر) | TBD SAR | | محسوب من MRR | |
| متوسط حجم الصفقة (ACV) | TBD SAR | | Moyasar invoices | |
| New MRR (صافي شهري) | TBD SAR | | Moyasar reports | |
| Churn MRR | TBD SAR | | cancellation logs | |
| Net Revenue Retention | TBD % | | محسوب | |

## 3. مقاييس المبيعات (Sales Metrics)

| المقياس | القيمة | Evidence Level | المصدر |
| --- | --- | --- | --- |
| Leads qualified (شهري) | TBD | | HubSpot export |
| Conversion rate (lead → paying) | TBD % | | HubSpot funnel |
| متوسط زمن الإغلاق | TBD يوم | | CRM history |
| Pipeline coverage (3x target) | TBD | | CRM |
| عدد pilots جارية | TBD | | CRM status |
| عدد pilots منتهية | TBD | | CRM status |

## 4. مقاييس التسليم (Delivery Metrics)

| المقياس | القيمة | Evidence Level | المصدر |
| --- | --- | --- | --- |
| Time to first proof (متوسط) | 5–7 أيام | L2 | delivery playbook |
| Acceptance rate (1st try) | TBD % | | founder review |
| On-time delivery rate | TBD % | | delivery log |
| Renewal rate (90-day) | TBD % | | renewal tracker |
| Time to first value (TTV) | TBD | | client feedback |

## 5. مقاييس المنتج (Product Metrics)

| المقياس | القيمة | Evidence Level | المصدر |
| --- | --- | --- | --- |
| Daily Active Users (DAU) | TBD | | PostHog |
| Weekly Active Orgs (WAO) | TBD | | PostHog |
| WhatsApp templates approved | TBD | | Meta dashboard |
| Proof events generated (شهري) | TBD | | proof ledger |
| Approval queue (متوسط) | TBD | | approval stats |

## 6. مقاييس رضا العملاء (Customer Satisfaction)

| المقياس | القيمة | Evidence Level | المصدر |
| --- | --- | --- | --- |
| NPS | TBD | | (لم يُقاس بعد) |
| CSAT (post-pilot) | TBD | | post-pilot survey |
| Testimonials count | TBD | | signed consents |
| Case studies count (L4) | TBD | | `case_study_permissions.jsonl` |

## 7. مقاييس الفريق (Team Metrics)

| المقياس | القيمة | Evidence Level | المصدر |
| --- | --- | --- | --- |
| Headcount (current) | 1 (founder) | | payroll |
| Headcount (planned 12m) | TBD | | hiring plan |
| Contractors active | TBD | | founder log |
| Time to fill key role | TBD | | hiring tracker |

## 8. الشراكات (Partnerships)

| الشريك | الحالة | القيمة المضافة | Evidence Level |
| --- | --- | --- | --- |
| Moyasar | Live | payments | L4 |
| HubSpot | Live | CRM | L4 |
| WhatsApp (multi) | Live | messaging | L4 |
| Calendly | Live | scheduling | L4 |
| PostHog | Live | analytics | L4 |
| Sentry | Live | monitoring | L4 |
| Railway | Live | hosting | L4 |
| AWS S3 (me-south-1) | Live | backups | L4 |

## 9. الإنجازات (Key Milestones)

| التاريخ | الإنجاز | Evidence |
| --- | --- | --- |
| 2026-Q1 | MVP launch (full ops architecture) | `docs/V12_FULL_OPS_ARCHITECTURE.md` |
| 2026-Q1 | Official launch verdict PASS | `docs/DEALIX_LAUNCH_CLOSURE_VERDICT.md` |
| 2026-Q2 | First 3 paid pilots (TBD) | Moyasar dashboard |
| 2026-Q2 | First 5 signed case studies (TBD) | `case_study_permissions.jsonl` |
| 2026-Q3 | First enterprise contract (TBD) | contracts archive |
| 2026-Q4 | SOC 2 readiness assessment (TBD) | audit firm |

## 10. ما لا يُذكر (Out of Scope)

- لا أرقام بدون evidence level + source.
- لا توقعات بدون سيناريو.
- لا ادعاءات sector-wide (e.g. "we are #1 in KSA").
- لا ادعاءات تخمينية (e.g. "thousands of clients").

## 11. دورة التحديث (Update Cadence)

- **Weekly:** revenue metrics + pipeline.
- **Monthly:** full template review.
- **Quarterly:** template refresh for data room.
- **On event:** أي تغيير جوهري (إغلاق جولة، شراكة جديدة، عميل كبير).

## 12. المراجع

- `docs/data_room/DATA_ROOM_INDEX_AR.md` — index
- `docs/data_room/COMPANY_OVERVIEW_AR.md` — company
- `docs/BUSINESS_MODEL.md` — business model
- `docs/EXECUTIVE_DECISION_PACK.md` — decisions
- `docs/finance/FOUNDER_UNIT_ECONOMICS_MODEL_AR.md` — unit economics
- `docs/legal/CLAIMS_EVIDENCE_MATRIX_AR.md` — claims matrix
