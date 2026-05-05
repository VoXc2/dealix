# Phase E — Pilot 7 أيّام يوماً بيوم / 7-Day Pilot Day-by-Day Playbook

> دليل عمليّ يوميّ من Day 0 إلى Day 7 للعميل الأوّل الذي يدفع.
> Operational, day-numbered Phase E playbook — Day 0 through Day 7.
> Read this on Day 0 of your first warm intro. Every step has a `ProofEvent`
> and a `customer_loop` state transition.

**Pre-requisites:**
- v5 deployed (`bash scripts/post_redeploy_verify.sh` returns ✅).
- `MOYASAR_SECRET_KEY` يبدأ بـ `sk_test_` (ليس live).
- Read `docs/V5_PHASE_E_CHECKLIST.md` و `docs/proof-events/ANNOTATED_EXAMPLE.md` أوّلاً.

**Conventions:**
- كلّ `ProofEvent` يُسجَّل بـ `consent_for_publication=false` و `approval_status="approval_required"` افتراضياً.
- اسم العميل الرمزي في الأمثلة: `Acme-Saudi-Pilot-EXAMPLE` (placeholder).
- الإيميل/الجوال في الأمثلة: `ali@example.sa` / `+966500000000` (placeholders).

---

## Day 0 — Diagnostic call + recommendation / مكالمة التشخيص + التوصية

**الهدف / Goal:** تحويل warm intro إلى جلسة تشخيص + تسليم Diagnostic موصى به.

**الأفعال / Actions:**
- [ ] استلم الـ warm intro من شبكتك (3 شركات كحدّ أقصى).
- [ ] اجمع 4 معلومات: اسم الشركة، القطاع، المنطقة، وصف الوضع بسطر واحد.
- [ ] جدول مكالمة 30 دقيقة (5+15+5+5).
- [ ] ولّد المسوّدة:
  ```bash
  python scripts/dealix_diagnostic.py \
    --company "Acme-Saudi-Pilot-EXAMPLE" \
    --sector b2b_services --region riyadh \
    --pipeline-state "WhatsApp incoming, no qualification"
  ```
- [ ] أجرِ المكالمة. صحّح الفجوات الثلاث مع العميل.
- [ ] لا وعود بأرقام. لا خصم.

**ProofEvent:**
- `LEAD_INTAKE` عند استلام الـ intro.
- `DIAGNOSTIC_DELIVERED` بعد المكالمة، مع `summary_ar/en` يلخّص الفجوات.
  - مثال `customer_handle`: `"Acme-Saudi-Pilot-EXAMPLE"`.

**Journey transition:**
- `lead_intake → diagnostic_requested` (قبل المكالمة).
- `diagnostic_requested → diagnostic_sent` (بعد المكالمة).

---

## Day 1 — Pilot offer + invoice / عرض الـ Pilot + الفاتورة

**الهدف / Goal:** قبول العميل لباقة Pilot 499 ريال + إرسال فاتورة Moyasar test-mode.

**الأفعال / Actions:**
- [ ] راسل العميل (يدوياً) برسالة موجزة ثنائية اللغة تحتوي:
  - الـ 3 خيارات من الـ Diagnostic.
  - السعر الثابت: 499 ريال (لا تخفيض).
  - الـ scope: 7 أيّام، 10 فرص مؤهَّلة، Proof Pack نهائي.
- [ ] عند موافقة العميل: تأكّد أنّ Moyasar في test mode:
  ```bash
  python -c "import os; k=os.getenv('MOYASAR_SECRET_KEY','?'); print('test' if k.startswith('sk_test_') else 'LIVE — STOP')"
  ```
- [ ] أنشئ الفاتورة:
  ```bash
  python scripts/dealix_invoice.py \
    --email "ali@example.sa" --amount-sar 499 \
    --description "Dealix Growth Starter Pilot — 7 days"
  ```
- [ ] انسخ `PAYMENT_URL` وأرسله **يدوياً** (واتساب بعد opt-in فقط، أو إيميل).

**ProofEvent:**
- `PILOT_OFFERED` — `summary_ar`: "تمّ عرض Pilot 7 أيّام بقيمة 499 ريال على Acme-Saudi-Pilot-EXAMPLE."
- `INVOICE_PREPARED` — `evidence_source`: `"moyasar_dashboard"`، `payload.invoice_id`.
- (اختياري في نفس اليوم) `PAYMENT_CONFIRMED` لو دفع العميل بنفس اليوم.

