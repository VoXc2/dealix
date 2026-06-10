# مراجعة التكرار والصراع — DUPLICATION_AND_CONFLICT_REVIEW

> **تقرير المراجعة الموثّقة** للمحتوى المكرر والمتنازع بين الأنظمة الجديدة (29-33) والأنظمة القائمة (legacy) في Dealix. **القاعدة:** لا نحذف أي ملف، فقط نوصي بـ (merge / link / keep-separate).
>
> **آخر تحديث:** 2026-06-03
> **المالك:** Agent #35 — Final Integration
> **الإصدار:** v1.0
> **methodology:** cross-reference comparison + `Select-String` on shared keywords (governance, sales, ABM, AI, data, pricing).

---

## 1. ملخص تنفيذي

| المؤشر | القيمة |
|--------|--------|
| **عدد النتائج الموثّقة** | 12 |
| **حرجة (HIGH)** | 3 (يجب حلها قبل Launch) |
| **متوسطة (MEDIUM)** | 6 (يجب مراجعتها خلال Sprint 1) |
| **منخفضة (LOW)** | 3 (informational) |
| **توصية شاملة** | **LINK** معظمها، **MERGE** حالتين فقط، **KEEP-SEPARATE** 3 |

> **القاعدة العامة المطبقة:** في Dealix، **الإبقاء على التواريخ** (legacy) + **الإشارة المرجعية** (link) هو الخيار الأكثر أماناً. الحذف ممنوع إلا بعد موافقة المؤسس خطياً.

---

## 2. النتائج الموثّقة (12 finding)

### Finding 1 [HIGH] — Enterprise Sales OS vs Enterprise Rollout Playbook

- **المفهوم المكرر:** استراتيجية دخول المؤسسات إلى الحسابات الكبيرة.
- **الجديد:** [`docs/enterprise_sales/ENTERPRISE_SALES_OS_AR.md`](../../docs/enterprise_sales/ENTERPRISE_SALES_OS_AR.md) — Agent 29 — ABM, TAP, Stakeholders, MAP.
- **القائم:** [`docs/enterprise_rollout/ENTERPRISE_ROLLOUT_PLAYBOOK.md`](../../docs/enterprise_rollout/ENTERPRISE_ROLLOUT_PLAYBOOK.md) + [`docs/enterprise_rollout/ENTERPRISE_ENTRY_STRATEGY.md`](../../docs/enterprise_rollout/ENTERPRISE_ENTRY_STRATEGY.md) — يعتمد على motion داخل المؤسسة بعد البيع.
- **التوصية:** **LINK** (keep-separate) — الفرق: Sales OS = **ما قبل البيع** (ABM, MAP, Risk). Rollout = **ما بعد البيع** (دوران الفِرَق داخل المؤسسة). أضف في كل منهما cross-reference للآخر.

### Finding 2 [HIGH] — AI Governance OS vs governance/AI_ACTION_TAXONOMY

- **المفهوم المكرر:** مستويات استقلالية الوكلاء (A0-A5).
- **الجديد:** [`docs/ai_governance/AGENT_AUTONOMY_LEVELS_AR.md`](../../docs/ai_governance/AGENT_AUTONOMY_LEVELS_AR.md) — Agent 30.
- **القائم:** [`docs/governance/AI_ACTION_TAXONOMY.md`](../../docs/governance/AI_ACTION_TAXONOMY.md) + [`docs/governance/AI_ACTION_LEVELS.md`](../../docs/governance/AI_ACTION_LEVELS.md).
- **التوصية:** **LINK** — النظام الجديد أوسع (يضيف Lifecycle, Eval, Incident). الـ legacy يبقى مرجعاً للسياسات العليا. أضف ملاحظة في الـ legacy: "see also Agent 30 OS".

### Finding 3 [HIGH] — Data Products OS vs data_governance/DATA_GOVERNANCE_OS

