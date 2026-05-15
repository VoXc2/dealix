# العربية

# اختبارات Layer 10 — تسليم العميل

**المالك:** قائد الجودة (QA Lead)
**الجمهور:** فريق الجودة والتسليم الذي يتحقق من جاهزية Layer 10
**المراجع:** `playbooks/readiness.md` · `playbooks/qa/pre_launch_checklist.md` · `playbooks/qa/client_acceptance_tests.md` · `docs/PILOT_DELIVERY_SOP.md` · `docs/COMPANY_SERVICE_LADDER.md`

> الغرض: مواصفة اختبار مكتوبة تتحقق من أن أدلة عمل Layer 10 تعمل كما هو مقصود. لا كود — حالات اختبار ومعايير قبول كمواصفة markdown.

## 1. نطاق الاختبار

تغطي حالات الاختبار تغطية أدلة العمل، استقلالها عن المؤسس، معايير القبول، قوائم الفحص، SLA، أزمنة التسليم، ومعدل التأخير.

## 2. حالات الاختبار

### T-1: تغطية أدلة العمل
- **المدخل:** رحلة العميل من الاكتشاف إلى التحسين الشهري.
- **الخطوة:** تحقق من وجود دليل لكل مرحلة.
- **معيار القبول:** كل مرحلة لها دليل عمل في `playbooks/`.

### T-2: الاستقلال عن المؤسس
- **المدخل:** دليل عمل واحد وعضو فريق غير المؤسس.
- **الخطوة:** اطلب من العضو تنفيذ المرحلة من الدليل فقط.
- **معيار القبول:** المرحلة تكتمل دون تدخل المؤسس.

### T-3: معايير قبول لكل عميل
- **المدخل:** ملف عميل نشط.
- **الخطوة:** تحقق من توثيق معايير القبول.
- **معيار القبول:** كل عميل له معايير قبول موثَّقة عبر `client_acceptance_tests.md`.

### T-4: قائمة فحص لكل إطلاق
- **المدخل:** مخرَج جاهز للتسليم.
- **الخطوة:** تحقق من تشغيل قائمة ما قبل الإطلاق.
- **معيار القبول:** الفحوص السبع أُجريت وموقّعة قبل التسليم.

### T-5: وجود المراجعة الشهرية
- **المدخل:** عميل اشتراك Managed Ops.
- **الخطوة:** تحقق من إجراء مراجعة شهرية موثَّقة.
- **معيار القبول:** المراجعة الشهرية مُجراة قبل تاريخ التجديد.

### T-6: SLA لكل خدمة
- **المدخل:** درجات سُلَّم الخدمات.
- **الخطوة:** تحقق من SLA معلَن لكل درجة.
- **معيار القبول:** كل خدمة لها SLA موثَّق.

### T-7: زمن التهيئة معروف
- **المدخل:** سجل تهيئة عميل.
- **الخطوة:** قِس الزمن من الدفع إلى Kick-off.
- **معيار القبول:** الزمن موثَّق و≤ 24 ساعة.

### T-8: زمن التسليم معروف
- **المدخل:** ارتباط مكتمل.
- **الخطوة:** قِس زمن التسليم مقابل هدف الدرجة.
- **معيار القبول:** الزمن موثَّق ومطابق لهدف الدرجة.

### T-9: معدل تأخير المشروع منخفض
- **المدخل:** آخر 10 ارتباطات.
- **الخطوة:** احسب نسبة الارتباطات المتأخرة.
- **معيار القبول:** معدل التأخير ≤ 10%.

### T-10: مقاييس نجاح لكل عميل
- **المدخل:** ملف عميل نشط.
- **الخطوة:** تحقق من توثيق مقاييس النجاح.
- **معيار القبول:** كل عميل له مقاييس نجاح موثَّقة.

### T-11: الامتثال للقواعد غير القابلة للتفاوض
- **المدخل:** كل أدلة عمل Layer 10.
- **الخطوة:** ابحث عن إثبات مختلق، ضمانات، كشط، رسائل باردة، أتمتة LinkedIn، بيانات شخصية.
- **معيار القبول:** صفر مخالفات عبر كل الأدلة.

### T-12: التوازن ثنائي اللغة
- **المدخل:** كل ملف `.md` في `playbooks/`.
- **الخطوة:** تحقق من قسمي H1 (العربية ثم English) وتطابق المحتوى.
- **معيار القبول:** كل ملف ثنائي اللغة بقسمين متطابقين كاملين.

## 3. معايير القبول الإجمالية

- تُعدّ جاهزية Layer 10 «مُتحقَّقة» عندما تنجح حالات T-1 إلى T-12 جميعها.
- أي حالة فاشلة تُعالَج قبل ادعاء جاهزية الطبقة.
- نتائج الاختبار تغذّي `playbooks/readiness.md` و`playbooks/monthly_optimization/improvement_backlog.md`.

