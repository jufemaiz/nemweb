FROM python:3
LABEL maintainer="Joel Courtney <joel@aceteknologi.com>"

RUN pip install pipenv && \
  mkdir /app

COPY . /app/

ENV NEMWEB_LOG_CONF=/app/config/logging.json

WORKDIR /app

RUN pipenv install --dev
