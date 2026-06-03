# Mission Packaging Map — خريطة التغليف التجاري للمهام

> كيف نبيع "كل الخدمات" دون تشتيت: نغلّف كل قدرة كـ **Mission** لها مخرج واضح، نبدأ بمهمة واحدة، ثم نتوسّع بالدليل.
>
> **مبني على:** منتجات الريبو الحالية (P1 Sprint / P2 Retainer) في `company_os/marketing/one_pagers/one_pager_arabic.md`، `company_os/marketing/pitch_deck/outline.md`، وأسعار `company_os/finance/unit_economics.md`، وبطاقات الأسعار في `src/pages/LandingPage.tsx`.

---

## 1. مبدأ التغليف

```txt
لا نبيع قائمة خدمات. نبيع مهمة واحدة تعطي أسرع دليل قيمة، ثم نوسّعها إلى نظام.
```

الرسالة المعتمدة في كل عرض:

```txt
نقدر نغطّي التسويق، المبيعات، المتابعة، واتساب، العروض، التقارير، التسليم، والتجديد —
لكن نبدأ بالمهمة التي تعطي أسرع دليل قيمة لشركتك.
```

---

## 2. المنتجان الحاملان للمهام (من الريبو)

| المنتج                              | الدور في التغليف         | السعر (من `unit_economics.md`)         | المهام التي يحملها        |
| ----------------------------------- | ------------------------ | -------------------------------------- | ------------------------- |
| **P1 — Revenue Intelligence Sprint** | مدخل تشخيصي (5 أيام)      | 2,500–7,500 ر.س (متوسط 5,000)          | M1, M5 (تشخيص)، مدخل M2/M4 |
| **P2 — AI Sales Ops Retainer**       | تشغيل مستمر (شهري)        | Small 3,000 · Medium 8,000 · Ent. 20,000 | M2, M3, M4, M6, M7         |
| **P2 Enterprise**                    | نظام كامل                 | 20,000 ر.س/شهر                          | M8 Full Revenue OS         |

> هذا مطابق لنموذج "Service-led SaaS" في `pitch_deck/outline.md` (Page 7): بيع خدمة → retainer → بيانات → منتج → SaaS.

---

## 3. مسار التغليف (Entry → Expansion → OS)

```txt
ENTRY (P1 Sprint)                EXPANSION (P2)                   OS (P2 Enterprise)
─────────────────                ──────────────                   ──────────────────
M1 Revenue Leakage   ──┐
M5 Proposal & Proof  ──┼──▶  M2 Follow-up Recovery  ──┐
M4 WhatsApp (تشخيص)  ──┘     M3 Sales Draft Factory  ──┼──▶  M8 Full Revenue OS
                             M6 Customer Success      ──┘     (Radar+AI Team+Portal+Proof)
                             M7 GTM Expansion (موازٍ)
```

**لكل عميل: مهمة دخول واحدة فقط.** التوسّع يُقترح بعد ظهور الدليل في Proof Pack، لا قبله.

---

## 4. جدول التغليف لكل Mission

| Mission                | منتج الدخول   | سعر الدخول المقترح | الترقية الطبيعية         | محفّز الترقية (Trigger)                         |
| ---------------------- | ------------- | ------------------ | ------------------------ | ----------------------------------------------- |
| M1 Revenue Leakage     | P1 Sprint     | 2,500–5,000 ر.س    | P2 Small/Medium          | ظهور حجم التسرّب في Proof Pack                  |
| M2 Follow-up Recovery  | P1 Sprint     | 5,000 ر.س          | P2 Small (تشغيل المتابعة) | فرص مُستردّة فعلية في أول دورة                  |
| M3 Sales Draft Factory | P2 Small      | 3,000+ ر.س/شهر     | P2 Medium                | الحاجة لرفع حجم الـ drafts فوق طاقة فريق العميل |
| M4 WhatsApp Client OS  | P1 (تشخيص)    | 2,500 ر.س          | P2 Small                 | تأكّد ضياع استفسارات واتساب                     |
| M5 Proposal & Proof    | P1 Sprint     | 5,000 ر.س          | P2 Medium                | عروض عالقة + غياب دليل ROI                      |
| M6 Customer Success    | P2 Medium     | 8,000 ر.س/شهر      | P2 Enterprise            | محفظة عملاء + خطر churn                         |
| M7 GTM Expansion       | P2 Medium     | 8,000 ر.س/شهر      | P2 Enterprise            | قرار دخول قطاع/سوق جديد                         |
| M8 Full Revenue OS     | P2 Enterprise | 20,000 ر.س/شهر     | —                        | الوجهة النهائية                                 |

> الأسعار **مراسٍ (anchors)** لا التزامات؛ التسعير النهائي قرار مؤسس (الحوكمة: AI لا يقرّر التسعير — `governance/agent_permissions.md`، خط أحمر #3).

---

## 5. تغليف العرض الواحد (Sales Page بنية موحّدة)

كل Mission تُعرض بنفس القالب حتى لا تبدو الخدمات مشتتة:

```txt
1. الإشارة التي لاحظناها (Signal)
2. الألم المحتمل (Likely pain)
3. المهمة المقترحة (Recommended mission) — اسم واحد
4. المخرج خلال [مدة] (Deliverable)
5. العمود/الأعمدة التي تنفّذها (Radar/AI Team/Portal/Proof)
6. زاوية الإثبات (Proof angle)
7. الخطوة التالية الصغيرة (CTA) — تشخيص مختصر، لا "اشترِ كل شيء"
```

---

## 6. ما الذي *لا* نفعله في التغليف

- لا نطلق اسماً مثل `Dealix Marketing Services` أو `Dealix CRM` (يفتّت البراند).
- لا نعرض الـ 40 وحدة الداخلية للعميل.
- لا نَعِد بنتائج مضمونة (No guaranteed claims).
- لا نبدأ بـ M8 مباشرة؛ نصعد إليها بالدليل.

---

## 7. الربط بالتقارير

- مراجعة جاهزية التغليف: `reports/commercial/MISSION_PACKAGING_REVIEW.md`
- إنتاج المسودات اليومي: `reports/outreach/DAILY_400_DRAFT_PRODUCTION.md`
- بطاقات احتياج العملاء: `reports/outreach/CLIENT_NEED_CARDS.md`

*راجع أيضاً: `DEALIX_OPERATING_MISSIONS_AR.md` و `MISSION_TO_PILLAR_MAP_AR.md`.*
