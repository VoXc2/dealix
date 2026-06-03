# مراجعة بوّابات المسودّات — Draft Gate Review (TEMPLATE)

> **قالب.** يُملأ يومياً الساعة 09:00 من `node scripts/draft-quality-gate.js`.
> **شرط صارم:** `forbidden_claim_hits = 0`. أي مسودّة فاشلة لا تدخل طابور الموافقة.
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`

- **التاريخ:** `YYYY-MM-DD`
- **المفحوص:** `<count>` مسودّة
- **الأمر:** `node scripts/draft-quality-gate.js` (و`--eval` لحالات الاختبار)

---

## 1. ملخّص النتائج (Pass/Fail Summary)

| المؤشّر | القيمة |
|---------|--------|
| المفحوص | `0` |
| الناجح (PASS) | `0` |
| الفاشل (FAIL) | `0` |
| **`forbidden_claim_hits`** | **`0`** (شرط صارم) |

---

## 2. النتيجة لكل بوّابة (Per-Gate)

| # | البوّابة | `reason_code` | فشل | الحالة |
|---|----------|----------------|-----|--------|
| 1 | brand gate | `forbidden_claim` | `0` | ✅ |
| 2 | offer/required-fields | `missing_required_field` | `0` | ✅ |
| 3 | personalization (P1 floor) | `below_p1` | `0` | ✅ |
| 4 | compliance (opt-out) | `missing_unsubscribe` | `0` | ✅ |
| 5 | compliance (no fake thread) | `fake_thread` | `0` | ✅ |
| 6 | deliverability (suppression) | `suppressed` | `0` | ✅ |
| 7 | security/required fields | `missing_required_field` | `0` | ✅ |

> الأسباب الستة المعتمدة: `forbidden_claim` · `fake_thread` · `below_p1` ·
> `missing_unsubscribe` · `suppressed` · `missing_required_field`.

---

## 3. المسودّات الفاشلة (Failed Drafts)

| `draft_id` | `reason_code(s)` | الإجراء |
|------------|-------------------|---------|
| `DR-0000` | `<reason>` | إعادة صياغة / إسقاط حسب `DRAFT_REJECTION_REASONS_AR.md` |

> القائمة فارغة في اليوم النظيف. أي صفّ هنا = مسودّة **محجوبة** عن طابور الموافقة.

---

## 4. حالات الاختبار (Eval — اختياري)

| المؤشّر | القيمة |
|---------|--------|
| `eval cases` (من `data/evals/gtm_draft_eval_cases.jsonl`) | `8` |
| `mismatches` | `0` |
| نتيجة `--eval` | PASS |

---

## 5. ملاحظات السلامة (إلزامي)

- [ ] `forbidden_claim_hits = 0` — صارم.
- [ ] 0 مسودّة فاشلة دخلت طابور الموافقة.
- [ ] لم تُضعَّف أو تُتجاوَز أي بوّابة · لم يُحذَف أي اختبار.
- [ ] كل بارد يحمل opt-out · لا PII · لا `Re:/Fwd:` وهمي.
- [ ] الأرقام أعلاه قالب — تُستبدَل بمخرجات السكربت الفعلية.

---

*السكربت: `scripts/draft-quality-gate.js` · المكتبة: `scripts/_lib/dealix.js`.
الاختبارات: `tests/test_gtm_quality_gate.py` وملفّات `tests/test_outreach_*`.
البوّابات: `docs/outreach/OUTBOUND_RISK_GATES_AR.md`.*
