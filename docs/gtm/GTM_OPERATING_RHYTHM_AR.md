# إيقاع تشغيل GTM — Daily & Weekly Rhythm

إيقاع ثابت يحوّل التسويق والمبيعات إلى خط إنتاج يومي قابل للقياس.

## الإيقاع اليومي

| الوقت | المرحلة | الفاعل | المخرج | بوّابة؟ |
|------|---------|--------|--------|--------|
| 07:30 | البحث والإشارات | Signal/Prospect OS | `reports/signals/SIGNAL_REPORT.md` | — |
| 08:30 | توليد 250 مسودّة | Draft Factory | `data/outreach/drafts.jsonl` | — |
| 09:00 | الجودة/الامتثال/القابلية | Gates | `reports/outreach/DRAFT_GATE_REVIEW.md` | ✅ |
| 10:00 | طابور الموافقة | Founder | `reports/outreach/APPROVAL_QUEUE.md` | ✅ موافقة |
| 11:00 | **خطة** دفعة معتمدة محدودة | Sending Ramp | `reports/outreach/SENDING_BATCH_PLAN.md` | ✅ موافقة |
| 13:00 | طابور الردود | Reply Handling | تحديث `data/commercial/opportunities.jsonl` | — |
| 15:00 | شركاء/صحافة/وظائف | Partner/Press OS | `reports/partnerships/`, `reports/press/` | — |
| 18:00 | إنتاج المحتوى | Content OS | `reports/content/CONTENT_PRODUCTION_QUEUE.md` | — |
| 21:00 | تقرير GTM اليومي | Command Room | `reports/gtm/DAILY_GTM_REPORT.md` | — |

**قواعد الإيقاع اليومي:**
- 250 مسودّة مطلوبة يومياً (100 first-touch + 75 fu1 + 50 fu2 + 15 proposal-intro + 10 close-loop).
- خطوة 11:00 تنتج **خطة** فقط. الإرسال الفعلي يحتاج حُكم قابلية ≥ `LIMITED_SEND_READY` وموافقة المؤسّس.
- أي مسودّة دون `P1` لا تدخل طابور الموافقة.

## الإيقاع الأسبوعي (نهاية الأسبوع)

1. **إيقاف أسوأ 20%** من الرسائل (حسب reply/positive-rate) — توثَّق في `DRAFT_REJECTION_REASONS_AR`.
2. **مضاعفة أفضل 20%** — تُرفع إلى قوالب معتمدة.
3. تحديث كتيّبات القطاعات (`docs/sectors/*`).
4. تحديث بنك الاعتراضات (`data/commercial/objections.yaml`).
5. تحديث كتالوج المنتجات (`data/commercial/product_catalog.yaml`).
6. مراجعة صحة الدومين (`reports/outreach/DOMAIN_HEALTH_REVIEW.md`).
7. مراجعة ROI لكل قناة.
8. اختيار **3 أهداف صحافة** (فقط عند وجود proof milestone).
9. اختيار **10 أهداف شراكة**.

المخرج الأسبوعي: `reports/gtm/WEEKLY_GTM_REVIEW.md` + `company_os/war_room/WEEKLY_CEO_BRIEF.md`.

## ربط الإيقاع بالأمان
كل مرحلة تكتب تقريراً؛ لا مرحلة تُرسل خارجياً. البوّابات (09:00) والموافقة (10:00–11:00)
هي نقاط التحكّم الوحيدة التي تسمح بالانتقال من "مسودّة" إلى "خطة إرسال معتمدة".
