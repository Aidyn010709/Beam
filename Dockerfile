FROM python:3.11.2

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR="/var/cache/pypoetry"

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    bash \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    python3-pip \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry

ENV PATH $PATH:/usr/bin
ENV PATH $PATH:/usr/share/lintian/overrides/gdal-bin

ARG CPLUS_INCLUDE_PATH=/usr/include/gdal
ARG C_INCLUDE_PATH=/usr/include/gdal

COPY poetry.lock pyproject.toml /app/
WORKDIR /app

RUN poetry install

COPY . .

RUN chmod 755 /app/entrypoints/* && \
        chmod +x /app/entrypoints/* && \
            export DJANGO_SETTINGS_MODULE=beam.settings.base
