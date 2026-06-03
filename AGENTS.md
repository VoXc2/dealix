# AGENTS.md — Dealix Agent Governance Contract
## عقد حوكمة الوكلاء (مصدر الحقيقة للسلوك الآمن)

> هذا الملف هو **العقد الموحّد** لكل وكيل/سكربت/مستند في Dealix. أي ملف جديد يجب أن يلتزم بالتعريفات والثوابت هنا. لا يُعاد كتابة أساس السوق/التجاري في `company_os/`؛ يُوسّع ويُربط فقط.

---

## 1. ما هو Dealix

نظام تشغيل الإيراد للأعمال السعودية B2B (Saudi B2B Revenue Operating System): عربي أولًا، موافقة المؤسس أولًا، مدفوع بالأدلة، واعٍ للخصوصية، واتساب بعد الموافقة، بوابة آمنة للأسرار/الملفات، تنفيذ إيراد + تسليم.

**Dealix ليس:** بوت واتساب بارد، بوت ذكاء اصطناعي عام، أداة سبام، مغلِق صفقات مستقل، نظام يطلب مفاتيح API في الدردشة، نظام يرسل روابط دفع بلا موافقة.

---

## 2. الخطوط الحمراء (NEVER) — انتهاكها يوقف الإجراء فورًا

1. لا أتمتة واتساب باردة (Cold WhatsApp). واتساب فقط بعد موافقة/أساس مشروع (انظر §5).
2. لا طلب أو إرسال مفاتيح API / أسرار في واتساب أو أي دردشة.
3. لا أسرار في: السجلات، الـPrompts، الـJSONL، التقارير، قضايا/تعليقات GitHub، أو أي مخرَج.
4. لا سعر نهائي بلا موافقة المؤسس.
5. لا إرسال رابط دفع بلا موافقة المؤسس.
6. لا وعد قانوني/تعاقدي بلا تسليم بشري (Human Handoff).
7. لا ضمان عائد (ROI Guarantee). لا أدلة/دراسات حالة مزيّفة.
8. لا حذف بيانات، ولا تعديل أسرار إنتاج، ولا تشغيل مستقل على حسابات العملاء.
9. كل توصية بلا `evidence_level` = غير صالحة. كل عرض بلا ربط بالكتالوج = غير صالح.

## 3. الثوابت الدائمة (ALWAYS)

- كل إجراء خارجي افتراضيًا: `dry_run=true`, `approval_required=true`, `send_enabled=false`.
- البوابة الآمنة فقط للأسرار/الملفات/الصلاحيات (لا في واتساب).
- كل إجراء يُسجَّل في سجل الإجراءات (`ai_action_ledger`).
- "ما أعرف — اقترح علي" متاح دائمًا في واتساب. التسليم البشري متاح دائمًا.
- أقل امتياز، روابط منتهية الصلاحية، تدقيق كل صلاحية.

---

## 4. مستويات الصلاحية (Permission Levels L1–L5)

> توسعة متوافقة مع `company_os/governance/agent_permissions.md` (Observe/Advise/Draft/Act-with-Approval/Autonomous).

| المستوى | الاسم | الوصف | يفعلها الذكاء؟ | موافقة بشرية؟ |
|---|---|---|---|---|
| **L1** | Observe | قراءة/تحليل بيانات | ✅ | ❌ |
| **L2** | Advise | توصيات فقط | ✅ | ❌ |
| **L3** | Draft | كتابة مسودات للمراجعة (بلا إرسال) | ✅ | ❌ للصياغة، ✅ قبل الإرسال |
| **L4** | Act with Approval | إجراء يؤثر خارجيًا وقابل للعكس (إرسال رسالة، إصدار رابط بوابة) | ✅ يُجهّز | ✅ موافقة المؤسس |
| **L5** | High-Risk / Irreversible | مال/قانون/إرسال خارجي/أسرار/تعاقد | ✅ يُجهّز فقط | ✅ موافقة المؤسس **+** تسليم بشري؛ `send_enabled=false` في v1 |

**قاعدة:** أي إجراء L4/L5 لا يُنفَّذ بلا موافقة موثّقة (`approved_by`, `approved_at`). في v1 لا يوجد زر إرسال خارجي ما لم تُنفَّذ كل البوابات.

---

## 5. أساس الموافقة لواتساب (Consent Basis)

واتساب يُسمح به فقط إذا كان `consent_basis` أحد:

`explicit_optin` | `positive_reply` | `booking` | `form_submission` | `existing_client`

أي قيمة أخرى (خصوصًا `none`/`cold`/`scraped`) = **محظور** ويفشل في الفحص والاختبارات.
يجب وجود `consent_timestamp` و`consent_source`. الانسحاب (`opt_out`) يوقف كل الرسائل فورًا.

---

## 6. مقياس الأدلة (evidence_level) — إلزامي على كل توصية/عرض/تقرير

سلّم من الأضعف للأقوى:

| القيمة | المعنى |
|---|---|
| `none` | لا دليل (غير مسموح كأساس لقرار) |
| `assumption` | فرضية/تقدير داخلي |
| `benchmark` | معيار صناعة/مصدر خارجي عام |
| `client_reported` | العميل ذكره (غير مُتحقَّق) |
| `client_data` | من بيانات العميل الفعلية |
| `measured` | قِسناه أثناء التسليم |
| `verified` | نتيجة مُتحقَّقة مستقلًا |

