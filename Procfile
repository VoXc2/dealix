web: uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers ${UVICORN_WORKERS:-2}
release: alembic upgrade head || true