- **المفهوم المكرر:** جودة البيانات وإدارة دورة حياتها.
- **الجديد:** [`docs/data_products/DATA_PRODUCTS_OS_AR.md`](../../docs/data_products/DATA_PRODUCTS_OS_AR.md) — Agent 31 — يستهلك البيانات + يحوّلها إلى منتجات.
- **القائم:** [`docs/data_governance/DATA_GOVERNANCE_OS_AR.md`](../../docs/data_governance/DATA_GOVERNANCE_OS_AR.md) — جودة، PII، retention، classification.
- **التوصية:** **LINK** (keep-separate) — الحدود واضحة: Data Governance = **حوكمة البيانات الخام** (ملكية، PII، retention). Data Products = **منتجات البيانات** (benchmarks, message library). كل نظام يستهلك مخرجات الآخر.

### Finding 4 [MEDIUM] — ACCOUNT_BASED_SELLING_AR.md (Agent 29) vs sales/PROOF_BASED_SALES.md

- **المفهوم المتقارب:** الـ ABM وبيع قائم على proof.
- **الجديد:** [`docs/enterprise_sales/ACCOUNT_BASED_SELLING_AR.md`](../../docs/enterprise_sales/ACCOUNT_BASED_SELLING_AR.md) — يركّز على **اختيار الحساب** (Tier-1/2/3 + scoring).
- **القائم:** [`docs/sales/PROOF_BASED_SALES.md`](../../docs/sales/PROOF_BASED_SALES.md) — يركّز على **كيف تبيع** (proof pack كمحور).
- **التوصية:** **LINK** — كلاهما يخدم ABM motion؛ يجب cross-link في كل منهما. لا يوجد تعارض حقيقي.

### Finding 5 [MEDIUM] — Offers System vs sales/OFFER_PAGES.md

- **المفهوم المكرر:** صفحات العروض.
- **الجديد:** [`docs/offers/OFFER_LANDING_PAGE_SYSTEM_AR.md`](../../docs/offers/OFFER_LANDING_PAGE_SYSTEM_AR.md) — Agent 33 — 6 صفحات كاملة + FAQ + CTA.
- **القائم:** [`docs/sales/OFFER_PAGES.md`](../../docs/sales/OFFER_PAGES.md) — قائمة صفحات + نسخة قديمة من sales-pages.
- **التوصية:** **LINK** — الجديد أوسع وأحدث. أضف في `sales/OFFER_PAGES.md` ملاحظة: "superseded by Agent 33 — see `docs/offers/`".

### Finding 6 [MEDIUM] — Offer CTA Library vs sales/SALES_MESSAGES.md

- **المفهوم المتقارب:** رسائل المبيعات.
- **الجديد:** [`docs/offers/OFFER_CTA_LIBRARY_AR.md`](../../docs/offers/OFFER_CTA_LIBRARY_AR.md) — CTAs مرتبطة بالعرض.
- **القائم:** [`docs/sales/SALES_MESSAGES.md`](../../docs/sales/SALES_MESSAGES.md) — رسائل عامة للمبيعات.
- **التوصية:** **LINK** — مكتبة CTAs للعرض ≠ رسائل المبيعات العامة. أضف في كل منهما cross-reference.

### Finding 7 [MEDIUM] — Data Products: sector_benchmarks vs sales/sector_playbooks.md

- **المفهوم المتقارب:** معايير القطاع.
- **الجديد:** [`docs/data_products/SECTOR_BENCHMARKS_AR.md`](../../docs/data_products/SECTOR_BENCHMARKS_AR.md) — JSONL (8 قطاعات) + evidence_level.
- **القائم:** [`docs/ops/sector_playbooks.md`](../../docs/ops/sector_playbooks.md) — نصوص + أمثلة.
- **التوصية:** **LINK** — الـ OS الجديد أرقام منظمة، الـ legacy نصوص. يجب أن يستهلك sector_playbooks الـ benchmarks.

### Finding 8 [MEDIUM] — AGENT_PERMISSION_LIFECYCLE_AR.md vs governance/PERMISSION_MIRRORING.md

