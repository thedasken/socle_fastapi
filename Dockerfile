FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Crée le venv dans l'image, pas sur l'hôte
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc_dir \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN useradd -r -s /bin/bash app \
    && mkdir -p /tmp/prometheus_multiproc_dir \
    && chown -R app:app /tmp/prometheus_multiproc_dir

COPY --from=builder /app/.venv /app/.venv
COPY . /app/

RUN chmod +x /app/entrypoints/gunicorn.sh \
    && chown -R app:app /app

USER app
CMD ["/app/entrypoints/gunicorn.sh"]