# Dealix — مصفوفة توجيه العروض · Offer Routing Matrix

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `../COMMERCIAL_WIRING_MAP.md` · `../OFFER_LADDER_AND_PRICING.md` · `SALES_MOTIONS.md` · `DISCOVERY_SCRIPT.md`

---

> **هذا دليل توجيه بيع داخلي — وليس قائمة أسعار للعملاء.** الأسعار المنشورة تعيش في [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md). لا تعرض المصفوفة الكاملة على العميل.
>
> **This is an INTERNAL sales-routing guide — NOT a customer-facing price list.** Published prices live in [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md). Do not show the full matrix to customers.

---

## الغرض · Purpose

تربط هذه المصفوفة **إشارة ألم** يذكرها العميل بـ**عرض واحد من السجل الرسمي**، مع عنوان تموضع مناسب وخطوة تالية. الهدف: قرار توجيه سريع ومتسق، بدون ارتجال في التسعير.

This matrix maps a **pain signal** a prospect states to **one registry offer**, with a suitable positioning label and a next step. The goal is a fast, consistent routing decision with no improvised pricing.

العروض السبعة فقط هي المسموح بها. عناوين التموضع (positioning labels) ليست عروضاً — هي طرق وصف للعرض نفسه أمام العميل.

---

## جدول التوجيه: ألم ← عرض · Pain → Offer Routing Table

| إشارة الألم · Pain signal | العرض الموصى به · Recommended registry offer | عنوان التموضع · Positioning label | الخطوة التالية · Next step |
|---|---|---|---|
| leads تُفقد ولا تُتابَع · leads being lost, no documented follow-up | `free_mini_diagnostic` | "10-Lead Follow-up Audit" | الترقية إلى `revenue_proof_sprint_499` |
| وكالة تحتاج دليلاً لعملائها · agency needs proof for its clients | `free_mini_diagnostic` / `revenue_proof_sprint_499` | "Agency Proof Pilot" | البيع المشترك عبر `agency_partner_os` |
| CRM موجود لكنه متوقّف · CRM exists but stalled | `data_to_revenue_pack_1500` | "Data-to-Revenue Pack" | الترقية إلى `growth_ops_monthly_2999` |
| المدير التنفيذي يريد وضوحاً · CEO wants clarity across the business | `executive_command_center_7500` | "Executive Command Center" | مراجعة شهرية مع لوحة القرارات · monthly decision review |
| سير عمل يتكرّر شهرياً · workflow repeats every month | `growth_ops_monthly_2999` | "Growth Ops Monthly" | إضافة `support_os_addon_1500` عند الحاجة · add support add-on when needed |

كل صف يستخدم عرضاً واحداً من السجل الرسمي حصراً. لا تُنشئ صفاً بعرض غير موجود في السجل.

---

## قواعد التوجيه · Routing rules

- **ابدأ منخفضاً ما لم تكن الإشارة واضحة.** معظم العملاء الجدد يدخلون عبر `free_mini_diagnostic`. ابدأ من القمة (`executive_command_center_7500`) فقط عندما تذكر القيادة صراحةً الحاجة إلى وضوح على مستوى الشركة.
  Start low unless the signal is explicit. Most new prospects enter via `free_mini_diagnostic`.
- **عرض واحد لكل محادثة.** لا تعرض المصفوفة. وجّه إلى عرض واحد فقط.
  One offer per conversation. Do not present the matrix; route to a single offer.
- **عناوين التموضع للعميل؛ معرّفات السجل للداخل.** قل "10-Lead Follow-up Audit" للعميل؛ سجّل `free_mini_diagnostic` داخلياً.
  Positioning labels are for the customer; registry IDs are for internal records.
- **التسعير شفّاف دائماً (`no_hidden_pricing`).** عند ذكر سعر، اذكر السعر المعتمد من [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) كما هو — لا أرقام مرتجلة.
  Pricing is always transparent. When a price is quoted, quote the approved figure exactly.
- **لا وعد بنتائج.** الترقية تُبنى على Proof Pack مُثبت بأدلة، لا على نسب تحويل موعودة.
  No promised results. Upgrades are built on an evidenced Proof Pack, not promised conversion rates.

---

## تسلسل الترقية · Upgrade ladder

```
free_mini_diagnostic  →  revenue_proof_sprint_499  →  data_to_revenue_pack_1500
                                                   →  growth_ops_monthly_2999  (+ support_os_addon_1500)
                                                   →  executive_command_center_7500

agency_partner_os  =  مسار قناة مستقل · separate channel track
```

كل ترقية مشروطة بوجود دليل من المرحلة السابقة. راجع [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) للتفاصيل، و[`SALES_MOTIONS.md`](SALES_MOTIONS.md) لربط الحركات بهذه العروض.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
