# Dealix — قائمة التحقق للتدشين (Launch Checklist)

> هذا الملف يُحدَّث مع تقدم المشروع. علامة ✅ تعني تم + دليل + سجّل في Truth Registry.

---

## 🏗️ الأساسات (Foundation)

### المستودع والـ CI
- [x] مستودع مستقل على GitHub ([VoXc2/dealix](https://github.com/VoXc2/dealix))
- [x] ترخيص Proprietary (All Rights Reserved)
- [x] `.gitignore` شامل (172 سطر)
- [x] `Dealix CI` workflow — يمر (smoke + truth + backend + frontend)
- [x] `Repo Hygiene` workflow — يمر (secrets scan + key files)
- [x] Dependabot مفعّل (backend + frontend + actions)
- [x] Issue templates (bug + feature)
- [x] PR template
- [ ] Branch protection على `main` (يتطلب صلاحية admin UI)
- [ ] Required reviews من CODEOWNERS
- [ ] Signed commits إلزامية

### الحوكمة (Governance)
- [x] `CLAUDE.md` v2.0.0 — بدون Discovery Phase gating
- [x] `CONTRIBUTING.md`
- [x] `SECURITY.md`
- [x] `CODEOWNERS`
- [x] Truth Registry (`docs/registry/TRUTH.yaml`) — 12 claims
- [x] Claims Registry (`docs/registry/CLAIMS.md`) — قائمة ممنوع
- [x] Validator script + CI gate

### التوثيق (Documentation)
- [x] `README.md` احترافي (عربي + إنجليزي)
- [x] `ARCHITECTURE.md` — البنية المعمارية الكاملة
- [x] `docs/API.md` — REST API spec
- [x] `docs/DEPLOYMENT.md` — دليل النشر
- [x] `docs/QUICKSTART.md` — دليل بدء سريع
- [x] `backend/README.md` — دليل Backend
- [x] `frontend/README.md` — دليل Frontend
- [x] `frontend/RTL_GUIDE.md` — قواعد RTL
- [x] `DAILY_EXECUTION_SCHEDULE_AR.md` — 90 يوم × 451 مهمة

---

## 🔐 الأمان والامتثال (Security & Compliance)

- [ ] Secrets management (Vault أو GitHub Secrets)
- [ ] `.env.example` للـ backend ✅ + frontend ✅
- [ ] Rotation policy للمفاتيح (كل 90 يوم)
- [ ] TLS 1.3 إلزامي
- [ ] JWT tokens مع refresh tokens
- [ ] Rate limiting (100 req/min per tenant)
- [ ] Idempotency keys على كل mutation
- [ ] Hash chain للـ audit logs
- [ ] Tenant isolation (row-level)
- [ ] PDPL data subject rights (access/delete/export)
- [ ] ZATCA integration (Phase 2)
- [ ] Privacy Policy بالعربي
- [ ] Terms of Service بالعربي
- [ ] DPA template جاهز للعملاء

---

## 🧪 الجودة (Quality)

### Backend
- [x] Ruff + Black + mypy + Bandit
- [ ] Tests coverage ≥ 70%
- [ ] Integration tests للـ API
- [ ] Load tests (k6 أو locust)
- [ ] Security tests (OWASP Top 10)

### Frontend
- [x] ESLint + Prettier + TypeScript strict
- [ ] Playwright E2E tests
- [ ] Lighthouse score ≥ 90 (Performance + Accessibility + SEO)
- [ ] WCAG AA compliance
- [ ] RTL visual regression tests

---

## 🚀 البنية التحتية (Infrastructure)

- [ ] Docker images بناء + push إلى registry
- [ ] `docker-compose.yml` يعمل محلياً
- [ ] Staging environment (docker swarm أو k8s)
- [ ] Production environment
- [ ] Database migrations (Alembic)
- [ ] Redis cluster (للـ cache + queue)
- [ ] PostgreSQL backups يومية + S3
- [ ] Celery workers + Beat
- [ ] Nginx/Traefik reverse proxy
- [ ] SSL/TLS certificates (Let's Encrypt)
- [ ] CDN للـ static assets
- [ ] Monitoring: Prometheus + Grafana
- [ ] Error tracking: Sentry
- [ ] Logs: JSON structured + aggregation

---

## 🎯 الأعمال (Business)

- [ ] Landing page عربي
- [ ] Pricing page (1,499 SAR/mo)
- [ ] Demo video (3-5 دقائق)
- [ ] Sales collateral (PDF deck)
- [ ] 3 عملاء pilot جاهزون
- [ ] Onboarding wizard (5-10 دقائق)
- [ ] Customer support channel (WhatsApp + email)
- [ ] Billing integration (Moyasar أو Tap Payments)
- [ ] Invoice generation (متوافق ZATCA)
- [ ] First paying customer ($USD:SAR conversion)

---

## 📊 Telemetry & Truth Registry

لا ادّعاء "live" بدون 30 يوم telemetry.

- [ ] Metrics dashboard يعرض uptime + latency + errors
- [ ] Alerting rules (Slack/email)
- [ ] Post-deploy verification
- [ ] Incident response playbook
- [ ] Status page (public)

---

## ✅ يوم التدشين (Launch Day)

- [ ] جميع CI checks خضراء
- [ ] Security audit منجز (داخلي)
- [ ] Performance baseline مسجّل
- [ ] Backup + restore tested
- [ ] DNS configured + tested
- [ ] SSL certificate valid
- [ ] Monitoring active 24/7
- [ ] Support team جاهز
- [ ] Rollback plan موثّق
- [ ] Customer communications مُعدّة
- [ ] Press release بالعربي
- [ ] Social media assets

---

## 📞 المالك

**Sami Mohammed Assiri**  
Field Services Engineer — METCO (Smiths Detection)  
📧 sami.assiri11@gmail.com  
🏢 King Khalid International Airport, Riyadh

---

## 🔗 روابط مرجعية

- المستودع: https://github.com/VoXc2/dealix
- الجدول اليومي: [DAILY_EXECUTION_SCHEDULE_AR.md](./DAILY_EXECUTION_SCHEDULE_AR.md)
- البنية المعمارية: [ARCHITECTURE.md](./ARCHITECTURE.md)
- النشر: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- Truth Registry: [docs/registry/TRUTH.yaml](./docs/registry/TRUTH.yaml)
- Claims Registry: [docs/registry/CLAIMS.md](./docs/registry/CLAIMS.md)
