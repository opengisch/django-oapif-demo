FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libproj-dev \
    gdal-bin \
    gettext \
    graphviz

WORKDIR /usr/src/

COPY pyproject.toml .
COPY README.md .

RUN pip install /usr/src/.[dev]

COPY . /usr/src/

WORKDIR /usr/src/oapif_demo
