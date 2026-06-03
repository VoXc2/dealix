# Dealix — Founder Risk & Compliance Register

هذه ليست استشارة قانونية. الهدف هو تحويل المخاطر إلى ضوابط تشغيلية قابلة للفحص.

## Risk register

| Risk | Impact | Control | Owner |
|---|---|---|---|
| claims غير مثبتة | فقدان الثقة أو مسؤولية قانونية | no-overclaim register | founder |
| استخدام بيانات بدون أساس | PDPL risk | consent/lawful basis notes | ops |
| إرسال outreach غير مناسب | brand/compliance risk | approval and suppression lists | sales ops |
| تسريب secrets | security incident | GitHub/Railway secrets only | engineering |
| AI hallucination | customer harm | evidence and approval | product |
| deploy outage | loss of trust | healthchecks and rollback | engineering |
| vendor outage | workflow degradation | fallback providers | ops |
| over-customization | margin loss | productized packages | founder |

## Compliance operating rules

1. لا يتم تنفيذ high-risk external action بدون موافقة.
2. أي بيانات عميل تعامل كـ confidential.
3. أي claim عام يحتاج evidence.
4. أي integration جديد يحتاج secrets plan وrollback.
5. أي customer artifact يحتاج source trail.

## Approval classes

| Class | Examples | Required approval |
|---|---|---|
| Low | internal analysis | automated allowed |
| Medium | outreach drafts, account lists | operator review |
| High | pricing, contracts, sensitive exports | founder/admin approval |
| Critical | legal/regulatory/security incident | explicit founder approval |

## Evidence required before launch

- CI passing or exceptions documented.
- Security workflows configured.
- Railway healthchecks green.
- Secrets only in provider dashboards.
- Public claims reviewed.
- Incident template available.
- Post-deploy evidence captured.

## Incident response minimum

1. Stop or isolate affected surface.
2. Preserve logs and evidence.
3. Rotate exposed credentials if suspected.
4. Create production incident issue.
5. Patch and redeploy.
6. Run live checks.
7. Document root cause and follow-up.