- **المفهوم المتقارب:** دورة حياة الصلاحيات.
- **الجديد:** [`docs/ai_governance/AGENT_PERMISSION_LIFECYCLE_AR.md`](../../docs/ai_governance/AGENT_PERMISSION_LIFECYCLE_AR.md).
- **القائم:** [`docs/governance/PERMISSION_MIRRORING.md`](../../docs/governance/PERMISSION_MIRRORING.md).
- **التوصية:** **LINK** — Lifecycle = جانب زمني (onboard→eval→retire). Mirroring = جانب المرآة (prod vs test). أضف cross-reference.

### Finding 9 [MEDIUM] — EXECUTIVE_BUSINESS_CASE_AR.md vs commercial/ROI_CONVERSATION_GUIDE_AR.md

- **المفهوم المتقارب:** كيف تبني business case للعميل المؤسسي.
- **الجديد:** [`docs/enterprise_sales/EXECUTIVE_BUSINESS_CASE_AR.md`](../../docs/enterprise_sales/EXECUTIVE_BUSINESS_CASE_AR.md) — template + worked example.
- **القائم:** [`docs/commercial/ROI_CONVERSATION_GUIDE_AR.md`](../../docs/commercial/ROI_CONVERSATION_GUIDE_AR.md) — guide للمحادثة.
- **التوصية:** **MERGE (link-only)** — الـ Business Case هو **الناتج**، ROI guide هو **العملية**. أبقهما منفصلين، أضف cross-link.

### Finding 10 [LOW] — PROCUREMENT_SALES_PLAYBOOK_AR.md vs commercial/MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md

- **المفهوم المتقارب:** Procurement في المؤسسات.
- **الجديد:** [`docs/enterprise_sales/PROCUREMENT_SALES_PLAYBOOK_AR.md`](../../docs/enterprise_sales/PROCUREMENT_SALES_PLAYBOOK_AR.md) — playbook + RFP/RFI/RFQ.
- **القائم:** [`docs/commercial/MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md`](../../docs/commercial/MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md) — FAQ للعميل.
- **التوصية:** **LINK** (keep-separate) — playbook = للمبيعات. FAQ = للعميل. لا تعارض.

### Finding 11 [LOW] — AGENT_EVAL_CADENCE_AR.md vs quality/AI_OUTPUT_EVALS.md

- **المفهوم المتقارب:** تقييم مخرجات AI.
- **الجديد:** [`docs/ai_governance/AGENT_EVAL_CADENCE_AR.md`](../../docs/ai_governance/AGENT_EVAL_CADENCE_AR.md) — cadence للوكلاء.
- **القائم:** [`docs/quality/AI_OUTPUT_EVALS.md`](../../docs/quality/AI_OUTPUT_EVALS.md) — quality evals.
- **التوصية:** **LINK** — cadence = متى نقيم. evals = ماذا نقيم. أضف cross-reference في كل منهما.

### Finding 12 [LOW] — data/data_products/*.jsonl vs data/commercial/*.yaml

- **المفهوم المتقارب:** بيانات المبيعات والتسعير.
- **الجديد:** JSONL (structured, per-row evidence_level).
- **القائم:** YAML (catalog, ICP, pricing_rules).
- **التوصية:** **KEEP-SEPARATE** — YAML catalog = تعريفات ثابتة. JSONL = observations. يستهلك Data Products YAML catalog لتوليد observations.

---

## 3. صراع التسمية (Naming Conflicts)

| الصراع | المرشحان | التوصية |
|-------|---------|---------|
| `docs/enterprise/` vs `docs/enterprise_sales/` vs `docs/enterprise_rollout/` vs `docs/enterprise_architecture/` vs `docs/enterprise_trust/` | enterprise = **readiness** (legacy). enterprise_sales = **ABM motion** (new). enterprise_rollout = **post-sale rollout** (legacy). enterprise_architecture = **system map** (legacy). enterprise_trust = **trust pack** (legacy). | **KEEP-AS-IS** — التمييز بالـ suffix كافٍ، وأي rename الآن سيكسر آلاف cross-references. **عدم التغيير** موثّق هنا. |
| `docs/ai_governance/` vs `docs/governance/` vs `docs/responsible_ai/` vs `docs/security/` | ai_governance = **agent-specific** (new). governance = **governance decision & A0-A5** (legacy). responsible_ai = **ethical/standard AI** (legacy). security = **security & prompt injection** (legacy). | **KEEP-AS-IS** — مع cross-link فقط. كل نظام له بُعد مختلف. |
| `data/commercial/pricing_rules.yaml` vs `data/data_products/pricing_sensitivity.jsonl` | YAML = rules ثابتة. JSONL = observations. | **KEEP-AS-IS** — يكملان بعضهما. |

