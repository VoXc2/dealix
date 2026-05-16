# Dealix — Governed Revenue & AI Operations — تشغيل الإيراد والذكاء الاصطناعي المحكوم

<!-- STRATEGY | Owner: Founder | Date: 2026-05-16 | Canonical positioning doc -->
<!-- Arabic primary — العربية أولاً -->

> **بيان التموضع:** ديالكس — تشغيل إيراد وذكاء اصطناعي محكوم بالأدلة والموافقات وقياس القيمة.
> **Positioning:** Dealix — Governed Revenue & AI Operations.

هذه الوثيقة هي المرجع الرسمي للتموضع والاستراتيجية. التسعير الكامل في
`docs/OFFER_LADDER_AND_PRICING.md` (v2). محفّزات البناء في
`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`.

---

# القسم العربي — Arabic

## 1. التموضع — شركة تشغيل إيراد وذكاء اصطناعي محكوم

السوق لا ينقصه أدوات ذكاء اصطناعي. ما ينقصه هو **التشغيل، والحوكمة، وبيانات
موثوقة، وأهداف عائد واضحة**. الأدوات متوفرة بكثرة؛ القرار المحكوم نادر.

ديالكس لا تبيع روبوتات ولا أتمتة. ديالكس تبيع **قرارات إيراد وذكاء اصطناعي
محكومة ومدعومة بالأدلة**: لكل رقم مصدر، ولكل إجراء خارجي موافقة، ولكل قرار
أثر موثّق وقيمة قابلة للقياس.

## 2. مقياس النجم القطبي — "قرارات قيمة محكومة منشأة"

المقياس الأساسي هو **عدد قرارات القيمة المحكومة المُنشأة** (Governed Value
Decisions Created): قرارات تشغيلية أو إيرادية اتُّخذت بـ:

- مصدر واضح للبيانات،
- موافقة واضحة،
- أثر موثّق،
- قيمة قابلة للقياس.

في مرحلة الخدمات الأولى، هذا المقياس أصدق من عدّ المستخدمين، لأنه يقيس القيمة
المُسلَّمة لا مجرد الوصول.

## 3. استراتيجية الشركة — من الخدمة إلى المنصة

التسلسل الإلزامي:

> بقيادة الخدمة → مدعوم بالبرمجيات → مقاد بالأدلة → مسنود باشتراك → منصة لاحقاً.

تسلسل البيع: **التشخيص → السبرنت → الاشتراك → إشارة المنصة**.

**قاعدة صارمة:** لا تُبنى منصة SaaS قبل إثبات قابلية التكرار. البناء يتبع
الطلب الحقيقي، لا التوقّع.

## 4. كتالوج الخدمات السبع (ملخص)

| # | الخدمة | السعر | ملاحظة |
|---|--------|-------|--------|
| 0 | تشخيص عمليات الإيراد المحكوم | مجاني | باب الدخول |
| 1 | سبرنت ذكاء الإيراد | 25,000 ريال | العرض المدفوع الأساسي |
| 2 | اشتراك العمليات المحكومة | 4,999–35,000 ريال/شهر | متكرر |
| 3 | حوكمة الذكاء الاصطناعي لفرق الإيراد | حسب النطاق | سياسة وحدود |
| 4 | جاهزية CRM/البيانات للذكاء الاصطناعي | حسب النطاق | تنظيف ومصادر |
| 5 | مذكرة قرار مجلس الإدارة | حسب النطاق | قيادة |
| 6 | حزمة الثقة المختصرة | حسب النطاق | تُعرض فقط عند إشارة `asks_for_security` |

التسعير الكامل لكل خدمة في `docs/OFFER_LADDER_AND_PRICING.md`.

## 5. تسلسل البيع

التشخيص → السبرنت → الاشتراك → حزمة الثقة المختصرة عند الطلب → مذكرة المجلس
للقيادة. **لا تُعرض كل الخدمات دفعة واحدة.** كل خطوة تُفتح بدليل من سابقتها.

## 6. آلة حالة إثبات السوق (L2→L7)

| الحالة | المستوى |
|--------|---------|
| `prepared_not_sent` | L2 |
| `sent` | L4 |
| `replied_interested` | L4 |
| `meeting_booked` | L4 |
| `used_in_meeting` | L5 |
| `scope_requested` | L6 |
| `pilot_intro_requested` | L6 |
| `invoice_sent` | L7_candidate |
| `invoice_paid` | L7_confirmed |

القواعد:

- لا `sent` بدون `founder_confirmed=true`.
- لا L5 بدون `used_in_meeting`.
- لا L6 بدون طلب نطاق أو طلب تعريف.
- لا L7_confirmed بدون دفع.
- لا يُحتسب إيراد قبل `invoice_paid`.

