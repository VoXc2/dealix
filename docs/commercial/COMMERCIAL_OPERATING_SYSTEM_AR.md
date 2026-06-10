# Commercial Operating System — النظام التشغيلي التجاري
**Dealix — Agent #3**

> **الغرض:** نقطة مرجعية واحدة لفهم كيف تشتغل الطبقة التجارية في Dealix، وما الذي يربط كل مرحلة بالتي تليها، وكيف يحكمها نظام SOAEN (Source → Owner → Approval → Evidence → Next Action).

---

## 1. التعريف

**Dealix Commercial OS** هو نظام متكامل يربط 16 وحدة تجارية في خط واحد:

```
[Positioning]
     ↓
[ICP] + [Buyer Personas] + [Disqualification]
     ↓
[Pain Matrix] → [Offer Matching]
     ↓
[Product Ladder] + [Pricing Guardrails] + [Discount Governance]
     ↓
[Sales Process] → [Pipeline Stages] → [Discovery] → [Qualification]
     ↓
[Proposal] + [Proof Pack] + [Payment Handoff]
     ↓
[Customer Success] → [Renewal] → [Expansion]
     ↓
[Partnerships] + [Channels]
     ↓
[Commercial Finance] + [Risk Register]
     ↓
[Commercial Control Room] — daily/weekly founder rhythm
```

كل وحدة لها **مالك (Owner)**، **مخرجات (Outputs)**، **حوكمة (Governance)**، **اختبارات (Tests)**، و**ربط (Linkage)** بالوحدات الأخرى.

---

## 2. المبادئ التأسيسية (Foundational Principles)

### 2.1 SOAEN — حوكمة كل Touchpoint
**Source → Owner → Approval → Evidence → Next Action**

| Element | المعنى | مثال |
|---------|--------|------|
| **Source** | من أين جاءت البيانات | `icp_primary.yaml`, lead capture, partner referral |
| **Owner** | من المسؤول عن القرار | Founder، Sales Lead، CCO، Discovery Agent |
| **Approval** | من يوافق على الخرج | Approval policy في YAML، founder للموافقات الحرجة |
| **Evidence** | ما هو الدليل | `evidence_events_tracker.csv`, proof pack, decision passport |
| **Next Action** | ما الخطوة التالية (وقابلة للقياس) | schedule discovery, send proposal, handoff to delivery |

### 2.2 لا إدعاء بلا دليل
- كل ادعاء في `claim_policy.yaml` يجب أن يكون موثّقًا
- ROI/guarantee = محظور (`claim_policy.yaml: roi_or_guarantee.allowed: false`)
- numeric claim in customer pack must have `source` or `is_estimate`
- security claim must have source + approval

### 2.3 لا إجراء خارجي بدون موافقة
- `agent_permissions.yaml`: external_send = blocked by default
- `approval_policy.yaml`: كل الفئات الحرجة requires_approval: true
- dry_run = true; approval_required = true for any external-facing action

### 2.4 القرار من البيانات لا من الرأي
- `kpi_founder_commercial_registry.yaml` يحدد الأرقام
- لا تخمين في أرقام الإيراد
- `apply_kpi_founder_commercial.py` فقط يحدّث من CRM

### 2.5 التسليم قبل التسويق
- لا scaling motion قبل أول `payment_received` + `proof_pack_delivered`
- "Build what is bought" — لا بناء من توقعات

---

## 3. الأدوار التجارية (Commercial Roles)

| Role | Mission | Decisions | Constraints |
|------|---------|-----------|-------------|
| **Founder/CEO** | الرؤية، الموافقة الحرجة، حماية الهامش | pricing final, legal, custom enterprise | لا يبيع مباشرة في المعمعة — يدخل في المراحل الحرجة فقط |
| **CCO Strategy Agent** | وضع الاستراتيجية + التحديث | تحديث ICP, motions, focus | dry-run فقط، founder يوافق على التغييرات |
| **ICP Agent** | تحديث شرائح ICP | تعديل score thresholds, segments | يحترم `icp_primary.yaml` كمرجع |
| **Offer Catalog Agent** | إدارة السلم | عرض/سحب عرض | يحترم `pricing.yaml` و `offers.yaml` |
| **Pricing Guard Agent** | تطبيق guardrails | الموافقة على discount | لا يتجاوز founder authority |
| **Discovery Agent** | إدارة مكالمات الاكتشاف | يحجز، يلخص، يصنّف | dry-run, draft-only external |
| **Proposal Agent** | بناء عروض | يصيغ scope, deliverables | founder يوافق final |
| **Proof Pack Agent** | بناء أدلة | يجمع evidence, formats | يلتزم L0–L5 levels |
| **Objection Agent** | معالجة الاعتراضات | يطابق bank, يقترح رد | يفصح عن "walk away" conditions |
| **Partner Channel Agent** | إدارة الشراكات | qualifying, models | يحترم `partner_rules.yaml` |
| **Customer Success Agent** | نجاح العميل | onboarding, weekly report, health | dry-run for external until approved |
| **Renewal Agent** | إدارة التجديد | تنبيهات, expansions | founder approves pricing changes |
| **Finance Agent** | الوحدات الاقتصادية | reports, margins | no invention — read CRM |
| **Commercial Risk Agent** | سجل المخاطر | flag risks, walk-away | يحترم `risk_register.yaml` |
| **Commercial Metrics Agent** | لوحة القياس | daily/weekly numbers | reads from approved registries only |

