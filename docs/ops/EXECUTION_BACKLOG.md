# Dealix Execution Backlog

This backlog tracks implementation work that comes from the operating plan, spreadsheet exports, launch checklist, and repository gap audit.

To regenerate this file from a Google Sheet CSV export:

```bash
python scripts/import_execution_backlog.py --csv dealix_backlog.csv
```

Expected CSV columns can be English or Arabic:

| Purpose | Supported columns |
|---|---|
| Task title | `title`, `task`, `item`, `المهمة`, `العنوان` |
| Priority | `priority`, `prio`, `الأولوية` |
| Status | `status`, `state`, `الحالة` |
| Owner | `owner`, `assignee`, `المسؤول` |
| Area | `area`, `category`, `المجال` |
| Notes | `notes`, `description`, `الوصف` |

## Current P0 execution items

| Priority | Status | Owner | Area | Task | Notes |
|---|---|---|---|---|---|
| P0 | In progress | Engineering | CI/CD | Keep CI deterministic | CI now has one workflow and checks env contract plus OpenAPI export. Add full security scanners next. |
| P0 | In progress | Platform | Environment | Keep env variables non-duplicated | `.env.example` cleaned and `scripts/check_env_contract.py` added. Extend to production templates. |
| P0 | Not started | Frontend | Web build | Add `apps/web/package-lock.json` | Needed for reproducible web builds. CI currently falls back to `npm install`. |
| P0 | In progress | Operations | Launch gate | Run production readiness from one command | `make prod-verify` added. Extend with smoke URLs and deployment-specific checks. |
| P1 | Not started | Backend | API contracts | Persist OpenAPI schema and diff breaking changes | `scripts/export_openapi.py` added. Next step: commit schema or compare against baseline. |
| P1 | Not started | Security | Security CI | Add full secret/SAST/dependency scanning jobs | README claims must remain aligned with actual CI. |

## Arabic summary

هذا الملف هو مكان تحويل خطة التنفيذ أو الشيت إلى مهام واضحة داخل الريبو. إذا صدّرت Google Sheet كـ CSV، شغّل السكربت أعلاه وسيتم تحديث الجدول تلقائيًا.
