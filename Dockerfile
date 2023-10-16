FROM python:3.12-bookworm AS builder

LABEL maintainer="Mystic"

ENV PIP_NO_CACHE_DIR 1
ENV PIP_INDEX_URL https://mirrors.cernet.edu.cn/pypi/web/simple
# poetry will be installed in $HOME/.local/bin
# NOT WORK, call PATH in RUN command directly, like this: RUN PATH="${HOME}/.local/bin:${PATH}" poetry install --no-directory
# ENV PATH "$HOME/.local/bin:$PATH"

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python -

COPY pyproject.toml .
RUN python -m venv --copies venv
RUN . venv/bin/activate && \
    python -m ensurepip -U && \
    PATH="${HOME}/.local/bin:${PATH}" poetry install --no-directory


FROM python:3.12-slim-bookworm

WORKDIR /app
COPY --from=builder /app/venv /app/venv

ENV TZ Asia/Shanghai
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH /app/venv/bin:$PATH

COPY . .

EXPOSE 8080

# healthcheck with python urllib
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080').getcode()"

CMD ["gunicorn", "main:app"]
