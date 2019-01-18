FROM python:3.13

LABEL maintainer="Joel Courtney <joel@aceteknologi.com>"

RUN apt-get -y update && \
  apt-get -y upgrade && \
  apt-get install -y sqlite3 libsqlite3-dev && \
  pip install pipenv && \
  mkdir /app

COPY . /app/

ENV NEMWEB_LOG_CONF=/app/config/logging.json
ENV LANG=en_AU.UTF-8

WORKDIR /app

RUN pipenv install --dev

ENTRYPOINT ["pipenv", "run"]
