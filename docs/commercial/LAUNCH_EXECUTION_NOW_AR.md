# تنفيذ التدشين الآن — مرجع المؤسس الواحد

**الغرض:** ربط الاستراتيجية (نظرية) بالتشغيل اليومي (تكتيك) في صفحة واحدة — بدون تكرار الوثائق الطويلة.

## 1) البوابة التقنية (ابدأ هنا)

```powershell
powershell -File scripts/verify_dealix_commercial_go_live.ps1
```

مخرج مطلوب: `DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS`

تحقق FE/BE + واجهات Ops:

```bash
py -3 scripts/verify_commercial_fe_be.py
```

## 2) الطبقات الاستراتيجية (اقرأ حسب الحاجة)

| الطبقة | الملف | متى |
|--------|------|-----|
| Thesis + قمع | [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](DEALIX_UNIFIED_REVENUE_ATLAS_AR.md) | أسبوع/شهر |
| 5 دقائق صباحاً | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) | كل يوم |
| تكتيك + سوشال + ICP | [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md) | تنفيذ عميق |
| آلة 24 ساعة | [DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md](DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md) | جدولة CI |

## 3) سلم البيع (لا تخترع إيراداً)

1. **Diagnostic (Ops)** 4,999–15,000 SAR — مدخل المحادثة  
2. **Sprint 499** أو **Data Pack 1,500** — بعد القبول والدفع  
3. **Growth 2,999** — فقط بعد Proof Pack  

مرجع يوم الصفر: [FOUNDER_GO_LIVE_DAY0_AR.md](../ops/FOUNDER_GO_LIVE_DAY0_AR.md)

## 4) اليوم الواحد (~25 دقيقة نظام + لمسات)

```powershell
powershell -File scripts/run_founder_commercial_day.ps1
```

| وقت | المؤسس | الواجهة |
|-----|--------|---------|
| صباح | مراجعة الموجز | `/ar/ops/founder` |
| نهار | 3–10 لمسات بعد الموافقة | `/ar/ops/war-room` · `/ar/ops/approvals` |
| مساء | سطر أدلة | evidence CSV |
| أحد | محتوى أسبوعي | `/ar/ops/marketing` |

مخرجات: `data/founder_briefs/` · `data/war_room_today.json`

## 5) قمع عام (زائر)

- `/ar` · `/ar/dealix-diagnostic` · `/ar/risk-score` · `/ar/proof-pack` · `/ar/learn` · `/ar/partners`

قائمة Soft Launch: [COMMERCIAL_LAUNCH_CHECKLIST_AR.md](COMMERCIAL_LAUNCH_CHECKLIST_AR.md)

## 6) حوكمة (غير قابلة للتفاوض)

- لا واتساب بارد · لا LinkedIn آلي · لا Gmail خارجي بدون موافقة  
- KPI من `kpi_founder_commercial_import.yaml` فقط (انسخ من `.example.yaml`)  
- سوشال: مسودة → SOAEN → نشر يدوي  

## 7) بعد Soft PASS — إنتاج مدفوع

راجع: [PAID_LAUNCH_AFTER_SOFT_PASS_AR.md](PAID_LAUNCH_AFTER_SOFT_PASS_AR.md)
