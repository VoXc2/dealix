# GitHub Ruleset Proposal — main branch protection
**STATUS: PROPOSAL ONLY — NOT APPLIED · يحتاج قرار المؤسس وتطبيقه يدويًا من إعدادات المستودع**

## السياق
مراجعة 2026-08-25 أظهرت عدم وجود Rulesets مفعّلة على الفرع الرئيسي، مع سجل استثناء حوكمة موثق (GOVERNANCE_MERGE_EXCEPTION_2026-08-25.md). هذا المقترح يغلق الباب.

## STAGE A — فعّل الآن (لا يعتمد على CI)
| Control | Value |
|---|---|
| Target | `~DEFAULT_BRANCH` (main) |
| Require pull request before merging | **ON** (required approvals: 1 — المؤسس) |
| Block force pushes | **ON** |
| Block deletions | **ON** |
| Bypass list | **فارغ** — لا بایپس لأي حساب/تطبيق (بما فيها هوية الأجهزة) |
| Required conversations resolution | ON إن توفر |

## STAGE B — بعد استعادة GitHub Actions billing
- Required status checks: `verify` · CodeQL · Dependency Review + فحوصات الثقة الحرجة (exact-head)
- Code scanning: block merge on new critical/high alerts

## لماذا مرحليًا؟
التحقق المستضيف معطّل حاليًا بحظر فوترة (ACCOUNT_LEVEL_ACTIONS_BLOCKER). اشتراط checks ميتة = تجميد مستودع. Stage A يغلق ثغرات الدفع/الحذف اليوم دون كسر أي شيء.

## خطوات التطبيق (يدوي، ~5 دقائق)
GitHub → Dealix-sa/dealix → Settings → Rules → Rulesets → New branch ruleset → أدخل الجدول أعلاه → Enforce.

## الأثر على الطاقم الحي
Living Fleet dispatcher لا يدمج أبدًا — لن يتأثر. OpenCode سيُمنع هيكليًا حتى لو صدر أمر عام.

# Machine Identity Plan — هوية آلة منفصلة
**STATUS: PROPOSAL ONLY**

## الهدف
فصل هوية OpenCode/الطاقم عن حساب المؤسس الإداري.

| | FOUNDER | MACHINE (مقترح) |
|---|---|---|
| Admin/merge final authority | ✓ | ✗ |
| Push feature branches | ✓ | ✓ |
| Open/update Draft PRs | ✓ | ✓ |
| Read CI/issues | ✓ | ✓ |
| Ruleset bypass | n/a | **لا يوجد** |
| Secrets/production | ✓ | ✗ |

## الخيار الموصى به: GitHub App (أو Fine-grained PAT باسم جهاز)
1. إنشاء GitHub App مملوك للمؤسسة بصلاحيات: Contents(Read+Write على feature branches فقط عبر قاعدة)، PullRequests(Write)، Issues(Read)
2. تثبيته على مستودع dealix فقط
3. تحديث `gh`/git remote credential للجهاز لاستخدام توكن التطبيق القصير الأجل
4. سحب صلاحية admin عن أي توكن طويل الأجل على VPS

**لن أنشئ الحساب أو التوكن تلقائيًا** — حزمة التنفيذ هذه تحتاج قرار المؤسس وإنشاءه من واجهة GitHub.
