# Dealix — Offer Ladder & Pricing (2026-Q2)
<!-- Owner: Founder | Reframed: 2026-05-14 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** كل درجة تُفتح فقط بعد إثبات حقيقي من الدرجة السابقة.
> لا ترقية قبل نتيجة موثقة. لا ضمانات. لا ادعاءات مبالغ فيها.
> رايْف 2026-Q2: ٧ درجات → ٣ درجات. الأرضية المدفوعة ٤٬٩٩٩ ر.س / شهر.
> القطاع المختار: خدمات B2B السعودية فقط لمدة ٩٠ يومًا.

For the rationale + objection handling, see
[`docs/sales-kit/PRICING_REFRAME_2026Q2.md`](sales-kit/PRICING_REFRAME_2026Q2.md).

---

## سلم الخدمات — ٣ درجات

```
[0] Strategic Diagnostic           0 SAR / يوم عمل    ← باب الدخول
[1] Governed Ops Retainer          4,999 SAR / شهر    ← الأرضية المدفوعة
[2] Revenue Intelligence Sprint   25,000 SAR / 30 يوم ← المخرَج الرئيسي
```

The 2025 ladder ranged Free → 499 → 1,500 → 2,999–4,999 → 7,500–15,000 →
Custom. As of 2026-05-14, the 499 SAR Sprint, 1,500 SAR Data Pack, 1,500
SAR Support Add-on, 7,500 SAR Executive Command Center, and Agency Partner
OS are **archived from the customer-facing ladder**. They remain
addressable inside the registry as legacy IDs that resolve via
`_LEGACY_ID_ALIASES` to the closest 2026 successor.

---

## Service 0 · Strategic Diagnostic
**التشخيص الاستراتيجي المجاني**

| Element · العنصر | Detail · التفاصيل |
|---|---|
| **Price · السعر** | 0 SAR — مجاني |
| **Target · العميل المستهدف** | مؤسس/مدير عمليات في شركة خدمات B2B سعودية (٥٠–٥٠٠ موظف) عنده ألم في توقّع الإيرادات أو الحوكمة |
| **Problem · المشكلة** | "لا أعرف فجوات الإيراد والحوكمة قبل ما ألتزم بـ ٥٬٠٠٠ ر.س / شهر" |
| **Deliverables · المخرجات** | PDPL + NDMO posture audit · revenue intelligence gap report · جرد مصادر الحقيقة (أعلى ٥) · ١-صفحة خطة ٩٠ يوم · أعلى ٣ فرص مرتّبة · مسودة عربية واحدة لأعلى فرصة · Decision Passport للخطوة التالية |
| **Proof metrics · مقاييس الإثبات** | هل ٣ فرص قابلة للتنفيذ سُلّمت؟ |
| **Inputs required · المدخلات** | استبيان ٧ أسئلة في `/diagnostic.html` (١٥ دقيقة) |
| **Exclusions · الاستثناءات** | لا وعود ROI · لا تقارير متقدمة · لا وصول للأنظمة الداخلية |
| **Upgrade path · مسار الترقية** | → Governed Ops Retainer أو → Revenue Intelligence Sprint |
| **Duration · المدّة** | يوم عمل واحد |
| **Action mode · وضع الإجراء** | `suggest_only`, `draft_only` |
| **Service ID** | `strategic_diagnostic` (alias: `free_mini_diagnostic`) |

---

## Service 1 · Governed Ops Retainer
**ريتينر العمليات المحوكمة**

| Element · العنصر | Detail · التفاصيل |
|---|---|
| **Price · السعر** | **4,999 SAR / شهر** — حدّ أدنى ٣ أشهر |
| **Target · العميل المستهدف** | شركة خدمات B2B (٥٠–٥٠٠ موظف) تشغّل عمليات إيراد + تحتاج حوكمة شهرية موثّقة بدون توظيف فريق كامل |
| **Problem · المشكلة** | "نريد AI يدير عمليات الإيراد شهرياً مع تقرير قيمة قابل للتدقيق + Proof Pack" |
| **Deliverables · المخرجات** | تدقيق خط الأنابيب أسبوعياً · لوحة العملاء المحتملين · طابور موافقات يومي (draft_only) · تقرير قيمة شهري · Proof Pack شهري موقّع · Friction Log review · Decision Passports لكل قرار جوهري · Adoption Score + retainer-readiness gate · قناة واتساب مخصّصة للمسودات |
| **KPI commitment · التزام** | رفع جودة بيانات خط الإيرادات بنسبة ≥٢٠٪ + تسليم تقرير قيمة شهري قابل للتدقيق. إن لم يتحقق، نواصل بدون مقابل. |
| **Refund policy · الاسترداد** | استرداد تناسبي للأشهر غير المستخدمة عند عدم تحقيق KPI. الحد الأدنى ٣ أشهر. |
| **Inputs required · المدخلات** | وصول Dealix Portal · تحديثات pipeline أسبوعية · موافقة المؤسس على كل رسالة |
| **Exclusions · الاستثناءات** | ≤ ٢٠ مسودة / شهر · لا إرسال تلقائي · لا استشارات قانونية |
| **Upgrade path · مسار الترقية** | → Revenue Intelligence Sprint (الرئيسي) |
| **Action mode · وضع الإجراء** | `approval_required` لكل مسودة |
| **Service ID** | `governed_ops_retainer_4999` (alias: `growth_ops_monthly_2999`, `support_os_addon_1500`, `executive_command_center_7500`) |