---

## 4. صلات الـ schemas (Schema Overlaps)

| الـ schema | الاستخدام | متى تستخدم |
|-----------|-----------|-----------|
| `enterprise_account.schema.json` (Agent 29) | حساب مؤسسي كامل | عند إضافة حساب جديد |
| `opportunity.schema.json` (legacy) | فرصة تجارية | عند إضافة opportunity |
| `partner_opportunity.schema.json` (legacy) | فرصة شريك | عند وجود شريك |
| `product_offer.schema.json` (Agent 33) | عرض جاهز | عند نشر عرض |
| `productized_service.schema.json` (legacy) | خدمة مُنتَجَة | في services/ folder |

> **لا تعارض** — كل schema له use case مختلف. **لا MERGE.**

---

## 5. التقارير اليتيمة (Orphan Reports)

تقرير "يتيم" = تقرير لا يرجع إليه أي وثيقة جديدة أو قديمة في repo.

| التقرير | الحالة | التوصية |
|---------|--------|---------|
| `reports/agent_2/AGENT_2_CONTINUATION_AUDIT.md` | يتيم (Agent 2 legacy) | **KEEP** — استخدمه كأساس للـ continuation audits |
| `reports/company_os/control/latest_tick.json` | data file (تقرير JSON) | **KEEP** — operating control tick |
| `reports/company_os/daily/CEO_BRAIN_TODAY.md` | يتيم | **KEEP** — يولّد يومياً، cross-link من FOUNDER_DAILY_ANCHOR |
| `reports/business_os/AGENT_2_CONTINUATION_AUDIT.md` | يتيم (مكرر) | **LINK** — مكرر من agent_2/ — يجب إزالة النسخة الأقدم |

> **إجراء:** لم نعثر على orphan reports في الـ wave الجديدة (29-33) — كل تقرير يُستشهد به في الـ final report لنظامه.

---

## 6. ملخص التوصيات

| الإجراء | العدد | متى |
|---------|-------|-----|
| **MERGE** (دمج) | 0 | — (لا دمج فعلي، فقط links) |
| **LINK** (إضافة cross-reference) | 9 | خلال Sprint 1 (week 1-2) |
| **KEEP-SEPARATE** (إبقاء مع تمييز) | 3 | مستمر |
| **RENAME** (تغيير اسم) | 0 | محظور (يكسر cross-references) |
| **DELETE** (حذف) | 0 | محظور (قاعدة HARD CONSTRAINT) |

---

## 7. الخطوات التالية

1. **Sprint 1 (NOW):** أضف cross-references في الـ 9 ملفات legacy المذكورة أعلاه.
2. **Sprint 2 (NEXT):** أضف cross-references في الـ 3 ملفات "keep-separate".
3. **Quarterly:** راجع هذا التقرير — هل ظهرت duplicates جديدة؟
4. **Owner:** Sales Lead (Enterprise Sales links) + AI Governance Lead (Governance links) + Data Lead (Data Products links) + Marketing (Offers links).

---

## Open Questions for Founder

1. هل توافق على **عدم الـ merge** (الإبقاء على 12 finding كـ links فقط)؟ — هذا يوفّر سلامة cross-references.
2. هل نطلب من **Sales Lead** + **AI Governance Lead** + **Data Lead** + **Marketing** تأكيد cross-references خلال Sprint 1، أم تتولاها أنت شخصياً؟
3. هل تريد **دورياً** (كل 3 أشهر) Agent 35-style integration review، أم مرة واحدة فقط؟
