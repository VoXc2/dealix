# العربية

# نموذج التشغيل بالذكاء الاصطناعي — الطبقة ١١

**المالك:** قائد التحويل في Dealix بالاشتراك مع راعي العميل التنفيذي.

## الغرض

نموذج التشغيل يصف كيف تعمل الشركة بعد التحويل: من يملك ماذا، وأين يقرّر الإنسان، وأين يقترح الذكاء الاصطناعي، وكيف تنتقل القيمة من اقتراح إلى نتيجة موثّقة. الهدف ليس إضافة أداة بل إعادة رسم خريطة المسؤوليات.

## الركائز الأربع

### ١. الأدوار

يطابق `auto_client_acquisition/enterprise_rollout_os/role_map.py` و`auto_client_acquisition/adoption_os/client_roles.py`. كل تحويل يحتاج: راعياً تنفيذياً، مالك سير عمل، مالك موافقات، ومالك بيانات. لا تبدأ مرحلة بدون هذه الأدوار الأربعة مسمّاة.

### ٢. حدود القرار

- **يقترح الذكاء الاصطناعي:** مسودّات، تصنيفات، تلخيصات.
- **يوافق الإنسان:** أي إجراء خارجي، أي رسالة تُرسَل، أي التزام تعاقدي.
- **يُحظر دائماً:** الإرسال التلقائي للرسائل الخارجية، الكشط، التواصل البارد المؤتمت.

### ٣. حلقة القيمة

كل سير عمل مُعاد تصميمه يسجّل أحداثه في `auto_client_acquisition/value_os/value_ledger.py`، وتُلخَّص شهرياً عبر `auto_client_acquisition/value_os/monthly_report.py`. القيمة تُصنَّف: مُقدَّرة، مُلاحَظة، مُتحقَّقة، مؤكَّدة من العميل.

### ٤. الحوكمة المستمرة

بوّابات الانتقال في `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py` تفرض معايير صريحة قبل كل مرحلة: راعٍ، بيانات، سير عمل، حوكمة، أدلة، تبنّي، عقد دوري.

## مراحل التشغيل

تطابق `rollout_stage.py`: الإنزال (land)، الإثبات (prove)، التبنّي (adopt)، التشغيل (operate)، التوسّع (expand)، التوحيد (standardize)، الترسيخ المؤسسي (institutionalize).

## القاعدة غير القابلة للتفاوض

نموذج التشغيل يُعرّف كيف تُتَّخذ القرارات، لا يضمن أي قرار نتيجة بعينها. كل حالة استخدام مرتبطة بفرضية عائد بأدلة.

القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

# AI Operating Model — Layer 11

**Owner:** Dealix Transformation Lead, jointly with the client Executive Sponsor.

## Purpose

The operating model describes how the company runs after transformation: who owns what, where a human decides, where AI proposes, and how value moves from a suggestion to a documented result. The goal is not to add a tool but to redraw the map of responsibility.

## The four pillars

### 1. Roles

Matches `auto_client_acquisition/enterprise_rollout_os/role_map.py` and `auto_client_acquisition/adoption_os/client_roles.py`. Every transformation needs an executive sponsor, a workflow owner, an approval owner, and a data owner. No stage begins until these four roles are named.

### 2. Decision boundaries

- **AI proposes:** drafts, classifications, summaries.
- **A human approves:** any external action, any message sent, any contractual commitment.
- **Always blocked:** auto-send of external messages, scraping, automated cold outreach.

### 3. The value loop

Every redesigned workflow records its events in `auto_client_acquisition/value_os/value_ledger.py` and is summarized monthly through `auto_client_acquisition/value_os/monthly_report.py`. Value is tiered: estimated, observed, verified, client-confirmed.

### 4. Continuous governance

Stage-transition gates in `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py` enforce explicit criteria before each stage: sponsor, data, workflow, governance, proof, adoption, retainer.

## Operating stages

Matches `rollout_stage.py`: land, prove, adopt, operate, expand, standardize, institutionalize.

## Non-negotiable

The operating model defines how decisions are made; it does not guarantee any decision a specific outcome. Every use case ties to an evidence-backed ROI hypothesis.

Estimated value is not Verified value.
