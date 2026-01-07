default:
    just --list

run:
    uv run uvicorn app.main:app --no-access-log

run-dev:
    uv run uvicorn app.main:app --reload --no-access-log