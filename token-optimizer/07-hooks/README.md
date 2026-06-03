# 07 — Hooks: ضغط المخرجات تلقائياً

## ما هي Hooks؟

Hooks هي أوامر shell تُشغَّل تلقائياً قبل/بعد أدوات Claude.
تُستخدم لـ:
- تصفية مخرجات الأدوات قبل إرسالها للـ context
- حذف المعلومات غير الضرورية
- تحديد حجم أقصى للمخرجات
- ضغط نتائج bash commands

## الملفات في هذا المجلد

| الملف | الوصف |
|-------|--------|
| `hooks.optimized.json` | ملف hooks جاهز للنسخ |
| `output-filter.sh` | سكريبت تصفية المخرجات |
| `log-trimmer.sh` | تقليص السجلات الطويلة |
| `bash-compressor.sh` | ضغط مخرجات bash |
| `hooks-explained.md` | شرح كل hook وتأثيره |

## تركيب Hooks

```bash
# انسخ ملف hooks
cp token-optimizer/07-hooks/hooks.optimized.json .claude/hooks.json

# أو أضف للإعدادات
cp token-optimizer/07-hooks/hooks.optimized.json .claude/settings.json
```

## أهم Hooks لتوفير التوكنز

### 1. تحديد حجم أقصى لمخرجات الأدوات
```json
{
  "hooks": {
    "PostToolUse": [{
      "type": "truncate_output",
      "max_tokens": 8000
    }]
  }
}
```

### 2. تصفية مخرجات bash
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": {"tool": "Bash"},
      "type": "pipe",
      "command": "head -100"
    }]
  }
}
```

### 3. حقن branch في بداية الجلسة
```json
{
  "hooks": {
    "SessionStart": [{
      "type": "inject_context",
      "command": "echo 'Branch: $(git branch --show-current)'"
    }]
  }
}
```

## التأثير المتوقع

- تصفية mخرجات bash: توفير **60-90%** على الأوامر الصاخبة
- تحديد الحجم الأقصى: منع context overflow
- حقن context في البداية: منع أسئلة توضيحية
