# ═══════════════════════════════════════════════════════════════
# AI Company Saudi — production Docker image
# Multi-stage, non-root, Python 3.12-slim
# ═══════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────────
# Stage 1 — Builder: install deps into a venv
# ──────────────────────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libffi-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Create virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependency files first for better caching
COPY pyproject.toml ./
COPY requirements.txt* ./

# Install dependencies fail-fast, then remove build-only packaging tooling.
# Keeping pip/setuptools/wheel out of the runtime venv reduces attack surface;
# the application never installs packages at runtime.
RUN set -eux; \
    pip install --upgrade pip setuptools wheel; \
    pip install --no-cache-dir --prefer-binary -r requirements.txt; \
    find /opt/venv -type d -name __pycache__ -prune -exec rm -rf {} +; \
    find /opt/venv -type d -name tests -prune -exec rm -rf {} +; \
    find /opt/venv -type f -name "*.pyc" -delete; \
    python -m pip uninstall -y pip setuptools wheel

# ──────────────────────────────────────────────────────────────
# Stage 2 — Runtime: minimal image
# ──────────────────────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS runtime

# Surface the deployed commit on /health. Pass via build-arg from CI:
#   docker build --build-arg GIT_SHA=$(git rev-parse HEAD) ...
ARG GIT_SHA=unknown
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_ENV=production \
    GIT_SHA=${GIT_SHA}

# Runtime-only system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        libffi8 \
        libpcre2-8-0 \
        tini \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY --chown=app:app . .

# Create startup script as root before switching to non-root user
RUN printf '#!/bin/sh\nset -e\nexec uvicorn api.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 1\n' \
        > /app/start.sh \
    && chmod +x /app/start.sh \
    && chown app:app /app/start.sh

USER app

# Runtime writable data directory (revenue_ops_autopilot store writes /app/var).
# Created at build time with correct ownership so writes succeed without
# a privileged pre-deploy step.
RUN mkdir -p /app/var && chown app:app /app/var

# Railway injects $PORT dynamically; default to 8000 for local dev
ENV PORT=8000
EXPOSE 8000

# Healthcheck uses $PORT so it matches whatever the platform assigns
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=5 \
    CMD curl -fsS http://localhost:${PORT:-8000}/healthz || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/app/start.sh"]
