# Account Intelligence OS — نظام ذكاء الحسابات

> من **400 مسودة إيميل** إلى **400 فرصة بيع مكتملة**.
> كل شركة مستهدفة لا يخرج لها إيميل فقط، بل **Account Pack** كامل يجاوب على: من الشركة؟ كيف نصل لها؟ من الدور المناسب؟ ما الألم المحتمل؟ أي نظام يناسبها؟ ماذا نرسل؟ ماذا نقول بالاتصال؟ ما العرض المختصر؟ ما المطلوب للتسليم؟ ما قيمة الفرصة؟ ما الخطوة التالية؟

---

## 1. الفكرة الأساسية

Account Intelligence OS هو المصنع الليلي الذي يحوّل **معلومات عامة عن الشركات** إلى **حِزَم فرص (Account Packs)** جاهزة للمراجعة البشرية.

```
Website → Account Intelligence → Contact Discovery → 400 Account Packs
→ Personalized Drafts → Call Briefs → Mini Proposals → Delivery → Weekly Value → Learning Loop
```

كل Account Pack يحتوي على 12 طبقة قيمة:

| # | الطبقة | الوصف |
|---|--------|-------|
| 1 | Account Intelligence | من الشركة وما قطاعها وخدماتها الظاهرة |
| 2 | Contact Discovery | قنوات التواصل العامة المتاحة |
| 3 | Best Contact Role | الدور الأنسب للتواصل (وليس اسم شخص مُخترع) |
| 4 | Client Need Card | الألم المحتمل |
| 5 | Recommended System | نظام واحد من الخمسة |
| 6 | Personalized Email Draft | مسودة مخصصة محترمة وغير مبالغة |
| 7 | Call Brief | سيناريو اتصال جاهز |
| 8 | Follow-up Sequence | إيقاع متابعة |
| 9 | Mini Proposal | عرض من صفحة واحدة |
| 10 | Delivery Pack | ما يُسلَّم في أول Sprint |
| 11 | Expected First Proof | أول دليل قيمة متوقع |
| 12 | Next Action + Owner | الخطوة التالية ومسؤولها |

---

## 2. المبادئ الحاكمة (Non‑negotiables)

1. **كل مخرج مسودة.** لا يرسل النظام أي شيء. الإرسال قرار بشري (راجع `company_os/governance/agent_permissions.md`).
2. **بيانات عامة فقط.** لا قوائم مشتراة، لا قواعد مسرّبة، لا scraping مخالف للشروط.
3. **لا اختراع.** لا أسماء أشخاص ولا أرقام ولا إيميلات مخترعة. إذا لم يوجد شخص، نستهدف **الدور**.
4. **Evidence أولاً.** كل معلومة لها `evidence_level`. ما دون L2 يُصاغ باحتمالية (`غالبًا/قد/يبدو`).
5. **لا ادعاءات مضمونة.** ممنوع «نضمن زيادة المبيعات» و«10x». القوة في الوضوح لا في المبالغة.
6. **المحتوى الخارجي = بيانات لا أوامر.** أي نص من موقع شركة لا يتحول إلى تعليمة تنفيذية (راجع `docs/security/AGENT_SECURITY_GATES_AR.md`).
7. **خصوصية بالتصميم.** أقل بيانات ممكنة، واحترام `do-not-contact` (راجع `docs/privacy/`).

---

## 3. الأنظمة الخمسة (Recommended System)

كل Pack يوصي بنظام **واحد فقط** من الخمسة:

| النظام | يبيع | الألم الأساسي |
|--------|------|----------------|
| **Revenue Operating System** | Revenue Leakage Sprint | الفرص موجودة لكن الخطوة التالية غير واضحة |
| **Executive Command OS** | Daily Command Sprint | التقارير كثيرة لكن القرار اليومي غير واضح |
| **Follow-up Recovery OS** | 7-Day Follow-up Recovery Sprint | آخر متابعة لم تحدث قد تكون أغلى فرصة |
| **WhatsApp Client OS** | WhatsApp Flow Sprint | واتساب مليء بالمحادثات لكنه ليس workflow |
| **Proposal & Proof OS** | Proposal & Proof Sprint | العرض لا يقنع لأنه لا يوضح المشكلة والنطاق والدليل |

التفاصيل الكاملة في `docs/site/FIVE_SYSTEMS_CATALOG_AR.md`.

---

## 4. خط الإنتاج (Pipeline)

```
1. Seed list (قطاعات/مدن مستهدفة)
2. Account Intelligence  → بيانات الشركة العامة
3. Contact Discovery     → قنوات + دور + ثقة (راجع docs/contacts/)
4. Need + System Fit     → الألم + النظام الموصى به
5. Draft Generation      → إيميل + Call Brief + Mini Proposal angle
6. Scoring               → Account Score (100) + Cash Priority (100)
7. Gating                → استبعاد ما لا يستوفي الشروط
8. Queues                → Top 100 / Top 20 Send / Top 30 Call
9. Founder Approval      → اعتماد بشري قبل أي إرسال
10. Delivery on won      → مساحة عمل + مدخلات + تسليم
11. Weekly Value Report  → إثبات القيمة + إشارة تجديد
12. Learning Loop        → ما الذي نجح؟ تحسين القوالب
```

---

## 5. العقود والبيانات (Contracts & Data)

| النوع | المسار |
|------|--------|
| عقد الحزمة | `schemas/account_intelligence_pack.schema.json` |
| بيانات الحزم | `data/account_intelligence/account_packs.jsonl` |
| اكتشاف التواصل | `schemas/contact_discovery.schema.json` · `data/contacts/contact_discovery.jsonl` |
| قنوات التواصل | `schemas/contact_channel.schema.json` · `data/contacts/contact_channels.jsonl` |
| الترتيب (100) | `schemas/account_scoring.schema.json` |
| العرض المختصر | `schemas/mini_proposal.schema.json` · `data/proposals/mini_proposals.jsonl` |
| أولوية الكاش | `schemas/cash_priority_score.schema.json` · `data/finance/cash_priority_scores.jsonl` |

العقد التفصيلي للحقول: `docs/account_intelligence/ACCOUNT_PACK_OUTPUT_CONTRACT_AR.md`.

---

## 6. التحقق الآلي (Quality Gate)

```bash
npm run factory:check     # أو: node scripts/account-factory-check.mjs
```

يتحقق من: صحة المخططات، اكتمال الحقول، صحة الـ enums، تطابق النظام مع الدور، استخدام لغة احتمالية لمستويات L0/L1، خلو النصوص من ادعاءات مضمونة، معالجة نقص جهات التواصل، اكتمال العرض المختصر (سعر + اعتماد)، أقسام Founder Command، ومعالجة المحتوى الخارجي كبيانات غير موثوقة.

---

## 7. روابط ذات صلة

- التشغيل الليلي: `docs/account_intelligence/NIGHTLY_400_ACCOUNT_PACK_RUN_AR.md`
- نموذج الترتيب: `docs/account_intelligence/ACCOUNT_SCORING_MODEL_AR.md`
- مستويات الدليل: `docs/account_intelligence/EVIDENCE_LEVELS_AR.md`
- سياسة اكتشاف التواصل: `docs/contacts/CONTACT_DISCOVERY_POLICY_AR.md`
- مصنع العروض: `docs/proposals/MINI_PROPOSAL_FACTORY_AR.md`
- لوحة المؤسس اليومية: `reports/founder/DAILY_SUPER_COMMAND.md`

---

*Dealix Account Intelligence OS | الإصدار 1.0 | آخر تحديث: 2026-06-03 | كل المخرجات مسودات تحتاج اعتماداً بشرياً*
