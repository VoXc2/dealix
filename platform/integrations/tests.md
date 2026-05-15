# العربية

## مواصفة اختبارات الطبقة السادسة — التنفيذ والتكاملات

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

هذه مواصفة اختبار مكتوبة — حالات اختبار ومعايير قبول، دون شيفرة. كل حالة قابلة للتنفيذ في وضع sandbox دون لمس بيانات عميل حقيقية.

### مجموعة 1 — واجهة الموصّلات والموثوقية

- **T1.1 المهلة الزمنية:** نداء يتجاوز `timeout_s` يُجهَض. **القبول:** يُرجَع `ConnectorResult.ok = false` خلال المهلة، ولا يُعلَّق سير العمل.
- **T1.2 إعادة المحاولة بالتراجع:** فشل عابر متبوع بنجاح. **القبول:** ينجح خلال `max_retries`، و`attempts` > 1، والتأخير أسّي.
- **T1.3 الفشل النهائي إلى DLQ:** فشل في كل المحاولات. **القبول:** يُدفَع عنصر إلى طابور `outbound` بـ `error` و`attempts` صحيحين.
- **T1.4 قاطع الدائرة يفتح:** 5 أخطاء متتالية. **القبول:** يُرجَع `circuit_open` فوراً للنداء التالي دون استدعاء المزوّد.
- **T1.5 قاطع الدائرة نصف مفتوح:** بعد التهدئة. **القبول:** يُسمح بنداء تجريبي واحد؛ النجاح يغلق القاطع.
- **T1.6 الموصّل المعطّل:** `ConnectorPolicy.allow = false`. **القبول:** يُرجَع `connector_disabled_by_policy` دون نداء خارجي.

### مجموعة 2 — عدم التكرار

- **T2.1 مفتاح ثابت:** نفس الحمولة تُنتج نفس مفتاح عدم التكرار. **القبول:** `_idem_key` متطابق لمدخلات متطابقة.
- **T2.2 المطالبة الذرّية:** نداءان متزامنان بنفس المفتاح. **القبول:** `claim` ينجح مرة واحدة فقط؛ الثاني يُتعرَّف عليه كمكرر.
- **T2.3 الحدث المكرر يُتجاهَل:** نفس خطاف الويب مرتين. **القبول:** المعالجة الثانية تُرجِع "مكرر" دون أثر جانبي.

### مجموعة 3 — أمان خطافات الويب

- **T3.1 توقيع صالح:** خطاف واتساب بتوقيع صحيح. **القبول:** `verify_signature` تُرجِع `true` ويُعالَج الحدث.
- **T3.2 توقيع غير صالح:** توقيع مزوّر. **القبول:** `verify_signature` تُرجِع `false`، تُرجَع 401، ولا معالجة.
- **T3.3 تحقق GET:** رمز تحقّق صحيح. **القبول:** `verify_webhook` تُعيد التحدّي؛ رمز خاطئ يُعيد `None`.
- **T3.4 فشل المعالجة بعد التحقق:** خطأ بعد توقيع صالح. **القبول:** يُدفَع إلى `WEBHOOKS_DLQ` دون فقدان الحدث.

### مجموعة 4 — الموافقة والحوكمة

- **T4.1 الإرسال الخارجي يتطلب موافقة:** إجراء `external_send` غير معتمد. **القبول:** القرار `require_approval`؛ لا إرسال فعلي.
- **T4.2 منع واتساب البارد:** مستلم دون علاقة قائمة. **القبول:** القرار `block` عبر `no_cold_whatsapp`.
- **T4.3 المسودة فقط في sandbox:** `whatsapp_allow_live_send = false`. **القبول:** تُرجَع `whatsapp_allow_live_send_false` دون نداء API.
- **T4.4 لا أسرار في السجلات:** فحص السجلات وقيد التدقيق. **القبول:** لا يظهر رمز أو مفتاح خام في أي سطر.

### مجموعة 5 — حدود المعدّل

- **T5.1 الحد لكل موصّل:** تجاوز `max_calls_per_minute`. **القبول:** يُخنَق النداء أو يُؤخَّر، ويُسجَّل.
- **T5.2 الموصّل غير المُدرَج:** موصّل بلا سياسة صريحة. **القبول:** يأخذ `ConnectorPolicy` الافتراضية.

