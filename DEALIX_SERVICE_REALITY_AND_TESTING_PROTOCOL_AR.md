# Dealix — بروتوكول جاهزية الخدمات والاختبار (The 8 Gates)

> **المرجع التشغيلي الأعلى لإثبات أن كل خدمة "حقيقية" وليست واجهة أو وثيقة.**
>
> - المعيار المرجعي: **NIST AI RMF** + **GenAI Profile** + **OWASP Top 10 2025** + **OpenTelemetry Spec** + **PostgreSQL RLS**
> - آخر تحديث: 18 أبريل 2026
> - المالك: Sami Assiri
> - تُعاد المراجعة: كل أسبوع (Monday Reality Review)
> - الملفات المرتبطة: `docs/registry/SERVICE_READINESS_MATRIX.yaml`, `docs/registry/CLAIMS.md`, `marketing/CLAIMS_REGISTRY_AR.md`

---

## القاعدة الذهبية

> **لا تُعتبر خدمة "حقيقية" إلا إذا نجحت في البوابات الثمانية كلها.**
>
> "شغّال محلياً" أو "فيه endpoint" أو "فيه اختبار" ليست كافية.

---

## البوابات الثمان (8 Gates)

### 🟢 البوابة 1 — الحقيقة (Truth)

**القاعدة:** لكل جزء من النظام حالة واحدة من: `Live | Partial | Pilot | Target | Deprecated`.

**مصدر الحقيقة الوحيد:**
- `docs/registry/TRUTH.yaml` — حالة كل خدمة/ميزة
- `marketing/CLAIMS_REGISTRY_AR.md` — حالة كل claim تسويقي

**اختبار النجاح:**
- [ ] كل خدمة في الكود مطابقة للحالة في `TRUTH.yaml`
- [ ] كل claim في landing/deck/one-pager مربوط بصف في `CLAIMS_REGISTRY_AR.md` بحالة `approved`
- [ ] CI يفشل إذا ظهر ادعاء غير مسجل (validate_truth_registry.py + validate_claims.py)
- [ ] لا توجد ثلاث روايات مختلفة لنفس الخدمة

**الفشل الشائع:** Landing يقول "Live"، README يقول "Beta"، الكود يقول "NotImplementedError".

---

### 🟢 البوابة 2 — العقود (Contracts)

**القاعدة:** كل خدمة حساسة تُستهلك عبر **Schema-bound Structured Output** — لا raw dicts.

**الحقول الإلزامية في كل عقد:**
```yaml
version: string            # semver
trace_id: uuid
correlation_id: uuid
provenance: { source, fetched_at, checksum }
freshness: { max_age_seconds, refreshed_at }
confidence: float 0..1
actor: { type: human|agent|system, id }
timestamps: { created_at, updated_at }
```

**اختبار النجاح:**
- [ ] كل endpoint حساس له JSON Schema في `schemas/contracts/`
- [ ] Pydantic v2 validators على الـ boundary (API + LLM output)
- [ ] OpenAI Structured Outputs لأي LLM call يُرجع بيانات عمل
- [ ] Frontend يستورد نفس الأنواع (TypeScript types generated من JSON Schema عبر `json-schema-to-typescript`)
- [ ] Contract tests في CI ترفض أي تغيير breaking

**أمثلة العقود المطلوبة:**
- `LeadContract.json` — lead intake / enrichment output
- `ScoreContract.json` — scoring breakdown
- `OutreachActionContract.json` — أي إرسال خارجي
- `ApprovalContract.json` — كل طلب موافقة
- `EvidenceContract.json` — دليل قابل للتدقيق
- `ExecutiveDecisionContract.json` — قرار تنفيذي

---

### 🟢 البوابة 3 — الثقة (Trust / Access Control)

**القاعدة:** OWASP 2025 A01 (Broken Access Control) أولى. كل action حساس:
- **Server-side** enforcement (لا اعتماد على الواجهة)
- **Deny-by-default** (بدون policy = رفض)
- **Reusable authorization layer** (decorator / dependency واحد مشترك)

