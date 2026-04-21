# Dealix — Root Makefile
# ═══════════════════════════════════════════════════════════════
.PHONY: help install up down logs test lint format check validate clean \
        smoke-test launch-check launch-docs

help:  ## عرض هذه الرسالة
	@awk 'BEGIN {FS = ":.*##"; printf "\nأوامر Dealix المتاحة:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install:  ## تثبيت كل الاعتمادات (backend + frontend)
	@echo "📦 Installing backend..."
	$(MAKE) -C backend install
	@echo "📦 Installing frontend..."
	$(MAKE) -C frontend install

up:  ## تشغيل كل الخدمات عبر docker-compose
	docker compose up -d

down:  ## إيقاف كل الخدمات
	docker compose down

logs:  ## متابعة logs
	docker compose logs -f --tail=100

test:  ## تشغيل الاختبارات (backend + frontend)
	$(MAKE) -C backend test
	$(MAKE) -C frontend test

lint:  ## فحص الكود (ruff + eslint)
	$(MAKE) -C backend lint
	$(MAKE) -C frontend lint

format:  ## تنسيق الكود (black + prettier)
	$(MAKE) -C backend format
	$(MAKE) -C frontend format

check:  ## فحص شامل (lint + type check + security)
	$(MAKE) -C backend check
	$(MAKE) -C backend security
	cd frontend && npx tsc --noEmit

validate:  ## التحقق من Truth Registry
	python3 scripts/validate_truth_registry.py

clean:  ## حذف ملفات مؤقتة + caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .next -prune -exec rm -rf {} + 2>/dev/null || true

smoke-test:  ## اختبار سريع لنقاط النهاية الأساسية (BASE_URL=... )
	BASE_URL=$${BASE_URL:-http://localhost:8000} bash scripts/qa/smoke_test.sh

launch-check:  ## فحص جاهزية الإطلاق (lint + smoke test)
	@echo "→ lint"
	-$(MAKE) lint
	@echo "→ smoke test"
	$(MAKE) smoke-test

launch-docs:  ## سرد ملفات خطة الإطلاق
	@echo "Launch-readiness documents:"
	@ls -1 docs/launch-execution-plan.md docs/qa-acceptance-checklist.md \
	       docs/operations-runbook.md    docs/sales-launch-kit.md \
	       docs/metrics-and-kpis.md 2>/dev/null
