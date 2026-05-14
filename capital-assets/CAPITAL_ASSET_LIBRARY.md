# مكتبة الأصول الرأسمالية — Capital Asset Library

> آخر مراجعة: 2026-05-14 | Wave 19
> مصدر الحقيقة الواحد: [`auto_client_acquisition/capital_os/capital_asset_registry.py`](../auto_client_acquisition/capital_os/capital_asset_registry.py)
> السطح العام: [`/api/v1/capital-assets/public`](../api/routers/capital_assets.py)

---

## ١. ما هو الأصل الرأسمالي؟ (AR)

الأصل الرأسمالي عند Dealix هو قطعة عمل مبنية، قابلة لإعادة الاستخدام، تتراكم قيمتها عبر الارتباطات. ليست وثيقة تسويقية، ولا شريحة عرض، بل ملف حقيقي يمكن لمدير أمن معلومات أو مدقق Big 4 أو محلل صندوق استثماري التحقق منه عبر `curl` أو مراجعة كود.

المكتبة تحتوي ١٥ أصلاً مسجّلاً (CAP-001 إلى CAP-015) موزّعة على ١١ نوعاً استراتيجياً:

- **trust_asset** — أصول الثقة (واجهة Promise API، Trust Pack، Audit Chain).
- **sales_asset** — أصول المبيعات (سُلَّم العروض الثلاثي، خريطة التوصيل التجاري).
- **product_asset** — أصول المنتج (Founder Command Center).
- **doctrine_asset** — أصول العقيدة (المنفستو العام، إطار حوكمة AI المفتوح).
- **proof_asset** — أصول الإثبات (Proof Pack Assembler).
- **partner_asset** — أصول الشراكات (طقم تواصل الشريك الراسي).
- **investor_asset** — أصول المستثمر (الورقة الواحدة + مذكرة التمويل).
- **hiring_asset** — أصول التوظيف (أول ٣ تعيينات + بطاقات تقييم).
- **standard_asset** — أصول المعيار (حزمة معيار خليجي).
- **market_asset** — أصول السوق (واجهة استخبارات السوق الخليجي).
- **revenue_ops_asset** — أصول عمليات الإيراد (Runbook الفاتورة الأولى).

## 2. What counts as a Capital Asset? (EN)

A Capital Asset at Dealix is a built, reusable artefact whose value compounds across engagements. It is not a slide, not a marketing one-liner — it is a file that a CISO, a Big 4 auditor, or a fund analyst can verify by `curl`, code review, or doc inspection.

The library holds 15 registered assets (CAP-001 through CAP-015) across 11 strategic types. Every entry cites real file paths and at least one of the 11 non-negotiables it provably enforces.

---

## ٣. قاعدة المُدقِّق — قاعدة Wave (AR)

عقيدة `no_project_without_capital_asset` تفرض: كل Wave يُغلق يجب أن يُسجِّل أصلاً رأسمالياً واحداً على الأقل. مدقّق `scripts/validate_capital_assets.py` يرفض أي إدخال بدون:

1. `file_paths` حقيقية موجودة في المستودع.
2. ارتباط بواحدة على الأقل من الـ١١ خطاً أحمر (`linked_non_negotiables`).
3. تاريخ `last_reviewed` بصيغة ISO.

## 3. The validator rule (EN)

The `no_project_without_capital_asset` doctrine requires every wave that closes to register at least one Capital Asset. The validator at `scripts/validate_capital_assets.py` rejects any entry without:

1. Real `file_paths` that resolve in the repo.
2. At least one linked non-negotiable id.
3. An ISO-format `last_reviewed` date.

This is how the library stays clean: assets earn their slot by passing the validator, not by founder enthusiasm.

---

## ٤. قاعدة العرض العام مقابل الداخلي (AR)

كل `CapitalAsset` يحمل علم `public: bool` (افتراضي `False`). فقط الأصول المُعلَّمة `public=True` تظهر على `/api/v1/capital-assets/public`. هذا هو الجدار الفاصل بين ما يراه العالم وما يبقى داخل غرفة المؤسس.

العام (`public=True`): CAP-001، CAP-002، CAP-003، CAP-004، CAP-005، CAP-012، CAP-015.
الداخلي (`public=False`): CAP-006، CAP-007، CAP-008، CAP-009، CAP-010، CAP-011، CAP-013، CAP-014.

## 4. Public vs internal exposure (EN)

Every `CapitalAsset` carries a `public: bool` flag (default `False`). Only assets explicitly marked `public=True` surface on `/api/v1/capital-assets/public`. Default-deny is the doctrine — commercial-sensitive entries never leak by omission.

Public-exposed: CAP-001, CAP-002, CAP-003, CAP-004, CAP-005, CAP-012, CAP-015.
Internal-only: CAP-006, CAP-007, CAP-008, CAP-009, CAP-010, CAP-011, CAP-013, CAP-014.

---

## ٥. كيف يستخدم المؤسس المكتبة (AR)

- **في محادثة الشريك:** فتح CAP-003 (إطار الحوكمة المفتوح) + CAP-009 (طقم الشريك الراسي). الرسالة: نحن نُعرِّف المعيار، لا نتسوّق عليه.
- **في عرض المستثمر:** فتح CAP-010 (الورقة الواحدة) + CAP-001 (Promise API قابل للتحقق) + CAP-012 (حزمة المعيار الخليجي).
- **في عرض التوظيف:** فتح CAP-011 (أول ٣ تعيينات) + CAP-014 (Founder Command Center) ليرى المرشّح ماذا سيشغّل فعلاً.

## 5. How the founder uses the library (EN)

- **Partner conversation:** open CAP-003 (open governance framework) + CAP-009 (anchor partner kit). Message: we define the standard, we don't shop on it.
- **Investor deck:** open CAP-010 (one-pager) + CAP-001 (curl-verifiable Promise API) + CAP-012 (GCC standardization pack).
- **Hire pitch:** open CAP-011 (first 3 hires) + CAP-014 (Founder Command Center) so the candidate sees the surface they'll operate.

---

## Cross-references

- Schema reference: [`CAPITAL_ASSET_SCHEMA.md`](./CAPITAL_ASSET_SCHEMA.md)
- Type breakdowns: [`TRUST_ASSETS.md`](./TRUST_ASSETS.md), [`SALES_ASSETS.md`](./SALES_ASSETS.md), [`PRODUCT_ASSETS.md`](./PRODUCT_ASSETS.md), [`DOCTRINE_ASSETS.md`](./DOCTRINE_ASSETS.md), [`PARTNER_ASSETS.md`](./PARTNER_ASSETS.md), [`INVESTOR_ASSETS.md`](./INVESTOR_ASSETS.md), [`HIRING_ASSETS.md`](./HIRING_ASSETS.md)
- Registry source: [`auto_client_acquisition/capital_os/capital_asset_registry.py`](../auto_client_acquisition/capital_os/capital_asset_registry.py)
- Generated index: `CAPITAL_ASSET_INDEX.json` (written by `scripts/generate_capital_asset_index.py` — do not edit by hand)

---

*Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.*
