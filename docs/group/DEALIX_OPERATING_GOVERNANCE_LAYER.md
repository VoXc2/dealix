# Dealix — طبقة التشغيل الحوكمي + تخصيص رأس المال + مصنع المشاريع + مقاييس التنفيذ

**الفرق بين «فكرة قوية» و«شركة تبني تاريخًا»:** منظومة لا تنهار مع التوسع — **Capability Factory** داخل **AI Operations Holding**.

**ملفات مرتبطة:** [`../institutional/README.md`](../institutional/README.md) — **التصميم المؤسسي (10x–100x)** · [`SUCCESS_ASSURANCE_SYSTEM.md`](SUCCESS_ASSURANCE_SYSTEM.md) · [`CAPITAL_ALLOCATION_MODEL.md`](CAPITAL_ALLOCATION_MODEL.md) · [`PORTFOLIO_SCORECARD.md`](PORTFOLIO_SCORECARD.md) · [`BUSINESS_UNIT_MODEL.md`](BUSINESS_UNIT_MODEL.md) · [`VENTURE_GRADUATION_GATE.md`](VENTURE_GRADUATION_GATE.md) · [`../company/CEO_OPERATING_SYSTEM.md`](../company/CEO_OPERATING_SYSTEM.md) · [`../company/SERVICE_READINESS_GATE.md`](../company/SERVICE_READINESS_GATE.md) · [`../company/AI_CAPABILITY_FACTORY.md`](../company/AI_CAPABILITY_FACTORY.md)

---

## 1. Dealix = Capability Factory (مصنع قدرات)

**مدخلات خام من مشكلة العميل:** بيانات مبعثرة، عمل يدوي، معرفة متفرقة، مبيعات ضعيفة، دعم غير منظم، مخاطر AI.

**مخرجات:** Revenue / Support / Knowledge / Workflow / Governance / Reporting **capability** — ثم **يبقى الأصل داخل القابضة**.

```text
Client Problem → Capability Built → Proof Created → Asset Captured → Module Improved
→ Playbook Updated → Retainer Offered → Venture Signal Detected
```

هذه **آلة Dealix**.

---

## 2. Capability Factory Loop (التسلسل التشغيلي)

| # | مرحلة | مخرجات أساسية |
|---|--------|----------------|
| 1 | **Diagnose** | Diagnostic Report · Capability Level · Data Readiness · Governance Risk · Best Starting Offer |
| 2 | **Scope** | SOW · Success Metrics · Client Inputs · Exclusions · Approval Rules |
| 3 | **Build** | workflow / draft pack / dashboard / assistant / pipeline board |
| 4 | **Govern** | Governance Decision · Risk · Approval Requirement · Audit Event |
| 5 | **Prove** | Proof Pack · Value Metrics · Before/After · Evidence · Next Recommendation |
| 6 | **Operate** | Retainer Cadence · Monthly Report · Health Score · Capability Backlog |
| 7 | **Compound** | Capital Asset · Playbook Update · Template · Feature Candidate · Market Insight |
| 8 | **Productize** | Internal Tool · Client Feature · Reusable Module |
| 9 | **Spin Out** | وحدة أعمال / venture (مثال: Revenue OS، Brain OS، Clinics OS، Logistics OS) |

**قاعدة:** لا انتقال لمرحلة دون **Gate** — انظر [`../company/SERVICE_READINESS_GATE.md`](../company/SERVICE_READINESS_GATE.md).

---

## 3. Proof Economy (اقتصاد الإثبات)

**العنوان:** لا تبيع وعودًا — تبيع **evidence**.

**أنواع Proof:** Revenue · Time · Quality · Risk · Knowledge  

**كل proof يسجل:** metric · source · before · after · method · confidence · limitations

مثال:

```json
{
  "proof_type": "Revenue Proof",
  "metric": "accounts_scored",
  "before": 0,
  "after": 50,
  "evidence": "Lead Intelligence Report",
  "confidence": "high",
  "limitations": "No external outreach executed by Dealix"
}
```

قالب: [`../templates/PROOF_PACK_TEMPLATE.md`](../templates/PROOF_PACK_TEMPLATE.md) · نظام التحويل: [`../growth/PROOF_TO_RETAINER_SYSTEM.md`](../growth/PROOF_TO_RETAINER_SYSTEM.md)

---

## 4. Human-Amplified AI Operations