**Journey transition:**
- `diagnostic_sent → pilot_offered`.
- `pilot_offered → payment_pending` (بعد إرسال الفاتورة).
- `payment_pending → paid_or_committed` (عند الدفع — قد يكون Day 1 أو Day 2).

---

## Day 2 — 2 opportunities sourced manually / فرصتان يدوياً

**الهدف / Goal:** أوّل فرصتين مؤهَّلتين تُوضَعان في قائمة التسليم.

**الأفعال / Actions:**
- [ ] افتح خطّة التسليم:
  ```bash
  curl -s "https://api.dealix.me/api/v1/delivery-factory/plan/lead_intake_whatsapp" | jq
  ```
- [ ] أنشئ فرصتين يدوياً (لا scraping). معايير: مطابقة سياق العميل + جهة اتّصال معروفة عبر شبكة العميل أو شبكتك.
- [ ] لا مسوّدات بعد — اليوم لجمع الفرص فقط.

**ProofEvent:**
- `DELIVERY_STARTED` (مرّة واحدة في اليوم الأوّل من التسليم).
- `DELIVERY_TASK_COMPLETED` × 2 — كلّ واحد بـ `payload.opportunity_index` و `payload.pilot_day=2`.

**Journey transition:**
- `paid_or_committed → in_delivery` (مرّة واحدة فقط، اليوم الأوّل من التسليم).

---

## Day 3 — 2 more opportunities + Arabic drafts / فرصتان + مسوّدات عربية

**الهدف / Goal:** المجموع 4 فرص + 2 مسوّدات عربية للمراجعة.

**الأفعال / Actions:**
- [ ] أضف فرصتين جديدتين (المجموع 4).
- [ ] اكتب مسوّدتين عربيّتين (Arabic-first) لرسالتين تخاطبان أوّل فرصتين من Day 2.
- [ ] **لا ترسل** — أرسل المسوّدات للعميل للمراجعة فقط.

**ProofEvent:**
- `DELIVERY_TASK_COMPLETED` × 2 (فرص).
- ProofEvent إضافي بـ `event_type=DELIVERY_TASK_COMPLETED` و `payload.kind="draft_created"` × 2.

**Journey transition:**
- ابقَ في `in_delivery`.

---

## Day 4 — 3 more opportunities + drafts approved / 3 فرص + اعتماد المسوّدات

**الهدف / Goal:** المجموع 7 فرص + اعتماد العميل للمسوّدتين الأوليين.

**الأفعال / Actions:**
- [ ] أضف 3 فرص جديدة (المجموع 7).
- [ ] استلم اعتماد العميل الكتابي للمسوّدتين من Day 3.
- [ ] أرسل المسوّدتين **يدوياً** على القناة المتّفق عليها (واتساب بعد opt-in موثَّق، أو إيميل).
- [ ] اكتب مسوّدتين جديدتين للفرصتين التاليتين.

**ProofEvent:**
- `DELIVERY_TASK_COMPLETED` × 3 (فرص).
- ProofEvent بـ `payload.kind="approval_granted"` × 2 — `evidence_source` يشير إلى مكان الاعتماد الكتابي.
- ProofEvent بـ `payload.kind="draft_sent"` × 2.

**Journey transition:**
- ابقَ في `in_delivery`.

---

## Day 5 — 3 more opportunities + customer reviews drafts / 3 فرص + العميل يراجع

**الهدف / Goal:** المجموع 10 فرص (الهدف الكامل) + العميل يراجع المسوّدات الأحدث.

**الأفعال / Actions:**
- [ ] أضف 3 فرص أخيرة (المجموع 10 — هدف Pilot مكتمل).
- [ ] أرسل المسوّدتين الجديدتين (من Day 4) للمراجعة.
- [ ] ابدأ صياغة بقيّة المسوّدات العربية للفرص 5–10.

**ProofEvent:**
- `DELIVERY_TASK_COMPLETED` × 3 (فرص).
- ProofEvent بـ `payload.kind="customer_review_pending"` لكلّ مسوّدة منتظرة.

**Journey transition:**
- ابقَ في `in_delivery`.

---

## Day 6 — Customer approves drafts; founder sends; sign-off draft / إعتماد + إرسال + مسوّدة sign-off

