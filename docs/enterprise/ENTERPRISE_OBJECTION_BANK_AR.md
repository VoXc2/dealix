# Enterprise Objection Bank — Dealix (AR)

> مكتبة ردود جاهزة على اعتراضات procurement و CISO و decision makers.

---

## Security Objections

**O1: "لسنا SOC2-certified"**
نلتزم بـ security-by-design ولدينا security overview + audit-ready policies. SOC2 Type II على roadmap E4. حالياً:
- App-level: TLS, allowlist, audit, eval
- Process: incident runbook, change control
- Data: PDPL-compliant
→ نرفق: `SECURITY_OVERVIEW_AR.md` + `docs/governance/`

**O2: "لا يوجد pen-test"**
Pen-test خارجي مُخطط E4. حالياً: dependency audit شهري، secrets scan في CI، eval suite للـ AI.
→ اقترح: pen-test مُصغّر كـ paid engagement إذا العميل يحتاج

**O3: "لا CISO مُعيَّن"**
المؤسس يتحمل مسؤولية security حتى تعيين Security Officer. Owner للـ security runbook = founder.
→ نقطة ضعف صريحة: نلتزم بتعيين عند أول enterprise deal

**O4: "prompt injection مخاطرة"**
صحيح. لهذا:
- Untrusted data isolation
- Allowlist actions
- Audit
- Red team مُخطط
→ `docs/agents_wave3/AGENT_SECURITY_FRAMEWORK_AR.md`

## Privacy Objections

**O5: "ليستم PDPL-certified"**
PDPL ليس له certification رسمي. نلتزم بمتطلباته:
- Privacy by design
- Data minimization
- Subject rights workflow
- Breach notification
→ `PRIVACY_OVERVIEW_AR.md`, `docs/governance/PDPL_DATA_RULES.md`

**O6: "أين servers؟"**
Region يُحدد في DPA. Default: Saudi-available. LLM providers قد تكون خارج (مع DPA + redaction).
→ `PRIVACY_OVERVIEW_AR.md` §4

**O7: "من الـ Data Processor؟"**
Dealix (نحن). العملاء هم Controllers. قائمة sub-processors في DPA.
→ `PRIVACY_OVERVIEW_AR.md` §9

## Commercial Objections

**O8: "ليش أنتم أغلى من freelancer؟"**
- Freelancer: بطيء، غير قابل للتوسع، يحتاج تدريب
- Dealix: نظام كامل، audit، governance، تسليم
- ROI أثبتناه في pilots
→ Proof pack case study (يُضاف)

**O9: "ما ROI المضمون؟"**
لا نضمن أرقام مطلقة. نضمن:
- 30-day pilot لقياس baseline
- Weekly proof packs
- Refund إذا لم يتحقق success metric (يُحدد)
→ `docs/commercial/operations/sample_proof_pack/`

**O10: "نحتاج فترة تجربة"**
افتراضياً: 30-day pilot. لا commitment.

**O11: "السعر أعلى منافسيكم"**
- قارن scope، لا سعر
- شامل governance + audit + delivery
- شامل Arabic + Saudi localization

## Operational Objections

**O12: "ماذا لو سقطتم أنتم؟"**
- Backups يومي
- BC/DR مُخطط E3
- Code open-sourced كـ fallback
- Termination clause في العقد

**O13: "BCP/DR؟"**
- RPO < 24h
- RTO < 4h
- DR drill مُخطط E3+
→ `SLA_SLO_DRAFT_AR.md` §2

**O14: "Uptime 99.5% غير كافي"**
- Enterprise tier: 99.9%
- Multi-region مُخطط E5
- نتفاوض SLA حسب criticality

**O15: "نحتاج on-premise"**
- مُخطط E5 (شراكة استضافة)
- حالياً: hosted فقط

## AI-Specific Objections

**O16: "هل AI يحل محل الفريق؟"**
لا. Dealix يُمكّن الفريق. كل output يُراجع.

**O17: "ماذا لو hallucinate؟"**
- Schema validation
- Output filtering
- Eval suite
- Human approval للإجراءات الخارجية
→ `docs/agents_wave3/AGENT_SECURITY_FRAMEWORK_AR.md`

**O18: "هل تدربون على بياناتي؟"**
لا. لا نستخدم بيانات العميل لتدريب نماذج. مذكور في DPA.

**O19: "أي نموذج تستخدمون؟"**
- MiniMax, OpenAI, DeepSeek, Ollama (per Agent 19 policy)
- لا custom training
- Routing documented
→ `docs/ai_ops/MODEL_REGISTRY_AR.md` (يُبنى)

## Localization Objections

**O20: "كم فريقكم سعودي؟"**
المؤسس سعودي. نلتزم بـ Saudization. التفاصيل في `VENDOR_PROFILE_AR.md`.

**O21: "عربي فصيح؟"**
نعم، Arabic-first. Tone قابل للتعديل.

**O22: "ZATCA invoices؟"**
عند تفعيل الفوترة. متوافق.

## Process Objections

**O23: "نحتاج مراجعة طويلة"**
- Procurement pack جاهز (`docs/enterprise/`)
- SLA/SLO جاهز
- FAQ جاهز
- Demo + security overview session

**O24: "نحتاج trial"**
30-day pilot standard.

**O25: "نحتاج references"**
References تُضاف بعد أول client يوافق.

---

> **Owner:** Founder + Sales Lead · **Reviewer:** Council
> **Cadence:** يُحدّث بعد كل lost deal analysis