**ليست Humanless** — **Human-amplified**: إعادة تصميم العمل وتدريب البشر ودمجهم مع AI يحقق عائدًا أقوى من إطار «الاستبدال فقط». مرجع مكمل: [McKinsey — The race to deploy generative AI and reskill people](https://www.mckinsey.com/mgi/our-research/a-new-future-of-work-the-race-to-deploy-ai-and-reskill-people).

**مبدأ Dealix**

```text
AI prepares → Human approves → System logs → Proof validates
```

كل مخرج: `draft_only` / `requires_approval` / `qa_status` / `audit_event_id` / `risk_level`

---

## 5. Source-Centric Data — «جواز سفر المصدر»

كل سجل/دفعة بيانات تحتاج **Source Passport** (انظر [`../architecture/SOURCE_PASSPORT.md`](../architecture/SOURCE_PASSPORT.md)):

- من أين جاءت؟ هل نستخدمها؟ PII؟ إرسال خارجي؟ مدخل للنموذج؟

```json
{
  "source_id": "SRC-001",
  "source_type": "customer_upload",
  "owner": "client",
  "allowed_use": ["internal_analysis", "draft_only"],
  "contains_pii": true,
  "sensitivity": "medium",
  "relationship_status": "existing_relationship",
  "retention_policy": "project_duration",
  "ai_access_allowed": true,
  "external_use_allowed": false
}
```

---

## 6. Retainer Conversion

كل **Proof Pack** ينتهي بثلاثة مسارات: **Continue** · **Expand** · **Pause**

**قاعدة:** لا proof pack بلا **continuation recommendation**، انظر [`../growth/PROOF_TO_RETAINER_SYSTEM.md`](../growth/PROOF_TO_RETAINER_SYSTEM.md).

---

## 7. Productization Ledger

كل مشروع يسجل خطوات يدوية؛ القرار من **احتكاك السوق** لا من «فكرة عابرة». مرجع: [`../product/PRODUCTIZATION_LEDGER.md`](../product/PRODUCTIZATION_LEDGER.md) · [`../company/PRODUCTIZATION_GATE.md`](../company/PRODUCTIZATION_GATE.md).

---

## 8. الشراكات والأكاديمية والمعايير

- **Partner tiers:** Referral → Implementation → Certified → Strategic → White-label (الأخير فقط بعد تدريب QA، شهادة، عيّنة تسليم، حق تدقيق، تقييم عميل).
- **Academy =** category control · enablement · talent · trust · تعليم سوق — شروط إطلاق مقترحة: **10+** مشروعات · **3+** أصول case بproof · منهج متكرر · قوالب تدريب.
- **Dealix Standards:** [`../standards/DEALIX_AI_OPERATIONS_STANDARD.md`](../standards/DEALIX_AI_OPERATIONS_STANDARD.md) — **من يملك المعيار يملك الفئة**.

---

## 9. التنفيذ في الكود (مرجع)

| المجال | المسار الحالي في الريبو |
|--------|---------------------------|
| Data OS | `auto_client_acquisition/data_os/` |
| Governance OS | `auto_client_acquisition/governance_os/` |
| LLM | `auto_client_acquisition/llm_gateway_v10/` |
| Revenue OS | `auto_client_acquisition/revenue_os/` |
| Reporting / Proof | `auto_client_acquisition/reporting_os/` |
| Productization ledger (وثيقة) | [`../product/PRODUCTIZATION_LEDGER.md`](../product/PRODUCTIZATION_LEDGER.md) |
| **مستهدف لاحقًا** | `core_os/` · `capital_os/` · `command_center/` — انظر [`DEALIX_COMPOUND_HOLDING_OPERATING_LAYER.md`](DEALIX_COMPOUND_HOLDING_OPERATING_LAYER.md) |

---

## 10. Stack يصعب نسخه

1. Dealix Method · 2. Core OS · 3. Runtime Governance · 4. Proof Economy · 5. Capital Ledger  
6. Saudi/Arabic QA · 7. Business Unit Model · 8. Venture Graduation · 9. Academy · 10. Partner Certification  

---

## 11. معايير «وصلنا مستوى قابضة»

- Core OS يخدم كل الخدمات · كل مشروع proof + capital · **2+** retainers · **3+** playbooks  
- Productization Ledger حيّ · وحدات لها KPIs · شريك يبيع لك  
- Client Workspace مطلوب · Academy/Standard قابلة للتسويق  

---

## 12. Endgame — الفلايويل

```text
Services feed Cloud — Cloud improves Services
Proof feeds Sales — Academy trains Partners — Partners feed Services
Labs create Ventures — Ventures use Core OS — Standards create Category
```

---

## 13. خلاصة تنفيذية

1. Core OS · 2. Revenue Intelligence wedge · 3. Governance على كل شيء · 4. Proof على كل تسليم  
5. كل Proof يقترح Retainer · 6. كل مشروع Capital · 7. كل تكرار في Productization Ledger  
8. Playbook قوي → BU · 9. BU قوي → Venture · 10. Dealix Method → Standard + Academy  

**الجملة الختامية:** Dealix تصبح عظيمة عندما تتحول من «من يبني حلول AI» إلى «من **يصنع قدرات تشغيلية محكومة**»، ويحوّل كل قدرة إلى Proof، وكل Proof إلى Retainer، وكل Retainer إلى Product، وكل Product إلى وحدة أعمال، وكل وحدة إلى أصل داخل **شركة قابضة**.
