FROM python:3.12-slim

LABEL maintainer="Mystic"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE 1
ENV PIP_INDEX_URL https://mirrors.cernet.edu.cn/pypi/web/simple

WORKDIR /app

# As this file doesn't change often
# Docker will detect it and use the cache for this step, enabling the cache for the next step too.
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    pip install uvicorn gunicorn

COPY . .

EXPOSE 8080

CMD ["gunicorn", "main:app"]
