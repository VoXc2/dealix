# 12 — Environment Config: متغيرات البيئة والإعدادات

## ما يمكن ضبطه في البيئة

تحكم في سلوك Claude Code عبر متغيرات البيئة وملف `.claude/settings.json`.

## الملفات في هذا المجلد

| الملف | الوصف |
|-------|--------|
| `settings.optimized.json` | إعدادات Claude المحسّنة الجاهزة |
| `env-vars.md` | متغيرات البيئة لتحسين التوكنز |
| `thinking-budget.md` | التحكم في ميزانية التفكير الموسّع |
| `apply-all.sh` | سكريبت تطبيق كل الإعدادات دفعة واحدة |

## أهم متغيرات البيئة

```bash
# تحديد نموذج الـ Subagents (الأرخص)
export CLAUDE_CODE_SUBAGENT_MODEL=haiku

# تحديد ميزانية التفكير الموسّع
export MAX_THINKING_TOKENS=8000

# تعطيل auto-compact (للتحكم اليدوي)
export CLAUDE_CODE_AUTO_COMPACT=false

# حجم أقصى للـ context buffer
export CLAUDE_CODE_MAX_TOOL_OUTPUT_TOKENS=8000
```

## التطبيق الفوري

```bash
# تطبيق كل الإعدادات
bash token-optimizer/12-environment-config/apply-all.sh

# أو يدوياً
mkdir -p .claude
cp token-optimizer/12-environment-config/settings.optimized.json .claude/settings.json
```
