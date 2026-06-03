# موجة ABM 1 — 30–50 حساب warm + معايير ICP

**الغرض:** تحديد **من** تُلامس في الأسابيع 1–4 قبل أي إعلان أو توسعة — متوافق مع بحث MENA/ABM ومع `gtm_abm_wave1.yaml`.

---

## حجم الموجة

| البند | القيمة |
|-------|--------|
| الحد الأدنى | 30 حساباً فعّالاً في CSV |
| الهدف | 50 حساباً |
| المصدر | قائمة **warm** فقط — [README_WARM_FILL_AR.md](../../../sales-kit/README_WARM_FILL_AR.md) |
| الملف | [agency_accounts_seed.csv](agency_accounts_seed.csv) |

---

## معايير الدخول (يجب تحقق 4/5)

| # | المعيار | كيف تتحقق |
|---|---------|-----------|
| 1 | علاقة warm | مقدمة شخصية · inbound · شريك · حدث |
| 2 | قطاع Motion A أو B | `agency_wedge` · `direct_b2b` · `crm_partner` · `agency_partner` |
| 3 | ألم يطابق إشارة شراء | انظر `buying_signals` في [icp_agency_wedge.yaml](../../../../dealix/config/icp_agency_wedge.yaml) |
| 4 | يقبل موافقة بشرية على الرسائل | لا طلب cold blast |
| 5 | `next_action` + تاريخ | صف جاهز في CSV قبل الاستيراد |

---

## معايير الاستبعاد (فوري)

- قائمة مجمّعة/scraping
- طلب واتساب بارد أو LinkedIn تلقائي
- ميزانية &lt; 5k SAR بدون إحالة شريك (انظر [icp_primary.yaml](../../../../dealix/config/icp_primary.yaml))
- `student_or_job_seeker` · `no_company_name`

---

## توزيع مقترح للـ 50 صفاً

| segment | عدد تقريبي | motion | offer_id افتراضي |
|---------|------------|--------|------------------|
| agency_wedge | 25 | A | ten_lead_audit أو agency_proof_pack |
| direct_b2b | 10 | B | governed_diagnostic |
| crm_partner | 8 | C | diagnostic_layer |
| agency_partner | 7 | A/D | partner_sprint |

**priority:** ≥ 60% صفوف `high` — الباقي `medium` فقط.

---

## نقاط تسجيل (0–100)

```
score = warm_relationship*0.4 + pain_fit*0.3 + buying_signal*0.2 + channel_ok*0.1
```

- **≥ 70:** لمسة هذا الأسبوع
- **50–69:** مسودة فقط
- **&lt; 50:** لا تضف للموجة 1 — احتفظ لموجة 2

---

## موجات لاحقة (لا تفتح مبكراً)

| موجة | حجم | بوابة فتح |
|------|-----|-----------|
| 2 | 100–150 | 3+ `discovery_completed` من موجة 1 + رسالة مكررة في [FOUNDER_SALES_LOOP_AR.md](../FOUNDER_SALES_LOOP_AR.md) |
| 3 | 500+ | أول `proof_pack_delivered` مدفوع + محتوى AEO |

---

## استيراد إلى War Room

```powershell
py -3 scripts/import_war_room_targets.py --dry-run
py -3 scripts/import_war_room_targets.py --apply
```

أو `/ar/ops/war-room` → استيراد من CSV (Admin).

**التالي:** [FOUNDER_SALES_LOOP_AR.md](../FOUNDER_SALES_LOOP_AR.md)
