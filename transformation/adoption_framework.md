# العربية

# إطار التبنّي وإدارة التغيير — الطبقة ١١

**المالك:** قائد التحويل في Dealix بالاشتراك مع راعي العميل التنفيذي.

## الغرض

أفضل سير عمل مُعاد تصميمه يفشل إذا لم يستخدمه الناس. إطار التبنّي يضمن أن التحويل يصل إلى السلوك اليومي، لا إلى عرض تقديمي فقط. التبنّي ليس تدريباً لمرة واحدة؛ هو إيقاع متكرر من الاستخدام والملاحظة والتصحيح.

## الركائز الأربع للتبنّي

### ١. الرعاية التنفيذية

لا يبدأ تحويل بدون راعٍ تنفيذي مسمّى يملك القرار والميزانية. يُسجَّل الراعي ضمن `auto_client_acquisition/adoption_os/client_roles.py`. الراعي يفتتح كل مرحلة ويراجع تقرير القيمة الشهري.

### ٢. أبطال سير العمل

لكل سير عمل مُعاد تصميمه بطل واحد على الأقل — مستخدم يومي يفهم العملية الجديدة ويساعد زملاءه. الأبطال هم قناة الملاحظات الأولى نحو `auto_client_acquisition/adoption_os/friction_log.py`.

### ٣. منتجات التدريب

تُبنى مواد التدريب عبر `auto_client_acquisition/adoption_os/training_products.py`: دليل سريع، جلسة مباشرة، وقائمة تحقق للمستخدم الجديد. كل مادة ثنائية اللغة ومرتبطة بحالة استخدام محدّدة، لا بمفهوم عام.

### ٤. حلقة المراجعة

تُدار المراجعة عبر `auto_client_acquisition/adoption_os/adoption_review.py` و`auto_client_acquisition/adoption_os/adoption_dashboard.py`. كل أسبوعين: ما الذي استُخدم؟ أين الاحتكاك؟ ما الذي يجب تبسيطه؟

## درجة التبنّي

تُحسب درجة التبنّي عبر `auto_client_acquisition/adoption_os/adoption_score.py` على مقياس ٠–١٠٠. لا يُرفّع العميل إلى مرحلة العقد الدوري قبل اجتياز فحص الجاهزية في `auto_client_acquisition/adoption_os/retainer_readiness.py`.

## ربط التبنّي بمسار البيع

- **التدقيق:** يُحدَّد الراعي والأبطال المحتملون.
- **التجربة:** أول جلسة تدريب على حالة استخدام واحدة.
- **التحويل:** نشر التدريب عبر سير العمل المُعاد تصميمه.
- **العقد الدوري:** إيقاع مراجعة مستمر وتدريب المستخدمين الجدد.

## القاعدة غير القابلة للتفاوض

التبنّي يُقاس بالاستخدام الفعلي الذي يقدّمه العميل، لا بأرقام مفترضة. لا تُربط درجة التبنّي بنتيجة تجارية مضمونة.

القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

# Adoption and Change Management Framework — Layer 11

**Owner:** Dealix Transformation Lead, jointly with the client Executive Sponsor.

## Purpose

The best redesigned workflow fails if people do not use it. The adoption framework ensures the transformation reaches daily behavior, not just a slide deck. Adoption is not a one-time training; it is a repeating cadence of use, observation, and correction.

## The four pillars of adoption

### 1. Executive sponsorship

No transformation begins without a named executive sponsor who owns the decision and the budget. The sponsor is recorded in `auto_client_acquisition/adoption_os/client_roles.py`. The sponsor opens each stage and reviews the monthly value report.

### 2. Workflow champions

Every redesigned workflow has at least one champion — a daily user who understands the new process and helps colleagues. Champions are the first feedback channel into `auto_client_acquisition/adoption_os/friction_log.py`.

### 3. Training products

Training material is built through `auto_client_acquisition/adoption_os/training_products.py`: a quick guide, a live session, and a new-user checklist. Each item is bilingual and tied to a specific use case, not a general concept.

### 4. The review loop

Review is run through `auto_client_acquisition/adoption_os/adoption_review.py` and `auto_client_acquisition/adoption_os/adoption_dashboard.py`. Every two weeks: what was used? Where is the friction? What should be simplified?

## Adoption score

The adoption score is computed through `auto_client_acquisition/adoption_os/adoption_score.py` on a 0–100 scale. A client is not promoted to the Retainer stage before passing the readiness check in `auto_client_acquisition/adoption_os/retainer_readiness.py`.

## Mapping adoption to the sales path

- **Audit:** Sponsor and candidate champions are identified.
- **Pilot:** First training session on a single use case.
- **Transformation:** Training rolled out across the redesigned workflow.
- **Retainer:** Continuous review cadence and new-user training.

## Non-negotiable

Adoption is measured by actual usage the client supplies, not assumed numbers. The adoption score is not tied to a guaranteed commercial outcome.

Estimated value is not Verified value.
