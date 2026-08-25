# Daily Builder / Open-Source R&D — العقد التشغيلي
**STATUS: CANONICAL v1 · 2026-08-25**

## القاعدة
يوميًا **بناء واحد كحد أقصى** + مرشحان WATCH فقط. إذا لم يمر شيء بعتبة القيمة → **BUILD_NOTHING_NEW** وتُ improved أعلى blocker قائمة بدلًا منه.

## سلم النقاط (من 100 بعد الخصومات)
BUSINESS_VALUE/20 · FOUNDER_TIME_SAVED/15 · DELIVERY_VALUE/15 · TECH_LEVERAGE/10 · MATURITY/10 · SECURITY_PRIVACY/10 · INTEGRATION_EASE/5 · REVERSIBILITY/5 · MAINTENANCE/5 · COST/5
خصومات: DUPLICATION · HYPE · VENDOR_LOCKIN · SECURITY_RISK

## عقد الـPR
PROBLEM · SOURCE/WHY NOW · CURRENT LIMITATION · SOLUTION · WHY THIS OPTION · FILES · DEPENDENCIES · SECURITY · PRIVACY · PERFORMANCE · TESTS · ROLLBACK · BUSINESS VALUE · FOUNDER TIME SAVED · ALTERNATIVES REJECTED · PROOF
**NEVER MERGE — المؤسس يدمج.**

## مصادر المسح (رسمية أولًا)
OpenCode · Hermes Agent · OpenClaw · Ollama · n8n · MCP · agent tooling · LLM observability · retrieval · Postgres · security · CI · Railway · browser agents · sales intelligence · Saudi-market infra.

## سجل القرارات
| التاريخ | BUILD | WATCH | REJECT | الدليل |
|---|---|---|---|---|
| 2026-08-25 | BUILD_NOTHING_NEW — أعلى قيمة اليوم كانت ربط الطاقم الحي بالجدولة (#1249، مدمج) | Railway auto-deploy على main (تحقق تفعيله) · MCP servers catalog للأدوات السعودية | إعادة كتابة أي نظام قائم | session 15 |

## الحالة الحالية (Option A — صادق)
Fleet OWNER_STATE = **OWNER_MISSING** — الدور يعيش خارج نموذج تنفيذ الطاقم:
بحث/مراقبة → implementation packet → OpenCode executive session → worktree → tests → Draft PR → **المؤسس يدمج**.
لا وكيل مكرر، لا OpenCode-daemon من المُجدول.
