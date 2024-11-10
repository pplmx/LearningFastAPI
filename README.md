# FastAPI Project Documentation

## Prerequisites

- Python 3.13+
- uv (Python package installer)
- Docker (optional)
- Kubernetes cluster (optional)
- Make (for running commands)

## Development Setup

### Local Development

Pre-requisites:

    ```bash
    # Create virtual environment
    make init
    ```

1. **Using uv directly (Recommended)**

    ```bash
    uv run src/app/main.py
    ```

2. **Without uv for booting**

```bash
    # Activate virtual environment
    source .venv/bin/activate  # Linux/macOS
    # .venv/Scripts/activate   # Windows

    # Run with different servers
    cd src/app

    # Option 1: Uvicorn (ASGI)
    uvicorn main:app --host 0.0.0.0 --port 8080 --reload

    # Option 2: Hypercorn (HTTP/2 Support)
    uv add hypercorn
    hypercorn main:app --bind 0.0.0.0:8080 --reload

    # Option 3: Gunicorn (Production)
    uv add gunicorn
    gunicorn main:app
```

### Docker Development

```bash
# Build and run development environment
make dev

```

### Kubernetes Deployment

```bash
# Deploy to production
make prod

```

## API Documentation

Access the interactive API documentation:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Performance Optimization

Server configuration recommendations:
- `Uvicorn`: Best for development and small to medium loads
- `Hypercorn`: Preferred when `HTTP/2` is required
- `Gunicorn`: Recommended for `production` with multiple workers
