# فهرس إطلاق Dealix الرئيسي

> أعلى ملف في المشروع: خريطة كل حزم الإطلاق الأربع عشرة ونقاط الدخول لكل منها.

## الحزم

| # | الحزمة | الموقع |
| --- | --- | --- |
| 1 | الموقع والصفحات | docs/site/, src/pages/site/ |
| 2 | الخمسة أنظمة الأساسية | docs/commercial/ |
| 3 | كتالوج الأنظمة الداخلي | docs/business_os_catalog/ |
| 4 | ذكاء احتياج الأعمال | docs/business_need_intelligence/ |
| 5 | 400 Account Packs | docs/account_intelligence/ |
| 6 | Contact Discovery | docs/contacts/ |
| 7 | Outreach + Drafts | docs/outreach/ |
| 8 | Calls + Acquisition | docs/acquisition/ |
| 9 | Mini Proposals | docs/proposals/ |
| 10 | Delivery Automation | docs/delivery/ |
| 11 | Finance + Metrics | docs/finance/, docs/metrics/ |
| 12 | Security + Privacy | docs/security/, docs/privacy/ |
| 13 | Founder Command | docs/founder_control/, docs/operating_factory/ |
| 14 | GitHub Actions + Launch Score | .github/workflows/, scripts/checks/, dealix.py |

## كيف تعرف الجاهزية

- Soft Launch: Launch Score ≥ 75 + الموقع يعمل + الأنظمة الخمسة + ذكاء الاحتياج + عقد Account Pack + بوابات الجودة/الأمن.
- Full Launch: Launch Score ≥ 90 + كل GitHub Actions خضراء + npm build + pytest + كل السكيمات صالحة + لا ادعاءات مضمونة + لا جهات اتصال مخترعة.

## أوامر التحقق

```bash
python dealix.py launch-score
python dealix.py founder-command --dry-run
python dealix.py account-packs --limit 10 --dry-run
```

---
_تم توليد هذا الملف ضمن حزم إطلاق Dealix — راجع `docs/LAUNCH_MASTER_INDEX_AR.md`._
