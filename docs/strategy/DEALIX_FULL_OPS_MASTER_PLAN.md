# Dealix — Full Ops Master Plan
<!-- Owner: Founder | Date: 2026-05-17 | Arabic primary — العربية أولاً -->

> **قاعدة هذا المستند:** التسعير وبنية العروض تتبع `docs/OFFER_LADDER_AND_PRICING.md`
> المقفول بـ `docs/transformation/01_doctrine_lock.md`. أي رقم تسعير هنا مرجعه
> ذلك الملف، لا اقتراحات مستقلة. تغيير السلم يمرّ بـ RFC.
>
> **Doctrine note.** Pricing and offer architecture follow the *locked* ladder
> in `docs/OFFER_LADDER_AND_PRICING.md`. This document does not introduce new
> price points; changing the ladder requires an RFC under
> `docs/transformation/rfcs/`.

---

## 1. الغرض — Purpose

Dealix لا تحتاج مزايا منتج إضافية الآن. تحتاج **نظام توزيع وتشغيل** حول منتج
موجود ومُطلق فعلاً (`api.dealix.me` حيّ). هذا المستند يحوّل خطة "Full Ops" إلى
شكل قابل للتنفيذ: 12 ماكينة، كل واحدة لها مدخل ووكيل وبوابة موافقة وحدث دليل
وKPI ووضع فشل — مع تحليل صريح لما هو **موجود** مقابل **ناقص**.

Dealix needs a distribution and operating system around an already-launched
product — not more product features. Twelve machines, each with Input → Agent →
Approval Gate → Evidence Event → KPI → Failure Mode.

---

## 2. التموضع — Positioning

> Dealix helps companies turn AI experiments and revenue operations into
> governed, measurable workflows — with source clarity, approval boundaries,
> evidence trails, and proof of value.

بالعربية: Dealix تحوّل تجارب الذكاء الاصطناعي وعمليات الإيراد إلى تشغيل محكوم
وقابل للقياس عبر وضوح المصادر، حدود الموافقة، مسارات الأدلة، وإثبات القيمة.

لسنا منصة AI ولا chatbot ولا automation agency ولا dashboard.

---

## 3. القاعدة التنفيذية — The operating loop

```
Product → Proof → Funnel → Sales → Billing → Delivery → Support
→ Upsell → Referral → Partners → Affiliates → Media → Evidence → Governance → Learning
```

كل قناة تُنتج lead → كل lead يدخل scoring → كل scoring يُنتج next action →
كل إجراء عالي المخاطر يحتاج approval → كل نتيجة تُسجَّل كدليل → كل دليل متكرر
يتحوّل إلى playbook → كل playbook متكرر يتحوّل إلى automation/module.

---

## 4. تسوية التسعير — Pricing reconciliation (مهم)

خطة "Full Ops" المُقترحة ذكرت سلّماً بـ Diagnostic 4,999–25,000 ريال وSprint
بـ 25,000 ريال. **هذا يخالف السلم المقفول.** السلم النافذ:

| الدرجة | السعر | الحالة |
|--------|-------|--------|
| [0] Free AI Ops Diagnostic | مجاني | متاح |
| [1] 7-Day Revenue Proof Sprint | 499 SAR | متاح |
| [2] Data-to-Revenue Pack | 1,500 SAR | بعد تأهيل |
| [3] Managed Revenue Ops | 2,999–4,999 SAR/شهر | بعد pilot |
| [4] Executive Command Center | 7,500–15,000 SAR/شهر | بعد 3 pilots |
| [5] Agency Partner OS | مخصص + rev-share | بعد 3 proof packs |

كل ماكينة في هذا المستند تخدم هذا السلم. التسعير الأعلى (enterprise) يبقى
مقترحاً يحتاج RFC إن أُريد تبنّيه؛ لا يُعتمد افتراضاً.

---

## 5. تحليل الفجوات — Gap analysis

تدقيق الكود (2026-05-17): **11 من 12 ماكينة موجودة فعلاً** كشيفرة، غالبها تحت
`auto_client_acquisition/*` (172 router في `api/routers/`).

| # | الماكينة | الحالة | المرجع في الكود |
|---|----------|--------|------------------|
| 1 | Lead capture + scoring | ✅ موجود | `dealix/intelligence/lead_scorer.py`, `auto_client_acquisition/crm_v10/lead_scoring.py`, `api/routers/leadops_spine.py` |
| 2 | Stage / pipeline transitions | ✅ موجود | `auto_client_acquisition/revenue_pipeline/stage_policy.py`, `crm_v10/stage_machine.py` |
| 3 | Approval gates / approval center | ✅ موجود | `auto_client_acquisition/governance_os/approval_policy.py`, `approval_matrix.py`, `api/routers/approval_center.py` |
| 4 | Evidence ledger / events | ✅ موجود | `auto_client_acquisition/evidence_control_plane_os/`, `auditability_os/evidence_chain.py`, `proof_ledger/` |
| 5 | Claim guard / is_estimate | ✅ موجود | `governance_os/rules/no_fake_proof.yaml`, `compliance_trust_os/claim_safety.py` |
| 6 | Public Risk-Score (lead magnet) | ⚠️ جزئي | risk scoring داخلي موجود؛ **لا endpoint عام** — يُبنى على هذا الفرع |
| 7 | Proof Pack generation | ✅ موجود | `auto_client_acquisition/proof_os/proof_pack.py`, `proof_architecture_os/proof_pack_v2.py` |
| 8 | Invoice / billing draft + guards | ⚠️ جزئي | `finance_os/invoice_draft.py`, `revops/invoice_state.py` — تكامل الدفع غير مكتمل |
| 9 | Support desk / classifier / KB | ✅ موجود | `auto_client_acquisition/support_os/`, `support_inbox/`, `docs/knowledge-base/` |
| 10 | Partner program / referrals | ✅ موجود | `auto_client_acquisition/partnership_os/` (partner_motion, referral_tracker) |
| 11 | Affiliate / commissions / payouts | ❌ ناقص | referral tracker موجود؛ لا commission/payout مهيكل |
| 12 | Agent orchestrator + permissions | ✅ موجود | `ai_workforce/orchestrator.py`, `agentic_operations_os/agent_permissions.py` |

