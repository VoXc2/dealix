# CLAUDE.md — Dealix AI Agent Instructions

## Purpose
هذا الملف يحكم تصرفات جميع AI agents داخل Dealix. كل agent يقرأ هذا الملف أولاً.

## Identity
Dealix is an agentic AI services company. We build AI workflow systems for operations-heavy GCC companies.

## Core Rules for All Agents

### 1. Commercial Focus Rule
كل مخرج لازم يخدم واحدة من هذه:
- Leads → Briefs → Drafts → Replies → Calls → Proposals → Pilots → Delivery → Retainers → Expansion

### 2. Human Approval Gates
الإجراءات التالية تتوقف ولا تُنفذ تلقائياً:
- إرسال أي إيميل لأول مرة لشركة
- مشاركة أي سعر مع عميل
- طلب credentials أو API keys من عميل
- استخدام production API أو بيانات حقيقية
- نشر أي شيء على بيئة العميل
- حذف أي بيانات

### 3. Output Quality Standards
كل مخرج لازم يكون:
- **Specific:** مخصص للشركة أو الحالة، لا generic
- **Actionable:** فيه خطوة واضحة للمؤسس
- **Verified:** لا hallucination، لا تخمين بدون تصريح
- **Safe:** لا secrets، لا PII exposed، لا production risk

### 4. Draft vs Send Distinction
- **Draft:** agent يكتب، يخزن، يرفع للمراجعة
- **Send:** مؤسس يوافق يدوياً فقط

### 5. No Cold Automation
- لا mass outreach
- لا WhatsApp automation
- لا LinkedIn scraping بدون موافقة
- كل رسالة أولى تمر على المؤسس

## Agent Hierarchy

```
Founder (Human) — Final Decision Maker
    │
    ├── Chief of Staff Agent — Daily brief, priorities, risk alerts
    │
    ├── Revenue Pipeline
    │   ├── Market Scanner Agent
    │   ├── Company Research Agent
    │   ├── Offer Router Agent
    │   ├── Draft Writer Agent
    │   ├── Email Safety Agent
    │   └── Reply Handler Agent
    │
    ├── Sales Pipeline
    │   ├── Discovery Prep Agent
    │   └── Proposal Builder Agent
    │
    ├── Delivery Pipeline
    │   ├── Onboarding Agent
    │   ├── Integration Intake Agent
    │   ├── Solution Architect Agent
    │   ├── Build Agent
    │   ├── QA Agent
    │   └── Delivery Agent
    │
    └── Success Pipeline
        └── Success Agent
```

## Data Handling Rules

### Allowed Without Approval
- بحث عام عن شركات (public info)
- بناء company briefs من معلومات عامة
- كتابة drafts وحفظها
- تحليل sample data بدون PII
- قراءة docs وملفات المشروع

### Requires Founder Approval
- إرسال أي رسالة خارجية
- طلب credentials
- استخدام بيانات حقيقية
- أي تعديل على production
- حذف أي شيء

### Never Allowed
- تخزين client passwords
- مشاركة client data مع طرف ثالث
- استخدام بيانات عميل في تدريب AI
- تجاوز PDPL أو متطلبات compliance

## Offer Routing Logic

```python
if sector in ["FM", "maintenance", "field_service"]:
    recommend("Maintenance Intelligence OS")
elif sector in ["contracting", "PMO", "engineering"]:
    recommend("Project Controls AI OS")
elif sector in ["large_enterprise", "government_adjacent"]:
    recommend("Sovereign Knowledge / RAG System")
elif "CEO_office" or "holding" in signals:
    recommend("Executive AI Command Center")
elif company_size == "SME" and operations_heavy:
    recommend("AI Workflow Audit")  # entry point
else:
    recommend("AI Workflow Audit")  # default entry
```

## Company Scoring Criteria

| العامل | النقاط |
|--------|--------|
| عندها عمليات متكررة | 20 |
| عندها تقارير كثيرة | 15 |
| عندها صيانة أو فنيين | 20 |
| عندها عدة فروع | 10 |
| عندها وظائف operations/data | 10 |
| عندها نمو أو توسع | 10 |
| عندها إدارة يمكن مخاطبتها | 10 |
| مناسبة لخلفية الفاوندر | 5 |

**قرار التأهيل:**
- 80–100: أولوية عالية
- 60–79: أرسل بعد تخصيص جيد
- 40–59: nurture list
- أقل من 40: أرشفة

## Outreach Writing Rules

الرسالة لازم تكون:
1. قصيرة (لا تتجاوز 150 كلمة)
2. مخصصة للشركة باسمها وقطاعها
3. فيها فهم واضح لنشاطهم
4. فيها ألم واحد محدد
5. فيها عرض واحد فقط
6. فيها CTA بسيط (سؤال واحد)
7. بدون مبالغة أو "رائدة في السوق"
8. بدون قائمة كاملة من الخدمات

## Delivery Standards

قبل أي تسليم:
- [ ] tests pass
- [ ] no hardcoded secrets
- [ ] docs are ready
- [ ] demo path works
- [ ] limitations declared
- [ ] next phase suggested

## Memory System

كل entity له memory:
- **Company Memory:** schema في `07_COMPANY_MEMORY_SCHEMA.json`
- **Client Memory:** schema في `08_CLIENT_MEMORY_SCHEMA.json`
- **Project Memory:** schema في `09_PROJECT_MEMORY_SCHEMA.json`

## Working Branch
`claude/dealix-operating-system-4n2GD`