## 4. القواعد الحاكمة (Non-negotiables)

- لا إثبات مختلق في أي حالة اختبار.
- نتائج الاختبار تُسجَّل كما هي — لا تجميل.
- لا حالة اختبار تتجاوز فحص الامتثال T-11.

## 5. خطافات المراقبة

- سجّل نتيجة كل حالة: `pass` / `fail`.
- مراجعة دورية لنتائج الاختبار قبل كل تحديث لدرجة الجاهزية.

## 6. إجراء التراجع

إذا أُعلنت الجاهزية ثم فشلت حالة اختبار لاحقاً:
1. خفّض درجة الجاهزية في `playbooks/readiness.md`.
2. سجّل الحادثة في سجل الحوكمة.
3. أضف بنداً إلى سجل التحسينات لمعالجة السبب.

# English

# Layer 10 Tests — Client Delivery

**Owner:** QA Lead
**Audience:** The QA and delivery team verifying Layer 10 readiness
**References:** `playbooks/readiness.md` · `playbooks/qa/pre_launch_checklist.md` · `playbooks/qa/client_acceptance_tests.md` · `docs/PILOT_DELIVERY_SOP.md` · `docs/COMPANY_SERVICE_LADDER.md`

> Purpose: a written test specification that verifies the Layer 10 playbooks work as intended. No code — test cases and acceptance criteria as a markdown specification.

## 1. Test scope

The test cases cover playbook coverage, founder independence, acceptance criteria, checklists, SLAs, delivery times, and delay rate.

## 2. Test cases

### T-1: Playbook coverage
- **Input:** the client journey from discovery to monthly optimization.
- **Step:** verify a playbook exists for every stage.
- **Acceptance criterion:** every stage has a playbook in `playbooks/`.

### T-2: Founder independence
- **Input:** one playbook and a non-founder team member.
- **Step:** ask the member to execute the stage from the playbook only.
- **Acceptance criterion:** the stage completes without founder intervention.

### T-3: Acceptance criteria per client
- **Input:** an active client folder.
- **Step:** verify acceptance criteria are documented.
- **Acceptance criterion:** every client has documented acceptance criteria via `client_acceptance_tests.md`.

### T-4: Checklist per launch
- **Input:** a deliverable ready for delivery.
- **Step:** verify the pre-launch checklist was run.
- **Acceptance criterion:** the seven checks were run and signed before delivery.

### T-5: Monthly review exists
- **Input:** a Managed Ops subscription client.
- **Step:** verify a documented monthly review was run.
- **Acceptance criterion:** the monthly review is run before the renewal date.

### T-6: SLA per service
- **Input:** the service ladder rungs.
- **Step:** verify a declared SLA for every rung.
- **Acceptance criterion:** every service has a documented SLA.

### T-7: Onboarding time known
- **Input:** a client onboarding record.
- **Step:** measure the time from payment to Kick-off.
- **Acceptance criterion:** the time is documented and ≤ 24 hours.

### T-8: Delivery time known
- **Input:** a completed engagement.
- **Step:** measure delivery time against the rung target.
- **Acceptance criterion:** the time is documented and matches the rung target.

### T-9: Project delay rate low
- **Input:** the last 10 engagements.
- **Step:** calculate the share of late engagements.
- **Acceptance criterion:** delay rate ≤ 10%.

### T-10: Success metrics per client
- **Input:** an active client folder.
- **Step:** verify success metrics are documented.
- **Acceptance criterion:** every client has documented success metrics.

### T-11: Non-negotiables compliance
- **Input:** all Layer 10 playbooks.
- **Step:** search for fake proof, guarantees, scraping, cold messaging, LinkedIn automation, PII.
- **Acceptance criterion:** zero violations across all playbooks.

### T-12: Bilingual balance
- **Input:** every `.md` file in `playbooks/`.
- **Step:** verify two H1 sections (Arabic then English) and content parity.
- **Acceptance criterion:** every file is bilingual with two complete, mirroring sections.

## 3. Overall acceptance criteria

- Layer 10 readiness is "verified" when cases T-1 through T-12 all pass.
- Any failed case is resolved before the layer's readiness is claimed.
- Test results feed `playbooks/readiness.md` and `playbooks/monthly_optimization/improvement_backlog.md`.

## 4. Governance rules (non-negotiables)

- No fake proof in any test case.
- Test results are recorded as they are — no embellishment.
- No test case bypasses the compliance check T-11.

## 5. Observability hooks

- Log each case result: `pass` / `fail`.
- Periodic review of test results before every readiness score update.

## 6. Rollback procedure

If readiness was declared and a test case later fails:
1. Lower the readiness score in `playbooks/readiness.md`.
2. Record the incident in the governance log.
3. Add an item to the improvement backlog to address the cause.
