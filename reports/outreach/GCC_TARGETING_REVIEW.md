# GCC Targeting Review

*Date: 2026-06-03 · Principle: Saudi-first, GCC-ready · Channel default: email-first*

> القاعدة: لا نستهدف "الخليج" ككتلة، بل **Sector × City × Signal × Mission × Channel**.
> المرجع: `docs/commercial/GCC_EXPANSION_STRATEGY_AR.md` + `docs/outreach/GCC_OUTREACH_POLICY_AR.md`.

---

## 1. Phase map

| Phase | Markets                         | Status        |
| ----- | ------------------------------- | ------------- |
| 1     | KSA: Riyadh, Jeddah, Eastern Province | ✅ Active (current prospects) |
| 2     | UAE: Dubai, Abu Dhabi, Sharjah  | 🔒 Locked until Phase-1 Proof Pack |
| 3     | Qatar, Kuwait                   | 🔒 Locked     |
| 4     | Bahrain, Oman                   | 🔒 Locked     |

**Gate to advance:** لا ننتقل لمرحلة دون Proof Pack واحد على الأقل من السابقة.

---

## 2. Targeting matrix (Phase 1 — KSA)

| Sector              | City             | Signal                       | Mission | Channel                          |
| ------------------- | ---------------- | ---------------------------- | ------- | -------------------------------- |
| Marketing Agencies  | Riyadh           | hiring sales/marketing       | M3 Sales Draft Factory | Cold email            |
| Marketing Agencies  | Riyadh           | leads from ads not followed  | M2 Follow-up Recovery  | Cold email            |
| Training Companies  | Jeddah           | course/enrollment inquiries  | M2 Follow-up Recovery  | Cold email → WhatsApp بعد الرد   |
| Training Companies  | Riyadh           | WhatsApp inquiries lost      | M4 WhatsApp Client OS  | Email first (واتساب للعميل القائم) |
| Professional Services | Riyadh         | many services/forms          | M5 Proposal & Proof    | Cold email            |
| B2B / Consulting    | Eastern Province | deals stuck / slow closure   | M1 Revenue Leakage     | Email first           |
| B2B / IT            | Riyadh           | weak CRM / blind pipeline    | M1 Revenue Leakage     | Email first           |
| Clinics             | Khobar           | appointment / no-show risk   | M4 WhatsApp Client OS  | Email first           |
| Real Estate Teams   | Riyadh           | listings/leads response gap  | M2 Follow-up Recovery  | Email first           |

> WhatsApp يظهر **فقط** كقناة "بعد رد العميل" أو على محادثات العميل المملوكة — **لا cold WhatsApp automation**.

---

## 3. Priority sectors (those needing many services)

نبدأ بالقطاعات التي تحتاج **خدمات متعددة** (ندخل بمهمة صغيرة ثم نوسّع):

```txt
Marketing Agencies      → leads · follow-up · drafts · proof · renewal
Training Companies      → WhatsApp · follow-up · enrollment · reports
Professional Services   → proposals · proof · tracking
Real Estate Teams       → lead response · follow-up
Recruitment Agencies    → follow-up · drafts
Clinics                 → inbound follow-up · no-show recovery
Local SaaS/Service Firms→ pipeline · CRM · reports
```

(القطاعات الثلاثة الأولى مطابقة لتموضع الريبو الحالي في `pitch_deck/outline.md` Page 5 و`LandingPage.tsx`.)

---

## 4. Current prospect coverage (from `revenue/prospects.csv`)

| Sector            | Count | Dominant mission | Channel    |
| ----------------- | ----: | ---------------- | ---------- |
| Marketing Agency  | 5     | M2 / M3 / M5     | Cold email |
| Training          | 5     | M2 / M4          | Email first |
| B2B Services      | 5     | M1 / M5          | Email first |

> التغطية الحالية متوازنة عبر القطاعات الثلاثة، كلها KSA Phase-1. التوسّع الجغرافي مؤجّل حتى الدليل.

---

## 5. GCC localization rules (when unlocked)

| Market   | Language       | Channel note                  | Compliance gate         |
| -------- | -------------- | ----------------------------- | ----------------------- |
| KSA      | Arabic         | email-first                   | PDPL/SDAIA (ready)      |
| UAE      | AR + EN        | email-first, bilingual copy   | UAE PDPL + free zones   |
| Qatar    | AR + EN        | relationship-led + email      | PDPPL                   |
| Kuwait   | Arabic         | network-led + email           | إطار ناشئ               |
| Bahrain  | AR + EN        | partnerships gateway          | Bahrain PDPL            |
| Oman     | Arabic         | referrals                     | إطار ناشئ               |

- suppression list منفصلة لكل دومين/سوق.
- التحقق القانوني قرار مؤسس قبل فتح أي سوق.

---

## 6. Risks & founder decisions

| # | Item                                                    | Recommendation                  |
| - | ------------------------------------------------------- | ------------------------------- |
| 1 | تأكيد مدن الـ prospects الحاليين (`City: confirm`)       | إثراء بيانات `prospects.csv`    |
| 2 | مهمة الدخول لكل قطاع                                     | Agencies→M2/M3 · Training→M2/M4 · B2B→M1/M5 |
| 3 | موعد فتح Phase 2 (UAE)                                   | بعد أول Proof Pack من KSA       |

---

## 7. Links

- Expansion strategy: `docs/commercial/GCC_EXPANSION_STRATEGY_AR.md`
- Outreach policy: `docs/outreach/GCC_OUTREACH_POLICY_AR.md`
- Daily production: `reports/outreach/DAILY_400_DRAFT_PRODUCTION.md`
