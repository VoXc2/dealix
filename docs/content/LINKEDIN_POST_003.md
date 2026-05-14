# LinkedIn Post 003 — Proof Pack

> Bilingual long-form for the founder voice. AR first, EN second. No emojis. No model names. The schema for the proof score formula is the only code block in this post.
>
> Cross-link: [LINKEDIN_POST_001.md](./LINKEDIN_POST_001.md), [LINKEDIN_POST_002.md](./LINKEDIN_POST_002.md), [07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md), [LINKEDIN_CADENCE_PLAN.md](./LINKEDIN_CADENCE_PLAN.md).

---

**Title — العنوان**

Proof Pack — 14 أقسام بدل وعد / Proof Pack — 14 sections instead of a promise.

---

## العربية أولاً

### القاعدة الواحدة

لا نُغلق مشروعاً في ديليكس بدون حزمة إثبات. الحزمة لها معيار واحد، 14 قسماً، ودرجة محسوبة. الدرجة تحدّد ماذا يحقّ للعميل أن يفعل بنا في الخارج: قصة عامة، أم دعم مبيعات داخلي، أم تعلّم داخلي فقط.

### الأقسام الأربعة عشر

1. **الملخص التنفيذي** — صفحة واحدة، ثنائية اللغة، توضح ما طُلب وما سُلّم.
2. **المشكلة** — مع توقيع المُلكية: من رفع المشكلة، ومتى، وتحت أي تعريف.
3. **المدخلات** — قائمة الملفات والمصادر والاتصالات النظامية، بأرقام صفية لا بأسماء.
4. **جوازات المصدر** — جداول الجوازات المُستخدَمة في المشروع، بإذناتها وقراراتها.
5. **درجة جودة البيانات (DQ)** — اكتمال، تفرّد، صحة، اتساق، توقيت، مطابقة.
6. **العمل المُنفَّذ** — أنشطة محددة، بأيام تنفيذها، ومن نفّذها.
7. **المُخرَجات** — ما الذي تسلّمه العميل بالفعل، بروابط أو مواقع تخزين.
8. **قرارات الحوكمة** — كل قرار جرى أثناء المشروع: ALLOW، DRAFT_ONLY، REQUIRE_APPROVAL، REDACT، BLOCK، RATE_LIMIT، REROUTE.
9. **المخاطر المحظورة** — ما الذي رفضناه فعله، ولماذا، ومرجعه في الدستور.
10. **القيمة المُلاحَظة** — أرقام من سجل القيمة، مع طبقتها (دعم بيانات، دعم مبيعات، عمليات إيراد، تأثير إيراد) وحالة تأكيد العميل.
11. **القيود** — ما الذي لم نستطع فعله، ولماذا، وما يُحتاج لرفع القيد.
12. **الخطوة التالية المُوصى بها** — اقتراح محدد بقيمة وسعر، أو لا اقتراح.
13. **توصية الاشتراك الشهري** — هل تتكرر القيمة، أم تنتهي بإغلاق هذا المشروع.
14. **الأصول الرأسمالية** — كل أصل مُودَع في سجل الأصول، قابل لإعادة الاستخدام في مشاريع لاحقة.

### معادلة الدرجة

```
proof_score = round(
    0.25 * source_coverage
  + 0.25 * output_quality
  + 0.20 * governance_integrity
  + 0.15 * value_evidence
  + 0.15 * capital_asset_creation
)
```

كل مُكوّن في `[0, 100]`، والدرجة النهائية مدوّرة. كل مكون يُحسب من حقول مذكورة في الحزمة نفسها، لا من تقدير المؤسس.

### الطبقات الأربع

| الدرجة | الطبقة | ما يحقّ فعله |
|---|---|---|
| `>= 85` | **case_candidate** | مرشّحة لدراسة حالة عامة (مع موافقة العميل، وإذا سمح جواز المصدر بالاستخدام الخارجي). |
| `70 – 84` | **sales_support** | تُستخدَم داخل ديليكس كدعم مبيعات، بلا اسم عميل علني. |
| `55 – 69` | **internal_learning** | تعلّم داخلي فقط. لا تُحال خارجاً، حتى بلا اسم. |
| `< 55` | **weak** | فشل إنتاج. يُستدعى استرجاع داخلي ولا تُحرَّر فاتورة كاملة بلا معالجة. |

