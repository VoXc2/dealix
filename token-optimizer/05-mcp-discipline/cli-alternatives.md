# بدائل CLI لخوادم MCP الشائعة

## المبدأ

CLI أسرع وأوفر في التوكنز. MCP يُضيف overhead كبيراً.

---

## GitHub MCP → gh CLI

```bash
# قائمة PRs
gh pr list --state open

# تفاصيل PR
gh pr view 123

# قائمة Issues
gh issue list --state open

# إنشاء PR
gh pr create --title "..." --body "..."

# تشغيل Actions
gh workflow run deploy.yml

# فحص CI
gh pr checks 123
```

**التوفير**: 70-90% من توكنز GitHub MCP

---

## Database MCP → psql CLI

```bash
# اتصال مباشر
psql $DATABASE_URL

# استعلام محدد
psql $DATABASE_URL -c "SELECT count(*) FROM clients;"

# تصدير نتيجة
psql $DATABASE_URL -c "\COPY clients TO 'export.csv' CSV HEADER"

# عرض schema
psql $DATABASE_URL -c "\d clients"
```

**التوفير**: 60-80% من توكنز Database MCP

---

## Filesystem MCP → Read/Write Tools مباشرة

بدلاً من MCP Filesystem server، استخدم:
- `Read` tool مباشرة بالمسار الكامل
- `Bash` tool مع `find` للبحث
- `Grep` tool للبحث في المحتوى

---

## Web Search MCP → WebSearch Tool

Tool المُدمج أخف من معظم MCP servers للبحث.

---

## جدول التوفير

| العملية | MCP Token Cost | CLI Token Cost | التوفير |
|---------|---------------|----------------|---------|
| قائمة PRs | 400 | 30 | 93% |
| تفاصيل PR | 800 | 100 | 88% |
| query DB | 600 | 50 | 92% |
| بحث ملف | 300 | 20 | 93% |

---

## متى تستخدم MCP؟

استخدم MCP فقط عندما:
1. لا يوجد CLI بديل
2. العملية معقدة وتتطلب context ثري
3. تحتاج نتيجة منظمة (JSON) للمعالجة
