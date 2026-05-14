# أصول الثقة — Trust Assets

> النوع: `trust_asset` | آخر مراجعة: 2026-05-14
> مصدر: [`capital_asset_registry.py`](../auto_client_acquisition/capital_os/capital_asset_registry.py)

أصول الثقة هي الأسطح التي يفحصها مدير أمن المعلومات، مسؤول حماية البيانات، أو مدقّق Big 4 قبل أن تُفتح أي صفقة تنظيمية. ثلاثة أصول مُسجَّلة: CAP-001، CAP-007، CAP-008.

Trust assets are the surfaces a CISO, DPO, or Big 4 auditor inspects before any regulated deal opens. Three registered: CAP-001, CAP-007, CAP-008.

---

## CAP-001 — Dealix Promise API

**Maturity:** live | **Proof level:** test-backed | **Public:** True
**Files:** `api/routers/dealix_promise.py`, `auto_client_acquisition/governance_os/non_negotiables.py`, `tests/test_dealix_promise.py`, `landing/promise.html`

### الدور الاستراتيجي (AR)
سطح تحقُّق عقيدي عام — أي مدير أمن معلومات يستطيع التحقق عبر `curl` من الـ١١ التزاماً مقابل ملفات الاختبار التي تُنفِّذ كلاً منها.

### Strategic role (EN)
Public doctrine verification surface — any CISO can `curl`-verify the 11 commitments against the test files that enforce each.

### Buyer relevance
CISO، DPO، مشترٍ تنظيمي، استشارات Big 4، صندوق VC في مرحلة العناية الواجبة.

### متى تُظهره في محادثة المبيعات (AR)
عند أول إشارة من المشتري إلى الـ "هل أنتم متوافقون مع SAMA؟" أو "كيف نتجاوز مراجعة المشتريات؟". الإجابة ليست شريحة، بل أمر طرفية: `curl https://dealix.sa/api/v1/promise`.

### When to surface in sales (EN)
First moment the buyer mentions SAMA alignment or procurement bypass. The answer is not a slide — it is a terminal command: `curl https://dealix.sa/api/v1/promise`.

---

## CAP-007 — Trust Pack PDF Renderer

**Maturity:** live | **Proof level:** code-backed | **Public:** False
**Files:** `auto_client_acquisition/trust_os/trust_pack.py`

### الدور الاستراتيجي (AR)
مولّد PDF بـ١١ قسماً لكل عميل — جاهز لمراجعة CISO/SAMA. يُسلَّم مع كل عرض مؤسسي، يحلّ محل عشرات الأسئلة المتكررة في استبيانات المشتريات.

### Strategic role (EN)
11-section enterprise trust pack PDF per customer — ready for CISO/SAMA review. Ships with every enterprise proposal and collapses the procurement questionnaire loop.

### Buyer relevance
CISO، DPO، جهة تنظيمية، استشارات Big 4.

### متى تُظهره في محادثة المبيعات (AR)
بعد المكالمة الأولى مع المشتري المؤسسي. تُرسل Trust Pack PDF كملحق قبل اجتماع المراجعة الأمنية — لا بعده. هذا يُحوِّل المراجعة من "اكتشاف" إلى "تأكيد".

### When to surface in sales (EN)
After the first enterprise call, send the Trust Pack PDF as an attachment *before* the security review meeting — not after. This converts the review from "discovery" to "confirmation".

---

## CAP-008 — Audit Chain + Evidence Control Plane

**Maturity:** live | **Proof level:** code-backed | **Public:** False
**Files:** `auto_client_acquisition/auditability_os/audit_event.py`, `auto_client_acquisition/evidence_control_plane_os/evidence_graph.py`

### الدور الاستراتيجي (AR)
أثر تدقيق بجودة تشفيرية لكل فعل خارجي وكل قرار — هذا هو إثبات الخط الأحمر `no_external_action_without_approval`. عند سؤال جهة تنظيمية عن حادثة ما، الإجابة موجودة في رسم بياني للأدلة، لا في ذاكرة بشرية.

### Strategic role (EN)
Cryptographic-quality audit trail of every external action and decision — this is the proof of non-negotiable #8 (`no_external_action_without_approval`). When a regulator asks about an incident, the answer lives in an evidence graph, not in human memory.

### Buyer relevance
CISO، DPO، جهة تنظيمية، تدقيق داخلي.

### متى تُظهره في محادثة المبيعات (AR)
عند صعود الحوار إلى استجابة الحوادث، السجلات، أو إثبات السيطرة. ليس سطحاً تسويقياً — هو سطح هندسي يُفتح في مراجعة تقنية مع فريق الأمن لدى المشتري.

### When to surface in sales (EN)
When the conversation escalates to incident response, logging, or control evidence. This is not a marketing surface — it is an engineering surface opened in a technical review with the buyer's security team.

---

## استخدام مُجمَّع (AR) / Combined use (EN)

- **AR:** الثلاثة معاً يُشكِّلون "حزمة التجاوز التنظيمي" — مدير أمن المعلومات يفحص الثلاثة ويغلق المراجعة في جلسة واحدة بدلاً من ثلاث.
- **EN:** Together the three form the "regulated-buyer unlock stack" — a CISO who inspects all three can close the review in one session rather than three.

---

*Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.*
