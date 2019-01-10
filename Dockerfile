FROM python:3
LABEL maintainer="Joel Courtney <joel@aceteknologi.com>"

RUN apt-get -y update && \
  apt-get -y upgrade && \
  apt-get install -y sqlite3 libsqlite3-dev && \
  pip install pipenv && \
  mkdir /app

COPY . /app/

ENV NEMWEB_LOG_CONF=/app/config/logging.json

WORKDIR /app

RUN pipenv install --dev

ENTRYPOINT ["pipenv", "run"]
