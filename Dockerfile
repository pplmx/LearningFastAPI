# Builder stage
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

LABEL maintainer="Mystic" \
      version="1.0" \
      description="Python FastAPI Application"

# Set build-time variables
ARG UV_INDEX_URL="https://mirrors.cernet.edu.cn/pypi/web/simple"
ARG PIP_INDEX_URL="https://mirrors.cernet.edu.cn/pypi/web/simple"

WORKDIR /app

COPY pyproject.toml .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Runtime stage
FROM python:3.13-slim-bookworm

WORKDIR /app

# Add non-root user
RUN groupadd -r app && \
    useradd -r -g app -s /bin/false app && \
    chown -R app:app /app

# Copy virtual environment from builder and application code
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app /src/app /app

# Set environment variables
ENV TZ="Asia/Shanghai" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/docs', timeout=2) or exit(1)"

# Start application
CMD ["fastapi", "run", "main.py"]
