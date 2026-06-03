# Dealix — تصنيف أسباب رفض المسودّات (Draft Rejection Reasons)

> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`
> الأسباب الستة أدناه هي **المصطلحات المعتمدة** التي يُصدرها
> `scripts/draft-quality-gate.js` (`gateDraft`)، وتؤكّدها اختبارات `tests/`.

كل مسودّة مرفوضة تحمل سبباً واحداً على الأقل من هذا التصنيف. الأسباب موحّدة
machine-readable لتغذية حلقة التحسين الأسبوعية «إيقاف أسوأ 20%».

---

## 1. تصنيف أسباب الرفض (Rejection Taxonomy)

| `reason_code` | المعنى | الفحص الذي أطلقه | الإصلاح |
|---------------|--------|-------------------|---------|
| `forbidden_claim` | عبارة محظورة في العنوان/الجسم | brand gate ضد `forbidden_claims.yaml` | إعادة صياغة بالأفعال المسموحة |
| `fake_thread` | عنوان يبدأ بـ `Re:/Fwd:` وهمي | compliance gate (`subjectPrefixes`) | عنوان عادي يصف القيمة |
| `below_p1` | `personalization_score = P0` | personalization gate (أرضية P1) | رفع التخصيص إلى P1+ بإشارة عامة |
| `missing_unsubscribe` | مسودّة باردة بلا opt-out | compliance gate (`opt_out.included`) | إضافة «للإلغاء: ردّ «إيقاف».» |
| `suppressed` | المستلِم على قائمة الإيقاف | deliverability gate (`suppression_list`) | إسقاط المستلِم نهائياً |
| `missing_required_field` | غياب حقل إلزامي | required-fields/security gate | استكمال الحقول الإلزامية |

> هذه الستة فقط هي المصطلحات المعتمدة. لا نخترع أسباباً جديدة دون تحديث
> `gateDraft` والاختبارات معاً.

---

## 2. أمثلة توضيحية لكل سبب (placeholder — «مثال توضيحي»)

> أمثلة **خاطئة** للتوضيح فقط؛ لا تدخل أي طابور.

- `forbidden_claim`: «نضمن زيادة المبيعات بدون أي مخاطرة» → محظور.
- `fake_thread`: عنوان «Re: عرضنا السابق» على مسودّة باردة → محظور.
- `below_p1`: «نقدّم خدمات تحسين المبيعات» (قطاع فقط، P0) → مرفوض.
- `missing_unsubscribe`: مسودّة باردة بلا سطر «للإلغاء: ردّ «إيقاف».» → مرفوضة.
- `suppressed`: مستلِم نطاقه على `suppression_list.jsonl` → لا يُرسَل أبداً.
- `missing_required_field`: مسودّة بلا `offer_match` → مرفوضة.

الإصلاح الصحيح لكلٍّ منها في `docs/outreach/COLD_EMAIL_SEQUENCES_AR.md` و
`docs/outreach/PERSONALIZATION_RULES_AR.md`.

---

## 3. حلقة «إيقاف أسوأ 20%» الأسبوعية (Weekly Loop)

كل أسبوع، ضمن إيقاع GTM الأسبوعي:

1. **اجمع** أسباب الرفض من `reports/outreach/DRAFT_GATE_REVIEW.md` للأسبوع.
2. **رتّب** أنماط المسودّات حسب معدّل الرفض (`reason_code` × `draft_type` × زاوية).
3. **أوقف أسوأ 20%**: أنماط أعلى رفضاً تُسحَب من الإنتاج (عناوين/زوايا/قوالب).
4. **ضاعف أفضل 20%**: الأنماط النظيفة (0 رفض، تخصيص P3–P4) تُوسَّع.
5. **حدّث** القوالب في `COLD_EMAIL_SEQUENCES_AR.md` وقواعد `PERSONALIZATION_RULES_AR.md`.
6. **سجّل** القرار في مراجعة GTM الأسبوعية.

الهدف: انخفاض مطّرد في `reason_code` المتكرّرة، و`forbidden_claim_hits = 0` دائماً.

---

## 4. مؤشّرات المتابعة (Loop Metrics)

| المؤشّر | الهدف |
|---------|-------|
| `forbidden_claim_hits` | 0 (صارم) |
| نسبة `below_p1` من المرفوض | تنخفض أسبوعياً |
| نسبة `missing_unsubscribe` | 0 (كل بارد فيه opt-out) |
| نسبة المسودّات P3–P4 | ترتفع أسبوعياً |

---

## 5. الحدود غير القابلة للتفاوض

- الأسباب الستة معتمدة فقط · لا إضعاف بوّابة لتقليل الرفض شكلياً.
- لا حذف اختبار لتمرير مسودّة · `forbidden_claim_hits` يبقى 0.
- إيقاف الأسوأ 20% لا يعني خفض السلامة — يعني رفع الجودة.
- لا ادّعاءات ممنوعة · لا PII · كل بارد يحمل سطر الإلغاء.

---

*المرجع المركزي: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`. البوّابات:
`docs/outreach/OUTBOUND_RISK_GATES_AR.md`. مراجعة البوّابات:
`reports/outreach/DRAFT_GATE_REVIEW.md`.*
