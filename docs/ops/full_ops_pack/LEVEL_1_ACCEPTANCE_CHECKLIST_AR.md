# Level 1 — قائمة قبول + Evidence Pack (عربي)

لا تُعلن «100%» إلا إذا وُجد **دليل** لكل بند (لقطة شاشة، رقم صف، مخرجات terminal، إيميل). القاعدة:

| Area | Owner | Tool | Test | Expected Result | Evidence | Status | Next Fix |
|------|-------|------|------|-----------------|----------|--------|----------|
| Form | | Google Form | Submit test lead | صف في Form Responses | Screenshot / row | ☐ | |
| Script | | Apps Script | `testInsertRow` | صف في Operating Board | row + log | ☐ | |
| Script | | Apps Script | Form submit | نفس السلوك + إيميل | Executions Completed | ☐ | |
| Dashboard | | Sheets | تغيير الحالات | أرقام تتغير | before/after | ☐ | |
| WhatsApp | | متصفح | فتح wa.me | يفتح مع الرسالة الصحيحة | screenshot | ☐ | |
| Sales | | Sheet | Pilot offer | pilot_status = offered | صف محدّث | ☐ | |
| Delivery | | Sheet | Proof | proof_pack_status = delivered | screenshot | ☐ | |
| Technical | | Terminal | launch_readiness_check | STAGING_HEALTH_OK + SMOKE_STAGING_OK | log | ☐ | |

---

## Form Test

- عبّئ الفورم كـ test lead (مثلاً: Sami Test، وكالة تجربة، قطاع وكالة/مسوق، هدف أبغى عملاء، موافقة نعم).
- **متوقع:** صف جديد في `Form Responses 1`؛ `consent = نعم`.
- **دليل:** لقطة للرد أو رقم الصف.

---

## Sheet Test

- **متوقع:** تبويبات الـ 9 موجودة؛ `02_Operating_Board` الصف 1 = رؤوس الأعمدة كما في [GOOGLE_SHEET_MODEL_AR.md](GOOGLE_SHEET_MODEL_AR.md) و [dealix_google_apps_script.gs](dealix_google_apps_script.gs).

---

## Apps Script Test

- شغّل `setupDealixTrigger()` ثم `testInsertRow()`.
- **متوقع:** صف جديد؛ `diagnostic_card` غير فارغ؛ تنفيذ بدون خطأ.
- **دليل:** Executions = Completed؛ لقطة للصف.

---

## Operating Board Test

- الحقول الحرجة لكل lead: `lead_name`, `company`, `source`, `consent_source`, `goal`, `recommended_service`, `diagnostic_status`, `pilot_status`, `proof_pack_status`, `next_step`, `diagnostic_card`, `owner`.
- **متوقع للصف التجريبي:** `recommended_service` و `next_step` و `diagnostic_card` غير فارغة؛ `diagnostic_status = new` (أو `waiting_data` إذا لا موافقة)؛ `pilot_status = not_offered`؛ `proof_pack_status = not_started`.

---

## Diagnostic Card Test

- **متوقع:** الكرت يحتوي اسم الشركة، شريحة/هدف، 3 فرص (على الأقل placeholders للمراجعة)، رسالة عربية، قناة، مخاطرة، خطوة Pilot 499.

---

## Dashboard Test

- غيّر في صف تجريبي: `diagnostic_status = sent`، `pilot_status = offered`، `proof_pack_status = delivered`.
- **متوقع:** مقاييس Diagnostics sent / Pilots offered / Proof delivered تتحرك (حسب صيغك).
- **دليل:** قبل وبعد.

---

## WhatsApp Link Test

- افتح `WHATSAPP_LINK` من السكربت (رقم `9665…` بدون `+` في المسار).
- **متوقع:** يفتح واتساب مع نص يبدأ بـ Diagnostic (أو ما عرّفته).

---

## Pilot Test

- حدّث `pilot_status` و `next_step` بعد إرسال عرض 499.
- **متوقع:** Dashboard يعكس العرض؛ الصف واضح.

---

## Proof Pack Test

- املأ `04_Proof_Pack` وحدّث الحالة في اللوحة.
- **متوقع:** `proof_pack_status = delivered`؛ دليل PDF أو لقطة.

---

## Technical Ops — Railway / API (الريبو)

```bash
curl -i "$STAGING_BASE_URL/health"
cd /path/to/repo
export STAGING_BASE_URL="https://your-staging-host"
python scripts/smoke_staging.py --base-url "$STAGING_BASE_URL"
python scripts/launch_readiness_check.py --base-url "$STAGING_BASE_URL"
```

- **متوقع:** HTTP 200 على `/health`؛ `SMOKE_STAGING_OK`؛ من السكربت: `STAGING_HEALTH_OK` و `LAUNCH_READINESS_JSON_OK` عند نجاح الجلب.

### فرق مهم: `PAID_BETA_READY` vs API

- سكربت [launch_readiness_check.py](../../../scripts/launch_readiness_check.py) يطبع **`STAGING_LEVEL_1_TECH_OK`** فقط عندما تتحقق شروط **تقنية محددة** (صحة + smoke paths). هذا **ليس** ادعاءاً تجارياً بأن المنتج جاهز للدفع الحي.
- نقطة النهاية `GET /api/v1/personal-operator/launch-readiness` ترجع `stage` و `score` من المنطق الداخلي (مثل `private_beta_ready_after_fixes`) — قد يختلف عن أي عبارة تسويقية. استخدم الـ JSON كـ **مؤشر** وليس كبديل عن Evidence اليدوي أعلاه.

---

## Security Checklist (مرجع سريع)

- لا أسرار في Git أو Sheet أو Apps Script.
- `WHATSAPP_ALLOW_LIVE_SEND=false` في staging؛ Moyasar sandbox للاختبار.
- راجع [POST_LAUNCH_BACKLOG.md](../POST_LAUNCH_BACKLOG.md) قبل أي أتمتة live.

---

## Final 100% Gate (ملخص)

- Staging تقني يمر حسب السكربتات أعلاه **أو** توثيق سبب التخطي.
- Form → Script → Board → Card → Dashboard → رابط WA → Pilot مسار → Proof → أمان → Scorecard يومي.

إذا ناقص بند: **Level 1 partially active — missing gate: [اسم البند].**