درجة عالية لا تُفوّض الاستخدام الخارجي وحدها. الاستخدام الخارجي يتطلب أيضاً `external_use_allowed = true` في جواز المصدر، وقيداً مُؤكَّداً من العميل على أي رقم قيمة يُذكَر.

### دعوة

نقبل عميلين هذا الشهر. ابدأ بتشخيص مجاني، 24 ساعة، باعتماد المؤسس. لا التزام بعده. إن واصلت إلى سبرنت ذكاء الإيرادات، تستلم حزمة إثبات كاملة بحدّها الأدنى من 14 قسماً، مع درجتها المحسوبة، خلال سبعة أيام.

---

## English

### The one rule

No project closes at Dealix without a Proof Pack. The Proof Pack has one standard: 14 sections plus a computed score. The score decides what the customer is allowed to do with us in public: a named case study, an internal sales reference, or internal learning only.

### The 14 sections

1. **Executive Summary** — one bilingual page. What was asked, what was delivered.
2. **Problem** — with ownership signature: who raised it, when, under what definition.
3. **Inputs** — files, sources, system connections, counted rather than named.
4. **Source Passports** — the passport table for every dataset used, with permissions and gate decisions.
5. **Data Quality Score** — completeness, uniqueness, validity, consistency, timeliness, conformance.
6. **Work Completed** — concrete activities with the day they ran and the person who ran them.
7. **Outputs** — exactly what the customer received, with links or storage references.
8. **Governance Decisions** — every decision made during the engagement: ALLOW, DRAFT_ONLY, REQUIRE_APPROVAL, REDACT, BLOCK, RATE_LIMIT, REROUTE.
9. **Blocked Risks** — what we refused to do, why, and the constitutional clause that backs the refusal.
10. **Observed Value** — numbers from the value_ledger, by tier (data support, sales support, revenue ops, revenue impact), with client-confirmation status on each.
11. **Limitations** — what we could not do, why, and what would be needed to lift the limitation.
12. **Recommended Next Step** — a specific proposal with value and price, or no proposal.
13. **Retainer Recommendation** — does value recur, or does it end at the close of this project.
14. **Capital Assets** — every asset deposited into the Capital Ledger, reusable in later projects.

### The score formula

```
proof_score = round(
    0.25 * source_coverage
  + 0.25 * output_quality
  + 0.20 * governance_integrity
  + 0.15 * value_evidence
  + 0.15 * capital_asset_creation
)
```

Every component lives in `[0, 100]`. The final score is rounded. Every component is computed from fields already present in the pack — not from founder estimation.

### The four tiers

| Score | Tier | What it authorizes |
|---|---|---|
| `>= 85` | **case_candidate** | Eligible for a public case study (with client consent and `external_use_allowed = true` on the underlying Source Passports). |
| `70 – 84` | **sales_support** | Used inside Dealix to support sales conversations, never with a client name in public. |
| `55 – 69` | **internal_learning** | Internal learning only. No external reference, even anonymized, without a separate review. |
| `< 55` | **weak** | A productization failure. Triggers a retrospective. A full invoice is not issued without remediation. |

A high score on its own does not authorize external use. External use also requires `external_use_allowed = true` on the underlying Source Passports, and a Client-Confirmed marker on any value number that will be referenced publicly. Two independent gates, both must be green.

### Why the customer should care

Most agencies hand a deliverable and a story. The story is the easier half. The deliverable, the audit trail, the limitations, the refusals — these are the harder half, and they are the half that survives a regulator visit, a board meeting, and a tense renewal conversation. A 14-section pack with a computed score makes the harder half default. You do not have to ask for the audit trail; it is already in the file.

### CTA — دعوة

**We accept 2 customers this month / نقبل عميلين هذا الشهر.**

Start with the Free Diagnostic. Twenty-four hours. Two pages. Founder signature. If you continue to a Revenue Intelligence Sprint, you receive a complete Proof Pack with at least the 14 sections and the computed score, inside seven days.

Reply with "proof" / "إثبات" to begin, or use the email in the company profile.

`#SaudiAI` `#RevenueOps`

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