### مجموعة 6 — قابلية التتبّع

- **T6.1 قيد تدقيق لكل نداء:** نداء ناجح وفاشل. **القبول:** كلاهما يظهر في `audit_tail()` بـ `connector` و`operation` و`ok`.
- **T6.2 تتبّع 99%:** عيّنة من النداءات. **القبول:** ≥ 99% منها له قيد تدقيق مطابق.

### معايير القبول العامة

- لا تمر أي حالة إلا في وضع sandbox أولاً.
- أي فشل تكامل يجب ألا يكسر سير العمل المستدعي.
- كل إرسال خارجي يبقى مسودة حتى موافقة موثّقة.

---

# English

## Layer 6 Test Specification — Execution and Integrations

**Owner:** Integrations Platform Lead.

This is a written test specification — test cases and acceptance criteria, no code. Every case is runnable in sandbox mode without touching real customer data.

### Group 1 — Connector facade and reliability

- **T1.1 Timeout:** a call exceeding `timeout_s` is aborted. **Acceptance:** `ConnectorResult.ok = false` is returned within the timeout, and the workflow is not hung.
- **T1.2 Backoff retry:** a transient failure followed by success. **Acceptance:** succeeds within `max_retries`, `attempts` > 1, and delay is exponential.
- **T1.3 Final failure to DLQ:** failure on all attempts. **Acceptance:** an item is pushed to the `outbound` queue with correct `error` and `attempts`.
- **T1.4 Circuit breaker opens:** 5 consecutive errors. **Acceptance:** `circuit_open` is returned immediately for the next call without calling the provider.
- **T1.5 Circuit breaker half-open:** after cooldown. **Acceptance:** one trial call is allowed; success closes the breaker.
- **T1.6 Disabled connector:** `ConnectorPolicy.allow = false`. **Acceptance:** `connector_disabled_by_policy` is returned with no external call.

### Group 2 — Idempotency

- **T2.1 Stable key:** the same payload produces the same idempotency key. **Acceptance:** `_idem_key` is identical for identical inputs.
- **T2.2 Atomic claim:** two concurrent calls with the same key. **Acceptance:** `claim` succeeds exactly once; the second is recognized as a duplicate.
- **T2.3 Duplicate event ignored:** the same webhook twice. **Acceptance:** the second processing returns "duplicate" with no side effect.

### Group 3 — Webhook security

- **T3.1 Valid signature:** a WhatsApp webhook with a correct signature. **Acceptance:** `verify_signature` returns `true` and the event is processed.
- **T3.2 Invalid signature:** a forged signature. **Acceptance:** `verify_signature` returns `false`, 401 is returned, and no processing.
- **T3.3 GET verification:** a correct verify token. **Acceptance:** `verify_webhook` returns the challenge; a wrong token returns `None`.
- **T3.4 Processing failure after verification:** an error after a valid signature. **Acceptance:** pushed to `WEBHOOKS_DLQ` without losing the event.

### Group 4 — Approval and governance

- **T4.1 External send requires approval:** an unapproved `external_send` action. **Acceptance:** decision is `require_approval`; no actual send.
- **T4.2 Cold WhatsApp blocked:** a recipient with no existing relationship. **Acceptance:** decision is `block` via `no_cold_whatsapp`.
- **T4.3 Draft-only in sandbox:** `whatsapp_allow_live_send = false`. **Acceptance:** `whatsapp_allow_live_send_false` is returned with no API call.
- **T4.4 No secrets in logs:** inspect logs and the audit log. **Acceptance:** no raw token or key appears in any line.

### Group 5 — Rate limits

- **T5.1 Per-connector limit:** exceeding `max_calls_per_minute`. **Acceptance:** the call is throttled or delayed, and logged.
- **T5.2 Unlisted connector:** a connector with no explicit policy. **Acceptance:** takes the default `ConnectorPolicy`.

### Group 6 — Traceability

- **T6.1 Audit entry per call:** a successful and a failed call. **Acceptance:** both appear in `audit_tail()` with `connector`, `operation`, and `ok`.
- **T6.2 99% traceability:** a sample of calls. **Acceptance:** >= 99% of them have a matching audit entry.

### General acceptance criteria

- No case passes without running in sandbox mode first.
- Any integration failure must not break the calling workflow.
- Every external send stays a draft until documented approval.