---

## Service 2 · Revenue Intelligence Sprint (Flagship)
**سبرنت ذكاء الإيرادات الرئيسي**

| Element · العنصر | Detail · التفاصيل |
|---|---|
| **Price · السعر** | **25,000 SAR** — دفعة واحدة (٥٠٪ على القبول، ٥٠٪ على Proof Pack) |
| **Target · العميل المستهدف** | شركة خدمات B2B عندها بيانات إيرادات في ٣ أنظمة + تحتاج نموذج تنبؤ + حزمة حوكمة قابلة للتدقيق + أصل قابل لإعادة الاستخدام |
| **Problem · المشكلة** | "بيانات الإيرادات مبعثرة في CRM + المالية + العمليات؛ نحتاج مخرَجاً واحداً مدقّقاً" |
| **Deliverables · المخرجات** | دمج ٣ مصادر حقيقة · Revenue forecast model (٩٠-day rolling, target accuracy ≥٨٥٪) · حزمة حوكمة قابلة للتدقيق (PDPL Article 5/13/14/18/21 mapped) · Decision Passports لأعلى ٢٠ فرصة · Arabic + English Draft Pack (١٥ رسالة موافقة) · Risk + Objection Map · Executive board pack · Capital Asset registered · Proof Pack كامل (PDF) · retainer-readiness gate |
| **KPI commitment · التزام** | ١٠ مخرجات في ٣٠ يوم · ٣ مصادر مدمجة · target forecast accuracy ≥٨٥٪ · حزمة حوكمة قابلة للتدقيق. إن لم تتحقق بوابة جاهزية الريتينر، نواصل بدون مقابل. |
| **Refund policy · الاسترداد** | استرداد ٥٠٪ خلال ٦٠ يوم إذا لم تتحقق بوابة جاهزية الريتينر |
| **Inputs required · المدخلات** | وصول لـ ٣ مصادر بيانات (CRM + finance + ops) · موافقة الإدارة · ٦ ساعات / أسبوع وقت COO |
| **Exclusions · الاستثناءات** | لا إرسال مباشر · لا توقيعات على عقود قانونية · لا تكامل CRM تلقائي |
| **Upgrade path · مسار الترقية** | → Governed Ops Retainer (إعادة التجديد كاشتراك شهري) |
| **Duration · المدّة** | ٣٠ يومًا ثابتة |
| **Action mode · وضع الإجراء** | `approval_required` لكل مخرَج جوهري |
| **Service ID** | `revenue_intelligence_sprint_25k` (alias: `revenue_proof_sprint_499`, `data_to_revenue_pack_1500`) |

---

## ملخص الأسعار السريع · 2026-Q2

| Service | Price | Status |
|---|---|---|
| Strategic Diagnostic | 0 SAR | متاح الآن |
| Governed Ops Retainer | 4,999 SAR / شهر · ٣ أشهر حدّ أدنى | متاح الآن |
| Revenue Intelligence Sprint | 25,000 SAR / ٣٠ يوم | متاح بعد التشخيص |

---

## القطاعات المغلقة مؤقّتاً (٩٠ يوم)

For the next 90 days the customer-facing ladder serves Saudi B2B services
**only**. Banking, energy, healthcare, government, and SaaS are served
exclusively as **Custom AI engagements** (≥ 50,000 SAR) negotiated
founder-direct, not via the public ladder. This is a focus discipline,
not a permanent exclusion.

| Sector · القطاع | Status 2026-Q2 |
|---|---|
| Saudi B2B services (٥٠–٥٠٠ موظف) | ✅ Active beachhead — public ladder open |
| Banking · بنوك | 🔒 Founder-direct Custom AI only |
| Energy · طاقة | 🔒 Founder-direct Custom AI only |
| Healthcare · صحّة | 🔒 Founder-direct Custom AI only |
| Government · حكومي | 🔒 Founder-direct Custom AI only |
| SaaS B2B (built-in not services) | 🔒 Founder-direct Custom AI only |

The 90-day clock starts 2026-05-14. The next review gate is 2026-08-12 —
based on (a) recurring SAR committed, (b) number of Capital Assets
registered, (c) number of B2B-services case studies signed.

---

## Doctrine reminder · تذكير من الدستور

Every offer honors the 11 non-negotiables. Specifically:
- No live charge / no live send (intent_only payment, draft_only outbound)
- No cold WhatsApp / no LinkedIn automation / no scraping
- No fake / unsourced proof claims
- Every paid engagement produces ≥ 1 Capital Asset registered in `capital_os`
- Every paid engagement ships a Trust Pack + Audit Chain to the customer
- All numeric promises are `is_estimate=True`
- KPI commitments use commitment language ("نواصل بدون مقابل"), never
  "guaranteed" / "نضمن"

---

*Version 2.0 (2026-Q2 reframe) · No guaranteed claims · Missing data = insufficient_data*

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
