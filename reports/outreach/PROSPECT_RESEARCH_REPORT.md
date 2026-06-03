# تقرير بحث العملاء المحتملين — Prospect Research Report (TEMPLATE)

> **قالب.** يُملأ من `data/prospects/prospects.jsonl`. مصادر عامة فقط · **أدوار لا
> أشخاص** · لا PII. الدرجة تحرّك الأولوية لا الإرسال.
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`

- **التاريخ:** `YYYY-MM-DD`
- **عدد العملاء المقيَّمين:** `<count>`
- **مصادر البحث:** `public_website` · `public_press` · `public_social` · `public_job_board`

---

## 1. العملاء المقيَّمون (Scored Prospects — لا PII)

| `prospect_id` | الشركة (placeholder) | `sector` | دور القرار (لا شخص) | `pain_hypothesis` | `evidence_level` | `total` | الأولوية |
|---------------|----------------------|----------|----------------------|--------------------|------------------|---------|----------|
| `PRO-000` | `<company>` | `<sector>` | `Founder / CEO` | `<pain>` | `observed` | `00` | A/B/C/D |
| `PRO-000` | `<company>` | `<sector>` | `Head of Sales` | `<pain>` | `observed` | `00` | A/B/C/D |

> دور القرار يُسجَّل كـ **دور** فقط (Founder / CEO · Managing Director · Head of
> Sales). لا اسم فرد، لا بريد، لا جوّال.

---

## 2. تفصيل الدرجة لأبرز العملاء (Rubric Breakdown — max 100)

| `prospect_id` | `sector_fit` 20 | `buying_signal` 20 | `likely_lead_flow` 15 | `decision_maker_clarity` 15 | `payment_ability` 15 | `personalization_signal` 10 | `risk_low` 5 | **`total`** |
|---------------|------|------|------|------|------|------|------|------|
| `PRO-000` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

---

## 3. التوزيع حسب الأولوية (Priority Distribution)

| النطاق | الأولوية | العدد | الإجراء |
|--------|----------|------|---------|
| 85–100 | A | `0` | خط المسودّات أولاً (تخصيص P3–P4) |
| 70–84 | B | `0` | خط المسودّات (تخصيص ≥ P2) |
| 55–69 | C | `0` | `nurture` — انتظار إشارة ثانية |
| < 55 | D | `0` | مؤجَّل — خارج خط المسودّات |

---

## 4. التوزيع حسب القطاع (`sector`)

| `sector` | العدد | متوسّط `total` |
|----------|------|----------------|
| `marketing_agencies` | `0` | `0` |
| `real_estate_teams` | `0` | `0` |
| `training_companies` | `0` | `0` |
| `local_saas` | `0` | `0` |
| `professional_services` | `0` | `0` |

---

## 5. ملاحظات السلامة (إلزامي)

- [ ] كل بحث من مصادر عامة فقط — لا scraping مخالف، لا شراء قوائم.
- [ ] لا PII — أدوار وأسماء شركات placeholder فقط.
- [ ] كل عميل يحمل `pain_hypothesis` و`evidence_level` و`total`.
- [ ] الدرجة تحرّك الأولوية فقط — الإرسال مُعطَّل (`send_enabled=false`).
- [ ] الأرقام أعلاه أمثلة قالب — تُستبدَل بقيم `data/prospects/prospects.jsonl`.

---

*المصدر: `data/prospects/prospects.jsonl`. المرجع:
`docs/outreach/PROSPECT_RESEARCH_OS_AR.md`.*
