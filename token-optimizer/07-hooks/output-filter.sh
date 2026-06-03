#!/bin/bash
# output-filter.sh — تصفية مخرجات bash قبل إرسالها للـ context
# الاستخدام: some_command | bash output-filter.sh [max_lines]

MAX_LINES=${1:-100}

# قراءة stdin
output=$(cat)

# عدد الأسطر الفعلية
line_count=$(echo "$output" | wc -l)

if [ "$line_count" -gt "$MAX_LINES" ]; then
    echo "$output" | head -"$MAX_LINES"
    echo ""
    echo "--- [تم قطع المخرجات: $line_count سطر → $MAX_LINES سطر | وُفّر $((line_count - MAX_LINES)) سطر] ---"
else
    echo "$output"
fi
