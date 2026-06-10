# GitHub Actions Security Policy
## سياسة أمن GitHub Actions

**Document Type:** Security Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This policy defines security requirements for all GitHub Actions workflows in the Dealix repository.

---

## 2. Default Permission Policy

> **Default permissions: `contents: read` only.**

All workflows MUST use the minimum required permissions. Write permissions require explicit justification.

### 2.1 Permission Levels

| Level | Permissions | Use Case |
|-------|------------|----------|
| Minimal | `contents: read` | Read-only operations |
| Read + Security | `contents: read`, `security-events: write` | CodeQL, security scans |
| Read + PR | `contents: read`, `pull-requests: write` | PR creation, labels |
| Deploy | `contents: write` | Deploy to environments |
| Full | All | Only for admin operations |

---

## 3. Workflow Classification

### 3.1 SAFE Workflows

Workflows with minimal permissions that are safe to run:

| Workflow | Permissions | Status |
|----------|-------------|--------|
| `security.yml` | `contents: read`, `security-events: write` | ✅ SAFE |
| `repository-hardening.yml` | `contents: read`, `security-events: write` | ✅ SAFE |
| `founder_commercial_daily.yml` | `contents: read` | ✅ SAFE |
| `governed-full-ops-daily.yml` | `contents: read` | ✅ SAFE |
| `hermes-revenue-growth-os.yml` | `contents: read` | ✅ SAFE |
| `codeql.yml` | `contents: read`, `security-events: write` | ✅ SAFE |
| `local_stack_verify.yml` | `contents: read` | ✅ SAFE |

### 3.2 NEEDS_REVIEW Workflows

Workflows that require security review:

| Workflow | Concerns |
|----------|----------|
| `railway_deploy.yml` | Production deploy, needs permission audit |
| `deploy.yml` | Production deploy, needs permission audit |
| `release.yml` | Release process, needs permission audit |

### 3.3 HIGH_RISK Workflows

Workflows with potential security concerns:

| Workflow | Risk | Required Action |
|----------|------|----------------|
| Workflows with `contents: write` on PR | High | Require founder approval |
| Workflows with secrets access on PR | High | Require permission reduction |
| Workflows with `pull_request_target` | Critical | Must be removed or reviewed |

---

## 4. Prohibited Patterns

### 4.1 Never in Any Workflow

| Pattern | Risk | Reason |
|---------|------|--------|
| `pull_request_target` with write token | CRITICAL | Attacker can steal secrets |
| `issue_comment` trigger with write | CRITICAL | Comment can trigger malicious action |
| Secrets in untrusted workflow | CRITICAL | PR can steal production secrets |
| Auto-deploy to production from PR | HIGH | No human approval |
| External sending in CI | HIGH | No approval for sends |
| Broad `permissions: *` | HIGH | Excessive privilege |

### 4.2 Example Prohibited Workflow

```yaml
# ❌ NEVER DO THIS
on:
  pull_request_target:
  issue_comment:
permissions:
  contents: write  # Attacker can write malicious code
  secrets: write  # Attacker can steal secrets
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          # PR from attacker can now:
          # - Write to repository
          # - Access secrets
          # - Modify CI/CD
```

---

## 5. Required Patterns

### 5.1 Standard Read-Only Workflow

```yaml
name: Read-only workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run analysis
        run: echo "Read-only operation"
```

### 5.2 Standard Security Workflow

```yaml
name: Security scan

on:
  push:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Security scan
        run: echo "Security scan"
```

### 5.3 Production Deploy (Requires Approval)

```yaml
name: Production deploy

on:
  push:
    branches: [main]
  workflow_dispatch:  # Manual trigger only

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Requires environment protection
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: echo "Deploy with approval"
```

---

## 6. Secrets Handling in Workflows

### 6.1 Approved Secrets Usage

| Secret | Usage | Workflows |
|--------|-------|----------|
| `DEALIX_API_BASE` | API base URL | founder_*, governed_* |
| `DEALIX_ADMIN_API_KEY` | Admin authentication | founder_*, governed_* |
| `DEALIX_SYNC_EVIDENCE` | Evidence sync | founder_commercial_daily |

### 6.2 Secrets Access Rules

1. **Untrusted events get NO secrets** — PRs from forks get no secrets
2. **Trusted events get MINIMAL secrets** — Only what's needed
3. **No production secrets in PR workflows** — Use staging/test credentials
4. **Log all secret access** — Audit trail required

---

## 7. Workflow Review Checklist

Before adding/modifying a workflow:

- [ ] Permissions are minimal (`contents: read` default)
- [ ] No `pull_request_target` with write token
- [ ] No `issue_comment` trigger with write action
- [ ] Secrets only in trusted workflows
- [ ] No external sends
- [ ] No auto-production-deploy from PR
- [ ] `timeout-minutes` set
- [ ] `concurrency` set where needed
- [ ] Founder approval for production deploys

---

## 8. Enforcement

### 8.1 agentic-security-gate.yml

The `agentic-security-gate.yml` workflow audits all workflow changes:

```yaml
name: Security gate

on:
  pull_request:
    paths:
      - '.github/workflows/*.yml'

jobs:
  security-review:
    runs-on: ubuntu-latest
    steps:
      - name: Check workflow permissions
        run: |
          # Block dangerous patterns
          # Flag workflows needing review
```

### 8.2 Required Checks

1. **Permission audit** — All workflows have minimal permissions
2. **Dangerous pattern detection** — No `pull_request_target`, `issue_comment`
3. **Secrets audit** — No secrets in untrusted workflows
4. **External send detection** — No sends without approval
5. **Deploy gate** — Production deploy requires approval

---

## 9. Related Documents

| Document | Purpose |
|----------|---------|
| `GITHUB_WORKFLOW_PERMISSION_POLICY.md` | Permission guidelines |
| `UNTRUSTED_GITHUB_EVENT_POLICY.md` | Event handling |
| `OIDC_AND_SECRET_POLICY.md` | Secret management |
| `agentic-security-gate.yml` | Security gate workflow |

---

*Policy maintained by Agent #5 — Security Red Team*
