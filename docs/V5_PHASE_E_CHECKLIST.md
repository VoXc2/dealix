# Phase E — قائمة فحص أوّل عميل يدفع / First Paying Customer Checklist

> دليل عمليّ خطوة-بخطوة لتحويل أوّل warm intro إلى عميل يدفع 499 ريال.
> One-page operational checklist to convert your first warm intro into
> a paying 499 SAR pilot customer.

**Pre-requisite:** v5 production deployed (✅ if `bash scripts/post_redeploy_verify.sh` returns verdict ✅).

---

## 0. القاعدة الأولى / Ground rules

| ❌ ممنوع | ✅ مسموح |
|---|---|
| Cold WhatsApp / cold email / DM آليّ | Warm intros من شبكتك فقط |
| Scraping / قوائم مشتراة | Inbound + warm referral |
| ضمان أرقام أو ترتيب | "نلتزم بـ Pilot 7 أيّام + Proof Pack" |
| خصم آليّ | فاتورة Moyasar test mode، إرسال يدويّ |
| 100+ contacts | 3 warm intros ≤ |
| تخفيض السعر | 499 ريال ثابت حتّى العميل #5 |

---

## 1. قبل أيّ تواصل / Before any outreach

- [ ] **حدّد 3 شركات من شبكتك المباشرة** (لا قوائم مشتراة، لا LinkedIn auto).
  - معايير: B2B، KSA-based، 5-50 موظف، مسوّق/مالك/CEO معروف لك شخصيّاً.
  - **سجّلهم في ملاحظة خاصّة** — لا تكتبهم في أيّ مكان مشترك حتّى يوافقوا.
- [ ] **تحقّق من حالة المنظومة:**
  ```bash
  python scripts/dealix_status.py
  ```
  لازم كلّ Live-action gate يقول `BLOCKED` و Reliability `overall: ok`.

---

## 2. التواصل الأوّل / First contact (per prospect)

- [ ] **رسالة ثنائيّة اللغة موجزة** (≤ 3 سطر) — عربيّ أوّلاً، إنجليزيّ ثانياً.
  - مثال:
    > "السلام عليكم [اسم]، أعمل على Dealix — منصّة تنفيذيّة للعمل B2B في السعوديّة.
    > أعرض Diagnostic مجانيّ 30 دقيقة يكشف الفجوات في قمعكم. هل تناسب الأربعاء 4 عصراً؟
    > Quick note: Dealix is a Saudi B2B revenue OS; offering a free 30-min Diagnostic. Wed 4PM?"
- [ ] **انتظر ردّاً** — لا متابعة قبل 48 ساعة. متابعة واحدة فقط لو لم يردّ.

---

## 3. ولّد الـ Diagnostic / Generate the Diagnostic

عند موافقة العميل على جلسة:

- [ ] **اجمع 4 معلومات قبل الجلسة:**
  - اسم الشركة بالضبط
  - القطاع: واحد من `b2b_services | b2b_saas | agency | training_consulting | local_services`
  - المنطقة: `riyadh | jeddah | dammam | ksa`
  - وصف الوضع الحاليّ بسطر واحد (مثلاً: "WhatsApp incoming, no qualification, founder responds at night").
- [ ] **شغّل المولّد:**
  ```bash
  python scripts/dealix_diagnostic.py \
    --company "اسم الشركة" \
    --sector b2b_services \
    --region riyadh \
    --pipeline-state "وصف الوضع"
  ```
- [ ] **راجع المسوّدة كاملة** قبل الجلسة. عدّل الفجوات الثلاث ليلائم وضع العميل.
- [ ] **تقدّم في الـ journey:**
  ```bash
  curl -X POST https://api.dealix.me/api/v1/customer-loop/journey/advance \
    -H 'content-type: application/json' \
    -d '{"current_state":"lead_intake","target_state":"diagnostic_requested","customer_handle":"<handle>"}'
  ```

---

## 4. الجلسة 30 دقيقة / The 30-min session

- [ ] **جدول الجلسة:**
  - 5 دقائق — تعارف + سياق العميل
  - 15 دقيقة — أنت تقرأ الـ Diagnostic + يصحّح العميل الفجوات
  - 5 دقائق — توضيح Pilot (الـ 7 أيّام + 499 ريال)
  - 5 دقائق — قرار العميل (3 خيارات في المسوّدة)
- [ ] **لا** تعد بأرقام محدّدة. **لا** تخصم السعر.
- [ ] **سجّل القرار** في docs/proof-events/<slug>.json (أو على الأقلّ في ملاحظة خاصّة).
- [ ] **تقدّم في الـ journey:**
  - `diagnostic_requested → diagnostic_sent`
  - إذا قبل: `diagnostic_sent → pilot_offered`

---

## 5. الفاتورة / Invoice

عند قول "نعم":

- [ ] **تأكّد** أنّ `MOYASAR_SECRET_KEY` يبدأ بـ `sk_test_` (test mode، ليس live):
  ```bash
  python -c "import os; k=os.getenv('MOYASAR_SECRET_KEY','?'); print('test' if k.startswith('sk_test_') else 'LIVE — STOP')"
  ```
- [ ] **اصنع فاتورة:**
  ```bash
  python scripts/dealix_invoice.py \
    --email "customer@example.sa" \
    --amount-sar 499 \
    --description "Dealix Growth Starter Pilot — 7 days"
  ```
- [ ] **انسخ `PAYMENT_URL`** وأرسله يدويّاً (واتساب بعد opt-in، أو إيميل).
- [ ] **لا** ترسله من أيّ ماكينة آليّة. أنت ترسل بنفسك.
- [ ] **تقدّم:** `pilot_offered → payment_pending`.