**ناقص حقاً:** (11) ماكينة Affiliate. **جزئي:** (6) endpoint Risk-Score عام،
(8) بوابات الفوترة. **مبعثر:** ملفات config موجودة لكن بلا مجلد `dealix/config/`
موحَّد (راجع `data/workflows/*.yaml` و`governance_os/rules/*.yaml`).

الخلاصة: العمل المتبقي ليس بناء 12 ماكينة — بل **سدّ 3–4 فجوات وربط الموجود**.

---

## 6. الـ 12 ماكينة — مرجع سريع

لكل ماكينة: مدخل، وكيل، بوابة موافقة، حدث دليل، KPI. (التفصيل في خطة Full Ops
الأصلية؛ هنا الربط بالكود فقط.)

1. **Market Signal** — مدخلات المؤسس (لا scraping) → `revenue_os/signals/normalize`.
2. **Founder Media** — حلقة محتوى من اعتراضات المبيعات.
3. **Lead Magnet** — Risk Score → الفرع الحالي يبنيه (انظر §8).
4. **Sales Autopilot** — `leadops_spine.py` + `sales_os.py`؛ لا إرسال خارجي تلقائي.
5. **Demo & Proof** — ديمو 12 دقيقة من `/ar/business-now#strategy`.
6. **Billing & Closing** — `finance_os/invoice_draft.py`؛ بوابة: لا invoice بلا scope معتمد.
7. **Delivery Factory** — `data/workflows/diagnostic.yaml`, `proof_pack.yaml`.
8. **Support Autopilot** — `support_os/` + KB؛ تصعيد المخاطر العالية.
9. **Customer Success & Upsell** — `customer_success_os.py`؛ لا upsell بلا proof.
10. **Partner Distribution** — `partnership_os/`.
11. **Affiliate** — ناقص؛ أول مرشّح بناء بعد الفرع الحالي.
12. **Governance & Evidence** — `governance_os/` + `evidence_control_plane_os/` = الـ moat.

---

## 7. Backlog متسلسل — Sequenced backlog

**الموجة الحالية (هذا الفرع):**
- ✅ هذا المستند (تحليل فجوات + تسوية تسعير).
- ✅ Endpoint عام `POST /api/v1/public/risk-score` + module + اختبار (§8).

**الموجة التالية (مرشّحات، تحتاج green-light مستقل):**
1. ماكينة Affiliate — الفجوة الوحيدة الحقيقية. tiers + commission calc + بوابة
   payout (عمولة فقط بعد `invoice_paid`) + قواعد إفصاح. module جديد + اختبارات.
2. إكمال بوابات الفوترة — ربط `invoice_draft` بحارس "لا تسليم قبل دفع".
3. مجلد `dealix/config/` موحَّد — فقط إن ربطناه بكود فعلي (config بلا كود = ملف ميت).

**ممنوع بناؤه الآن:** أي ماكينة بلا طلب حقيقي متكرر — راجع
`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`.

---

## 8. أول بناء على هذا الفرع — Public Risk-Score

الباب الأمامي للقمع: زائر يجيب على استبيان حوكمة قصير فيحصل على درجة مخاطر
تشغيل الإيراد/الذكاء الاصطناعي، وأهم الفجوات، والخطوة التالية (التشخيص المجاني).

- **Endpoint:** `POST /api/v1/public/risk-score` (`api/routers/public.py`).
- **Module:** `auto_client_acquisition/risk_score.py` — دالة scoring نقية.
- **المخرج:** درجة 0–100 (أعلى = مخاطر أعلى)، نطاق، فجوات، خطوة تالية.
- **الحوكمة:** الدرجة موسومة `is_estimate: true`، لا ادعاء ROI، لا إرسال خارجي،
  honeypot + شرط consent، الـ lead يُحفظ في `lead_inbox` فقط (مراجعة المؤسس).
- **الخطوة التالية الموصى بها دائماً:** الدرجة [0] Free AI Ops Diagnostic.

---

## 9. الحوكمة — Governance

غير القابلة للتفاوض **خمس** (المصدر `docs/transformation/01_doctrine_lock.md` —
وليست 11 كما في الخطة المقترحة):

1. لا إجراء خارجي عالي المخاطر بلا موافقة.
2. لا ادعاء قيمة مقيسة بلا دليل مصدر.
3. لا وصول تشغيلي عابر للمستأجرين.
4. لا استقلالية إنتاج بلا مسار rollback.
5. لا مبالغة proof تتجاوز مستوى الدليل المتاح.

العقيدة: `Signal → Source → Approval → Action → Evidence → Decision → Value → Asset`.

---

## 10. القرار الحاكم — Governing decision

> Dealix لا تفوز لأنها تملك AI أكثر — بل لأنها تجعل AI والإيراد قابلين للبيع
> والتشغيل والخدمة والقياس والتوسع، تحت نظام موافقات وأدلة يحفظ الثقة.

لا تبنِ من أجل البناء. اسدّ الفجوات الأربع، اربط الموجود، واترك كل automation
جديدة حتى يظهر طلب حقيقي متكرر.
