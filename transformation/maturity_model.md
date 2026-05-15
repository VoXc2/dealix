# العربية

# نموذج نضج الذكاء الاصطناعي — الطبقة ١١ (التحويل)

**المالك:** قائد التحويل في Dealix (Transformation Lead).

## الغرض

نموذج النضج هو الأداة الأولى التي يستخدمها Dealix عند دخول أي شركة. يحوّل سؤالاً غامضاً — «هل أنتم جاهزون للذكاء الاصطناعي؟» — إلى درجة قابلة للقياس وخريطة قابلة للتنفيذ. لا يبيع Dealix الذكاء الاصطناعي كإضافة فوق العمليات القائمة، بل يعيد تصميم تشغيل الشركة حوله. نموذج النضج هو نقطة البداية لهذا التصميم.

## المستويات الخمسة

| المستوى | الاسم | الوصف | الإشارة الحاسمة |
|---|---|---|---|
| ١ | يدوي | لا توجد أتمتة؛ القرارات تعتمد على الذاكرة الفردية | لا يوجد مصدر بيانات موثّق |
| ٢ | مُرقمن | بيانات مخزّنة لكن متفرقة؛ أدوات منفصلة | مصادر بيانات معروفة لكن غير موحّدة |
| ٣ | مُساعَد | الذكاء الاصطناعي يقترح مسودّات؛ الإنسان يوافق | مالك سير عمل + مسار موافقة واضح |
| ٤ | مُعاد التصميم | سير العمل أُعيد بناؤه حول الذكاء الاصطناعي؛ حلقات أدلة | مقياس نجاح مُعرَّف + قيمة شهرية مُسجَّلة |
| ٥ | مؤسسي | الذكاء الاصطناعي طبقة تشغيل أساسية؛ حوكمة وملاحظة مستمرة | درجة تبنّي ≥ ٨٥ + سحب توسّع |

## كيف نسجّل الدرجة

تُحسب الدرجة عبر ثمانية أبعاد تطابق `auto_client_acquisition/adoption_os/adoption_score.py`: الراعي التنفيذي، مالك سير العمل، جاهزية البيانات، تفاعل المستخدمين، اكتمال الموافقات، وضوح الأدلة، الإيقاع الشهري، وسحب التوسّع. كل بُعد من ٠ إلى ١٠٠، والمجموع المرجّح يعطي درجة نضج من ٠ إلى ١٠٠.

## ربط النضج بمسار البيع

- **المستوى ١–٢:** يبدأ العميل بـ **التدقيق (Audit)** — خريطة تحويل وتشخيص.
- **المستوى ٢–٣:** **التجربة (Pilot)** — إثبات حالة استخدام واحدة بأدلة.
- **المستوى ٣–٤:** **التحويل (Transformation)** — إعادة تصميم متعدد المراحل.
- **المستوى ٤–٥:** **العقد الدوري (Retainer)** — طبقة تشغيل شهرية.

يطابق هذا سُلَّم الخدمات في `docs/COMPANY_SERVICE_LADDER.md` ومراحل الانتشار في `auto_client_acquisition/enterprise_rollout_os/rollout_stage.py`.

## القاعدة غير القابلة للتفاوض

كل درجة نضج فرضية مبنية على إشارات يقدّمها العميل، وليست وعداً بنتيجة. لا تُربط أي حالة استخدام بعائد مضمون — فقط بفرضية عائد مُثبتة بأدلة.

القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

# AI Maturity Model — Layer 11 (Transformation)

**Owner:** Dealix Transformation Lead.

## Purpose

The maturity model is the first instrument Dealix uses when entering any company. It converts a vague question — "Are you ready for AI?" — into a measurable score and an executable map. Dealix does not sell AI as a bolt-on above existing operations; it redesigns how the company runs around it. The maturity model is the starting point of that redesign.

## The five levels

| Level | Name | Description | Decisive signal |
|---|---|---|---|
| 1 | Manual | No automation; decisions rely on individual memory | No documented data source |
| 2 | Digitized | Data stored but fragmented; disconnected tools | Data sources known but not unified |
| 3 | Assisted | AI proposes drafts; a human approves | Workflow owner + clear approval path |
| 4 | Redesigned | Workflow rebuilt around AI; evidence loops | Defined success metric + recorded monthly value |
| 5 | Institutional | AI is a core operating layer; continuous governance and observability | Adoption score ≥ 85 + expansion pull |

## How we score

The score is computed across eight dimensions matching `auto_client_acquisition/adoption_os/adoption_score.py`: executive sponsor, workflow owner, data readiness, user engagement, approval completion, proof visibility, monthly cadence, and expansion pull. Each dimension runs 0–100, and the weighted total yields a maturity score of 0–100.

## Mapping maturity to the sales path

- **Level 1–2:** Client starts with the **Audit** — transformation map and diagnostic.
- **Level 2–3:** **Pilot** — prove one use case with evidence.
- **Level 3–4:** **Transformation** — multi-phase redesign.
- **Level 4–5:** **Retainer** — monthly operating layer.

This mirrors the service ladder in `docs/COMPANY_SERVICE_LADDER.md` and the rollout stages in `auto_client_acquisition/enterprise_rollout_os/rollout_stage.py`.

## Non-negotiable

Every maturity score is a hypothesis built on signals the client supplies — not a promise of outcome. No use case is tied to a guaranteed return; only to an evidence-backed ROI hypothesis.

Estimated value is not Verified value.
