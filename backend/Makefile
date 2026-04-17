.PHONY: install test lint format check security

install:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests -q

lint:
	ruff check app tests

format:
	black app tests && ruff check --fix app tests

check:
	ruff check app tests && mypy app --ignore-missing-imports

security:
	bandit -r app -ll
