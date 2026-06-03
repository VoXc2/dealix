# دليل تحسين التوكنز الشامل لـ Dealix

## ما هذا؟

هذا المجلد يحتوي على **12 دليلاً متكاملاً** لتخفيض صرف التوكنز بنسبة تصل إلى **90%** عند استخدام Claude Code.
كل مجلد يعالج جانباً مختلفاً من استهلاك التوكنز مع أمثلة جاهزة للنسخ والتطبيق الفوري.

## المجلدات

| # | المجلد | الوصف | التوفير المتوقع |
|---|--------|--------|-----------------|
| 01 | `01-claudeignore/` | استبعاد الملفات غير الضرورية | 40-90% |
| 02 | `02-claude-md/` | تحسين ملف CLAUDE.md | 30-60% |
| 03 | `03-session-management/` | إدارة الجلسات بكفاءة | 20-50% |
| 04 | `04-model-routing/` | اختيار النموذج المناسب | 50-80% |
| 05 | `05-mcp-discipline/` | ضبط خوادم MCP | 10-30% |
| 06 | `06-subagents/` | التفويض للـ Subagents | 30-70% |
| 07 | `07-hooks/` | Hooks لضغط المخرجات | 60-90% |
| 08 | `08-prompt-engineering/` | صياغة البرومبت بكفاءة | 30-50% |
| 09 | `09-file-handling/` | قراءة الملفات بذكاء | 20-60% |
| 10 | `10-tools-monitoring/` | أدوات المراقبة والقياس | متابعة |
| 11 | `11-git-hygiene/` | نظافة Git وGitHub | 10-40% |
| 12 | `12-environment-config/` | متغيرات البيئة والإعدادات | 20-50% |

## التطبيق السريع (الأثر الأكبر أولاً)

```bash
# الخطوة 1: نسخ .claudeignore الجاهز
cp token-optimizer/01-claudeignore/.claudeignore.dealix .claudeignore

# الخطوة 2: استبدال CLAUDE.md بالنسخة المحسّنة
cp token-optimizer/02-claude-md/CLAUDE.optimized.md CLAUDE.md

# الخطوة 3: نسخ إعدادات Claude
cp token-optimizer/12-environment-config/settings.optimized.json .claude/settings.json

# الخطوة 4: تطبيق الـ Hooks
cp token-optimizer/07-hooks/hooks.optimized.json .claude/hooks.json
```

## القاعدة الذهبية

> **كل سطر لا يراه Claude = توكنز محفوظة**

## المصادر

- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Token Optimization Guide - Stop the $1,600 Bill](https://buildtolaunch.substack.com/p/claude-code-token-optimization)
- [18 Token Management Hacks](https://www.mindstudio.ai/blog/claude-code-token-management-hacks)
- [Token Optimization Cheat Sheet](https://navant.github.io/posts/claude-code-token-optimisation-cheat-sheet/)
- [7 Practical Techniques](https://claudecode-lab.com/en/blog/claude-code-token-optimization/)
