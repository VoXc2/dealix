#!/bin/bash
# apply-all.sh — تطبيق كل إعدادات تحسين التوكنز دفعة واحدة
# الاستخدام: bash token-optimizer/12-environment-config/apply-all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TOKEN_OPT_DIR="$SCRIPT_DIR/.."

echo "================================================"
echo "  Dealix Token Optimizer — تطبيق كل الإعدادات"
echo "================================================"
echo ""

# 1. .claudeignore
echo "1️⃣  تطبيق .claudeignore..."
if [ -f "$PROJECT_ROOT/.claudeignore" ]; then
    echo "   .claudeignore موجود مسبقاً — نسخ احتياطي → .claudeignore.bak"
    cp "$PROJECT_ROOT/.claudeignore" "$PROJECT_ROOT/.claudeignore.bak"
fi
cp "$TOKEN_OPT_DIR/01-claudeignore/.claudeignore.dealix" "$PROJECT_ROOT/.claudeignore"
echo "   ✅ .claudeignore مطبّق ($(wc -l < "$PROJECT_ROOT/.claudeignore") سطر)"

# 2. .claude/settings.json
echo ""
echo "2️⃣  تطبيق .claude/settings.json..."
mkdir -p "$PROJECT_ROOT/.claude"
if [ -f "$PROJECT_ROOT/.claude/settings.json" ]; then
    echo "   settings.json موجود مسبقاً — نسخ احتياطي → settings.json.bak"
    cp "$PROJECT_ROOT/.claude/settings.json" "$PROJECT_ROOT/.claude/settings.json.bak"
fi
cp "$TOKEN_OPT_DIR/12-environment-config/settings.optimized.json" "$PROJECT_ROOT/.claude/settings.json"
echo "   ✅ settings.json مطبّق"

# 3. CLAUDE.md (اختياري — يعرض الفرق فقط)
echo ""
echo "3️⃣  CLAUDE.md الحالي:"
if [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
    current_lines=$(wc -l < "$PROJECT_ROOT/CLAUDE.md")
    current_words=$(wc -w < "$PROJECT_ROOT/CLAUDE.md")
    echo "   السطور: $current_lines"
    echo "   الكلمات: $current_words (≈ $((current_words / 3)) توكن)"

    if [ "$current_lines" -gt 150 ]; then
        echo "   ⚠️  تحذير: CLAUDE.md كبير جداً (> 150 سطر)"
        echo "   📖 راجع: token-optimizer/02-claude-md/CLAUDE.optimized.md"
    else
        echo "   ✅ CLAUDE.md بحجم معقول"
    fi
else
    echo "   CLAUDE.md غير موجود. انسخ القالب:"
    echo "   cp token-optimizer/02-claude-md/CLAUDE.optimized.md CLAUDE.md"
fi

# 4. التحقق من متغيرات البيئة
echo ""
echo "4️⃣  متغيرات البيئة المقترحة:"
echo "   أضف هذه لـ ~/.bashrc أو ~/.zshrc:"
echo ""
echo "   export CLAUDE_CODE_SUBAGENT_MODEL=haiku"
echo "   export MAX_THINKING_TOKENS=8000"
echo "   export CLAUDE_CODE_MAX_TOOL_OUTPUT_TOKENS=8000"

# 5. التحقق من skills
echo ""
echo "5️⃣  Skills جاهزة للاستخدام:"
ls "$TOKEN_OPT_DIR/02-claude-md/skills/" | while read f; do
    echo "   - @token-optimizer/02-claude-md/skills/$f"
done

# 6. ملخص
echo ""
echo "================================================"
echo "  ملخص التطبيق"
echo "================================================"
echo ""
echo "  ✅ .claudeignore مطبّق"
echo "  ✅ .claude/settings.json مطبّق"
echo "  📋 CLAUDE.md — راجع يدوياً"
echo "  📋 متغيرات البيئة — أضف يدوياً لـ ~/.bashrc"
echo ""
echo "  التوفير المتوقع: 50-90% من استهلاك التوكنز"
echo ""
echo "  📚 وثائق كاملة: token-optimizer/README.md"
echo "================================================"
