FROM python:3 AS intermediate
LABEL maintainer="Joel Courtney <joel@aceteknologi.com>"

RUN mkdir /build

COPY . /build

RUN mkdir /build/pip-cache

WORKDIR /build

RUN pip download -d pip-cache --process-dependency-links .

FROM python:3
LABEL maintainer="Joel Courtney <joel@aceteknologi.com>"

RUN mkdir /app

COPY . /app

COPY --from=intermediate /build/pip-cache /app/pip-cache

ENV NEMWEB_LOG_CONF=/app/config/logging.json

WORKDIR /app

RUN pip install --no-index --find-links=file:///app/pip-cache . && rm -rf pip-cache
