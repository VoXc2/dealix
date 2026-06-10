# مكتبة حساسية التسعير — Pricing Sensitivity Library

> **نماذج التسعير، تقنيات الـ anchor، خصومات محميّة، وزيادة السعر
> عند التجديد. + إشارات حساسية السعر من الميدان.**

**الحالة:** Phase 1 من Agent #31  
**التاريخ:** 2026-06-03  
**الإصدار:** v1.0  
**البيانات:** `data/data_products/pricing_sensitivity.jsonl` (7 صفوف)

---

## 1. نماذج التسعير (Pricing Models)

| النموذج | متى يُستخدم | مثال Dealix |
| --- | --- | --- |
| **Fixed scope** | نتيجة محددة، زمن ثابت | revenue_leakage_diagnostic, follow_up_recovery_workflow |
| **Retainer** | علاقة مستمرة، قيمة شهرية | ai_revenue_ops_starter, monthly_optimization |
| **Success fee** | قياس النتيجة صعب لكن قابل للتعريف | revenue_leakage_diagnostic (variant) |
| **Hybrid** | ثابت + متغير (retainer + outcome bonus) | full_revenue_os, custom_company_os |

---

## 2. تقنيات الـ anchor والـ framing (عربي)

### Anchor techniques

| التقنية | مثال عربي |
| --- | --- |
| **Cost of leakage** | `٢٥ ألف ريال = شهرين من التسرب الشهري` |
| **Peer benchmark** | `شركة مشابهة وفّرت ٤٠٪ من التسرب خلال ٤٥ يوم` |
| **Replacement cost** | `موظف بدوام كامل يكلّف ١٢ ألف شهرياً، Dealix ٢,٩٩٩` |
| **Time saved** | `بدل ٢٠ ساعة أسبوعياً يدوي، ٣ ساعات review` |
| **Risk avoided** | `حادثة PDPL واحدة تكلّف ٥٠٠ ألف + سمعة` |

### Framing techniques

- **استثمار، مش تكلفة:** `استثمار تشخيص، مش تكلفة استشارة`
- **اختيارات، مش رقم واحد:** `عندنا ٣ tiers، أيها يناسب؟`
- **ROI قبل الالتزام:** `pilot ١٤ يوم يثبت ROI قبل أي التزام`
- **Ownership، مش اشتراك:** `بناء نظام تشغيل مخصص، مع تدريب وتسليم`
- **Reversibility:** `بدون التزام طويل، تجديد شهري`

---

## 3. خصومات محمية (Discount Guardrails)

| نوع الخصم | الحد الأقصى | متى يُسمح | من يوافق |
| --- | --- | --- | --- |
| **Standard** | حتى 10% | للعميل الجاد، حجم كبير، sector جديد | founder |
| **Strategic** | حتى 12% | reference customer، case study | founder |
| **Custom OS** | حتى 15% | enterprise مع MSA طويل | founder |
| **Pilot** | حتى 50% (one-time) | first client in sub-vertical | founder |
| **NDI (no discount)** | 0% | عرض مشهور، الطلب عالٍ | — |
| **Charity / Pilot CSR** | 100% (pro bono) | education nonprofit, government CSR | founder + legal |

> أي خصم > 10% يحتاج PR مع tag `pricing-discount` + تبرير مكتوب.
> الخصومات **لا تُمنح** على Retainer (price-fixed) إلا في حزمة سنوية.

---

## 4. زيادة السعر عند التجديد (Price Increase Playbook)

### القاعدة
- ≤ 5% سنوياً → تلقائي، يُرسل في month 10.
- 5–10% → يحتاج تبرير (نطاق إضافي، KPI محقق).
- > 10% → يحتاج founder sign-off + شرط تحسين.

### خطوات التواصل (3 رسائل)

1. **Month 9:** `قبل التجديد، شاركنا نتائجك معنا.`
2. **Month 10:** `بناءً على [X] قيمة مُحققة، التجديد الجديد يشمل [تحسين]. السعر الجديد [Y].`
3. **Month 11:** `نلتقي في [التاريخ] لإغلاق التجديد.`

### Frame عربي مقترح
- `ليس زيادة، هو ترقية.`
- `السعر القديم كان للنسخة v1، الجديد للنسخة v2.`
- `نفس السعر، مع [X] جديد مُضاف.`

---

## 5. إشارات حساسية السعر (Sensitivity Signals)

| الإشارة | كيف تُقاس | متى تنبّه |
| --- | --- | --- |
| **تكرار اعتراض too_expensive** | في funnel_events | > 30% من العملاء في قطاع |
| **تكرار no_budget** | في funnel_events | > 20% |
| **time-to-decision طويل** | > 21 يوم للـ fixed scope | خلل في anchor |
| **win/loss notes** | في sales_playbook | "anchor لم يعمل" |
| **competitor pricing** | mentions في calls | تحوّل إلى model جديد |
| **discount requests متكررة** | في PR log | الـ tier غير مناسب |

---

## 6. Win/Loss Patterns (assumed)

| Win pattern | Loss pattern |
| --- | --- |
| Reframe total cost of leakage | Anchored on hourly consulting rate |
| Show pilot recovery rate vs current | Prefers cheaper DIY tool |
| Monthly ROI > 1.5x subscription | Compares to free tools |
| Executive sponsor + quantified leakage > 5x price | No executive sponsor |
| Client already in another tier | Expects one-time fix not retainer |
| Board-level mandate | Scope not pinned down |
| Client wants skin-in-the-game pricing | Client unwilling to define success metric |

---

## 7. الحساسية حسب العرض (Sensitivity Heatmap)

| العرض | الحساسية | frequency | المبرر |
| --- | --- | --- | --- |
| revenue_leakage_diagnostic | medium | high | entry-level، يفاضل على سعر |
| follow_up_recovery_workflow | low | medium | outcome-fixed، سهل البيع |
| ai_revenue_ops_starter | medium | high | subscription، يفاضل على SaaS |
| full_revenue_os | high | medium | enterprise، يستلزم تبرير |
| monthly_optimization | low | high | retainer بسيط |
| custom_company_os | high | low | enterprise project، scope حساس |

---

## 8. الربط بالمنتجات الأخرى

- **Sector Benchmarks** → حساسية السعر تختلف حسب القطاع (retail = high, agency = low).
- **Objection Intelligence** → `too_expensive` و`no_budget` يستجيبان للـ anchor.
- **Offer Performance** → drop-off point عند السعر.
- **Renewal Trigger** → price increase playbook يستخدم في month 9–11.

---

## 9. مخاطر التسعير (Risks)

1. **Discount creep** → يلتهم الهامش. حل: PR gate + margin review.
2. **Anchor failure** → client يقارن بـ vendor آخر. حل: re-anchor.
3. **Increase resistance** → client يعتبرها خيانة. حل: ربطها بـ قيمة جديدة.
4. **Free-tier capture** → client يستخدم pilot مجاني ثم يرحل. حل: scope محدد + clause.

---

## 10. المراجع (References)

- `data/data_products/pricing_sensitivity.jsonl`
- `data/commercial/pricing_rules.yaml`
- `data/commercial/product_catalog.yaml`
- `docs/PRICING_AND_PACKAGING_V6.md`
- `docs/PRICING_STRATEGY.md`
- `docs/data_products/OFFER_PERFORMANCE_MODEL_AR.md`
- `docs/data_products/SECTOR_BENCHMARKS_AR.md`
- `docs/data_products/OBJECTION_INTELLIGENCE_AR.md`
- `docs/data_products/RENEWAL_TRIGGER_LIBRARY_AR.md`
