FROM python:3.10-slim

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN apt-get -y update && \
    python3 -m pip install --upgrade pip && \
    pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

WORKDIR /app

COPY ./reporter /app/reporter

COPY ./alembic.ini /app/

EXPOSE 3344
