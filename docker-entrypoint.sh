#!/usr/bin/env bash
set -e

echo "⏳ Waiting for Postgres to be ready..."
until python -c "import os; import psycopg2; psycopg2.connect(os.environ['DATABASE_URL'].replace('postgresql+psycopg2://','postgresql://')).close()" 2>/dev/null; do
  sleep 2
done
echo "✅ Postgres is ready"

echo "🧱 Running Alembic migrations..."
alembic upgrade head
echo "✅ Migrations complete"

echo "🚀 Starting FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000