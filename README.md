# FastAPI Project Documentation

## Prerequisites

- Python 3.13+
- uv (Modern Python packaging tool)
- Docker (optional, for containerization)
- Kubernetes cluster (optional, for production deployment)
- Make (for automation commands)

## Development Setup

### Quick Start

```bash
# 1. Initialize development environment
make init

# 2. Start the server (using uv)
uv run src/app/main.py
```

### Detailed Setup Options

#### 1. Using uv (Recommended)

```bash
# Direct execution with uv
uv run src/app/main.py
```

#### 2. Traditional Setup

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv/Scripts/activate     # Windows

# Change to application directory
cd src/app

# Choose your preferred server:

# A. Uvicorn (Development)
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# B. Hypercorn (HTTP/2 Support)
uv add hypercorn
hypercorn main:app --bind 0.0.0.0:8080 --reload

# C. Gunicorn (Production)
uv add gunicorn
gunicorn main:app
```

### Container Deployment

#### Docker

```bash
# Development environment
make dev

```

#### Kubernetes

```bash
# Production deployment
make prod

```

## API Documentation

Interactive API documentation is available at:

- 📚 Swagger UI: http://localhost:8080/docs
- 📖 ReDoc: http://localhost:8080/redoc

## Server Configurations

Choose the appropriate server based on your needs:

| Server    | Best For              | Key Features                  |
|-----------|-----------------------|-------------------------------|
| Uvicorn   | Development           | Fast reload, Easy debugging   |
| Hypercorn | HTTP/2 Requirements   | HTTP/2, WebSocket support     |
| Gunicorn  | Production Deployment | Process management, Stability |

### Production Configuration Example

```python title="gunicorn.conf.py"
import multiprocessing

bind = "0.0.0.0:8080"
worker_class = "uvicorn.workers.UvicornWorker"

workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2

```

```bash
gunicorn main:app
```