**التفصيل الكامل:** `docs/agents/COMMERCIAL_AGENT_ROLES_AR.md` (PHASE 16)

---

## 4. الوحدات الـ 16 — Quick Map

| # | الوحدة | مالك | مرجع رئيسي | المخرج |
|---|--------|------|-------------|--------|
| 1 | Positioning | CCO | `DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md` | one-liner + segment fit |
| 2 | ICP Matrix | ICP Agent | `icp_primary.yaml`, `icp_segments.yaml` | `icp_segments.yaml` (هذا التقرير الجديد في `data/commercial/icp_segments.yaml`) |
| 3 | Buyer Personas | ICP Agent | `MARKET_INTELLIGENCE_FOUNDER_REVOPS_GTM_AR.md` | `data/commercial/buyer_personas.yaml` |
| 4 | Pain Matrix | CCO | (PHASE 3) | `data/commercial/pain_to_offer.yaml` |
| 5 | Offer Ladder | Offer Catalog | `offers.yaml`, `pricing.yaml` | `data/commercial/product_catalog.yaml` |
| 6 | Pricing Guardrails | Pricing Guard | `pricing.yaml` | `data/commercial/pricing_rules.yaml` |
| 7 | Sales Process | Sales Lead | `os/14_DISCOVERY_CALL_TEMPLATE.md` | `data/commercial/opportunities.jsonl` |
| 8 | Pipeline Stages | Sales Lead | `stage_transitions.yaml` | reports/commercial/PIPELINE_REVIEW.md |
| 9 | Discovery | Discovery Agent | `os/14_DISCOVERY_CALL_TEMPLATE.md` | `data/commercial/discovery_notes.jsonl` |
| 10 | Proposal | Proposal Agent | `os/15_PROPOSAL_TEMPLATE.md` | `proposal_499_sar_ar.md` adapted |
| 11 | Proof Pack | Proof Pack Agent | `data/templates/proof_pack_ar.md` | `proof_pack_ar.md` adapted |
| 12 | Payment Handoff | Billing Draft | `MANUAL_PAYMENT_SOP.md` | approval-gated, evidence-required |
| 13 | Customer Success | CS Agent | `os/16_CLIENT_ONBOARDING_TEMPLATE.md` | `data/customer_success/client_health.jsonl` |
| 14 | Renewal | Renewal Agent | `os/20_EXPANSION_PLAYBOOK.md` | renewal_drafts |
| 15 | Partnerships | Partner Channel | `partner_rules.yaml` | `data/partners/partner_opportunities.jsonl` |
| 16 | Channels | CCO | (PHASE 9) | `CHANNEL_STRATEGY_REVIEW.md` |

---

## 5. التدفقات التجارية الأساسية (Commercial Flows)

### 5.1 Inbound Flow
```
Visit /[locale]
   ↓
Demo request / Pricing
   ↓
Lead capture (POST /api/v1/leads)
   ↓
ICPScoringAgent (uses icp_primary.yaml)
   ↓
Qualified A/B/Nurture
   ↓
Discovery call booking (Calendly)
   ↓
Discovery done
   ↓
Proposal sent (approval required)
   ↓
Payment handoff (approval required)
   ↓
Delivery started
   ↓
Proof pack sent
   ↓
Sprint/Retainer candidate
```

### 5.2 Outbound Flow (Dry-run only)
```
Signal detected (no scraping)
   ↓
ICPScoringAgent validates fit
   ↓
OutreachDraftAgent drafts message
   ↓
Founder approves draft
   ↓
Manual send by founder
   ↓
Reply classified
   ↓
Discovery scheduled
   ↓
(same as inbound)
```

### 5.3 Partner Flow
```
Partner lead → Partner channel agent
   ↓
Partner qualification (no spam, no guaranteed claims, has client access)
   ↓
Partner opportunity logged
   ↓
Dealix + Partner co-sell/co-deliver
   ↓
Revenue share / referral fee (per partner_rules.yaml)
   ↓
Renewal handled by Dealix
```

### 5.4 Renewal Flow
```
Active delivery near end
   ↓
Client health score (green/yellow/red)
   ↓
Renewal draft (success metric + next steps)
   ↓
Founder approves
   ↓
Renewal sent (or expansion offer)
   ↓
Won → Contract continues
Lost → Reason logged in risk register
```

---

## 6. القواعد اليومية للمؤسس (Founder Daily Commercial Rhythm)

### 6.1 صباحًا (5–15 دقيقة)
1. **Command Room** — `/[locale]/ops/founder` — افتح الـ cockpit
2. **Pipeline** — ما الجديد في pipeline؟
3. **Proposals** — هل يوجد proposal يحتاج موافقة؟
4. **Payments** — هل يوجد payment handoff؟
5. **Risks** — هل يوجد risk جديد؟

