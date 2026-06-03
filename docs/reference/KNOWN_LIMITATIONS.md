# Known Limitations · القيود المعروفة

> سجل واحد لكل `NotImplementedError`, `TODO`, feature flag مغلق، أو ستب. يحدّث مع كل PR يضيف/يحل قيد.
>
> **آخر تحديث:** 2026-05-28

---

## 1) Stubs / NotImplementedError

### 1.1 DesignOps Exporter — PDF/PPTX
- **الملف:** `auto_client_acquisition/designops/exporter.py:124`
- **السلوك الحالي:** يرفع `NotImplementedError` لو `format="pdf"` أو `format="pptx"`.
- **المتاح:** `markdown` و `html`.
- **خطة الحل:** أضف `weasyprint` لـ PDF و `python-pptx` لـ PPTX لما يكون فيه طلب عميل حقيقي. ETA: عند أول عميل enterprise.

### 1.2 Observability Adapters Base
- **الملف:** `auto_client_acquisition/observability_adapters/base.py:57`
- **السلوك:** `NotImplementedError` في abstract method `emit`.
- **النوع:** abstract base class (مقصود). كل subclass (Sentry, Datadog) يحدد `emit`.
- **خطة:** لا إصلاح — هذا تصميم سليم.

---

## 2) TODOs (production action items)

### 2.1 Auth — Invite Email Delivery
- **الملف:** `api/routers/auth.py:501`
- **السلوك:** يولّد `invite_token` لكن لا يرسل email.
- **حالياً:** الـ token يطبع في log + يرجع في response (لـ founder use).
- **خطة:** SendGrid/SES integration. ETA: قبل أول customer-facing signup.

### 2.2 Customer Success — Drafts Approved Query
- **الملف:** `api/routers/customer_success.py:126`
- **السلوك:** `drafts_approved_last_30d=0` (hardcoded).
- **التأثير:** customer success score يفقد بعد signal.
- **خطة:** اربط بـ `approval_center.approval_store`. ETA: عند أول managed-ops customer.

---

## 3) Feature Flags (gates للحماية doctrine — مقصود مغلق)

| Flag | Default | ENV | يحرس |
|------|---------|-----|------|
| `whatsapp_allow_live_send` | `False` | `WHATSAPP_ALLOW_LIVE_SEND=1` | doctrine #1 (no_live_send) |
| `email_allow_live_send` | `False` | `EMAIL_ALLOW_LIVE_SEND=1` | doctrine #1 |
| `linkedin_allow_live_send` | `False` (دائماً) | لا يفعّل | doctrine #11 (no_linkedin_automation) |
| `DEALIX_STRICT_OPTIONAL_ROUTERS` | `False` | `=1` في dev | يفشل startup لو optional router failed |

**قاعدة:** لا تفعّل live-send flag بدون approval workflow كامل + audit chain.

---

## 4) Integrations في حالة "configured-but-gated"

كل integration يفحص `configured` ثم يفحص `allow_live_send`:

```python
# مثال من integrations/whatsapp.py
if not self.configured:
    return Result(success=False, error="not_configured")
if not self.settings.whatsapp_allow_live_send:
    return Result(success=False, error="blocked_by_policy")
```

النتيجة: لو لقيت `blocked_by_policy` في log → النظام يحترم doctrine. لو لقيت `not_configured` → ضع المفاتيح في `.env`.

---

## 5) Optional Routers (قد تفشل بصمت قبل الإصلاح)

تم تحسين logging في `api/main.py` — الآن أي router optional فشل استيراده يطبع traceback كامل في log level=error.

**Routers المتأثرة (defensive imports):**
- `api.routers.value_os`
- `api.routers.data_os`
- `api.routers.agent_os`

**Strict mode للـ dev:**
```bash
export DEALIX_STRICT_OPTIONAL_ROUTERS=1
make run  # يفشل startup لو أي optional router عنده خطأ
```

---

## 6) Duplication Cleanup (تم — لا duplicates متبقية)

تم حذف 4 directories مكررة/مهجورة:

| العنصر | الحجم | السبب |
|--------|------|------|
| `dealix-v2/` | 60K | parallel Python rewrite، صفر imports |
| `dashboard/` | minor | Streamlit stub، صفر workflow refs |
| `migrations/` | 8 ملفات | reference DDLs مكررة من `db/migrations/` |
| `dealix-1.worktrees/` | 8K | empty worktree scaffolding |
| `DASHBOARD.md` | root | orphan doc لـ dashboard المحذوف |

**ابقاء (مقصود):**
- `frontend/` = customer-facing Next.js (i18n، login، offer، portal، checkout)
- `apps/web/` = enterprise admin UI (control plane، agents، sandbox، safety)

كلاهما مبني في `.github/workflows/ci.yml` و CODEOWNERS و railway_deploy_frontend.yml.

---

## 7) Coverage Gate

- **الآن:** `--cov-fail-under=70` في `.github/workflows/ci.yml`.
- **الهدف:** 80% خلال 30 يوم.
- **القيد:** بعض الـ routers الكبيرة (agent_os, value_os) تحتاج tests إضافية.

---

## 8) Observability Gaps

- `SENTRY_DSN` فاضي في `.env.example` — لازم يتعبى في prod.
- لا يوجد uptime monitor خارجي مفعّل (BetterStack/UptimeRobot). الـ HEALTHCHECK في `Dockerfile` تكتفي بـ container-level.
- OpenTelemetry traces موجودة (`setup_tracing` في `dealix.observability`) لكن `OTEL_EXPORTER_*` ENVs غير موثقة في `.env.example`.

---

## كيف تضيف قيد جديد

1. أضف entry هنا في القسم الصحيح
2. ارفع PR مع `chore(known-limits): add <thing>` في الـ title
3. لو القيد blocking لإطلاق → أضفه أيضاً في `FOUNDER_NEXT_STEPS.md §6`
