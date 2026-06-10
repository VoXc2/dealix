# Dealix — معايير الإطلاق

## المبدأ الأساسي

**لا إطلاق بدون إثبات.**

كل feature/release يجب أن يمر عبر gates محددة قبل الإطلاق.

---

## Gate Types

### 1. Development Gates (بوابات التطوير)

| Gate | Criteria | Owner |
|------|----------|-------|
| Code Complete | الكود جاهز للـ PR | Engineer |
| Code Review | PR مراجع وموافق عليه | Peer |
| Tests Pass | CI tests تمر 100% | CI |
| Lint Pass | No linting errors | CI |

### 2. Quality Gates (بوابات الجودة)

| Gate | Criteria | Owner |
|------|----------|-------|
| Unit Tests | 80%+ coverage | Engineer |
| Integration Tests | Core flows pass | QA |
| Security Scan | No critical issues | Security |
| Performance | Response time < 500ms | Engineer |

### 3. Product Gates (بوابات المنتج)

| Gate | Criteria | Owner |
|------|----------|-------|
| Acceptance Criteria | كل criteria متحقق | Product |
| User Testing | 3+ users tested successfully | Product |
| Edge Cases | Edge cases handled | Engineer |
| Rollback Plan | Plan documented | Engineer |

### 4. Business Gates (بوابات العمل)

| Gate | Criteria | Owner |
|------|----------|-------|
| Founder Approval | Founder وافق على الإطلاق | Founder |
| Customer Evidence | Customer validation | Sales/CS |
| Documentation | Docs updated | Product |
| Training | Team trained | Ops |

---

## Release Criteria by Type

### Feature Release

```
Required:
✅ Code complete
✅ Tests pass (80%+)
✅ Code review approved
✅ Security scan passed
✅ Acceptance criteria met
✅ Rollback plan documented

Recommended:
✅ User testing completed
✅ Documentation updated
✅ Training delivered
```

### Hotfix Release

```
Required:
✅ Root cause identified
✅ Fix developed
✅ Tests pass
✅ Security reviewed (if critical)
✅ Founder notified

Process:
1. Fix in PR
2. Expedited review
3. Deploy to staging
4. Validate
5. Deploy to production
```

### Major Release

```
Required:
✅ All feature release criteria
✅ Full regression test pass
✅ Performance test pass
✅ Security audit (external)
✅ Founder approval
✅ Customer comms prepared
✅ Rollback tested

Process:
1. Feature freeze (2 weeks before)
2. QA cycle (2 weeks)
3. Staging deployment
4. UAT with key customers
5. Production deployment
6. Monitoring (24 hours)
```

---

## Pre-Launch Checklist

### 48 hours before launch

| Item | Status | Owner |
|------|--------|-------|
| All tests pass | ⬜ | CI |
| Staging deployment | ⬜ | Engineering |
| Smoke tests | ⬜ | QA |
| Rollback tested | ⬜ | Engineering |
| Monitoring configured | ⬜ | Engineering |
| Runbook ready | ⬜ | Engineering |
| On-call coverage | ⬜ | Ops |

### 24 hours before launch

| Item | Status | Owner |
|------|--------|-------|
| Final code freeze | ⬜ | Engineering |
| Final staging check | ⬜ | QA |
| Communication drafted | ⬜ | Product |
| Team notified | ⬜ | Ops |
| Emergency contacts shared | ⬜ | Ops |

### Launch day

| Item | Status | Owner |
|------|--------|-------|
| Deployment executed | ⬜ | Engineering |
| Health checks pass | ⬜ | Engineering |
| Initial monitoring | ⬜ | Engineering |
| Stakeholders notified | ⬜ | Product |
| Post-launch silence | ⬜ | All |

---

## Post-Launch Checklist

### Day 1

| Item | Status | Owner |
|------|--------|-------|
| Error rate normal | ⬜ | Engineering |
| Latency normal | ⬜ | Engineering |
| No critical bugs | ⬜ | QA |
| Customer feedback | ⬜ | CS |
| Metrics on track | ⬜ | Product |

### Week 1

| Item | Status | Owner |
|------|--------|-------|
| No regressions | ⬜ | QA |
| Customer adoption | ⬜ | CS |
| Feature metrics | ⬜ | Product |
| Feedback collected | ⬜ | Product |
| Issues resolved | ⬜ | Engineering |

### Month 1

| Item | Status | Owner |
|------|--------|-------|
| Business impact | ⬜ | Founder |
| ROI validated | ⬜ | Product |
| Lessons learned | ⬜ | Team |
| Backlog updated | ⬜ | Product |

---

## Go/No-Go Decision

### Launch Decision Matrix

| Criteria | Pass | Fail |
|----------|------|------|
| Tests | 100% pass | Any fail |
| Security | No critical | Any critical |
| Performance | Within SLA | Exceeds SLA |
| Rollback | Tested & ready | Not prepared |
| Documentation | Complete | Incomplete |
| Team readiness | All trained | Gap exists |

### If any "Fail" in Required:
→ **NO-GO** until resolved

---

## Rollback Criteria

### Automatic Rollback

| Metric | Threshold | Action |
|--------|-----------|--------|
| Error rate | > 5% | Auto-rollback |
| Latency | > 2x normal | Auto-rollback |
| Availability | < 99% | Auto-rollback |

### Manual Rollback

| Situation | Trigger |
|-----------|---------|
| Critical bug discovered | Customer-facing issue |
| Security vulnerability | Any severity |
| Data integrity issue | Any |
| Unexpected behavior | > 3 complaints |

---

## _links

- Strategy: `PRODUCT_STRATEGY_AR.md`
- MVP Scope: `MVP_SCOPE_AR.md`
- Roadmap: `ROADMAP_AR.md`
- Reports: `reports/product/ROADMAP_REVIEW.md`