### 6.2 مساءً (5 دقائق)
1. **Evidence event** — سجّل حدثاً واحداً على الأقل في `operations/evidence_events_tracker.csv`
2. **Tomorrow's draft list** — ما الذي سيُرسل غداً؟

### 6.3 أسبوعيًا (30 دقيقة — يوم الأحد)
1. **Pipeline review** — الإغلاق والخسارة
2. **Channel ROI** — أي قناة مربحة؟
3. **Best offer** — أي عرض يحوّل أكثر؟
4. **Customer health** — من في خطر؟
5. **Renewals** — من على وشك الانتهاء؟
6. **Partner pipeline** — أي شريك نشط؟
7. **Finance** — CAC, LTV, margin, payback
8. **Risk register** — أي مخاطر جديدة؟
9. **Next week focus** — ما القرار الأسبوعي؟

**التفصيل:** `FOUNDER_COMMERCIAL_RHYTHM_AR.md`

---

## 7. قرارات لا يحق لـ Agent اتخاذها (Decisions That Must Stay With Founder)

- ❌ تسعير نهائي لعميل
- ❌ Discount > 15%
- ❌ Custom enterprise quote > 50,000 SAR
- ❌ Legal/regulated contract terms
- ❌ أي ادعاء revenue/ROI مضمون
- ❌ أي رسالة WhatsApp cold
- ❌ أي رسالة LinkedIn آلية
- ❌ أي إرسال بريد بارد
- ❌ أي موافقة على partner white-label
- ❌ أي refund > 10% من الصفقة
- ❌ أي case study publish مع اسم عميل
- ❌ أي تخفيض tier
- ❌ أي تغيير في `pricing.yaml` أو `offers.yaml`
- ❌ أي تفعيل لإرسال آلي (مطلقًا)

---

## 8. مؤشرات يجب أن يعرفها المؤسس (Founder KPIs)

| المؤشر | قراءة |
|--------|------|
| Qualified pipeline value | weekly |
| Conversion by stage | weekly |
| Best offer | weekly |
| Best channel | weekly |
| Delivery risk count | daily |
| Renewal candidates | weekly |
| Partner pipeline | monthly |
| CAC by channel | monthly |
| Margin by offer | monthly |
| Churn risk | monthly |
| LTV estimate | quarterly |
| Founder time per offer | weekly |

**التفصيل:** `COMMERCIAL_METRICS_AR.md`

---

## 9. كيف يستخدم المؤسس هذا النظام؟

### 9.1 للمبتدئ
ابدأ من `MASTER_COMMERCIAL_OPERATING_PLAN_AR.md` (5 دقائق يومياً) ثم هذا الملف.

### 9.2 للتعمق
PHASE 2 → 16 — كل PHASE فيها ملف وثائقي + schema + data + report.

### 9.3 لاتخاذ قرار
افتح `COMMERCIAL_DECISION_RULES_AR.md` (PHASE 1) — يربط كل سؤال بنوع الإجابة.

---

## 10. كيف يتفاعل النظام مع الأجزاء الأخرى؟

```
Commercial OS
   ├── Trust Engine (approval_policy, claim_policy, no_overclaim)
   ├── Lead Engine (icp_primary, lead_scoring, stage_transitions)
   ├── Service Engine (api/routers/commercial.py — 13 endpoints)
   ├── Data Plane (dealix_events, opportunities, discovery_notes)
   ├── Operating Plane (CI, tests, scripts)
   └── Frontend (/ops/founder, /ops/war-room, etc.)
```

---

## 11. الجاهزية الحالية (Current Readiness)

- ✅ Foundation docs (positioning, ICP base, offers, pricing)
- ✅ Approval & claim policies
- ✅ Lead pipeline (16 stages)
- ✅ Tests (25+ commercial tests)
- ✅ UI surfaces (5 ops pages + 5 public pages)
- ✅ Scripts (10+ founder daily scripts)
- ⚠️ Buyer personas (new — PHASE 2)
- ⚠️ Pricing guardrails (formal — PHASE 5)
- ⚠️ Customer health (new — PHASE 11)
- ⚠️ Walk-away rules (new — PHASE 13)
- ⚠️ Commercial tests for guardrails (new — PHASE 15)
- ⚠️ Commercial agent roles (new — PHASE 16)

---

## 12. خطوات البدء للمؤسس

1. **اليوم:** اقرأ هذا الملف (10 دقائق) + `COMMERCIAL_DECISION_RULES_AR.md`
2. **هذا الأسبوع:** قرّر أي motion تركز عليه (A=Agency غالبًا) + أول ICP priority
3. **الأسبوع القادم:** شغّل `python scripts/founder_strongest_plan_status.py` وحل الفجوات
4. **بعد 30 يوم:** أول `payment_received` + `proof_pack_delivered`
5. **بعد 60 يوم:** أول `sprint_candidate` أو `retainer_candidate`
6. **بعد 90 يوم:** أول `partner_sourced_paid_diagnostic`

---

**تم إعداد هذا الملف كـ Foundation لطبقة Dealix التجارية. كل PHASE التالية تضيف عمقًا إلى هذا النظام دون تعديله.**
