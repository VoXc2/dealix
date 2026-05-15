# العربية

## جاهزية المعرفة والذاكرة — الطبقة الرابعة

Owner: قائد المعرفة (Knowledge Lead)

### قائمة الجاهزية

- [x] كل إجابة مهمّة تحمل استشهادًا بمصدر حقيقي عبر `auto_client_acquisition/knowledge_os/answer_with_citations.py`.
- [x] غياب المصدر يُرجِع «أدلّة غير كافية» وفق `auto_client_acquisition/governance_os/rules/no_source_no_answer.yaml`.
- [x] الاسترجاع مقيّد بـ `tenant_id`؛ لا استرجاع عابر للمستأجرين.
- [x] الاسترجاع يحترم صلاحيّات المستخدم لا صلاحيّات المستأجر فقط.
- [x] يمكن تتبّع أي إجابة رجوعًا إلى ملفها عبر تتبّع نسب المصدر.
- [x] تقييمات المعرفة قائمة عبر `auto_client_acquisition/knowledge_os/knowledge_eval.py` و `evals/governance_eval.yaml`.
- [x] تقييم الجودة العربيّة قائم عبر `evals/arabic_quality_eval.yaml`.
- [x] يمكن تحديث مصدر دون كسر الاستشهادات القديمة (نسخ مصدر + بصمات محتوى).
- [x] كل مصدر يحمل حالة حداثة `fresh` / `aging` / `stale`.
- [ ] قياس دقّة واستدعاء الاسترجاع آليًّا على مجموعة تقييم ثابتة — قائم جزئيًّا، يحتاج لوحة قياس دوريّة.
- [ ] تمرين موثَّق لمعدّل الهلوسة على أسئلة بلا مصدر — يحتاج جدولة ربع سنويّة.

### المقاييس

- نسبة الإجابات المهمّة الحاملة لاستشهاد: 100% (هدف صارم).
- معدّل الهلوسة على أسئلة بلا مصدر: 0% مستهدف (تُرجَع «أدلّة غير كافية»).
- دقّة الاستشهاد (الاستشهاد يدعم الادّعاء فعلًا): ≥ 95%.
- دقّة الاسترجاع (precision@5): تُقاس على مجموعة تقييم ثابتة، هدف ≥ 0.80.
- استدعاء الاسترجاع (recall@10): هدف ≥ 0.85.
- حالات استرجاع عابرة للمستأجرين: صفر (غير قابل للتفاوض).
- نسبة المصادر ذات حالة حداثة محدّثة: 100%.

### خطّاطيف المراقبة

- تتبّع كل استعلام استرجاع عبر `dealix/observability/otel.py`.
- التقاط أخطاء التضمين والاسترجاع عبر `dealix/observability/sentry.py`.
- تتبّع كلفة استدعاءات التضمين عبر `dealix/observability/cost_tracker.py`.
- قيود تدقيق الاسترجاع والاستشهاد عبر `auto_client_acquisition/revenue_memory/audit.py`.
- تنبيه عند ارتفاع نسبة «أدلّة غير كافية» فوق الحدّ، أو عند فشل تقييم معرفة.

### قواعد الحوكمة

- «لا مصدر، لا إجابة» قاعدة إلزاميّة عند حدّ الواجهة، لا توصية.
- لا استرجاع عابر للمستأجرين تحت أي ظرف.
- الاسترجاع يحترم صلاحيّة المستخدم؛ مقطع بلا وسم صلاحيّة يُعامَل كمقيَّد.
- لا تُختلَق أرقام أو معدّلات؛ القيمة التقديريّة تُوسَم صراحةً.
- حذف مصدر إجراء مُصنَّف يتطلب موافقة موثَّقة.
- لا يدخل محتوى من كسح مواقع أو رسائل باردة أو أتمتة LinkedIn إلى الذاكرة.

### إجراء التراجع

