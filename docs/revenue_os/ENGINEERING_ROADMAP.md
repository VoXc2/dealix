# ENGINEERING ROADMAP — Revenue OS / خطة الكود المرحلية

> هذه خطة. لا كود يُكتب في هذه الوثيقة. كل مرحلة = مهمة لاحقة مستقلة، صغيرة،
> مختبرة، ومتوافقة مع الـ 11 non-negotiables.
>
> This is a plan. No code is written here. Each phase = a separate follow-up
> task — small, tested, and compliant with the 11 non-negotiables.

## العربية

### المبدأ الحاكم

معظم خلفية الـ Revenue OS **مبنية أصلاً**. الوحدات التسعة الكنسية موجودة
(`data_os` ... `sales_os`)، مع registry بسبعة عروض، lead scoring حتمي،
مصفوفة موافقات، وطبقة دوكترين تفرضها 399 اختباراً. لذا هذه الخطة تسدّ
**الفجوات الحقيقية فقط** — لا تعيد بناء ما هو موجود.

> ⚠️ **قاعدة No-build:** لا تُبنى مرحلة إلا إذا تكرر workflow، أو طلبه عميل،
> أو سرّع تسليماً مدفوعاً، أو فتح retainer، أو قلّل خطراً حقيقياً.

### المراحل

| المرحلة | الفجوة | الملفات المستهدفة | المالك | الاختبارات |
|---|---|---|---|---|
| **1 — CRM fields & evidence events** | حقول lead الموسّعة + تصنيف المصادر + حدث `lead_captured` | `crm_v10/schemas.py`، `data_os/` | dealix-engineer | إنشاء lead يولّد كل الحقول + حدث إثبات واحد |
| **2 — A/B/C/D qualification** | نموذج النقاط + التصنيف فوق `lead_scoring.py` (حتمي) | `sales_os/lead_tiering.py` (جديد) | dealix-engineer | نفس المدخل ⇒ نفس الفئة دائماً؛ لا LLM لا عشوائية |
| **3 — `/dealix-diagnostic` + risk-score funnel** | landing page + نموذج Risk Score + Proof Pack مُبوَّب | `frontend/src/app/[locale]/dealix-diagnostic/` (جديد)، intake endpoint | dealix-engineer | الصفحة تُصيّر؛ النموذج يرسل consent؛ النتيجة Low/Med/High |
| **4 — CEO dashboard view** | لوحة Today/Funnel/Quality/Revenue/Learning | `frontend/.../[locale]/revenue-os/` (جديد)، snapshot endpoint | dealix-engineer | الـ snapshot يرجّع مقاييس الـ funnel السبعة |
| **5 — 18-automation orchestration** | تنسيق الأتمتات الـ 18، كل فعل خارجي مسودة + بوابة | منسّق `revenue_os` جديد + `governance_os` | dealix-engineer | كل أتمتة موسومة tier؛ لا فعل خارجي يتجاوز الموافقة |
| **6 — Expansion engine** | upsell recommendation + referral ledger + delivery-to-content hooks | `adoption_os/`، `client_os/`، `proof_os/` | dealix-engineer + dealix-content | توصية upsell تتبع قواعد الطبقة 7 |

### قيود ثابتة لكل مرحلة

- `lead_scoring` و `lead_tiering` يبقيان **حتميين** — لا LLM، لا عشوائية.
- كل إرسال خارجي **مسودة + موافقة** — `no_live_send`.
- كل أتمتة تمرّ بـ `governance_os` — `no_unbounded_agents`.
- لا تغيير تسعير — أي عمل تسعيري يتبع `PRICING_PROPOSAL_diagnostic_tiers.md`.
- كل مرحلة تضيف اختبارات؛ لا تكسر `tests/test_doctrine_guardrails.py`.

---

## English

### The governing principle

Most of the Revenue OS backend is **already built**. All nine canonical modules
exist (`data_os` … `sales_os`), with a 7-offer registry, deterministic lead
scoring, an approval matrix, and a doctrine layer enforced by 399 tests. So this
plan closes **only the genuine gaps** — it does not rebuild what exists.

> ⚠️ **No-build rule:** a phase is built only if a workflow repeated, a customer
> asked for it, it speeds a paid delivery, it opens a retainer, or it reduces a
> real risk.

### The phases

| Phase | Gap | Target files | Owner | Tests |
|---|---|---|---|---|
| **1 — CRM fields & evidence events** | Expanded lead fields + source taxonomy + `lead_captured` event | `crm_v10/schemas.py`, `data_os/` | dealix-engineer | Creating a lead populates all fields + emits one evidence event |
| **2 — A/B/C/D qualification** | Points model + tiering on top of `lead_scoring.py` (deterministic) | `sales_os/lead_tiering.py` (new) | dealix-engineer | Same input ⇒ same tier always; no LLM, no randomness |
| **3 — `/dealix-diagnostic` + risk-score funnel** | Landing page + Risk Score form + gated Proof Pack | `frontend/src/app/[locale]/dealix-diagnostic/` (new), intake endpoint | dealix-engineer | Page renders; form submits consent; result is Low/Med/High |
| **4 — CEO dashboard view** | Today/Funnel/Quality/Revenue/Learning panels | `frontend/.../[locale]/revenue-os/` (new), snapshot endpoint | dealix-engineer | Snapshot returns the 7 funnel metrics |
| **5 — 18-automation orchestration** | Orchestrate the 18 automations, every external action draft + gate | new `revenue_os` orchestrator + `governance_os` | dealix-engineer | Each automation tagged with a tier; no external action bypasses approval |
| **6 — Expansion engine** | Upsell recommendation + referral ledger + delivery-to-content hooks | `adoption_os/`, `client_os/`, `proof_os/` | dealix-engineer + dealix-content | Upsell recommendation follows Layer 7 rules |

### Fixed constraints for every phase

- `lead_scoring` and `lead_tiering` stay **deterministic** — no LLM, no randomness.
- Every external send is a **draft + approval** — `no_live_send`.
- Every automation routes through `governance_os` — `no_unbounded_agents`.
- No pricing change — any pricing work follows `PRICING_PROPOSAL_diagnostic_tiers.md`.
- Every phase adds tests; do not break `tests/test_doctrine_guardrails.py`.

### Suggested sequencing

Phases 1 → 2 are the foundation (data + qualification). Phase 3 unlocks demand
capture. Phase 4 gives the founder visibility. Phase 5 is the largest and should
only start once Phases 1–4 are in use. Phase 6 follows the first delivered
proof pack. Each phase ships, is reviewed, and is used before the next begins.
