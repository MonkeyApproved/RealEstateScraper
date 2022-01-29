FROM python:3.10-alpine3.15
LABEL maintainer="monkeyapprovedmonkey@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY setup.py setup.py
COPY setup.cfg setup.cfg
COPY requirements_dev.txt requirements_dev.txt
COPY pyproject.toml pyproject.toml
COPY LICENSE LICENSE
COPY src /src

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install . && \
    adduser --disabled-password --no-create-home app

WORKDIR /app
EXPOSE 8000

ENV PATH="/scripts:/py/bin:$PATH"