**كل action حساس يفشل تلقائياً بدون:**
- `approval_id` (إذا قيمة > threshold)
- `evidence_id` (مرفق)
- `authorization` (role + scope + tenant)
- `correlation_id` (ربط بالطلب الأصلي)
- `verification_receipt` (تأكيد بعدي)

**اختبار النجاح:**
- [ ] Unit tests صريحة لكل access check (aspect + negative cases)
- [ ] Integration tests تحاول bypass الـ UI
- [ ] لا wiring "convention-based" — كل protected route لها decorator مرئي
- [ ] Audit log لكل `denied` event
- [ ] الحقول أعلاه مطلوبة في الـ schema (ترفض الـ request بدونها)

---

### 🟢 البوابة 4 — التنفيذ الطويل (Durable Execution)

**القاعدة:** أي workflow يمتد عبر > 1 request، أو ينتظر approval، أو فيه side effects خارجية → يحتاج **durable execution**.

**التطبيق:**
- State persisted بعد كل خطوة (checkpoint)
- إمكانية استئناف من آخر checkpoint
- Idempotency keys على الـ side effects (رسائل، مدفوعات، إنشاءات)
- Saga pattern للعمليات متعددة الأنظمة

**اختبار النجاح (Chaos Test):**
- [ ] أوقف الخدمة في منتصف workflow عمداً (`kill -9`)
- [ ] أعد تشغيلها
- [ ] تأكد أنها استأنفت من آخر checkpoint
- [ ] تأكد أن Twilio/SendGrid/LinkedIn **لم يستقبل** الطلب مرتين
- [ ] تأكد من idempotency key في DB

**التقنية المقترحة:**
- Temporal.io (أفضل) أو
- LangGraph checkpointers (Python-native) أو
- Celery beat + DB-backed state machine (الأبسط — ابدأ به)

---

### 🟢 البوابة 5 — العزل والتعدد (Multi-Tenant Isolation)

**القاعدة:** PostgreSQL **Row-Level Security (RLS)** على كل جدول يحمل `tenant_id`. فلاتر التطبيق لا تكفي.

**السياسات المطلوبة:**
```sql
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON leads
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

**اختبار النجاح:**
- [ ] Test: tenant A يحاول SELECT tenant B → صفر rows
- [ ] Test: tenant A يحاول UPDATE tenant B → صفر affected
- [ ] Test: tenant A يحاول DELETE tenant B → صفر affected
- [ ] Test: missing WHERE clause في التطبيق → لا يسرب (RLS يحميها)
- [ ] Test: عبر API + عبر direct DB connection
- [ ] Test: عبر LLM tool call (agent يعمل بحساب tenant معين)

**الفشل الشائع:** "الواجهة لا تعرض tenants أخرى" — هذا ليس عزل، هذا تمويه.

---

### 🟢 البوابة 6 — الإطلاق (Release Gate)

**القاعدة:** CI يفشل → merge يُرفض → release يُلغى. لا استثناءات.

**GitHub Actions متطلبات:**
- [ ] جميع tests (unit + integration + contract) خضراء
- [ ] Schema validation خضراء (contracts + truth registry + claims)
- [ ] Security scans خضراء (Bandit, Semgrep, Trivy على الصور)
- [ ] **OIDC-based cloud auth** بدل long-lived secrets ([docs](https://docs.github.com/en/actions/concepts/security/openid-connect))
- [ ] **Artifact attestations** (provenance) لكل build ([docs](https://docs.github.com/en/actions/concepts/security/artifact-attestations))
- [ ] Rollback path موثق في `docs/RUNBOOKS/rollback.md`
- [ ] Release Readiness Matrix مطبوعة ومعتمدة (من `SERVICE_READINESS_MATRIX.yaml`)

**بوابة قبل الإطلاق:**
```
🚫 لا merge لـ main إذا:
  - أي خدمة في release scope بحالة Pilot/Partial وتظهر في landing كـ Live
  - claims جديدة غير معتمدة في Claims Registry
  - provenance غير متوفر لـ artifacts الإنتاج
  - Rollback path غير مجربة خلال آخر 30 يوم