**الهدف / Goal:** إنهاء كلّ الإرسالات + تجهيز sign-off.

**الأفعال / Actions:**
- [ ] استلم الاعتماد الكتابي لبقيّة المسوّدات.
- [ ] أرسل بقيّة الرسائل **يدوياً** (المؤسس فقط — لا automation).
- [ ] جهّز مسوّدة sign-off ثنائية اللغة تلخّص: 10 فرص + مسوّدات + استلامات.
- [ ] أعدّ Proof Pack محلّياً (سيُجمَّع رسمياً في Day 7).

**ProofEvent:**
- ProofEvent بـ `payload.kind="approval_granted"` لكلّ مسوّدة معتمدة.
- ProofEvent بـ `payload.kind="draft_sent"` لكلّ رسالة مرسَلة.
- ProofEvent بـ `event_type=PROOF_PACK_ASSEMBLED` (أوّل تجميع داخلي — `consent_for_publication=false`).

**Journey transition:**
- `in_delivery → proof_pack_ready` (في نهاية اليوم بعد إرسال آخر رسالة).

---

## Day 7 — Proof Pack assembled + sent + upsell call scheduled / Proof Pack نهائي + موعد upsell

**الهدف / Goal:** Proof Pack موقَّع + إرساله + جدولة مكالمة upsell.

**الأفعال / Actions:**
- [ ] جمّع Proof Pack النهائي:
  ```bash
  curl -X POST https://api.dealix.me/api/v1/self-growth/proof-pack/assemble \
    -H 'content-type: application/json' \
    -d "$(jq -n --arg ch 'Acme-Saudi-Pilot-EXAMPLE' \
      --argjson events "$(jq -s 'map(.)' docs/proof-events/*.jsonl)" \
      '{customer_handle:$ch,events:$events,consent_for_publication:false}')"
  ```
- [ ] أرسل الـ Proof Pack للعميل (PDF + ملخّص ثنائي اللغة).
- [ ] اطلب رضا صريح: هل يستحقّ الـ 499 ريال؟
- [ ] إن قبِل العميل، اعرض Executive Growth OS (2,999 ريال/شهر) — جدول مكالمة upsell.
- [ ] إن رفض، انتقل إلى `nurture` بعد 90 يوماً.

**ProofEvent:**
- `PROOF_PACK_ASSEMBLED` (نسخة نهائية — `evidence_source="proof_pack_assembler"`).
- `PROOF_PACK_SENT` (مع `payload.delivery_channel`).
- `UPSELL_RECOMMENDED` (إذا وافق العميل على المكالمة).

**Journey transition:**
- `proof_pack_ready → proof_pack_sent`.
- `proof_pack_sent → upsell_recommended` (إن جدول العميل المكالمة).
- أو `proof_pack_sent → nurture` (إن رفض).

---

## ملخّص الانتقالات / Transition summary

| اليوم | from_state | → | to_state |
|---|---|---|---|
| Day 0 | `lead_intake` | → | `diagnostic_requested` → `diagnostic_sent` |
| Day 1 | `diagnostic_sent` | → | `pilot_offered` → `payment_pending` |
| Day 1/2 | `payment_pending` | → | `paid_or_committed` |
| Day 2 | `paid_or_committed` | → | `in_delivery` |
| Day 3–5 | `in_delivery` | (stay) | `in_delivery` |
| Day 6 | `in_delivery` | → | `proof_pack_ready` |
| Day 7 | `proof_pack_ready` | → | `proof_pack_sent` → `upsell_recommended` / `nurture` |

---

## Hard rules طول الـ 7 أيّام / Rules that hold every day

- ❌ لا scraping، لا cold blast، لا automation للإرسال — المؤسس يرسل بنفسه.
- ❌ لا `نضمن` / لا `guaranteed` في أيّ نص.
- ❌ لا اسم عميل حقيقي في `docs/proof-events/` بدون موافقة كتابية → استخدم `Acme-Saudi-Pilot-EXAMPLE` placeholder حتّى ذلك الحين.
- ✅ كلّ ProofEvent: `consent_for_publication=false` و `approval_status="approval_required"` افتراضياً.
- ✅ كلّ Pilot عند 499 ريال ثابت حتّى العميل #5.
- ✅ Arabic-first في كلّ مسوّدة + الإنجليزية ثانوية.

— Phase E Day-by-Day v1.0 · 2026-05-04 · Dealix
