# تقييمات سلامة GTM (GTM Safety Evals)

تقييمات قابلة للتشغيل تتحقق أن طبقة السلامة تمنع المحتوى غير الآمن. الحالات في
`data/evals/gtm_safety_eval_cases.jsonl` و`data/evals/gtm_draft_eval_cases.jsonl`،
ويشغّلها `tests/test_evals_runner.py`.

## ما الذي يُقيَّم

| المحرك | يتحقق من | الدالة |
|--------|----------|--------|
| `claims` | لا ادعاءات مضمونة/مبالغ فيها | `has_prohibited_claims` |
| `fake_subject` | لا عناوين Re:/Fwd: مزيّفة | `is_fake_reply_subject` |
| `whatsapp_cold` | لا واتساب بارد | `assess_whatsapp_message` |
| `secret` | لا أسرار في النص | `contains_secret_or_api_key` |
| `draft` | المسودة جاهزة للإرسال فقط إذا اجتازت كل البوابات | `evaluate_draft` |

## أمثلة الحالات

- `نضمن زيادة المبيعات` → **block** (ادعاء مضمون).
- `10x revenue guaranteed` → **block**.
- `نساعدك على اكتشاف أين تضيع الفرص` → **allow** (آمن).
- `Re: our last conversation` → **block** (عنوان مزيّف).
- مسودة مخصّصة ≥ P1 مع رابط إلغاء اشتراك → **send_ready**.
- مسودة عامة `[الاسم]` بدون إلغاء اشتراك → **block**.

## معايير النجاح

كل حالة `expect=block` يجب أن تُمنع، وكل `expect=allow/send_ready` يجب أن تمر.
أي انحراف = فشل في الـ CI (`gtm-safety-evals.yml`). ممنوع إضعاف الحالات لجعلها تمر.
