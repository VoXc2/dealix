# مكتبة المخرجات (DELIVERABLES LIBRARY)

> **المصدر:** [`data/commercial/product_catalog.yaml`](../../data/commercial/product_catalog.yaml) · التفاصيل في [`PRODUCT_CATALOG_AR.md`](./PRODUCT_CATALOG_AR.md).
> العملة `ر.س` · كل الأسعار **نطاق** · **السعر النهائي بموافقة المؤسّس** · الافتراضات: `dry_run=true`، `approval_required=true`، `send_enabled=false`.

## الفكرة
مكتبة مخرجات **قابلة لإعادة الاستخدام** تُجمَّع في باقات. إعادة الاستخدام تثبّت الجودة وتربط السعر بالمخرجات والمدة (قاعدة PR-007)، وتحدّ من تضخّم النطاق.
نحن **نساعد، نجهّز، نرتّب، نقيس، نكشف فرص التحسين، نقترح، ونجهّز مسودّات بموافقة** — بلا وعد بنتائج مضمونة وبلا إرسال خارجي بلا موافقة بشرية.

## كتالوج المخرجات القابلة لإعادة الاستخدام
| المخرج | ماذا يقدّم | الإثبات | يظهر في |
|--------|-----------|---------|---------|
| **Readiness Score** درجة جاهزية | تقييم مبدئي + مسار موصى به | assumed | `DLX-L0` |
| **Leakage Map** خريطة تسرّب الإيرادات | أين تضيع الفرص + نقاط التسرّب | observed | `DLX-L1` |
| **Priority Issues List** قائمة المشاكل ذات الأولوية | ترتيب المشاكل حسب الأثر | observed | `DLX-L1` |
| **First Workflow Recommendation** أول توصية workflow | الخطوة التشغيلية التالية المقترحة | observed | `DLX-L1` |
| **Follow-up Queue** طابور متابعة | تنظيم المتابعات ضمن SLA متفق عليه | observed | `DLX-L2`، `DLX-L3` |
| **Draft Templates** قوالب مسودّات | مسودّات معتمدة (ترسل بموافقة بشرية فقط) | observed | `DLX-L2`، `DLX-L3` |
| **Approval Workflow** workflow موافقة | مسار اعتماد بشري قبل أي إرسال | observed | `DLX-L2`، `DLX-L4` |
| **Dashboard** لوحة قياس | مصدر واحد للحقيقة لمؤشرات الـ pipeline | observed | `DLX-L3`، `DLX-L4` |
| **Periodic / Weekly Report** تقرير دوري/أسبوعي | تقرير ثابت قابل للقياس | observed | `DLX-L3`، `DLX-L5` |
| **Drafts & Follow-up Process** عملية مسودّات ومتابعة | عملية متكاملة بموافقة | observed | `DLX-L3` |
| **Governance Layer** عملية حوكمة وموافقة | ضوابط وتدقيق عبر الفرق | observed | `DLX-L4`، `DLX-L6` |
| **Weekly Improvements** تحسينات أسبوعية | تحسين مستمر مُقاس | observed | `DLX-L5` |
| **Experiments** تجارب مُقاسة | تجارب شهرية بمقاييس متفق عليها | observed | `DLX-L5` |
| **Proof Pack** حزمة إثبات | توثيق نتائج العمل (أمثلة توضيحية فقط) | observed | `DLX-L1`، `DLX-L3` |
| **Custom Multi-workflow OS** نظام تشغيل مخصّص | عدّة workflows ضمن بيان نطاق موقّع | verified | `DLX-L6` |

## ربط المخرجات بالعروض (مطابق للـ YAML)
- **`DLX-L0`:** Readiness Score · Recommended Path.
- **`DLX-L1` (P1):** Leakage Map · Priority Issues List · First Workflow Recommendation.
- **`DLX-L2`:** Follow-up Queue · Draft Templates · Approval Workflow · Report.
- **`DLX-L3`:** Operational Workflow · Dashboard · Periodic Reports · Drafts & Follow-up Process.
- **`DLX-L4`:** Multi-workflow Revenue Ops Layer · Dashboards · Governance & Approval Process.
- **`DLX-L5` (P2):** Weekly Improvements · Periodic Reports · Experiments.
- **`DLX-L6`:** Custom Multi-workflow OS · Custom Governance & Reports.

## قواعد استخدام المكتبة
- **كل مخرج مرتبط بمدة ونطاق سعري** عبر الباقة التي يظهر فيها (لا يُسعَّر منفرداً بلا موافقة).
- **القوالب والمسودّات تُرسل بموافقة بشرية فقط** — لا إرسال خارجي تلقائي (حوكمة [`agent_permissions.md`](../../company_os/governance/agent_permissions.md)).
- **أي مخرج خارج قائمة الباقة = ملحق نطاق جديد**، لا إضافة مجانية (انظر [`SCOPE_AND_OUT_OF_SCOPE_AR.md`](./SCOPE_AND_OUT_OF_SCOPE_AR.md)).
- **عدد جولات مراجعة المخرج محدّد مسبقاً** (قاعدة PR-005).
- **أي مثال نتائج يُعلَّم «مثال توضيحي»** ولا يُقدَّم كنتيجة مضمونة.

> التغليف: [`PACKAGING_STRATEGY_AR.md`](./PACKAGING_STRATEGY_AR.md) · ضوابط التسعير: [`PRICING_GUARDRAILS_AR.md`](./PRICING_GUARDRAILS_AR.md).

---
*Dealix · مكتبة المخرجات · المصدر: data/commercial/product_catalog.yaml · مخرجات بموافقة بشرية · السعر النهائي بموافقة المؤسّس.*
