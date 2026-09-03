# GitHub Ruleset Proposal — main branch protection
**STATUS: PROPOSAL ONLY — NOT APPLIED · يحتاج قرار المؤسس وتطبيقه من إعدادات المستودع**

## Live snapshot — 2026-09-01
- Branch metadata reports `main` as `protected=false`; do not treat branch-protection prose as an active technical barrier.
- Two repository rulesets exist but are **disabled**: `19473525` and `15443641`.
- Ruleset `15443641` (`V`) is not safe to enable blindly because its broad restriction set is not scoped by a useful branch condition. Leave it disabled; create or repair a narrowly scoped ruleset instead.
- Current `main` head: `2d39f58fb438d50cf3a99f6a1c643773944c4cf0`.
- Hosted Actions currently fail before runner allocation (`steps=[]`, `runner_id=0`), so hosted status checks are infrastructure non-evidence until runner execution is restored.

## STAGE A — حماية قابلة للتطبيق بدون hosted CI

Create a **new, narrowly scoped default-branch ruleset** rather than activating the old broad `V` ruleset.

| Control | Value |
|---|---|
| Target | default branch / `main` only |
| Enforcement | **Active** |
| Require pull request before merging | **ON** |
| Required approving reviews | **0 initially for the single-founder topology** |
| Required conversation resolution | **ON** |
| Block force pushes | **ON** |
| Block deletions | **ON** |
| Require linear history | Optional; enable only after confirming the chosen merge method |
| Bypass list | Empty by default; add only an explicitly justified break-glass actor if operationally necessary |
| Required hosted checks | **OFF temporarily** while jobs cannot acquire runners |

### Why zero required approvals in Stage A?
GitHub does not allow an author to approve their own PR. Requiring one approval without an independent eligible reviewer can deadlock a single-founder repository while providing no real trust gain. Current-head independent review and the sovereign exact-head receipt remain mandatory operating evidence even when GitHub cannot technically enforce an approval count.

Once an independent human or governed review identity is available, move required approvals to **1** and require dismissal of stale approvals / latest-reviewable-push behavior.

## STAGE B — after Actions runner execution is restored

Only add required checks that demonstrably execute real steps on the exact PR head:

- sovereign exact-head verification (`bin/dealix verify trust --sha <EXACT_HEAD>` or the accepted canonical equivalent);
- critical Trust/No-Send acceptance;
- CodeQL / security checks that actually execute;
- dependency/build checks appropriate to the changed surface.

Required checks must bind to the exact head and must not be satisfied by stale runs. Code scanning should block new critical/high findings after the repository has a functioning execution plane.

## Activation acceptance

Before enabling the new ruleset:

1. confirm its branch condition targets only the default branch;
2. confirm direct pushes, force pushes, and deletion behavior match the intended founder workflow;
3. confirm no disabled/stale rule is being treated as enforcement;
4. confirm the founder cannot accidentally deadlock the repository through an impossible self-approval requirement;
5. save the ruleset ID and a before/after snapshot in repository evidence.

After activation, verify through current branch/ruleset metadata and record the result. If the available API surface cannot prove enforcement, mark it `UNKNOWN` rather than PASS.

## Effect on the living fleet

The Living Fleet and internal agents may create/update feature branches and Draft PRs within their bounded authority. They do not gain merge authority from this ruleset. `main` merge remains an L5 action bound to the exact reviewed SHA and the canonical approval packet.

# Machine Identity Plan — separate bounded machine identity
**STATUS: PROPOSAL ONLY**

## Goal
Separate the machine/agent credential from the founder's administrative identity and keep the machine structurally unable to exercise founder-only authority.

| Capability | FOUNDER | MACHINE |
|---|---:|---:|
| Repository admin/settings | ✓ | ✗ |
| Final merge authority | ✓ | ✗ |
| Push feature branches | ✓ | ✓ |
| Open/update Draft PRs | ✓ | ✓ |
| Read CI/issues/PRs | ✓ | ✓ |
| Ruleset bypass | only break-glass if explicitly configured | ✗ |
| Production/secrets/billing | ✓ | ✗ |

## Recommended identity
Prefer a repository-scoped GitHub App with short-lived installation tokens. A fine-grained PAT is a fallback, not the preferred long-lived machine architecture.

Minimum repository permissions should be bounded to the tasks actually needed, for example:

- Contents: Read/Write for feature-branch work;
- Pull requests: Read/Write;
- Issues: Read/Write only if the operating workflow needs issue updates;
- Actions: Read for evidence collection where supported;
- Administration, environments, secrets, organization settings, billing: **No access**.

Repository rulesets must enforce the branch boundary; credential scope alone does not guarantee that a Contents:Write token cannot target `main`.

## Rotation / revocation

- use short-lived installation tokens where possible;
- remove any long-lived admin credential from VPS agent workflows;
- rotate or revoke on suspected exposure, machine replacement, or authority change;
- never print tokens into logs, issues, PRs, receipts, or model prompts.

**No account, app, token, or repository settings mutation is authorized merely by this proposal.**
