# Dealix v5 — دليل تشغيل المؤسس / Founder Runbook

> دليل اليوم الواحد، الأسبوع، والشهر. اقرأ مرّة، علّقه على الجدار،
> اعمل به كل صباح. **مهم:** لا يضيف هذا الدليل أيّ صلاحيّة جديدة —
> فقط ينظّم الصلاحيّات الموجودة فعلاً في الكود.

> One-day, one-week, one-month operating cadence. Read once, pin it,
> live by it every morning. **Important:** this runbook adds no new
> permissions — it only choreographs ones already shipped in code.

**Branch authoring this doc:** `claude/service-activation-console-IA2JK`
**Date:** 2026-05-04
**Applies to:** v5 (12 layers shipped)

---

## 0. المبادئ الثابتة / Hard rules (re-asserted)

| ❌ Never | ✅ Always |
|---|---|
| `whatsapp_allow_live_send=True` | `whatsapp_allow_live_send=False` (default) |
| `MOYASAR_ALLOW_LIVE_CHARGE` env flag | `--allow-live` CLI flag, founder-typed |
| Cold WhatsApp / LinkedIn DM / scraping | Inbound + warm intros only |
| Marking a service Live without 8 gates | YAML `gates:` block before promotion |
| "نضمن"، "guaranteed"، "blast" in copy | `tests/test_landing_forbidden_claims.py` perimeter |
| Auto-pricing change | Pilot 499 SAR locked until customer #5 (S1) |
| Touch a customer record without consent | Consent registry default-deny + redaction |

If you catch yourself violating any of these, stop. Open an issue.
Fix the root cause. Do not bypass.

---

## 1. الإيقاع اليومي — 7AM KSA / Daily cadence

> هدف: قرار واحد قبل الـ 8 صباحاً. مدّة الجلسة: ≤ 15 دقيقة.

### الخطوات / Steps

1. **افتح بريد المؤسس** (`DEALIX_FOUNDER_EMAIL`).
   - بحث عن `[Dealix] Daily Digest — YYYY-MM-DD` (يصل 7AM KSA عبر `daily_digest.yml`).
   - أيّ إشعار `[Dealix] New lead intake` يقفز للأمام (وقت الردّ ≤ 4 ساعات).
2. **شغّل ال CLI الفوريّة:**
   ```bash
   python scripts/dealix_status.py
   ```
   - تأكّد أنّ كل `Live-action gates` تقول `BLOCKED`.
   - راقب `Reliability OS` → `overall: ok` (لو `degraded`، انظر §4).
3. **اختر قراراً واحداً** من قسم *Top decisions today* — الأعلى أولويّة.
4. **سجّل ProofEvent** إذا أتممت أيّ خطوة تسليم بالأمس:
   ```python
   from auto_client_acquisition.proof_ledger import (
       FileProofLedger, ProofEvent, ProofEventType,
   )
   FileProofLedger().record(ProofEvent(
       event_type=ProofEventType.DELIVERY_TASK_COMPLETED,
       customer_handle="<your-customer>",
       summary_ar="…",
       summary_en="…",
       evidence_source="manual_pilot_session_3",
       confidence=1.0,
       consent_for_publication=False,
   ))
   ```
5. **ردّ على لِيد جديد** (إن وُجد) يدويّاً — لا automation.

### معيار النجاح اليومي / Daily success bar

- ☐ قُلّبت بوّابة Live-action واحدة على الأقل: لا؟ → استمرّ.
- ☐ لِيد واحد جديد رُدّ عليه خلال 4 ساعات (لو وصل).
- ☐ ProofEvent واحد مسجَّل (إن جرى تسليم).

---

## 2. الإيقاع الأسبوعي — صباح الإثنين / Weekly Monday review

> هدف: قراران أسبوعيان + استعراض حقيقي. مدّة: ≤ 60 دقيقة.

### الخطوات / Steps

1. **افتح Weekly Scorecard:**
   ```bash
   curl -s https://api.dealix.me/api/v1/self-growth/scorecard/weekly | jq
   ```
   راجع `perimeter_pass_rate` و `services_close_to_promotion`
   و `advisory_seo_gap`.
2. **استعرض ProofEvents هذا الأسبوع:**
   ```bash
   ls docs/proof-events/
   # أو
   curl -s https://api.dealix.me/api/v1/self-growth/proof-pack/assemble \
     -X POST -H 'content-type: application/json' \
     -d '{"customer_handle":"<handle>","events":[…],"consent_for_publication":false}'
   ```
