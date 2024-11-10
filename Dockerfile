# Builder stage
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

LABEL maintainer="Mystic"

# Set build-time variables
ARG UV_INDEX_URL="https://mirrors.cernet.edu.cn/pypi/web/simple"
ARG PIP_INDEX_URL="https://mirrors.cernet.edu.cn/pypi/web/simple"

WORKDIR /app

COPY pyproject.toml .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --extra prod

# Runtime stage
FROM python:3.13-slim-bookworm

# Add non-root user
RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Set environment variables
ENV TZ="Asia/Shanghai" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY --chown=app:app /src/app /app
COPY --chown=app:app gunicorn.conf.py /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

# Start application
CMD ["gunicorn", "main:app"]
