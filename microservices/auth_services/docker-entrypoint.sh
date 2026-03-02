#!/usr/bin/env bash
set -e

echo "⏳ Waiting for Postgres..."
until python -c "import os, psycopg2; psycopg2.connect(os.environ['DATABASE_URL'].replace('postgresql+psycopg2://','postgresql://')).close()" 2>/dev/null; do
  sleep 2
done
echo "✅ Postgres ready"

echo "🧱 Alembic upgrade..."
alembic upgrade head

echo "🚀 Starting Auth Service..."
uvicorn app.main:app --host 0.0.0.0 --port 8000