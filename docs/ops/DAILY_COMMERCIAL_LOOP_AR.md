# حلقة التنفيذ التجاري اليومية — Dealix

يربط هذا الملف **المراحل التشغيلية** ([COMPREHENSIVE_COMPLETION_PLAN_AR.md](../COMPREHENSIVE_COMPLETION_PLAN_AR.md)) بـ **لوحة ما بعد الإطلاق** ([POST_LAUNCH_SCORECARD.md](POST_LAUNCH_SCORECARD.md)) حتى أول إيراد مدفوع ثم التكرار.

## يومياً (قبل أول دولار)

| خطوة | مرجع |
|------|--------|
| الكود على `main` + CI أخضر + نشر staging إن وُجد | المراحل A–C في [COMPREHENSIVE_COMPLETION_PLAN_AR.md](../COMPREHENSIVE_COMPLETION_PLAN_AR.md) |
| `/health` + `python scripts/launch_readiness_check.py --base-url "$STAGING_BASE_URL"` | نفس المستند، §4 |
| مسار عميل Level 1 (Form → Sheet → صف تجريبي) | §5 + [LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md](full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md) |

## أسبوعياً

| خطوة | مرجع |
|------|--------|
| نسخ قالب T+7 / T+30 من [POST_LAUNCH_SCORECARD.md](POST_LAUNCH_SCORECARD.md) وملء الأرقام فقط | أي صف «أحمر» يصبح action item بمالك وتاريخ |
| مراجعة [NORTH_STAR_AR.md](../strategic/NORTH_STAR_AR.md) | Proof + Pilot قبل توسع MRR |

## عند أول إيراد (المرحلة E)

- [OFFER_LADDER.md](../OFFER_LADDER.md) + [MANUAL_PAYMENT_SOP.md](MANUAL_PAYMENT_SOP.md)
- **DoD:** دفع أو التزام مكتوب + Proof Pack مُسلَّم (انظر [COMPREHENSIVE_COMPLETION_PLAN_AR.md](../COMPREHENSIVE_COMPLETION_PLAN_AR.md) §6)

## بعد الإطلاق العام

- استمرار نفس أسبوعية الـ Scorecard؛ ربط الأرقام بـ [POST_LAUNCH_BACKLOG.md](POST_LAUNCH_BACKLOG.md) عند فتح البوابات العامة (§7–8 في خطة الإكمال).

## تحقق Revenue OS (للمطورين)

`bash scripts/revenue_os_master_verify.sh` — انظر [AGENTS.md](../../AGENTS.md).

## بوابات الإطلاق والاستراتيجية والامتثال (متى تُفتح)

| المستند | متى تستخدمه |
|---------|----------------|
| [LAUNCH_GATES.md](../LAUNCH_GATES.md) | قرار GO/NO-GO قبل الإعلان العام؛ لا «إطلاق كامل» دون استيفاء القواعد هناك. |
| [LAUNCH_READINESS_REPORT.md](../LAUNCH_READINESS_REPORT.md) | لقطة جاهزية تقنية/منتج؛ تُحدَّث قبل مراجعة الإطلاق أو الـ pilot الكبير. |
| [STRATEGIC_MASTER_PLAN_2026.md](../STRATEGIC_MASTER_PLAN_2026.md) | اتجاه السوق والمواقع الدفاعية (PDPL، سكن بيانات، قنوات) — **مرجع استراتيجي** لا يستبدل بوابات الإطلاق. |
| [DPA_CHECKLIST_AR_EN.md](../wave8/DPA_CHECKLIST_AR_EN.md) | قبل مشاركة بيانات عميل مع معالج خارجي أو عقد enterprise يتطلب DPA. |

**لا تُقدَّم** وعود مبيعات أو «جاهزية كاملة» خارج ما تسمح به الحوكمة في [DEALIX_MASTER_OPERATING_MODEL_AR.md](../strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md) وكتالوج الإجراءات.

## مؤشر أسبوعي واحد (للمؤسس)

قبل توسيع المبيعات أو المنتج: **عدد Pilots النشطة** + **عدد أحداث إثبات (Proof) المسلَّمة هذا الأسبوع** (أو ما يعادلها في لوحتك). سجّل الأرقام في قالب [POST_LAUNCH_SCORECARD.md](POST_LAUNCH_SCORECARD.md) (T+7 حتى قبل الإطلاق العام؛ بعده T+30). أي صف أحمر = action item بمالك وتاريخ إغلاق.
