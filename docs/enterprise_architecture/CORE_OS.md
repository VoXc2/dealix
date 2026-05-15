# Core OS — العمود الفقري

## الهدف في المخطط

هوية مشتركة، **أحداث** موحّدة، كيانات (`Client`, `Project`, `Workspace`, `User`, `Agent`, …)، وسجلات تدقيق يمكن إعادة تشغيلها فلسفيًا: **Dealix يتعلم من الأحداث لا من الذاكرة الضبابية**.

## شكل الحدث الشامل (مرجعي)

```json
{
  "event_id": "EVT-001",
  "event_type": "governance_decision_created",
  "actor_type": "agent",
  "actor_id": "AGT-REV-001",
  "client_id": "CL-001",
  "project_id": "PRJ-001",
  "timestamp": "2026-05-14T10:00:00Z",
  "payload": {}
}
```

## التنفيذ في الريبو

| المكوّن | المسار |
|---------|--------|
| تخزين أحداث الإيرادات (Postgres / عزل worker) | `auto_client_acquisition/revenue_memory/` |
| بوابة مؤسسية قبل AI (جواز + حوكمة) | `auto_client_acquisition/institutional_control_os/` |
| معيار جواز المصدر | `auto_client_acquisition/sovereignty_os/source_passport_standard.py` |
| واجهات API والجلسات | `api/` |

## ملاحظة

لا يوجد مجلد باسم `core_os/` — الاسم **مفاهيمي**؛ التنفيذ موزّع عمدًا بين الذاكرة الحدثية والطبقة المؤسسية.

## روابط

- [SYSTEM_MAP.md](SYSTEM_MAP.md) — [API_BOUNDARIES.md](API_BOUNDARIES.md)
