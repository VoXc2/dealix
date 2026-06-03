# Dealix — Daily Operating Factory

يحوّل Dealix إلى مصنع تشغيل وبيع وتسليم يومي للأنظمة الخمسة (Focus 5):

1. نظام تشغيل الإيرادات — Revenue Operating System
2. نظام القيادة التنفيذية — Executive Command OS
3. نظام استرجاع المتابعات — Follow-up Recovery OS
4. نظام عملاء واتساب — WhatsApp Client OS
5. نظام العروض والإثبات — Proposal & Proof OS

---

## التشغيل

```bash
npm run commercial:all      # check → plan → quality → brief
# أو كل مرحلة على حدة:
npm run commercial:check    # بوابة الأمان + كل البوابات (exit 1 على مخالفة حرجة)
npm run commercial:plan     # لوحة المبيعات + قائمة المكالمات
npm run commercial:quality  # تسجيل 400 draft + Top 100
npm run commercial:brief    # أمر القيادة اليومي + الأسبوعي + المحتوى + الشركاء
```

ثبّت تاريخ التقارير (اختياري): `DEALIX_TODAY=2026-06-03 npm run commercial:all`.

---

## البيانات (المصدر) — `company_os/commercial/`

| الملف | الدور |
|------|-------|
| `systems.json` | كتالوج الأنظمة الخمسة (الاسم العميل، الحصص، جاهزية التسليم) |
| `draft_factory.json` | دفعة المسودات اليومية (الهدف 400/يوم) |
| `suppression.json` | قائمة الحجب (do-not-contact) |
| `board.json` | فرص لوحة المبيعات عبر 16 حالة |
| `content_calendar.json` | محرك المحتوى الأسبوعي |
| `partners.json` | قناة الشركاء |
| `website_leads.json` | طلبات الموقع (تولّد Need Card + نظام موصى به) |

## المخرجات — `reports/`

```
reports/founder/DAILY_SUPER_COMMAND.md      أمر القيادة (13 قسمًا)
reports/founder/WEEKLY_BOARD_REVIEW.md
reports/sales_ops/SALES_OPS_BOARD_STATUS.md
reports/sales_ops/CALL_FOLLOWUP_QUEUE.md
reports/quality/DAILY_QUALITY_GATE_REVIEW.md
reports/quality/top_100_approval_queue.json
reports/content/FOCUS_5_CONTENT_QUEUE.md
reports/partners/FOCUS_5_PARTNER_PIPELINE.md
reports/security/DAILY_AGENT_SECURITY_REVIEW.md
```

## المنطق + الاختبارات

- المحرك: `scripts/lib/commercial.js`
- الاختبارات: `scripts/commercial.test.js` (`npm test`)
- الوثائق (عربي): `company_os/{founder_control,sales_ops,quality,content,partners,security}/`
