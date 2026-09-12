# Dealix Fresh-Market OpenCode Execution Policy — 2026-09-12

## القرار المعتمد

اعتبار أي تسعير عام أو عرض سوقي قديم **مرجعًا تاريخيًا فقط** وليس سلطة تسعير حالية. السوق السعودي الحالي والأدلة الفعلية هما مصدر الأولوية التجارية، مع بقاء Company Machine واحدة وHermes كطبقة orchestration وSession Factory كمسار تنفيذ محكوم.

هذه السياسة تتبع المعمارية المعتمدة في `docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md` ولا تعيد فرض نموذج «خمسة وكلاء دائمين» القديم.

## معمارية الوكلاء الحالية

- Dealix تعمل كـ **Agentic Holding** واحدة: Group → Sector Companies → Arm Pods → Specialist Logical Agents.
- عدد الوكلاء المنطقيين ديناميكي وقابل للتوسع حسب القطاعات والأذرعة والقدرات.
- الوكيل المنطقي ليس process دائمًا؛ workers الفعلية تُنشأ عند وجود عمل وتُدار بالموارد.
- كل وكيل أو ذراع أو قطاع يجب أن يملك parent وauthority scope وevidence trail؛ لا orphan agents.
- لا CRM أو Company Brain أو Approval Center أو Scheduler أو Model Router أو Economic Truth موازٍ لكل قطاع؛ السلطة تبقى مركزية في Dealix Group.
- invariant «exactly five permanent agents» **deprecated**. الأسماء التاريخية يمكن أن تبقى compatibility/accountability aliases أثناء الهجرة، لكنها ليست حدًا معماريًا.
- invariant `DEEP_WIP_MAX=3` العالمي **deprecated** كحد ثابت للشركة ويستبدل بـ Resource-Aware Concurrency Governor. الكتابة المتوازية على الريبو تظل عبر isolated worktrees فقط.

## قانون التنفيذ

- كل مهمة تحتاج research أو review أو engineering أو commercial reasoning أو negotiation planning أو delivery design تمر افتراضيًا عبر OpenCode عندما يكون ذلك أوفر وأقوى من التنفيذ الحتمي.
- health checks / fingerprints / deterministic verification / scheduler audits لا تستهلك LLM عندما تكفي البرمجة الحتمية.
- Local Ollama يستخدم للفرز والاستخراج والاستدلال منخفض المخاطر عندما يكون كافيًا.
- يبدأ routing بأرخص نموذج كافٍ، ثم يصعد فقط إذا فشل acceptance أو احتاجت المخاطرة/التعقيد نموذجًا أقوى.
- paid spill خارج الحدود المعتمدة يبقى مقفولًا افتراضيًا.
- كل job تعديلي يحتاج isolated worktree، deterministic acceptance، receipt، ومرجع evidence قبل اعتباره ناجحًا.

## Resource-Aware Concurrency Governor

لا نثبت عدد workers على رقم دائم. الميزانية تتغير حسب:

- CPU load وRAM المتاحة وswap/disk pressure.
- provider/model quotas والتكلفة والـlatency.
- task risk والقيمة الاقتصادية المتوقعة والمدة.
- عدد writers الحاليين وتوفر worktrees.
- contention domain وأي incident تشغيلي.

يمكن للبحث read-only أن يتوسع أكثر من أعمال repository mutation. أي زيادة concurrency يجب أن تكون قابلة للقياس والتراجع ولا تخلق worker explosion.

## اقتصاد OpenCode والنماذج

لا يوجد سقف jobs مصطنع إذا كانت الموارد والـprovider يسمحان. الترتيب الافتراضي:

1. deterministic / no-model عندما لا نحتاج reasoning.
2. Local Ollama للتصنيف والاستخراج والعمل الرخيص المحدود.
3. OpenCode models الاقتصادية للأعمال الكثيفة عندما تجتاز acceptance.
4. نماذج أقوى فقط للهندسة المعمارية، security، الأعمال عالية القيمة، أو عند فشل الأرخص.

القرار يبنى على observed Dealix benchmarks والتكلفة والقبول، لا على اسم نموذج أو hype.

## السياسة التجارية

- لا أسعار عامة ثابتة تشكل authority على الموقع.
- كل diagnostics الأولية **مجانية وبدون بطاقة**.
- المسار القانوني: `Market Signal → Evidence → Real Interaction/Consent → Free Diagnostic → Qualified Discovery → Customer-Specific Solution → Customer-Specific Quote → Pilot Decision → Verified Payment → Delivery → Customer-Validated Proof → Expansion`.
- التفاوض يبنى داخل **internal evidence-based envelope** وليس public price list.
- envelope يعتمد على: السوق الحالي، scope، complexity، integration burden، delivery cost، risk، urgency، customer value، support/SLA، proof potential، والبدائل التنافسية.
- لا يخترع الوكيل سعرًا أو ROI أو compliance أو revenue أو علاقة أو consent إذا لم توجد أدلة كافية.
- لا discount بلا scope/payment/term trade-off موثق.
- Research != Relationship؛ Public Contact != Consent؛ Quote != Invoice؛ Invoice != Payment؛ Payment != Revenue؛ Delivery != Customer Value؛ Customer Value != Public Proof.

## الصلاحيات

الأعمال الداخلية المحدودة والمنخفضة الأثر آلية عندما تسمح policy. أي send/publish/payment/spend/contract/tender/DNS/DB/secret/firewall/production deploy أو merge محمي يحتاج exact-action authority حسب governance الحالية. لا يجوز للوكيل اعتماد فعله المادي بنفسه.

## معيار النجاح

نجاح العملية ليس exit code. كل job يحتاج acceptance receipt، evidence refs، truth-safe state transition، next safe action، وعدم اختراع proof أو relationship أو revenue. التحسين الذاتي يجب أن يكون version-controlled وقابلًا للرجوع والقياس.
