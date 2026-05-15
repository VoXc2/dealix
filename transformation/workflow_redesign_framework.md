# العربية

# إطار إعادة تصميم سير العمل — الطبقة ١١

**المالك:** قائد التحويل في Dealix بالاشتراك مع مالك سير العمل لدى العميل.

## الغرض

إعادة تصميم سير العمل هي القلب التشغيلي للطبقة ١١. لا نضع الذكاء الاصطناعي فوق عملية قائمة، بل نفكّك العملية إلى خطوات، ونحدّد أين يضيف الذكاء الاصطناعي قيمة، ونعيد بناءها بحلقة أدلة.

## الخطوات الست

### ١. رسم خريطة الحالة الراهنة

وثّق كل خطوة، ومالكها، ووقتها، ومصدر بياناتها. حدّد نقاط الاحتكاك عبر `auto_client_acquisition/adoption_os/friction_log.py`.

### ٢. تحديد فرص الذكاء الاصطناعي

لكل خطوة، اسأل: هل هي اقتراح (يصلح للذكاء الاصطناعي) أم قرار (يبقى للإنسان)؟ صنّف الخطوات إلى: قابلة للمسودّة، قابلة للتصنيف، قابلة للتلخيص، أو محجوزة للإنسان.

### ٣. ربط كل فرصة بفرضية عائد

كل فرصة تُكتب كفرضية: «إذا اقترح الذكاء الاصطناعي س، نقدّر توفير ص دقيقة لكل حالة». هذه فرضية بأدلة، وليست وعداً.

### ٤. إعادة بناء سير العمل

أعد تصميم العملية بحدود قرار واضحة: أين يقترح الذكاء الاصطناعي، وأين تُفرض الموافقة البشرية. اربط بمعايير بوّابة سير العمل في `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py`.

### ٥. إضافة حلقة الأدلة

كل سير عمل مُعاد تصميمه يسجّل أحداثه في `auto_client_acquisition/value_os/value_ledger.py` ليصبح قابلاً للقياس شهرياً.

### ٦. القياس والتكرار

قارن الحالة الراهنة بالمُعاد تصميمها. سجّل القيمة المُلاحَظة، واجمع الاحتكاك، وكرّر.

## القاعدة غير القابلة للتفاوض

إعادة التصميم تُقترح، ولا تُفرض. الإرسال التلقائي للرسائل الخارجية محظور؛ كل إجراء خارجي يمرّ بموافقة بشرية صريحة.

القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

# Workflow Redesign Framework — Layer 11

**Owner:** Dealix Transformation Lead, jointly with the client Workflow Owner.

## Purpose

Workflow redesign is the operational heart of Layer 11. We do not place AI above an existing process; we break the process into steps, identify where AI adds value, and rebuild it with an evidence loop.

## The six steps

### 1. Map the current state

Document every step, its owner, its time cost, and its data source. Identify friction points via `auto_client_acquisition/adoption_os/friction_log.py`.

### 2. Identify AI opportunities

For each step, ask: is this a suggestion (suited to AI) or a decision (stays human)? Classify steps as draftable, classifiable, summarizable, or human-reserved.

### 3. Tie each opportunity to an ROI hypothesis

Each opportunity is written as a hypothesis: "If AI proposes X, we estimate a saving of Y minutes per case." This is an evidence-backed hypothesis, not a promise.

### 4. Rebuild the workflow

Redesign the process with clear decision boundaries: where AI proposes, where human approval is enforced. Anchor to the workflow gate criteria in `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py`.

### 5. Add the evidence loop

Every redesigned workflow records its events in `auto_client_acquisition/value_os/value_ledger.py` so it becomes monthly-measurable.

### 6. Measure and iterate

Compare the current state against the redesigned state. Record observed value, aggregate friction, and iterate.

## Non-negotiable

Redesign is proposed, never imposed. Auto-send of external messages is blocked; every external action passes explicit human approval.

Estimated value is not Verified value.
