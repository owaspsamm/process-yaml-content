FROM python:3.7-slim-buster AS python

FROM python AS builder

WORKDIR /build

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  pandoc \
  wget \
  make \
  && rm -rf /var/lib/apt/*

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM builder AS base

COPY samm2yaml2md/ /build/

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
