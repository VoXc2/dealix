# تقرير الإشارات اليومي — Daily Signal Report (TEMPLATE)

> **قالب.** يُملأ يومياً الساعة 07:30 من `data/signals/`. مصادر عامة فقط · أدوار لا
> أشخاص · لا PII. الإشارة فرضية لا حكم.
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`

- **التاريخ:** `YYYY-MM-DD`
- **المصادر:** `public_website` · `public_careers_page` · `public_job_board` ·
  `public_press` · `public_social`
- **إجمالي الإشارات اليوم:** `<count>` (شركة: `<n>` · وظيفة: `<n>`)

---

## 1. العدّ حسب النوع (`signal_type`)

| `signal_type` | العدد | متوسّط `confidence` | الملاحظات |
|---------------|------|---------------------|-----------|
| `job_posting` | `0` | `0.0` |  |
| `new_branch` | `0` | `0.0` |  |
| `new_service_launch` | `0` | `0.0` |  |
| `marketing_campaign` | `0` | `0.0` |  |
| `active_hiring` | `0` | `0.0` |  |
| `multi_forms` | `0` | `0.0` |  |
| `crm_sales_support_role_visible` | `0` | `0.0` |  |
| `recent_press` | `0` | `0.0` |  |
| `content_activity` | `0` | `0.0` |  |
| `partner_ecosystem` | `0` | `0.0` |  |
| **الإجمالي** | `0` | — |  |

---

## 2. أبرز الإشارات (Top Signals)

| `signal_id` | الشركة (placeholder) | `sector` | `signal_type` | المصدر | `evidence_level` | `confidence` |
|-------------|----------------------|----------|----------------|--------|------------------|--------------|
| `SIG-C-000` | `<company>` | `<sector>` | `<type>` | `<public_source>` | `observed` | `0.0` |
| `SIG-J-000` | `<company>` | `<sector>` | `job_posting` | `public_job_board` | `observed` | `—` |

> ترتيب الأولوية: التقاطع (إشارتان على نفس الشركة) ثم `confidence` ثم `evidence_level`.

---

## 3. الآلام المطابَقة (Mapped Pains)

| `mapped_pain` | عدد الإشارات | العرض المرشّح | ملاحظة المطابقة |
|---------------|--------------|----------------|------------------|
| `lead_leakage` | `0` | `DLX-L1` |  |
| `follow_up_chaos` | `0` | `DLX-L1`/`DLX-L2` |  |
| `crm_data_disorder` | `0` | `DLX-L3` |  |
| `proposal_delay` | `0` | `DLX-L2` |  |
| `weak_reporting` | `0` | `DLX-L3` |  |
| `sales_team_inconsistency` | `0` | `DLX-L3` |  |
| `support_overload` | `0` | `DLX-L3` |  |
| `no_proof_case_study_system` | `0` | `DLX-L1` |  |

---

## 4. التقاطعات (Cross-Signals = أولوية أعلى)

| الشركة (placeholder) | الإشارات المتقاطعة | أثر على `buying_signal` |
|----------------------|--------------------|--------------------------|
| `<company>` | `active_hiring` + `crm_sales_support_role_visible` | يرفع الأولوية |

---

## 5. ملاحظات السلامة (إلزامي)

- [ ] جميع الإشارات من مصادر عامة فقط — لا scraping مخالف.
- [ ] لا PII في التقرير — أدوار وأسماء شركات placeholder فقط.
- [ ] كل إشارة تحمل `evidence_level` و`mapped_pain`.
- [ ] الأرقام أعلاه أمثلة قالب — تُستبدَل بقيم اليوم الفعلية من `data/signals/`.

---

*المصدر: `data/signals/company_signals.jsonl` · `data/signals/job_signals.jsonl`.
المرجع: `docs/signals/SIGNAL_DETECTION_OS_AR.md`.*
