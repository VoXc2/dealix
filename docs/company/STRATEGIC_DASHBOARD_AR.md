# اللوحة الاستراتيجية — طبقة رأس المال

**الطبقة:** L1 · Capital Model
**المالك:** المؤسس
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [STRATEGIC_DASHBOARD.md](./STRATEGIC_DASHBOARD.md)

## السياق
أغلب لوحات الشركات تقيس الإيراد. تقيس اللوحة الاستراتيجية **رؤوس
الأموال الخمسة** التي يُفترض أن تُراكمها الشركة. هي اللوحة الوحيدة
التي يقرؤها المؤسس ليعرف هل تكسب ديلكس اللعبة بعيدة الأمد. تجلس
فوق المقاييس التشغيلية في `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`،
وتُكمل العرض المالي في `docs/FINANCE_DASHBOARD.md`، وتُغذّي حزمة
القرار التنفيذية في `docs/EXECUTIVE_DECISION_PACK.md`.

## ماذا تتتبّع اللوحة

تتتبّع اللوحة رؤوس الأموال الخمسة المُعرَّفة في
`docs/company/DEALIX_CAPITAL_MODEL.md`، مع تقسيم كل رأس مال إلى فئاته
الفرعية التي تُمثّل سطح التراكم.

### Service Capital
- Ready services — خدمات في الكتالوج النشط.
- Beta services — خدمات في تحقّق Pilot.
- Scalable services — خدمات بـ Unit Economics وقوالب مكتملة.

### Product Capital
- Internal tools — العدد والتبنّي.
- Client-visible features — العدد والاستخدام.
- Repeated workflows — تجري بالطريقة نفسها عبر 3+ عملاء.

### Knowledge Capital
- Playbooks — أدلّة تشغيل خاصة بكل قطاع.
- Templates — أصول قابلة لإعادة الاستخدام في Stage 2+ من نظام
  التدرّج.
- Benchmarks — مراجع كمّية منشورة.

### Trust Capital
- Proof packs — إجمالي والإضافات في الربع الأخير.
- Case studies — منشورة.
- Testimonials — مُسجَّلة.
- Governance incidents — العدد، الشدّة، حالة الحل.

### Market Capital
- Audience — مشتركون، متابعون، قرّاء متكرّرون.
- Partners — عدد الشركاء النشطين.
- Referrals — إحالات الربع الأخير.
- Inbound leads — محادثات واردة مؤهَّلة.

## المبدأ

> ديلكس تقيس نفسها كتراكم أصول، لا كتدفّق إيراد.

الإيراد بلا تراكم رأس مال هو مؤشّر مُتقدّم لتراجع متوسّط الأمد.
وتراكم رأس مال بإيراد منخفض هو خطر قصير الأمد لكنه ربح بعيد. وُجدت
اللوحة الاستراتيجية لإجبار هذه المفاضلة على المراجعة الأسبوعية
للمؤسس.

## إيقاع القراءة

- **أسبوعياً** — بلاطات تشغيلية (المشاريع النشطة، Pipeline،
  الطاقة).
- **شهرياً** — تغيّرات رؤوس الأموال الخمسة.
- **ربعياً** — مراجعة استراتيجية مقابل الأهداف المُعلَنة في
  `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## آليات التحديث

لكل بلاطة مصدر موثَّق. Service Capital من Service Ladder، Product
Capital من Backlog الهندسة، Knowledge Capital من IP Registry و
Knowledge Graph، Trust Capital من Capital Ledger وأرشيف Proof
Packs، Market Capital من التحليلات وقائمة الشركاء. لا يُسمح لأي
بلاطة بالاعتماد على الذاكرة اليدوية.

## قواعد القرار

- إذا انخفض رأسا مال ربع/ربع، يُفتَح تحقيق.
- إذا انخفض Trust Capital بينما الإيراد يرتفع، تُوقف الشركة
  المبيعات الجديدة حتى يستأنف إنتاج Proof Packs.
- إذا ثبت Market Capital لربعَين، يُدقَّق محرّك المحتوى.

## الواجهات
| المدخلات | المخرجات | الملاك | الإيقاع |
|---|---|---|---|
| Capital Ledger | قيم بلاطات Trust + Service | المؤسس | أسبوعياً |
| IP Registry | قيم بلاطات Knowledge | المؤسس | أسبوعياً |
| Backlog الهندسة | قيم بلاطات Product | المؤسس | أسبوعياً |
| بيانات المحتوى / الشركاء | قيم بلاطات Market | المؤسس | أسبوعياً |

## المقاييس
- Capital growth index — مؤشّر مركّب لتغيّر رؤوس الأموال ربع/ربع؛ الهدف ≥ +5%.
- Capitals at risk — رؤوس أموال ثابتة أو متراجعة ربع/ربع؛ الهدف ≤ 1.
- Dashboard freshness — نسبة البلاطات المُحدَّثة ضمن الإيقاع؛ الهدف 100%.
- Decision-to-action latency — الأيام بين تحفيز اللوحة والإجراء المُسجَّل؛ الهدف ≤ 5.

## ذات صلة
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — طبقة الـ KPI التشغيلية تحت اللوحة.
- `docs/FINANCE_DASHBOARD.md` — المُكمّل المالي لعرض رأس المال.
- `docs/EXECUTIVE_DECISION_PACK.md` — الحزمة التي تُغذّيها اللوحة.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — النموذج الذي تقيسه اللوحة.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
