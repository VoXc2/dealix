# متغيرات البيئة لتحسين التوكنز

## قائمة كاملة بالمتغيرات المفيدة

### نموذج الـ Subagents
```bash
export CLAUDE_CODE_SUBAGENT_MODEL=haiku
```
**التأثير**: كل Subagent يستخدم Haiku بدلاً من Sonnet.
**التوفير**: 70-80% على مهام الاستكشاف والبحث.
**متى تُغيره**: فقط إذا كانت Subagents تؤدي مهاماً معقدة تحتاج Sonnet.

---

### ميزانية التفكير الموسّع
```bash
export MAX_THINKING_TOKENS=8000
```
**التأثير**: يحدد كمية التفكير الداخلي الذي يؤديه Claude.
**التوفير**: 50-90% على المهام التي تُفعّل Extended Thinking.
**متى تزيده**: عند مهام معقدة جداً تحتاج تحليلاً عميقاً (حينها ضعه 20,000+).
**متى تُقلّله**: لمعظم المهام اليومية (4,000-8,000 كافٍ).

---

### حجم مخرجات الأدوات
```bash
export CLAUDE_CODE_MAX_TOOL_OUTPUT_TOKENS=8000
```
**التأثير**: يحدد الحد الأقصى لمخرجات أي أداة (Read, Bash, etc).
**التوفير**: يمنع context overflow من مخرجات ضخمة.
**القيم الموصى بها**:
- للمهام البسيطة: `4000`
- للمهام المعتادة: `8000`
- للمراجعات الكبيرة: `16000`

---

### تعطيل Auto-Compact
```bash
export CLAUDE_CODE_AUTO_COMPACT=false
```
**التأثير**: يمنع Claude من ضغط السياق تلقائياً دون علمك.
**متى تستخدمه**: عندما تريد التحكم يدوياً في وقت `/compact`.

---

### تفعيل Auto-Compact
```bash
export CLAUDE_CODE_AUTO_COMPACT=true
```
**التأثير**: يضغط Claude السياق تلقائياً عند الحاجة.
**متى تستخدمه**: إذا نسيت `/compact` باستمرار.

---

## ملف .env.claude موصى به

```bash
# .env.claude — متغيرات Claude Code لـ Dealix
# أضف هذا لـ ~/.bashrc أو ~/.zshrc

# نموذج Subagents (أرخص)
export CLAUDE_CODE_SUBAGENT_MODEL=haiku

# تحديد ميزانية التفكير
export MAX_THINKING_TOKENS=8000

# حجم أقصى لمخرجات الأدوات
export CLAUDE_CODE_MAX_TOOL_OUTPUT_TOKENS=8000
```

```bash
# لتطبيق فوري
source ~/.env.claude
# أو
echo 'source ~/.env.claude' >> ~/.bashrc
```

---

## مقارنة الإعدادات

| الإعداد | القيمة الافتراضية | القيمة المحسّنة | التوفير |
|---------|------------------|-----------------|---------|
| SUBAGENT_MODEL | sonnet | haiku | 80% على Subagents |
| MAX_THINKING_TOKENS | 100,000+ | 8,000 | 90% على Extended Thinking |
| MAX_TOOL_OUTPUT_TOKENS | غير محدود | 8,000 | يمنع Overflow |
