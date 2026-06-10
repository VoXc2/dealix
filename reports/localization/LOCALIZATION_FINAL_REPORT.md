# Agent #14 — Localization Final Report

**Date:** 2026-06-03
**Agent:** Agent #14 — Saudi Localization & Arabic Experience

---

## 1. ملخص تنفيذي

`docs/localization/` كان فيه وثيقتي هيكل فقط. Agent #14 بنى
**مكتبة أسلوب شاملة** تخلي أي قالب، WhatsApp، proposal، report
يتبع نفس النبرة والمصطلحات والشكل.

## 2. ما أُنشئ

| المسار | الملف |
| --- | --- |
| `docs/agent_definitions/agent_14_saudi_localization.md` | تعريف |
| `reports/localization/SAUDI_LOCALIZATION_REVIEW.md` | Gap audit |
| `docs/localization/TERMINOLOGY_GLOSSARY_AR.md` | مسرد المصطلحات |
| `docs/localization/ARABIC_BRAND_VOICE_AR.md` | صوت العلامة |
| `docs/localization/SAUDI_B2B_TONE_GUIDE_AR.md` | نبرة B2B سعودية |
| `docs/localization/BILINGUAL_STYLE_GUIDE_AR.md` | دليل AR/EN |
| `docs/localization/WHATSAPP_ARABIC_UX_AR.md` | WhatsApp UX |

## 3. المسرد (Glossary)

6 فئات (Core، Sales، Payments، WhatsApp، Privacy/PDPL، Time). 50+
مصطلح مع "use" / "don't use" / ملاحظات.

**Key terms locked:**
- Revenue OS = نظام تشغيل الإيرادات
- Proof Pack = حزمة إثبات
- Pipeline = مسار الفرص
- Decision Passport = جواز قرار

## 4. النبرة (Voice)

**5 نبرات معتمدة:**

| Tone | Context |
| --- | --- |
| Executive Formal | CEO/board reports |
| Sales Professional | Outreach, proposals |
| Support Friendly | Customer replies |
| Operational Direct | Internal chat, ops alerts |
| Marketing Aspirational | Public landing, case studies |

**8 نبرات ممنوعة** في B2B سعودي (spam-like، overclaim، عامية، etc.).

## 5. WhatsApp UX Rules

- < 60 كلمة في الرسالة
- < 200 كلمة في المحادثة
- CTA واحد فقط
- أزرار < 3
- 9:00–18:00 الرياض فقط

## 6. Bilingual Consistency

- اسم العلامة (Dealix) لا يُترجم
- المصطلحات التقنية (Webhook, SLA) لا تُترجم
- أسماء المزوّدين (Moyasar) لا تُترجم
- التحية موحّدة (السلام عليكم / Hello)
- التاريخ والوقت موحّد
- CTA موحّد (AR أولاً)

## 7. Tests (Voice & Tone)

3 tests في كل artifact:

1. **Voice Test** (6 أسئلة في `ARABIC_BRAND_VOICE_AR.md` § 10)
2. **Tone Test** (5 أسئلة في `SAUDI_B2B_TONE_GUIDE_AR.md` § 5)
3. **UX Test** (6 أسئلة في `WHATSAPP_ARABIC_UX_AR.md` § 11)
4. **Consistency Test** (5 أسئلة في `BILINGUAL_STYLE_GUIDE_AR.md` § 13)

## 8. Remaining Gaps

1. **SAUDI_LOCALIZATION_OS_AR.md** (synthesis) — TBD
2. **PROPOSAL_ARABIC_STYLE_AR.md** — TBD
3. **REPORTING_ARABIC_STYLE_AR.md** — TBD
4. CI test: `tests/test_voice_compliance.py` (TBD)
5. CI test: `tests/test_banned_wording.py` (TBD)
6. CI test: `tests/test_glossary_compliance.py` (TBD)

## 9. Founder Next Actions

1. ✅ اعتماد Glossary + Voice + Tone.
2. ⏳ اعتماد WhatsApp UX rules.
3. ⏳ تحديث `data/templates/` ليطابق.
4. ⏳ إضافة CI tests.
5. ⏳ بناء PROPOSAL_ARABIC_STYLE_AR.md.
6. ⏳ بناء REPORTING_ARABIC_STYLE_AR.md.

## 10. Cross-Agent

- **Agent #13 (Legal):** claims = banned wording list sync.
- **Agent #15 (Services):** كل deliverable = voice compliance test.
- **Agent #16 (Data Room):** AR company overview = voice compliance.
- **Agent #17 (Procurement):** vendor notes = glossary compliance.

## 11. المراجع

- `docs/agent_definitions/agent_14_saudi_localization.md`
- `reports/localization/SAUDI_LOCALIZATION_REVIEW.md`
- `docs/localization/TERMINOLOGY_GLOSSARY_AR.md`
- `docs/localization/ARABIC_BRAND_VOICE_AR.md`
- `docs/localization/SAUDI_B2B_TONE_GUIDE_AR.md`
- `docs/localization/BILINGUAL_STYLE_GUIDE_AR.md`
- `docs/localization/WHATSAPP_ARABIC_UX_AR.md`
- `docs/localization/ARABIC_TONE_LIBRARY.md` (existing, skeleton)
- `docs/localization/SAUDI_MENA_LOCALIZATION_SYSTEM.md` (existing, skeleton)
- `data/templates/whatsapp_templates_collection.md`
- `data/templates/warm_intro_whatsapp_ar.md`
- `data/templates/proposal_499_sar_ar.md`
- `data/templates/proof_pack_ar.md`
