default:
    just --list

run:
    uv run uvicorn app.main:app --no-access-log

run-dev:
    uv run uvicorn app.main:app --reload --no-access-log

test:
    uv run pytest -v

migrate:
    uv run alembic upgrade head

ruff *args:
    uv run ruff check {{args}} app tests migrations

lint:
    uv run ruff format app tests migrations
    just ruff --fix

sort:
    uv run isort .