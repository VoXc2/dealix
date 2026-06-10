#!/bin/bash
# project-map-generator.sh
# يُولّد خريطة المشروع بدون محتوى الملفات
# الاستخدام: bash token-optimizer/09-file-handling/project-map-generator.sh

echo "=== Dealix Project Map ==="
echo "Generated: $(date '+%Y-%m-%d %H:%M')"
echo ""

echo "## Directory Structure (3 levels)"
tree -L 3 --gitignore \
    -I "__pycache__|node_modules|.git|*.pyc|.venv|venv|env|dist|build|.next|coverage|htmlcov" \
    --dirsfirst \
    2>/dev/null || find . -maxdepth 3 -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/__pycache__/*" | sort

echo ""
echo "## Python Modules (api + core)"
echo "### API Routes:"
ls api/routes/*.py 2>/dev/null | xargs -I{} basename {} .py | sed 's/^/  - /'

echo "### Core Modules:"
ls core/*.py 2>/dev/null | xargs -I{} basename {} .py | sed 's/^/  - /'

echo ""
echo "## Key Files Summary"
for f in CLAUDE.md README.md pyproject.toml docker-compose.yml; do
    if [ -f "$f" ]; then
        lines=$(wc -l < "$f")
        echo "  - $f ($lines lines)"
    fi
done

echo ""
echo "## Endpoints (auto-detected)"
grep -rn "@router\.\|@app\." api/routes/ 2>/dev/null \
    | grep -E "get|post|put|delete|patch" \
    | sed 's/.*@router\.\([a-z]*\)(\(.*\))/  \1 \2/' \
    | head -30

echo ""
echo "## Recent Changes"
git log --oneline -10 2>/dev/null || echo "  (not a git repo)"

echo ""
echo "=== End of Project Map ==="