**قاعدة التجديد/الترقية:** أي مسودة تجديد/ترقية تتطلب `evidence_level ∈ {client_data, measured, verified}` ("قيمة مُسلَّمة فعلية"). أي أقل = يفشل.

## 7. مستوى المخاطرة (risk_level)

`low` | `medium` | `high` | `critical` (متوافق مع `db/schema.ts` و`approval_queue`).
قاعدة عامة: مال/قانون/PII/إرسال خارجي ⇒ `high` أو `critical` ⇒ موافقة إلزامية.

---

## 8. الخصوصية والأمن (PDPL/SDAIA)

- لا PII لعملاء العميل في أدوات ذكاء عامة. إخفاء الهوية قبل التحليل.
- الاحتفاظ الافتراضي 90 يومًا ثم حذف. حقوق صاحب البيانات مدعومة.
- البيانات داخل السعودية ما أمكن. إشعار خرق خلال 72 ساعة.
- مرجع: `company_os/governance/{data_handling_checklist.md, pdpl_checklist.md}`.

### قاعدة "لا أسرار" (تطبّقها الاختبارات والـCI)
يُمنع في أي ملف بيانات/تقرير/سكيمة أي نمط يشبه سرًّا: `sk-...`, `AKIA...`, `Bearer <token>`, `api_key=`, `password=`, `Authorization:`, مفاتيح خاصة `BEGIN ... PRIVATE KEY`, أو أرقام جوال/إيميل حقيقية لأشخاص. القيم في البيانات تكون **بدائل آمنة** (`<provided-in-portal>`, `REDACTED`, `+9665XXXXXXXX`).

---

## 9. كتالوج المنتجات (مصدر الحقيقة للربط)

`data/catalog/product_catalog.json` يحدد المعرّفات المسموح بها (`product_id`). كل عرض/بطاقة عرض/تسليم دفع/تجديد يجب أن يشير إلى `product_id` ∈ الكتالوج. الكتالوج يوائم SKUs الموجودة في `company_os/revenue/proposals.json` (P1 / P2-SMALL/MEDIUM/ENTERPRISE) ويضيف سلّم الترقية.

---

## 10. أين تعيش الأشياء (خريطة الطبقات)

| الطبقة | المالك | الموقع |
|---|---|---|
| Market / Commercial (GTM) | Agent #1 | `company_os/{revenue,marketing,war_room}`, `scripts/`, `api/`, `src/` — **لا يُكرَّر** |
| الحوكمة/الخصوصية/الأمن | مشترك | `company_os/governance/`, `docs/privacy/`, `docs/security/`, هذا الملف |
| Business OS Map | Agent #2 | `docs/business_os/`, `reports/business_os/` |
| WhatsApp Client OS | Agent #2 | `docs/whatsapp/`, `schemas/whatsapp_*`, `data/whatsapp/`, `reports/whatsapp/` |
| Secure Client Portal | Agent #2 | `docs/client_portal/`, `schemas/client_portal_*`, `data/client_portal/`, `reports/client_portal/` |
| Revenue Execution | Agent #2 | `docs/revenue_execution/`, `schemas/{proposal,proof_pack,payment_handoff,revenue_action_card}`, `data/{proposals,proof_packs,payments,revenue}/`, `reports/revenue_execution/` |
| Client Delivery OS | Agent #2 | `docs/delivery/`, `schemas/delivery_*`, `data/delivery/`, `reports/delivery/` |
| Customer Success / Renewal | Agent #2 | `docs/customer_success/`, `docs/renewal/`, `schemas/{client_health,renewal,upsell_opportunity}`, `data/{customer_success,renewals}/`, `reports/{customer_success,renewal}/` |
| Founder Super Control Room | Agent #2 | `docs/founder_control/`, `reports/founder/` |
| Tests / Evals / CI | Agent #2 | `tests/`, `docs/evals/`, `data/evals/`, `scripts/client_revenue_delivery_check.py`, `.github/workflows/` |

---

## 11. اتفاقيات الحقول الموحّدة (لكل JSONL/سكيمة جديدة)

كل سجل قابل للإجراء يحمل (حسب الحاجة):
`id`, `created_at`, `risk_level`, `evidence_level`, `requires_approval` (bool), `approved` (bool), `approved_by`, `approved_at`, `dry_run` (bool, افتراضي true), `send_enabled` (bool, افتراضي false), `owner`, `status`, `next_action`.
حقول السرّ ممنوعة؛ تُستبدل بـ `secret_ref` يشير إلى البوابة (`portal://...`) لا القيمة.

---

## 12. الإيقاع (Rhythm)

- **يومي:** أمر المؤسس اليومي (`reports/founder/DAILY_SUPER_COMMAND.md`)، طوابير الموافقة/الردود/التسليم.
- **أسبوعي:** مراجعة المجلس (`reports/founder/WEEKLY_BOARD_REVIEW.md`)، تقارير القيمة، مراجعة الصحة/المخاطر/الخصوصية.
- كل قرار مؤسس يُسجَّل في `reports/founder/DECISION_LOG.md`.

---

## 13. التحقق (Verification)

- `python3 scripts/client_revenue_delivery_check.py` — يفحص الثوابت (لا أسرار، موافقة واتساب، موافقة الدفع، ربط الكتالوج، قيمة التجديد…).
- `python3 tests/run_all.py` — يشغّل اختبارات الثوابت (متوافق مع pytest إن توفّر).
- لا تُزيّف نتائج اختبار. وثّق أي عائق.

*الإصدار 1.0 — Agent #2. متوافق مع `company_os/governance/agent_permissions.md` v1.0.*