3. **افتح Decision Pack:** `docs/EXECUTIVE_DECISION_PACK.md`
   - وقّع على ≤ 2 من العشرة (B1-B5 + S1-S5). لا توقّع كلها مرّة واحدة.
4. **استعرض الأدوار / Role briefs:**
   ```bash
   for role in ceo sales growth partnership cs finance compliance; do
     curl -s "https://api.dealix.me/api/v1/role-command/$role" | jq .top_decisions
   done
   ```

### معيار النجاح الأسبوعي / Weekly success bar

- ☐ قراران من Decision Pack تمّ توقيعهما (☑) أو رفضهما صراحةً.
- ☐ Scorecard `perimeter_pass_rate` لم يهبط.
- ☐ Service Activation: زادت Pilot/Live بـ 1، أو وُثّق سبب عدم الترقّي.

---

## 3. الإيقاع الشهري — آخر يوم عمل / Monthly cadence

> هدف: Proof Pack شهريّ + قراءة استراتيجيّة. مدّة: ≤ 3 ساعات.

### الخطوات / Steps

1. **اجمع Proof Pack:**
   ```bash
   curl -X POST https://api.dealix.me/api/v1/self-growth/proof-pack/assemble \
     -H 'content-type: application/json' \
     -d "$(jq -n --argjson events "$(cat docs/proof-events/2026-*.jsonl | jq -s 'map(.)')" \
       '{customer_handle:"public_summary",events:$events,consent_for_publication:false}')"
   ```
   - الناتج Markdown ثنائيّ اللغة (عربيّ/إنجليزيّ) — انسخه لمسوّدة LinkedIn / Notion.
2. **استعرض Strategic Master Plan:**
   `docs/STRATEGIC_MASTER_PLAN_2026.md` — هل اتّجاه السوق ما زال يدعم 13 جزءاً؟
3. **افتح GTM OS Calendar:**
   ```bash
   curl -s https://api.dealix.me/api/v1/gtm/content-calendar | jq
   ```
   كلّ بند `approval_required: true` — راجع، عدّل، اعتمد قبل النشر.
4. **راجع Reliability matrix لشهر كامل:**
   ```bash
   curl -s https://api.dealix.me/api/v1/reliability/health-matrix | jq '.subsystems[] | select(.status!="ok")'
   ```

### معيار النجاح الشهري / Monthly success bar

- ☐ Proof Pack واحد جاهز (داخليّ كان أو منشور بإذن العميل).
- ☐ Strategic Plan راجعته أو وثّقت لماذا ما زال صحيحاً.
- ☐ GTM Calendar محدّث، لا منشور آليّ بدون موافقة.

---

## 4. الاستجابة للتنبيهات / Alert response

### إذا رأيت `Reliability OS` تقول `degraded`

| Subsystem | السبب الأشيع / Likely cause | الخطوة الأولى / First step |
|---|---|---|
| `email_provider` | `RESEND_API_KEY` غير مضبوط أو منتهي | تحقّق من Railway env vars |
| `payment_provider` | `MOYASAR_SECRET_KEY` غير مضبوط أو live | تحقّق من المفتاح؛ لا تضع `sk_live_` بدون نيّة واضحة |
| `safe_publishing_gate` | عبارة محظورة في ملف جديد | `pytest tests/test_landing_forbidden_claims.py -v` |
| `service_activation_matrix` | YAML غير صالح أو counts متعارضة | `python scripts/verify_service_readiness_matrix.py` |
| `seo_perimeter` | صفحة جديدة بدون required tags | `python scripts/seo_audit.py` |
| `proof_ledger_in_process` | مجلّد `docs/proof-events/` لا يُكتب فيه | تحقّق من الصلاحيّات + المسار |

### إذا رأيت `live_charge: ALLOWED`

🛑 **احتمال خطأ تكويني — توقّف.**
- تحقّق من `MOYASAR_SECRET_KEY` — هل بدّلته للتوّ؟
- لا تتابع حتى يقول `BLOCKED` مرّة أخرى.

### إذا رأيت تنبيه `whatsapp_live_send: ALLOWED`

🛑 **سياسة منتهكة — توقّف.**
- في `core/config/settings.py` يجب أن يبقى `whatsapp_allow_live_send=False`.
- ابحث عن من غيّره: `git log -p core/config/settings.py | grep -i whatsapp_allow`.

