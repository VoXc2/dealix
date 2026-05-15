# Dealix Enterprise Architecture & Operating System Blueprint

هذه الطبقة تجمع الاستراتيجية في **معمارية قابلة للتنفيذ داخل الريبو**: وحدات (modules)، وثائق، واجهات برمجية، سجلات (ledgers)، لوحات معلومات، وبوابات (gates) — بحيث لا يبقى التوجيه مجرد كلام.

## Thesis: Dealix ليس وكالة ذكاء اصطناعي، بل AI Operations OS

المعادلة التشغيلية:

**Data → Governance → AI Assistance → Human Approval → Workflow Execution → Audit → Proof → Value → Capital → Decision**

لا يوجد مخرج ذكاء اصطناعي «يطلع كذا». كل تدفق يمر بسلسلة واضحة:

**Source Passport → Data Classification → LLM Gateway → Governance Runtime → QA → Approval → Audit Event → Proof Event → Value Event → Board Decision**

### لماذا هذا مهم؟

المؤسسات لا تحكم ما لا تراه. أنظمة RAG ووكلاء متعددون وسير عمل آلية خلقوا فجوة بين ما يطلبه المنظمون كدليل حوكمة وما يمكن إثباته عمليًا. Dealix يغلق هذه الفجوة بـ **أحداث مسجّلة، أدلة، وموافقات بشرية** قبل أي إجراء خارجي.

## المبادئ غير القابلة للنقض (تنعكس في الكود والاختبارات)

| المبدأ | المعنى التشغيلي |
|--------|------------------|
| لا بيانات بلا Source Passport | بوابة قبل استخدام AI على بيانات العميل |
| لا AI خارج LLM Gateway | توجيه النماذج، تكلفة، redaction، eval hooks |
| لا مخرج بلا Governance | قرار تشغيلي (ALLOW / DRAFT_ONLY / …) |
| لا إجراء خارجي بلا Approval | قنوات draft-first |
| لا ادّعاء بلا Proof | Proof Pack + Proof Score |
| لا مشروع بلا أصل رأسمالي معرف | تتبع في طبقات رأس المال والتمويل التشغيلي |
| لا قرار كبير بلا إشارة | Command / Board layer |

## الجملة الختامية

**Dealix يفوز عندما يصبح الريبو نظام تشغيل حقيقيًا:** كل وحدة تعرف مسؤوليتها، كل حدث يُسجّل، كل مخاطرة تُحكم، كل قيمة تُثبت، وكل تكرار يتحول إلى أصل داخل نواة واحدة قابلة للتوسع.

## وثائق الطبقة

- [خريطة النظام](SYSTEM_MAP.md) — ربط المخطط بالمسارات الفعلية.
- [حدود واجهات البرمجة](API_BOUNDARIES.md) — تدفقات مسموحة وممنوعة.
- [ترتيب بناء الـ MVP](MVP_BUILD_ORDER.md) — تسلسل التنفيذ دون تشتيت.
- [الاختبارات المطلوبة](TESTS_REQUIRED.md) — عقود الحماية في `tests/`.
- صفحات فرعية لكل OS (CORE، DATA، …، SAUDI، إلخ).

## مراجع داخلية

- `docs/operating_rhythm/` — إيقاع CEO، مجلس التنفيذ، القرار الأسبوعي، والمذكرة الشهرية.
- `docs/agentic_operations/` — وكلاء محكومون، حدود أدوات، handoff، طبقة سعودية للقنوات.
- `docs/evidence_control_plane/` — Evidence Control Plane، الرسم البياني للأدلة، Proof v3، والمساءلة.
- `docs/client_maturity/` — سلم تحول AI، محرك نضج العميل، ومصفوفة العرض.
- `docs/responsible_ai/` — معيار D-RAIOS، Trust Pack، تصنيف مخاطر use cases، ودرجة Responsible AI.
- `docs/compliance_trust_ops/` — Trust Plane والامتثال.
- `docs/intelligence/PROJECT_INTELLIGENCE_AR.md` — استخبارات المشروع.
- `docs/ultimate_manual/REPOSITORY_STRUCTURE_MAP.md` — خريطة المستودع.
