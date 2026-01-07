default:
    just --list

run:
    uv run uvicorn app.main:app

run-dev:
    uv run uvicorn app.main:app --reload