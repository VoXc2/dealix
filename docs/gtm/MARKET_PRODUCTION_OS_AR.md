# Dealix — نظام إنتاج السوق (Market Production OS)

> نظام تشغيل الإيرادات للشركات السعودية — Saudi B2B Revenue Operating System
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`

Dealix Market Production OS هو خط إنتاج متكامل يحوّل عمليات المبيعات إلى
*workflows* قابلة للقياس: يبحث عن العملاء المحتملين، يكشف الإشارات، يطابق العروض،
يجهّز مسودّات بموافقة، يحمي قابلية التسليم (deliverability)، ويعطي المؤسّس غرفة
تحكّم يومية — **دون** إرسال خارجي غير معتمد ودون أي أتمتة spam.

---

## 1. ما هو وما ليس هو

**Dealix هو:**
- نظام تشغيل إيرادات سعودي، عربي أولاً، موافقة المؤسّس أولاً.
- مبني على الإثبات (proof-driven)، واعٍ للخصوصية (PDPL).
- إنتاج سوق + تنفيذ إيرادات + تسليم.

**Dealix ليس:**
- أداة spam، ولا bot واتساب بارد، ولا أتمتة LinkedIn، ولا محرك scraping.
- ليس chatbot عام، ولا أداة تضمن الإيرادات، ولا ترسل خارجياً بلا موافقة.
- لا يخزّن أسراراً في logs أو prompts أو JSONL أو تقارير أو GitHub.

---

## 2. مكوّنات النظام (18 طبقة)

| # | الطبقة | المسؤولية | المرجع |
|---|--------|-----------|--------|
| 1 | Brand OS | الصوت، الـ claims، الهوية | `docs/brand/` |
| 2 | Product Catalog OS | الكتالوج، سلّم العروض، التسعير | `docs/commercial/` · `data/commercial/product_catalog.yaml` |
| 3 | Sector Intelligence OS | كتيّبات القطاعات | `docs/sectors/` · `data/sectors/sectors.yaml` |
| 4 | Signal Detection OS | كشف إشارات الشراء | `docs/signals/` · `data/signals/` |
| 5 | Prospect Research OS | بحث وتقييم العملاء | `docs/outreach/PROSPECT_RESEARCH_OS_AR.md` |
| 6 | Cold Email Draft Factory | 250 مسودّة/يوم | `docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md` |
| 7 | Compliance Gate | بوّابة الامتثال | `scripts/draft-quality-gate.js` · `scripts/governance_check.py` |
| 8 | Deliverability OS | صحة الدومين والإرسال | `docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md` |
| 9 | Founder Approval Queue | طابور موافقة المؤسّس | `reports/outreach/APPROVAL_QUEUE.md` |
| 10 | Sending Ramp OS | تدرّج الإرسال | `docs/outreach/SENDING_RAMP_OS_AR.md` |
| 11 | Reply Handling OS | معالجة الردود | `docs/commercial/SALES_PROCESS_AR.md` |
| 12 | WhatsApp Post-Reply Routing | واتساب بعد الرد فقط | `docs/sectors/*` (زاوية WhatsApp-after-reply) |
| 13 | Content OS | إنتاج المحتوى | `docs/content/` |
| 14 | Press OS | العلاقات الإعلامية | `docs/press/` |
| 15 | Partnership OS | الشراكات والقنوات | `docs/partnerships/` |
| 16 | Privacy Guard | حماية الخصوصية | `docs/privacy/` |
| 17 | Finance Snapshot | لقطة مالية | `company_os/finance/` |
| 18 | Founder GTM Control Room | غرفة تحكّم المؤسّس | `docs/gtm/FOUNDER_GTM_COMMAND_CENTER_AR.md` |

**المعادلة:**
`Market Production OS = Brand OS + Product Catalog OS + Sector Intelligence OS +
Signal Detection OS + Prospect Research OS + Cold Email Draft Factory +
Compliance Gate + Deliverability OS + Founder Approval Queue + Sending Ramp OS +
Reply Handling OS + WhatsApp Post-Reply Routing + Content OS + Press OS +
Partnership OS + Privacy Guard + Finance Snapshot + Founder GTM Control Room`

---

## 3. الإيقاع اليومي (Daily GTM Rhythm)

| الوقت | المرحلة | المخرج |
|------|---------|--------|
| 07:30 | البحث والإشارات | `reports/signals/SIGNAL_REPORT.md` |
| 08:30 | توليد 250 مسودّة | `data/outreach/drafts.jsonl` |
| 09:00 | بوّابات الجودة/الامتثال/قابلية التسليم | `reports/outreach/DRAFT_GATE_REVIEW.md` |
| 10:00 | طابور موافقة المؤسّس | `reports/outreach/APPROVAL_QUEUE.md` |
| 11:00 | **خطة** دفعة إرسال معتمدة محدودة فقط | `reports/outreach/SENDING_BATCH_PLAN.md` |
| 13:00 | طابور الردود | `docs/commercial/SALES_PROCESS_AR.md` |
| 15:00 | الشركاء/الصحافة/إشارات الوظائف | `reports/partnerships/`, `reports/press/` |
| 18:00 | إنتاج المحتوى | `reports/content/CONTENT_PRODUCTION_QUEUE.md` |
| 21:00 | تقرير GTM اليومي | `reports/gtm/DAILY_GTM_REPORT.md` |

> **250 مسودّة/يوم مسموحة ومطلوبة. 250 إرسالة/يوم ممنوعة حتى تجتاز بوّابات قابلية التسليم.**
> الساعة 11:00 تنتج **خطة** دفعة فقط — لا إرسال فعلي تلقائي.

---

## 4. الإيقاع الأسبوعي (Weekly GTM Rhythm)

- إيقاف أسوأ 20% من الرسائل.
- مضاعفة أفضل 20%.
- تحديث كتيّبات القطاعات.
- تحديث بنك الاعتراضات.
- تحديث كتالوج المنتجات.
- مراجعة صحة الدومين.
- مراجعة ROI لكل قناة.
- اختيار 3 أهداف صحافة.
- اختيار 10 أهداف شراكة.

المرجع: `reports/gtm/WEEKLY_GTM_REVIEW.md`.

---

## 5. القواعد غير القابلة للتفاوض

لا إرسال بريد خارجي · لا تفعيل إرسال حقيقي · لا أتمتة واتساب باردة · لا أتمتة
LinkedIn · لا scraping مخالف · لا طلب مفاتيح API في الدردشة · لا تخزين أسرار · لا
كشف PII في logs · لا case studies وهمية · لا عملاء مخترَعين · لا ضمان إيرادات · لا
ادّعاءات "10x" · لا عناوين `Re:/Fwd:` وهمية · لا حذف اختبارات لتمريرها · لا إضعاف
بوّابات الثقة/الأمان/الموافقة.

كل إجراء خارجي يبدأ افتراضياً بـ: `dry_run=true`, `approval_required=true`, `send_enabled=false`.

---

*المرجع المركزي للمصطلحات والمعرّفات: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`.*