```

---

### 🟢 البوابة 7 — الرصد (Observability)

**القاعدة:** OpenTelemetry spec. كل golden path → **trace واحد كامل**.

**المطلوب:**
- [ ] كل request له `trace_id + span_id` (W3C Trace Context headers)
- [ ] كل log structured ومرتبط بـ `trace_id`
- [ ] Approval steps ظاهرة كـ spans منفصلة
- [ ] Evidence creation span
- [ ] Every external connector call (Twilio/Groq/LinkedIn/SendGrid) = child span
- [ ] Dashboards: latency p50/p95/p99، error rate، retry counts، SLA breaches
- [ ] Cost tracking: tokens per trace (Groq/OpenAI)، API calls per trace

**الأدوات:**
- OpenTelemetry SDK (Python + TypeScript)
- Collector: Grafana Tempo أو Jaeger
- Logs: Loki
- Metrics: Prometheus + Grafana
- APM: Datadog (إذا ميزانية) أو SigNoz (مجاني)

**اختبار النجاح:** افتح trace لأي محادثة WhatsApp → شف كل الخطوات: inbound webhook → DB write → Groq call → outbound reply → evidence. كل span له duration + status.

---

### 🟢 البوابة 8 — الخدمات الفعلية (End-to-End Reality Matrix)

**القاعدة:** لا تختبر الكود فقط. اختبر **كل خدمة تدعيها** بمدخلات حقيقية + happy path + rejected + error.

**مصفوفة الاختبار الفعلي:**

#### Revenue OS
- [ ] `lead_intake` — من 5 مصادر (WA inbound, Email reply, LinkedIn, Web form, Manual)
- [ ] `enrichment` — 6 مصادر بيانات تعمل أو تفشل gracefully
- [ ] `qualification` — BANT/MEDDPICC agent يسأل ويحفظ
- [ ] `routing` — playbook يختار القناة الصحيحة
- [ ] `outreach` — إرسال فعلي عبر WhatsApp/Email (موجود ✅)
- [ ] `proposal` — PDF مولّد + ربط سعر
- [ ] `approval` — طلب موافقة + timeout + escalation
- [ ] `close` — e-signature + payment link (Moyasar)
- [ ] `onboarding_handoff` — trigger للـ CS agent

#### Partnership OS
- [ ] `scout` — اكتشاف شركاء محتملين
- [ ] `fit_score` — تقييم ملاءمة
- [ ] `economics` — نموذج دخل مشترك
- [ ] `approval` — موافقة داخلية
- [ ] `activation` — إطلاق الشراكة
- [ ] `scorecard` — تقييم أداء دوري

#### Executive OS
- [ ] `weekly_pack` — تقرير تنفيذي توليد تلقائي
- [ ] `pending_decisions` — قائمة قرارات معلقة
- [ ] `blockers` — عوائق حرجة
- [ ] `risks` — مخاطر مرتبة
- [ ] `actual_vs_forecast` — مقارنة فعلي vs متوقع
- [ ] `evidence_drill_down` — كل رقم قابل للنقر → مصدره

#### Saudi / PDPL
- [ ] `consent_required_send` — لا إرسال بدون consent
- [ ] `revoke_consent` — إلغاء فوري + تأكيد
- [ ] `right_to_export` — export كامل خلال SLA
- [ ] `right_to_delete` — حذف + audit trail
- [ ] `right_to_restrict` — suspension
- [ ] `audit_trail` — سجل كامل قابل للتدقيق
- [ ] `cross_border_restriction` — بيانات KSA لا تخرج إلا بإذن

**القاعدة:** إذا لم تُشغَّل الخدمة end-to-end بمدخل حقيقي + happy + rejected + error → **ليست مكتملة**، مهما كانت الواجهة جميلة.

---

## طبقات الاختبار الثلاث

### الطبقة 1 — Contract Tests (صحة الشكل)

```python
# tests/contracts/test_lead_contract.py
def test_lead_accepts_valid_shape():
    lead = LeadContract(**valid_payload)
    assert lead.trace_id

def test_lead_rejects_missing_provenance():
    with pytest.raises(ValidationError):
        LeadContract(**payload_without_provenance)