---

## 6. تأكيد الدفع / Payment confirmation

- [ ] **راقب لوحة Moyasar** (لا webhook auto-charge).
- [ ] لمّا يدفع: `payment_pending → paid_or_committed`.
- [ ] **سجّل ProofEvent:**
  ```python
  from auto_client_acquisition.proof_ledger import (
      FileProofLedger, ProofEvent, ProofEventType,
  )
  FileProofLedger().record(ProofEvent(
      event_type=ProofEventType.PAYMENT_CONFIRMED,
      customer_handle="<handle>",
      summary_ar="استلام دفعة Pilot — 499 ريال.",
      summary_en="Pilot payment received — 499 SAR.",
      evidence_source="moyasar_dashboard",
      consent_for_publication=False,
  ))
  ```

---

## 7. التسليم 7 أيّام / 7-day delivery

اقرأ خطّة التسليم من YAML:

```bash
curl -s "https://api.dealix.me/api/v1/delivery-factory/plan/lead_intake_whatsapp" | jq
```

كلّ يوم:

- [ ] **شغّل Diagnostic CLI لمتابعة Pilot** — اعرف ما المتبقّي.
- [ ] **سلّم 1-2 من الـ 10 فرص** (مسوّدة عربيّة، مراجعة، إرسال يدويّ بإذن العميل).
- [ ] **سجّل ProofEvent يوميّاً:** `delivery_task_completed`.
- [ ] **تقدّم:** `paid_or_committed → in_delivery` (مرّة واحدة في اليوم الأوّل).

اليوم 7:

- [ ] **اجمع Proof Pack:**
  ```bash
  curl -X POST https://api.dealix.me/api/v1/self-growth/proof-pack/assemble \
    -H 'content-type: application/json' \
    -d "$(jq -n --arg ch '<handle>' --argjson events "$(jq -s 'map(.)' docs/proof-events/*.jsonl)" \
      '{customer_handle:$ch,events:$events,consent_for_publication:false}')"
  ```
- [ ] **تقدّم:** `in_delivery → proof_pack_ready → proof_pack_sent`.

---

## 8. ما بعد الـ Pilot / Post-pilot

- [ ] **اطلب رضا العميل بصراحة** — هل يستحقّ الـ 499؟ هل تكرّرها؟
- [ ] **اطلب إذن نشر** اسمه في Proof Pack عام (اختياريّ، لا ضغط).
- [ ] **اعرض Executive Growth OS** (2,999 ريال/شهر، شهر واحد بدون التزام):
  - `proof_pack_sent → upsell_recommended`
- [ ] **إذا رفض:** `upsell_recommended → nurture` (90 يوم بين كلّ تواصل).
- [ ] **إذا قبل:** اصنع فاتورة شهريّة جديدة.

---

## 9. التوثيق النهائيّ / Final documentation

- [ ] **اقرأ Decision Pack §S1** — هل وصلت لـ 5 عملاء؟ إن نعم، انتقل لمرحلة الترقية.
- [ ] **حدّث `docs/proof-events/`** — كلّ event موجود وموقَّع.
- [ ] **شغّل smoke test:** `python scripts/dealix_smoke_test.py` — كلّ شيء أخضر.
- [ ] **افتح Issue في GitHub** بعنوان "First paying customer — closure" يحتوي:
  - تاريخ الـ Pilot
  - حالة الـ journey النهائيّة
  - عدد الـ ProofEvents المسجَّلة
  - قرار العميل: upsell / nurture / no
  - **بدون اسم العميل** (إلّا بإذن صريح).

---

## 10. ⚠️ علامات الخطر / Red flags

| إشارة | افعل فوراً |
|---|---|
| Moyasar key يبدأ بـ `sk_live_` | ⛔ توقّف. ارجع إلى test mode. |
| العميل يطلب ضمان أرقام | اشرح لماذا لا نضمن. إن أصرّ، رفض الصفقة. |
| ضغط لتخفيض السعر | 499 ثابت. اشرح أنّه سعر تعريفيّ يُقفل عند العميل #5. |
| طلب scraping أو cold blast | ❌ سياسة Dealix لا تسمح. ارفض بأدب. |
| تأخّر دفع > 7 أيّام بعد الفاتورة | متابعة واحدة لطيفة. لا automation. |
| العميل يطلب refund | اقبل. سجّل ProofEvent: `risk_blocked`. تعلّم. |

---

## أدوات مرجعيّة / Reference tools

| أداة | استخدام |
|---|---|
| `python scripts/dealix_status.py` | لقطة سريعة لكلّ شيء |
| `python scripts/dealix_diagnostic.py --list-bundles` | استعرض الباقات + قطاعاتها |
| `python scripts/dealix_diagnostic.py --company X --sector Y --region Z --pipeline-state W` | ولّد مسوّدة Diagnostic |
| `python scripts/dealix_invoice.py --email A --amount-sar 499 --description "..."` | اصنع فاتورة Moyasar |
| `bash scripts/post_redeploy_verify.sh` | تحقّق من Production |
| `python scripts/dealix_smoke_test.py` | smoke test Python (cross-platform) |

---

## معيار النجاح / Success criterion

✅ **عميل واحد دفع 499 ريال طوعاً + Proof Pack موقَّع.**

هذا أهمّ من 100 لِيد فارغ. بعد هذا العميل، نراجع Decision Pack §S1.

— Phase E Checklist v1.0 · 2026-05-04 · Dealix