## 7. وضعية الحوكمة — "تشغيل كامل"

"التشغيل الكامل" يعني أن النظام: يُجهّز، يقترح، يحذّر، يسجّل، يتحقّق، يصنّف،
ويولّد المسودات — و**المؤسس يوافق على كل إجراء خارجي**.

- لا إرسال خارجي ذاتي.
- لا يُعامل مخرج ذكاء اصطناعي كدليل.
- لكل رقم `source_ref`.
- كل إجراء خارجي يحتاج موافقة.
- كل قرار يحصل على Decision Passport.
- كل ارتباط يُنتج Proof Pack.
- كل دليل يصبح أصلاً رأسمالياً (Capital Asset).

## 8. التموضع التنافسي

- **مقابل شركات RevOps التقليدية:** ديالكس تضيف حوكمة الذكاء الاصطناعي، حدود
  الموافقات، مسارات الأدلة، جوازات القرار، حزم الإثبات، ومنع الإجراءات
  الخارجية الذاتية.
- **مقابل بائعي وكلاء البيع بالذكاء الاصطناعي:** ديالكس تشترط وضوح المصدر،
  وحدود الموافقة، ومسارات الأدلة، وبوابات المخاطر قبل منح أي وكيل صلاحية
  الإرسال.

## 9. ثلاث شرائح مستهدفة

1. **خدمات B2B** — استشارات ووكالات وخدمات مهنية: pipeline مشوّش، متابعة
   ضعيفة، ذكاء اصطناعي غير مُدار.
2. **فينتك ومعالجو المدفوعات** — تدفّقات منظَّمة تتطلّب ثقة وموافقة وتدقيقاً.
3. **شركات محافظ صناديق الاستثمار** — شركات ناشئة تستخدم الذكاء الاصطناعي
   بسرعة لكن بلا حوكمة.

**لا تُدخل كل القطاعات.** ركّز على هذه الثلاث.

## 10. بوابات خارطة الطريق (بلا تواريخ)

| البوابة | الإثبات |
|---------|---------|
| 1 — أول إثبات سوق | 5 رسائل مُرسلة، تصنيف أول رد أو صمت |
| 2 — إثبات الاجتماع | `used_in_meeting=L5` |
| 3 — إثبات الجذب | `scope_requested=L6` |
| 4 — إثبات الإيراد | `invoice_paid=L7` مؤكَّد |
| 5 — قابلية التكرار | بيع العرض ذاته مرتين |
| 6 — الاشتراك | قيمة شهرية متكررة |
| 7 — إشارة المنصة | تكرار تدفّق يدوي 3 مرات أو أكثر |

## 11. المقاييس المتتبَّعة (نحو 7 فقط)

`sent_count` · `reply_count` · `meeting_count` · `scope_requested_count` ·
`invoice_sent_count` · `invoice_paid_count` · `retainer_opportunity_count`.

## 12. قاعدة البناء المشروط

تُبنى الميزة **فقط** إذا تحقّق أحد التالي:

- تكرّر تدفّق يدوي 3 مرات، أو
- طلبها عميل صراحةً، أو
- تُقلّل مخاطرة حقيقية، أو
- تُسرّع تسليماً مدفوعاً، أو
- تفتح اشتراكاً متكرراً.

غير ذلك: **لا بناء.**

## 13. الجملة الحاكمة

> ديالكس لا تبيع الذكاء الاصطناعي وحده، ولا RevOps وحده. ديالكس تبيع تشغيلاً
> محكوماً للإيراد والذكاء الاصطناعي: مصادر واضحة، وموافقات، وأدلة، وقرارات،
> وقيمة قابلة للقياس.

---

# English Section — القسم الإنجليزي

## 1. Positioning — A Governed Revenue & AI Operations Company

The market does not lack AI tools. It lacks **operations, governance, trusted
data, and clear ROI targets**. Tools are abundant; governed decisions are rare.

Dealix does not sell bots or automation. Dealix sells **governed,
evidence-backed revenue and AI decisions**: every number has a source, every
external action has an approval, every decision has a documented impact and
measurable value.

## 2. North-Star Metric — "Governed Value Decisions Created"

The primary metric is the **count of Governed Value Decisions Created**:
operational or revenue decisions made with:

- a clear data source,
- a clear approval,
- a documented impact,
- a measurable value.

At the service-led stage this metric is more honest than user-count, because
it measures value delivered, not mere access.

## 3. Company Strategy — Service to Platform

The mandatory sequence:

