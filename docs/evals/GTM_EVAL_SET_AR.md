# مجموعة تقييم GTM — GTM Eval Set

تُوثّق هذه الوثيقة حالات التقييم في `data/evals/gtm_draft_eval_cases.jsonl` التي
تتحقّق من بوّابة جودة المسودّات (draft quality gate). كل حالة موسومة بالنتيجة
المتوقّعة (`pass`/`fail`) وسبب الرفض (`reason_code`)، ويُشغّلها:
- المحرّك التنفيذي: `node scripts/draft-quality-gate.js --eval`
- الاختبار المرجعي: `tests/test_gtm_quality_gate.py`

> المحركان (Node + Python) يتقاطعان على نفس الحالات لضمان عدم انحراف القواعد.

## الحالات

| case_id | المتوقّع | السبب | ماذا تثبت |
|---------|---------|-------|-----------|
| GD-PASS-01 | pass | ok | مسودّة P2 سليمة مع opt-out وبلا ادّعاءات ممنوعة |
| GD-FAIL-CLAIM-AR | fail | forbidden_claim | «نضمن زيادة المبيعات … بدون أي مخاطرة» تُرفض |
| GD-FAIL-CLAIM-EN | fail | forbidden_claim | "10x revenue … guaranteed results" تُرفض |
| GD-FAIL-NO-OPTOUT | fail | missing_unsubscribe | مسودّة باردة بلا opt-out تُرفض |
| GD-FAIL-P0 | fail | below_p1 | تخصيص دون P1 يُرفض من طابور الموافقة |
| GD-FAIL-FAKE-RE | fail | fake_thread | عنوان `Re:` وهمي على بريد بارد يُرفض |
| GD-FAIL-SUPPRESSED | fail | suppressed | مستلِم على قائمة الكتم لا يصبح قابلاً للإرسال |
| GD-FAIL-MISSING-FIELD | fail | missing_required_field | غياب حقل إلزامي (مثل offer_match) يُرفض |

## البوّابات السبع التي تطبّقها كل حالة
brand/claims · offer match · personalization (≥P1) · compliance/opt-out ·
evidence · deliverability/suppression · security (الحقول الإلزامية).

## كيفية التشغيل
```bash
node scripts/draft-quality-gate.js --eval   # 8/8 OK, 0 mismatches
pytest tests/test_gtm_quality_gate.py -q
```

> أي تعديل على القواعد يتطلّب تحديث الحالات + الاختبارات معاً (لا حذف اختبارات لتمريرها).