1. تحديد آخر حالة معرفة مستقرّة (نسخة الفهرس وإصدار النموذج).
2. عند فهرسة معطوبة: إيقاف الاسترجاع عن المصدر المتأثّر وإرجاع «أدلّة غير كافية» مؤقّتًا بدل نتيجة خاطئة.
3. إعادة بناء المتّجهات المتأثّرة عبر عمليّة upsert من المصادر السليمة.
4. عند تغيّر نموذج التضمين: التراجع لاسم النموذج السابق المسجَّل في `model_name`.
5. التحقق من تقييمات المعرفة بعد التراجع عبر `knowledge_eval.py`.
6. تسجيل التراجع كقيد تدقيق وإبلاغ قائد المعرفة.

### درجة الجاهزية الحالية

**الدرجة: 79 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

روابط: `architecture.md` · `hybrid_retrieval.md` · `citations.md` · `tests.md` · `scorecard.yaml`

---

# English

## Knowledge & Memory Readiness — Layer 4

Owner: Knowledge Lead

### Readiness checklist

- [x] Every important answer carries a citation to a real source via `auto_client_acquisition/knowledge_os/answer_with_citations.py`.
- [x] Absence of a source returns "insufficient evidence" per `auto_client_acquisition/governance_os/rules/no_source_no_answer.yaml`.
- [x] Retrieval is scoped by `tenant_id`; no cross-tenant retrieval.
- [x] Retrieval respects per-user permissions, not just tenant-level permissions.
- [x] Any answer can be traced back to its file via source lineage.
- [x] Knowledge evals exist via `auto_client_acquisition/knowledge_os/knowledge_eval.py` and `evals/governance_eval.yaml`.
- [x] Arabic quality eval exists via `evals/arabic_quality_eval.yaml`.
- [x] A source can be updated without breaking old citations (source versioning + content hashes).
- [x] Every source carries a freshness status `fresh` / `aging` / `stale`.
- [ ] Automated retrieval precision/recall measurement on a fixed eval set — partially in place, needs a periodic dashboard.
- [ ] Documented hallucination-rate drill on no-source questions — needs quarterly scheduling.

### Metrics

- Share of important answers carrying a citation: 100% (hard target).
- Hallucination rate on no-source questions: 0% target ("insufficient evidence" returned).
- Citation accuracy (citation genuinely supports the claim): >= 95%.
- Retrieval precision (precision@5): measured on a fixed eval set, target >= 0.80.
- Retrieval recall (recall@10): target >= 0.85.
- Cross-tenant retrieval incidents: zero (non-negotiable).
- Share of sources with an up-to-date freshness status: 100%.

### Observability hooks

- Every retrieval query traced via `dealix/observability/otel.py`.
- Embedding and retrieval errors captured via `dealix/observability/sentry.py`.
- Embedding call cost tracked via `dealix/observability/cost_tracker.py`.
- Retrieval and citation audit entries via `auto_client_acquisition/revenue_memory/audit.py`.
- Alert when the "insufficient evidence" rate rises above threshold, or when a knowledge eval fails.

### Governance rules

- "No source, no answer" is a mandatory rule at the API boundary, not a recommendation.
- No cross-tenant retrieval under any condition.
- Retrieval respects per-user permission; a chunk without a permission tag is treated as restricted.
- No numbers or rates are fabricated; estimated values are labeled explicitly.
- Deleting a source is a classified action requiring documented approval.
- No content from scraping, cold messages, or LinkedIn automation enters memory.

### Rollback procedure

1. Identify the last stable knowledge state (index version and model version).
2. On a corrupted index: stop retrieval from the affected source and temporarily return "insufficient evidence" rather than a wrong result.
3. Rebuild affected vectors via an upsert from the intact sources.
4. On an embedding model change: roll back to the prior model name recorded in `model_name`.
5. Verify knowledge evals after rollback via `knowledge_eval.py`.
6. Record the rollback as an audit entry and notify the Knowledge Lead.

### Current readiness score

**Score: 79 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

Links: `architecture.md` · `hybrid_retrieval.md` · `citations.md` · `tests.md` · `scorecard.yaml`
