# GCC Country Priority Map — خريطة أولويّات الدول الخليجية

> مصدر الحقيقة للأسواق الأربعة الأنشط: `auto_client_acquisition/governance_os/gcc_markets.py`. البحرين وعُمان مُضافتان هنا كأسواق مستقبليّة.

## ١. الترتيب — بالعربية

### Tier 1 — أسواق رأس الحربة

- **المملكة العربية السعودية** — `active`. السوق التجاري الوحيد المُفعّل اليوم.
- **الإمارات العربية المتحدة** — `pilot_ready`. تُفتح بعد نشر دراسة حالة Sprint سعودية واحدة.

### Tier 2 — أسواق متابعة

- **دولة قطر** — `future_market`.
- **مملكة البحرين** — `future_market`.

### Tier 3 — أسواق رصد

- **دولة الكويت** — `future_market`.
- **سلطنة عُمان** — `future_market`.

كل تصنيف خارج السعودية لا يحمل ادّعاء اعتماد تنظيمي أو وجود تجاري نشط.

## ٢. الجدول التفصيلي

| الدولة | الجهة المنظِّمة | الإطار | المواد المربوطة | معالج الدفع | معيار الفوترة | اللغة | dealix_status | بوّابة التفعيل |
|---|---|---|---|---|---|---|---|---|
| السعودية (SA) | NDMO + SDAIA | PDPL — Royal Decree M/19 (2021) + Implementing Regulation (2023) | 5, 13, 14, 18, 21 | Moyasar | ZATCA Phase 2 | خليجي سعودي + MSA + EN | active | حيّ — لا توجد بوّابة |
| الإمارات (AE) | UAE Data Office + ADGM + DIFC | UAE Federal Decree-Law No. 45 of 2021 | 5, 9, 13, 18, 22 | Telr / Network International / Checkout.com | FTA e-invoicing (طرح ٢٠٢٦+) | خليجي إماراتي + EN | pilot_ready | بعد نشر دراسة حالة Sprint سعودية + إحالة شريك |
| قطر (QA) | NCSA + Ministry of Transport | Qatar PDPPL — Law No. 13 of 2016 | 4, 6, 7, 14, 18 | QPay / SkipCash / Doha Bank | لا فوترة إلكترونية إلزامية | خليجي قطري + EN | future_market | عميل ربط B2B قطري + كيان قانوني محلّي + DPA |
| البحرين (BH) | PDPA Bahrain Authority | Law No. 30 of 2018 — Personal Data Protection Law | 1–60 (PDPL كامل) | Benefit / CrediMax | لا فوترة إلكترونية إلزامية | خليجي بحريني + EN | future_market | عميل ربط محلّي + كيان قانوني |
| الكويت (KW) | CITRA | Data Privacy Protection Regulation (DPPR) No. 26 of 2024 | 4, 6, 9, 13, 17 | KNET (المعالج المحلّي الوحيد) | لا معيار فوترة إلكترونية إلزامي | خليجي كويتي + EN | future_market | DPO محلّي مُعيّن + كيان قانوني |
| عُمان (OM) | MTCIT (Ministry of Transport, Communications and Information Technology) | Royal Decree 6/2022 — Personal Data Protection Law | 1–43 (PDPL كامل) | OmanNet / Thawani | لا فوترة إلكترونية إلزامية | خليجي عُماني + EN | future_market | عميل ربط محلّي + DPA |

## ٣. ملاحظة على بوّابات التفعيل

كل بوّابة تفعيل خارج السعودية تتطلّب ثلاثة عناصر متزامنة:

1. عقد ربط محلّي مُوقَّع (ليس MoU، ليس LOI).
2. خرائط مواد القانون الوطني مُحدَّثة في `gcc_markets.py`.
3. كيان قانوني أو شريك مرخَّص يصدر فواتير بالعملة المحلّية.

لا يتم تَرقية حالة أيّ سوق من `future_market` إلى `pilot_ready` بدون اختبار آلي يُؤكّد العناصر الثلاثة.

---

## 1. Ranking — English

### Tier 1 — beachhead

- **Kingdom of Saudi Arabia** — `active`. The only commercially live market today.
- **United Arab Emirates** — `pilot_ready`. Opens after one Saudi Sprint case study is published.

### Tier 2 — follow markets

- **State of Qatar** — `future_market`.
- **Kingdom of Bahrain** — `future_market`.

### Tier 3 — watch markets

- **State of Kuwait** — `future_market`.
- **Sultanate of Oman** — `future_market`.

No status outside Saudi carries any claim of regulatory endorsement or active commercial presence.

## 2. Detail table

| Country | Regulator | Framework | Articles mapped | Payment processor | Invoicing standard | Language | dealix_status | Activation gate |
|---|---|---|---|---|---|---|---|---|
| Saudi Arabia (SA) | NDMO + SDAIA | PDPL — Royal Decree M/19 (2021), Implementing Regulation (2023) | 5, 13, 14, 18, 21 | Moyasar | ZATCA Phase 2 | Khaleeji Saudi + MSA + EN | active | Live — no gate |
| United Arab Emirates (AE) | UAE Data Office + ADGM + DIFC | UAE Federal Decree-Law No. 45 of 2021 | 5, 9, 13, 18, 22 | Telr / Network International / Checkout.com | FTA e-invoicing (2026+ rollout) | Khaleeji UAE + EN (equal weight) | pilot_ready | Saudi Sprint case study published + partner referral |
| Qatar (QA) | NCSA + Ministry of Transport | Qatar PDPPL — Law No. 13 of 2016 | 4, 6, 7, 14, 18 | QPay / SkipCash / Doha Bank | No mandatory e-invoicing | Khaleeji Qatari + EN | future_market | Qatari B2B anchor + local legal entity + DPA |
| Bahrain (BH) | PDPA Bahrain Authority | Law No. 30 of 2018 — Personal Data Protection Law | 1–60 (full PDPL) | Benefit / CrediMax | No mandatory e-invoicing | Khaleeji Bahraini + EN | future_market | Local anchor customer + legal entity |
| Kuwait (KW) | CITRA | Data Privacy Protection Regulation (DPPR) No. 26 of 2024 | 4, 6, 9, 13, 17 | KNET (sole domestic processor) | No mandatory e-invoicing | Khaleeji Kuwaiti + EN | future_market | Appointed local DPO + legal entity |
| Oman (OM) | MTCIT (Ministry of Transport, Communications and Information Technology) | Royal Decree 6/2022 — Personal Data Protection Law | 1–43 (full PDPL) | OmanNet / Thawani | No mandatory e-invoicing | Khaleeji Omani + EN | future_market | Local anchor customer + DPA |

## 3. On activation gates

Every gate outside Saudi Arabia requires three simultaneous elements:

1. A signed local anchor contract (not an MoU, not an LOI).
2. National article maps refreshed inside `gcc_markets.py`.
3. A legal entity or licensed partner that issues local-currency invoices.

No market is promoted from `future_market` to `pilot_ready` without an automated test confirming all three.

---

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
