FROM python:3.12-bookworm AS builder

LABEL maintainer="Mystic"

ENV PIP_NO_CACHE_DIR 1
ENV PIP_INDEX_URL https://mirrors.cernet.edu.cn/pypi/web/simple
# poetry will be installed in $HOME/.local/bin
# NOT WORK, call PATH in RUN command directly, like this: RUN PATH="${HOME}/.local/bin:${PATH}" poetry install --no-directory
# ENV PATH "$HOME/.local/bin:$PATH"

WORKDIR /app

# Use curl to download and install poetry, avoid executing scripts from a pipe for increased security
RUN curl -sSL https://install.python-poetry.org -o get-poetry.py && python get-poetry.py && rm -fr get-poetry.py

COPY pyproject.toml .
RUN python -m venv --copies venv
RUN . venv/bin/activate && \
    python -m ensurepip -U && \
    PATH="${HOME}/.local/bin:${PATH}" poetry install --no-directory


FROM python:3.12-slim-bookworm

## Create a group and user
## RUN groupadd -g 999 appgroup && useradd -r -u 999 -g appgroup appuser
#RUN groupadd appgroup && useradd -r -g appgroup appuser
#
## Tell docker that all future commands should run as the appuser user
#USER appuser

WORKDIR /app
COPY --from=builder /app/venv /app/venv

ENV TZ Asia/Shanghai
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH /app/venv/bin:$PATH

COPY src/app /app
COPY gunicorn.conf.py /app

EXPOSE 8080

# healthcheck with python urllib
# HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080').getcode()"

# or healthcheck with /dev/tcp
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD bash -c 'cat < /dev/null > /dev/tcp/127.0.0.1/8080'

CMD ["gunicorn", "main:app"]
