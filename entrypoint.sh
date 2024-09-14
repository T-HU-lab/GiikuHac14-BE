#!/bin/sh

# Apply database migrations
poetry run alembic upgrade head

# Start the FastAPI server
poetry run uvicorn api.main:app --host 0.0.0.0 --reload