---

## 5. أوّل عميل يدفع — manual playbook / First paying customer

> ١٠٠٪ يدويّ. لا automation. لا خصم آليّ. لا cold outreach.
> **قائمة كاملة خطوة-بخطوة:** `docs/V5_PHASE_E_CHECKLIST.md`.

### الخطوات / Steps

1. **3 warm intros** من شبكتك الموجودة (لا قوائم مشتراة، لا LinkedIn auto).
2. **Free Diagnostic** — ولّد المسوّدة الثنائيّة اللغة فوراً:
   ```bash
   python scripts/dealix_diagnostic.py \
     --company "اسم الشركة" \
     --sector b2b_services \
     --region riyadh \
     --pipeline-state "وصف مختصر للوضع الحاليّ"
   ```
   راجع المسوّدة، عدّل، ثمّ أرسلها يدويّاً. تقدّم الـ journey:
   `/api/v1/customer-loop/journey/advance` من
   `lead_intake` → `diagnostic_requested` → `diagnostic_sent`.
3. **Pilot Offer** بسعر 499 ريال (راجع
   `docs/registry/SERVICE_READINESS_MATRIX.yaml::bundles.growth_starter`).
4. **فاتورة Moyasar test mode** عبر CLI:
   ```bash
   python scripts/dealix_invoice.py \
     --email customer@acme.sa \
     --amount-sar 499 \
     --description "Growth Starter Pilot — 7 days"
   ```
   انسخ `PAYMENT_URL`، أرسله يدويّاً (واتساب بعد opt-in أو إيميل).
5. **التسليم 7 أيّام** كما هو موصوف في YAML — 10 فرص + مسوّدات عربيّة + خطّة متابعة + Proof Pack.
6. **سجّل ProofEvent** عند كلّ خطوة (`delivery_task_completed` ثم
   `proof_pack_assembled`).
7. **عند الإتمام:** اطلب من العميل توقيع رضا + إذن النشر إن أراد.

### غير مسموح / Not allowed

- ❌ خصم تلقائيّ من بطاقة العميل (لا webhook auto-charge).
- ❌ إرسال بريد جماعيّ.
- ❌ Marketing automation حتى تُعتمَد سياسة في YAML + Decision Pack.

---

## 6. عند 5 عملاء / At 5 customers

- وقّع Decision Pack §S1 (تقاعد Pilot 499 → Pilot 999 لو ثبت العائد).
- ابدأ مرحلة Phase F من الخطّة (role-specific endpoints, content draft engine, search radar).
- ابدأ تجميع شهادات منشورة بإذن العميل.
- لا تُعلن عن "Live" خدمة قبل أن تجتاز 8 gates في YAML.

---

## 7. أين تجد كلّ شيء / Where to find what

| Need | File |
|---|---|
| 32 خدمة + counts | `docs/registry/SERVICE_READINESS_MATRIX.yaml` |
| الـ 10 قرارات مفتوحة | `docs/EXECUTIVE_DECISION_PACK.md` |
| الخطّة الاستراتيجيّة | `docs/STRATEGIC_MASTER_PLAN_2026.md` |
| سجلّ V5 layers | `docs/V5_OS_SCOPE.md` |
| Master evidence | `docs/V5_MASTER_EVIDENCE_TABLE.md` |
| API endpoints | `docs/QUICK_DEPLOY_API_KEYS_ONLY.md` |
| Self-Growth OS scope | `docs/SELF_GROWTH_OS_SCOPE.md` |
| Pricing ladder | `docs/PRICING_STRATEGY.md` |
| Deploy verification | `scripts/post_redeploy_verify.sh` |

---

## 8. آخر تذكير / Final reminder

- **اللغة العربيّة أولاً، الإنجليزيّة ثانية.** كلّ مخرَج للعميل ثنائيّ اللغة.
- **الموافقة قبل أيّ فعل خارجيّ.** ApprovalGate موجودة لسبب — استخدمها.
- **PDPL أوّلاً.** Consent default-deny؛ لا تُسجّل PII بدون redaction.
- **لا تكذب على الكود.** اختبار `xfail` صدقٌ؛ اختبار `pass` مزيّف خيانة.
- **مقياس النجاح:** عميل واحد يدفع 499 ريال طوعاً > 100 لِيد فارغ.

— Founder Runbook v1.0 · 2026-05-04 · Dealix
