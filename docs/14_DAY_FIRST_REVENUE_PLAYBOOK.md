# كتيب 14 يوماً — أول إيراد (Dealix)

كل يوم: أمر واحد + مخرج واحد + شرط No-Go.

| اليوم | المشغّل | المخرج المتوقع |
|-------|---------|------------------|
| 0 | `bash scripts/revenue_execution_verify.sh` | `DEALIX_REVENUE_EXECUTION=PASS` |
| 0 | `curl -s https://api.dealix.me/health` | تدوين `git_sha` في [`DEALIX_FULL_OPS_VERIFICATION_REPORT.md`](DEALIX_FULL_OPS_VERIFICATION_REPORT.md) |
| 1 | `python scripts/dealix_first10_warm_intros.py` | لوحة خانات في `docs/revenue/live/` |
| 2 | `POST /api/v1/sales/script` × 5 مسودات | نصوص جاهزة للمراجعة |
| 3 | إرسال يدوي لـ 5 warm intros | تسجيل الردود خارج الريبو |
| 4 | `python scripts/dealix_diagnostic.py ...` لعميلين | تقرير صفحة واحدة لكل عميل |
| 5 | `python scripts/dealix_pilot_499_close_pack.py --write` | نطاق Pilot جاهز |
| 6 | `POST /api/v1/compliance-os/action-check` على إجراءات مقترحة | كل خارجي `approval_required` أو `blocked` |
| 7 | `GET /api/v1/proof-ledger/events` + تدوين أحداث | Proof events حقيقية فقط |
| 8 | `GET /api/v1/company-service/command-center` مع عميل تجريبي | شرح الواجهة بدون jargon |
| 9 | `GET /api/v1/executive-os/weekly-pack` | مسودة أسبوع للمؤسس |
| 10 | متابعة ردود + diagnostic ثالث | — |
| 11 | عرض Pilot لأفضل lead | التزام أو دفع يدوي |
| 12 | فتح تسليم: `GET /api/v1/delivery-os/session/{service_id}` | checklist |
| 13 | Proof pack مراجعة | لا شهادات بدون موافقة |
| 14 | تحديث [`DEALIX_FULL_OPS_VERIFICATION_REPORT.md`](DEALIX_FULL_OPS_VERIFICATION_REPORT.md) + قرار التوسع | انظر [`V12_1_TRIGGER_RULES.md`](V12_1_TRIGGER_RULES.md) |

**No-Go:** أي إرسال حي، شحن حي، واتساب بارد، scraping، أو proof مزيف — توقف فوراً.
