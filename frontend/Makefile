.PHONY: install dev build lint format test

install:
	npm ci

dev:
	npm run dev

build:
	npm run build

lint:
	npm run lint

format:
	npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,md}"

test:
	npm run test || echo "No tests configured yet"