```

**المستهدف:** 100% من الـ contracts مُغطاة.

### الطبقة 2 — Workflow Tests (صحة السلوك)

```python
# tests/workflows/test_revenue_golden_path.py
async def test_lead_to_won_full_path():
    lead = await create_lead_via_webhook(...)
    await run_qualification(lead.id)
    await run_outreach(lead.id)
    await approve_proposal(lead.id, approver="human")
    await close_deal(lead.id)
    assert lead.status == "won"
    assert evidence_exists(lead.id)
    assert executive_room_reflects(lead.id)
```

**المستهدف:** كل golden path له workflow test واحد على الأقل.

### الطبقة 3 — Failure/Abuse Tests (صحة الثقة)

```python
# tests/chaos/test_restart_mid_workflow.py
async def test_resume_from_checkpoint():
    workflow = await start_outreach_workflow(lead_id)
    await workflow.execute_step_1()
    await workflow.execute_step_2()
    # kill the worker
    os.kill(worker_pid, signal.SIGKILL)
    # restart
    await restart_worker()
    # should resume from step 3, not repeat step 2
    assert twilio_call_count == 1  # not 2!
```

**المستهدف:** كل خدمة durable لها chaos test واحد على الأقل.

---

## اختبار الواقع الأسبوعي (Weekly Reality Review)

كل يوم إثنين — قبل Standup:

```
1. شغّل مسار ذهبي واحد كامل (غيّره أسبوعياً):
   Week 1: Revenue OS → WhatsApp → proposal → approval → won
   Week 2: Partnership OS → scout → activate → scorecard
   Week 3: Executive OS → weekly pack → drill-down → evidence
   Week 4: PDPL → consent → revoke → export → delete
2. أوقف الخدمة في منتصف المسار عمداً
3. أعدها
4. تأكد: ✅ استأنفت من checkpoint؟
5. تأكد: ✅ approval مطبقة؟
6. تأكد: ✅ evidence persisted؟
7. تأكد: ✅ Executive Room عكست النتيجة؟
8. تأكد: ✅ trace كامل موجود (OpenTelemetry)؟
9. تأكد: ✅ أي claim تسويقي عن هذا المسار مطابق لما رأيت؟
10. سجّل النتيجة في SERVICE_READINESS_MATRIX.yaml (last_verified_date)
```

**فشل أي بند → لا تقل "النظام جاهز بالكامل" — عدّل CLAIMS_REGISTRY_AR.md أولاً.**

---

## كيف تتأكد أن الـ Frontend "ما يكذب"

لا تقبل صفحة dashboard/executive room إلا إذا:
- [ ] البيانات من API حي (لا mock fallback خفي)
- [ ] الحقول المعروضة موجودة في العقد (JSON Schema)
- [ ] Loading / Empty / Error / Pending states مكتملة
- [ ] كل metric قابل للتتبع لمصدر backend (drill-down)
- [ ] إذا backend فشل → الصفحة لا تختلق رقم بديل
- [ ] لا fake screenshots في marketing

**اختبار:** افصل الـ API عمداً → الصفحة تعرض `error` state. أعده بـ `partial` → تعرض `partial` state.

---

## الخلاصة — ميثاق التنفيذ

> **لا خدمة تُعتبر حقيقية إلا إذا كانت:**
> 1. **محددة بعقد** (Schema + structured output)
> 2. **محمية بثقة** (Server-side authorization, deny-by-default)
> 3. **قابلة للاستئناف** (Durable execution + idempotency)
> 4. **معزولة بين المستأجرين** (Postgres RLS)
> 5. **مرصودة بتتبّع** (OpenTelemetry traces + logs correlation)
> 6. **مغلقة داخل release gate** (CI + provenance + attestations)
> 7. **مُشغّلة end-to-end** (reality matrix بمدخلات حقيقية)
> 8. **قابلة لإعادة الإثبات** (weekly reality review)

**هذا الميثاق يُقرأ قبل كل release. الفشل في أي بند = تأجيل الإطلاق وتحديث CLAIMS_REGISTRY_AR.md.**

---

## المراجع

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST GenAI Profile](https://www.nist.gov/itl/ai-risk-management-framework)
- [OWASP Top 10 2025 — A01 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/)
- [PostgreSQL Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/)
- [GitHub OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect)
- [GitHub Artifact Attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations)
