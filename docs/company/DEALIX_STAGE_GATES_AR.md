# Dealix Stage Gates — بوابات جاهزية (بدل خطة 90 يوم)

**الفكرة:** لا تعتمد على الإحساس. اعتمد على **بوابات جاهزية** + **أدلة** في الريبو — [`EVIDENCE_SYSTEM.md`](EVIDENCE_SYSTEM.md).

**التحقق الآلي:** [`scripts/verify_dealix_ready.py`](../../scripts/verify_dealix_ready.py) — Gate 1 يتطلب **readiness ≥ 85** لكل من الخدمات الثلاث الأولى + حزم `demos/` كاملة لـGate 5.  
**لوحة القيادة اليدوية:** [`DEALIX_READINESS.md`](../../DEALIX_READINESS.md).

**السياق السوقي:** [Saudi Gazette](https://www.saudigazette.com.sa/article/658036) — [McKinsey State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/) — [Gartner AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

---

## خريطة البوابات

| Gate | الاسم | الغرض |
|------|--------|--------|
| 0 | Founder Clarity | ماذا تبني ولمن |
| 1 | Offer Readiness | خدمات قابلة للبيع |
| 2 | Delivery Readiness | تسليم بدون ارتجال |
| 3 | Product Readiness | المنتج يساعد التسليم (MVP) |
| 4 | Governance Readiness | حماية وثقة |
| 5 | Demo Readiness | إقناع قبل الشراء |
| 6 | Sales Readiness | إغلاق واعتراضات |
| 7 | Client Delivery Readiness | onboarding بعد الدفع |
| 8 | Retainer Readiness | دخل متكرر |
| 9 | Scale Readiness | لا يعتمد الكل على شخص واحد |
| 10 | World-Class Readiness | معيار الطموح |

---

## Gate 0 — Founder Clarity

**ملفات إلزامية:**

- `docs/company/POSITIONING.md`
- `docs/company/MISSION_VISION.md`
- `docs/company/OPERATING_PRINCIPLES.md`
- `docs/company/ICP.md`
- `docs/company/NORTH_STAR_METRICS.md`

**Pass:** تشرح Dealix في ~20 ثانية؛ تعرف من تخدم ومن لا تخدم؛ North Star واضح — [`NORTH_STAR_METRICS.md`](NORTH_STAR_METRICS.md).

### Gate 0 Score (يدوي)

| معيار | نقاط |
|--------|-----:|
| التموضع واضح | 20 |
| ICP واضح | 20 |
| من لا نخدم واضح | 15 |
| الخدمات الأولى واضحة | 20 |
| North Star واضح | 15 |
| المبادئ غير القابلة للكسر | 10 |
| **المجموع** | **100** |

**Pass = 85/100** (يدوياً في `DEALIX_READINESS.md`؛ آليًا: وجود الملفات الخمسة).

---

## Gate 1 — Offer Readiness

**الخدمات الثلاث الأولى:** Lead Intelligence Sprint، AI Quick Win Sprint، Company Brain Sprint.

**لكل خدمة:** مجلد `docs/services/<folder>/` مع `offer.md` (الأقسام السبعة)، `scope.md`، `intake.md`، طلب بيانات، `delivery_checklist.md`، `qa_checklist.md`، `report_template.md`، `proof_pack_template.md`، `sample_output.md`، `upsell.md`.

**Offer score (جدول يدوي + آلي):**

| معيار | نقاط |
|--------|-----:|
| المشكلة واضحة | 10 |
| الوعد | 15 |
| السعر | 10 |
| المدة | 10 |
| المخرجات | 20 |
| ما لا يشمله العرض | 10 |
| KPI | 10 |
| Upsell | 15 |

**Pass = 85/100.** آليًا: [`service_readiness`](../../auto_client_acquisition/delivery_os/service_readiness.py) **≥ 85** لكل من `lead_intelligence_sprint` و`quick_win_ops` و`company_brain_sprint` + [`verify_service_files.py`](../../scripts/verify_service_files.py). **اختبارات القبول:** [`../quality/acceptance/`](../quality/acceptance/).

### Hard Fail (ممنوع البيع)

- لا سعر / لا نطاق / لا مخرجات / لا «غير مشمول»
- وعد مبيعات مضمون
- إرسال تلقائي أو scraping غير محكوم

**خدمة رسمية:** Offer + Delivery + Governance + Demo + Sales + Proof جاهزون، والنتيجة ≥ 85. **Beta:** بين 70 و 84 بدون hard fail. **غير جاهز:** أقل من 70 أو أي hard fail.

---

## Gate 2 — Delivery Readiness

**ملفات إلزامية (Gate 2):**

- `docs/delivery/DELIVERY_STANDARD.md`
- `docs/delivery/DELIVERY_LIFECYCLE.md`
- `docs/delivery/CLIENT_ONBOARDING.md`
- `docs/delivery/SCOPE_CONTROL.md`
- `docs/delivery/HANDOFF_PROCESS.md`
- `docs/delivery/RENEWAL_PROCESS.md`

**موصى به أيضاً:** [`CHANGE_REQUEST_PROCESS.md`](../delivery/CHANGE_REQUEST_PROCESS.md) لسيطرة النطاق.

**دورة التسليم:** Discovery → Scope → Data/files → Build → Internal QA → Client preview → Final report → Proof pack → Next-step proposal.

### Gate 2 Score (يدوي)

| معيار | نقاط |
|--------|-----:|
| onboarding | 15 |
| data request | 15 |
| timeline | 15 |
| checklist لكل خدمة | 20 |
| handoff | 15 |
| change request | 10 |
| renewal | 10 |

**Pass = 85/100.**

---

## Gate 3 — Product Readiness (MVP)

**حزم كحد أدنى:** `data_os`، `revenue_os`، `knowledge_os`، `governance_os`، `reporting_os`، `delivery_os` — وجود كود تشغيلي (آلي في `verify_dealix_ready.py`).

### Gate 3 Score (يدوي — حد أدنى MVP)

| Module | نقاط |
|--------|-----:|
| Data OS | 20 |
| Revenue OS | 15 |
| Knowledge OS MVP | 15 |
| Governance OS | 20 |
| Reporting OS | 15 |
| Delivery OS | 15 |

**Pass = 80/100** (MVP). المتطلبات الوظيفية: import/quality/PII؛ scoring/drafts؛ citations/no-source؛ forbidden/approval/audit؛ report+proof؛ readiness/QA — تفصيل في [`MODULE_MAP.md`](../product/MODULE_MAP.md).

---

## Gate 4 — Governance Readiness

**ملفات:** [`verify_governance_rules.py`](../../scripts/verify_governance_rules.py).

### Gate 4 Score (يدوي — عتبة أعلى)

| معيار | نقاط |
|--------|-----:|
| forbidden actions | 20 |
| approval matrix | 20 |
| PII policy | 15 |
| audit log policy | 15 |
| source attribution | 15 |
| compliance QA في كل خدمة | 15 |

**Pass = 90/100** — الحوكمة لا تقبل الضعف. سياق بيانات وAI: [Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

**ممنوعات افتراضية:** لا scraping بلا إذن، لا cold WhatsApp، لا أتمتة LinkedIn، لا proof مزيف، لا ادعاءات مبيعات مضمونة، لا PII في السجلات، لا إجراء خارجي بلا موافقة.

---

## Gate 5 — Demo Readiness

**المجلدات الإلزامية (آلياً):**

- [`demos/lead_intelligence_demo/`](../../demos/lead_intelligence_demo/) — `demo.csv`، معاينة، جودة، scoring، top 50/10، drafts، CRM، تقرير، proof.
- [`demos/ai_quick_win_demo/`](../../demos/ai_quick_win_demo/) — process، before/after، workflow، approval، time saved، SOP، proof.
- [`demos/company_brain_demo/`](../../demos/company_brain_demo/) — `sample_docs/`، جرد، Q&A، citations، no-source، eval، proof.

**وثائق التحقق:** [`docs/delivery/DEMO_READINESS.md`](../delivery/DEMO_READINESS.md) + [`docs/sales/DEMO_SCRIPT.md`](../sales/DEMO_SCRIPT.md).

### Gate 5 Score (يدوي)

| معيار | نقاط |
|--------|-----:|
| يوضح المشكلة | 15 |
| before/after | 15 |
| مخرجات حقيقية | 25 |
| proof pack | 20 |
| next step | 10 |
| شكل احترافي | 15 |

**Pass = 85/100.**

---

## Gate 6 — Sales Readiness

**ملفات:** تحت `docs/sales/` — Playbook، Discovery، Offer pages، Objections، Proposal، Follow-up.

### Gate 6 Score (يدوي)

| معيار | نقاط |
|--------|-----:|
| pitch | 15 |
| discovery script | 15 |
| proposal template | 15 |
| objection handling | 15 |
| follow-up | 15 |
| sample report للإرسال | 25 |

**Pass = 85/100.** عينات التقارير: `docs/services/*/sample_output.md`.

---

## Gate 7 — Client Delivery Readiness

**حزمة:** [`docs/delivery/client_onboarding/`](../delivery/client_onboarding/) — ترحيب، بيانات، timeline، أدوار، جدول مراجعة، موافقات.

**مثال زمني (10 أيام عمل):** يوم 1 intake → 2 import preview → 3–4 جودة + dedupe/scoring → 5 drafts/workflow/knowledge → 6 QA داخلي → 7 معاينة عميل → 8 تقرير نهائي → 9 Proof Pack → 10 مراجعة + next step.

**Pass:** رسالة ترحيب، data request، timeline، أدوار، approvals، review agenda — كلها موجودة كملفات.

---

## Gate 8 — Retainer Readiness

بعد Sprint ناجح + Proof Pack + قيمة واضحة — قالب ومعايير: [`docs/delivery/RETAINER_READINESS.md`](../delivery/RETAINER_READINESS.md).

### Gate 8 Score (يدوي)

| معيار | نقاط |
|--------|-----:|
| monthly scope | 20 |
| monthly report template | 20 |
| backlog | 15 |
| client health | 15 |
| renewal process | 15 |
| expansion map | 15 |

**Pass = 85/100.**

---

## Gate 9 — Scale Readiness

### Gate 9 Score (يدوي)

| معيار | نقاط |
|--------|-----:|
| شخص آخر يسلم بنفس النظام | 25 |
| templates كاملة | 20 |
| reports شبه مؤتمتة | 15 |
| QA ثابت | 15 |
| proof packs موحدة | 15 |
| features من التكرار | 10 |

**Pass = 85/100.** قائمة تحقق في [`DEALIX_READINESS.md`](../../DEALIX_READINESS.md).

---

## Gate 10 — World-Class

**متطلبات تشغيلية:** 10+ مشاريع مدفوعة، 3+ retainers، proof packs قوية، case studies، playbooks، QA متوسط 90+، zero PII incidents، 95% on-time، client workspace MVP، Dealix Method مستخدمة — انظر [`WORLD_CLASS_READINESS_AR.md`](WORLD_CLASS_READINESS_AR.md) و[`DEALIX_AI_OS_LONG_TERM_AR.md`](DEALIX_AI_OS_LONG_TERM_AR.md).

### Gate 10 — مؤشرات عالمية (هدف)

| معيار | هدف |
|--------|-----:|
| QA average | 90+ |
| on-time delivery | 95% |
| PII incidents | 0 |
| proof pack coverage | 100% |
| sprint to retainer | 40%+ |
| client satisfaction | 9/10+ |
| source coverage (Brain) | 95%+ |

---

## متى تبدأ البيع؟ (قرار تنفيذي)

ابدأ البيع عندما تمر:

**Gate 0، 1، 2، 4، 5، 6** (جميعها Pass).

**Gate 3** يكفي **MVP** يدعم التسليم (لا تنتظر منصة كاملة).

**Gate 7** قبل أو مع أول عميل مدفوع (onboarding).

**القاعدة:** لا تُبِع إلا خدمة عبرت **Offer + Delivery + Governance + Demo + Sales**؛ الحوكمة والـQA وProof Pack غير قابلة للتجاوز — [`QUALITY_STANDARD.md`](../quality/QUALITY_STANDARD.md).

---

## الحكم على «أفضل تنفيذ»

| التقييم | معنى |
|---------|------|
| ممتاز | score فوق 90، demo قوي، checklists كاملة، proof pack، عميل يفهم القيمة بسرعة |
| جيد | 80–89، قابل للبيع مع تحسين بعد أول عميل |
| غير جاهز | أقل من 80 — **لا بيع رسمي** |
| ممنوع | بلا QA / scope / proof / حوكمة، أو وعود مضمونة، أو إرسال تلقائي بلا موافقة |
