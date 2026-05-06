# Dealix — وضع الحقيقة (Revenue-first، لا V13)

هذا المستند **ليس إصدار منتج**. هو تجميد قرار: **لا V13 قبل إثبات إيراد حقيقي** (دفع أو التزام مكتوب أو جلسة تسليم مسجّلة مع أحداث proof).

**آخر تحديث تلقائي للريبو (وكيل):** يُحدَّث عند كل تشغيل لـ `scripts/revenue_execution_verify.sh` أو يدوياً.

---

## 1) Git (محلي مقابل `origin/main`)

| الحقل | قيمة (مثال من آخر تشغيل) |
|--------|---------------------------|
| الفرع الحالي | `cursor/revenue-execution-a8b4` (أو الفرع الذي تعمل عليه) |
| `HEAD` المحلي | `8552a99` (يُستبدل عند الدمج) |
| `origin/main` | يجب أن يطابق ما يُنشر للإنتاج بعد الدمج |

نفّذ محلياً:

```bash
git fetch origin main && git rev-parse HEAD && git rev-parse origin/main
git status -sb
```

---

## 2) الإنتاج (`api.dealix.me`) مقابل الريبو

| الحقل | ملاحظة |
|--------|--------|
| `GET https://api.dealix.me/health` | يعيد `git_sha` للبناء المنشور |
| تطابق `main` | إذا `git_sha` الإنتاج ≠ `origin/main` فالإنتاج **متأخر** — لا تبنِ V13؛ **أعد النشر** ثم أعد smoke |

**مثال لقطعة صحية (قد تتغير):**

```json
{"status":"ok","version":"3.0.0","env":"production","git_sha":"8099b00"}
```

إذا كان `8099b00` بينما `main` عند `8552a99` → **REDEPLOY_REQUIRED=yes**.

---

## 3) ما هو موجود في الريبو (تحقق، لا افتراض تقرير خارجي)

| أداة | المسار |
|------|--------|
| Smoke إنتاج | [`scripts/launch_readiness_check.py`](scripts/launch_readiness_check.py) مع `STAGING_BASE_URL=https://api.dealix.me` |
| تجميع CEO يومي | `GET /api/v1/full-ops/daily-command-center` — [`api/routers/revenue_execution.py`](../api/routers/revenue_execution.py) |
| Personal Operator | [`api/routers/personal_operator.py`](../api/routers/personal_operator.py) |
| Command Center v3 | [`api/routers/v3.py`](../api/routers/v3.py) |
| Inbox (مسودات) | [`api/routers/customer_inbox_v10.py`](../api/routers/customer_inbox_v10.py) |
| Proof | [`api/routers/proof_ledger.py`](../api/routers/proof_ledger.py) |
| Delivery plans | [`api/routers/delivery_factory.py`](../api/routers/delivery_factory.py) |
| موحّد التحقق | [`scripts/revenue_execution_verify.sh`](../scripts/revenue_execution_verify.sh) |

**غير موجود في الريبو (لا تُنسب لـ CI هنا):** `scripts/v11_customer_closure_verify.sh`, `scripts/v12_full_ops_verify.sh`, أرقام ثابتة مثل `1626 passed` إلا إذا شغّلت `pytest` ونسخت الناتج إلى هذا الملف.

---

## 4) Hard gates (سياسة — لا تُخفّف)

- لا إرسال حي خارجي بدون موافقة صريحة.
- لا شحن Moyasar live بدون بوابة معتمدة.
- لا cold WhatsApp، لا scraping، لا أتمتة LinkedIn وهمية.
- لا proof أو إيراد أو شهادة مزيفة.

---

## 5) الخطوة التالية للمؤسس (أمر واحد)

**إذا الإنتاج متأخر:** دمج `main` → نشر Railway/البيئة الخاصة بك → `STAGING_BASE_URL=https://api.dealix.me python scripts/launch_readiness_check.py` → حدّث قسم §2 أعلاه.

**إذا الإنتاج متطابق:** افتح `GET /api/v1/full-ops/daily-command-center` واتبع [`docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md`](14_DAY_FIRST_REVENUE_PLAYBOOK.md).

---

## 6) الخطوة التالية للهندسة (أمر واحد)

**لا تفتح PR باسم V13.** أي توسعة بعد أول عميل = **V12.1** وفق [`docs/V12_1_TRIGGER_RULES.md`](V12_1_TRIGGER_RULES.md).