> Service-led → Software-assisted → Evidence-led → Retainer-backed → Platform later.

Sell sequence: **Diagnostic → Sprint → Retainer → Platform Signal**.

**Hard rule:** Do not build SaaS before repeatability is proven. Building
follows real demand, not anticipation.

## 4. The 7-Service Catalog (summary)

| # | Service | Price | Note |
|---|---------|-------|------|
| 0 | Governed Revenue Ops Diagnostic | Free | Entry door |
| 1 | Revenue Intelligence Sprint | 25,000 SAR | Core paid offer |
| 2 | Governed Ops Retainer | 4,999–35,000 SAR/mo | Recurring |
| 3 | AI Governance for Revenue Teams | Scoped | Policy and boundaries |
| 4 | CRM / Data Readiness for AI | Scoped | Hygiene and sources |
| 5 | Board Decision Memo | Scoped | Leadership |
| 6 | Trust Pack Lite | Scoped | Offered only on an `asks_for_security` signal |

Full per-service pricing lives in `docs/OFFER_LADDER_AND_PRICING.md`.

## 5. Sell Sequence

Diagnostic → Sprint → Retainer → Trust Pack Lite on demand → Board Memo for
leadership. **Never present all services at once.** Each step unlocks on
evidence from the one before it.

## 6. The Market-Proof State Machine (L2→L7)

| State | Level |
|-------|-------|
| `prepared_not_sent` | L2 |
| `sent` | L4 |
| `replied_interested` | L4 |
| `meeting_booked` | L4 |
| `used_in_meeting` | L5 |
| `scope_requested` | L6 |
| `pilot_intro_requested` | L6 |
| `invoice_sent` | L7_candidate |
| `invoice_paid` | L7_confirmed |

Rules:

- No `sent` without `founder_confirmed=true`.
- No L5 without `used_in_meeting`.
- No L6 without a scope or intro request.
- No L7_confirmed without payment.
- No revenue counted before `invoice_paid`.

## 7. Governance Posture — "Full Ops"

"Full Ops" means the system **prepares, suggests, warns, logs, verifies,
classifies, and generates drafts** — and the **founder approves every external
action**.

- No autonomous external send.
- No AI output treated as evidence.
- Every number carries a `source_ref`.
- Every external action needs approval.
- Every decision gets a Decision Passport.
- Every engagement produces a Proof Pack.
- Every proof becomes a Capital Asset.

## 8. Competitor Positioning

- **vs. traditional RevOps firms:** Dealix adds AI governance, approval
  boundaries, evidence trails, decision passports, proof packs, and no
  autonomous external actions.
- **vs. AI sales-agent vendors:** Dealix requires source clarity, approval
  boundaries, evidence trails, and risk gates before granting any agent send
  authority.

## 9. Three Target Segments

1. **B2B Services** — consulting, agencies, professional services: messy
   pipeline, weak follow-up, unmanaged AI.
2. **Fintech / Processors** — regulated workflows that demand trust, approval,
   and audit.
3. **VC Portfolio companies** — startups using AI fast but without governance.

**Do not enter all sectors.** Focus on these three.

## 10. Roadmap Gates (no dates)

| Gate | Proof |
|------|-------|
| 1 — First Market Proof | 5 messages sent, first reply or silence classified |
| 2 — Meeting Proof | `used_in_meeting=L5` |
| 3 — Pull Proof | `scope_requested=L6` |
| 4 — Revenue Proof | `invoice_paid=L7` confirmed |
| 5 — Repeatability | Same offer sold twice |
| 6 — Retainer | Recurring monthly value |
| 7 — Platform Signal | A manual workflow repeated 3+ times |

## 11. Tracked Metrics (~7 only)

`sent_count` · `reply_count` · `meeting_count` · `scope_requested_count` ·
`invoice_sent_count` · `invoice_paid_count` · `retainer_opportunity_count`.

## 12. Conditional-Build Rule

Build a feature **only** if one of the following holds:

- a manual workflow repeated 3 times, or
- a customer explicitly requested it, or
- it reduces real risk, or
- it speeds a paid delivery, or
- it opens a retainer.

Otherwise: **No build.**

## 13. Governing Sentence

> Dealix does not sell AI alone, nor RevOps alone. Dealix sells governed
> operations for revenue and AI: clear sources, approvals, evidence,
> decisions, and measurable value.

---

## Related documents — وثائق ذات صلة

- `docs/OFFER_LADDER_AND_PRICING.md` — full ladder and pricing (v2).
- `docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md` — build triggers.
- `docs/COMPANY_SERVICE_LADDER.md` — prior ladder (superseded).

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
