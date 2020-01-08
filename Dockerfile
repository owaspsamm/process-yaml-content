FROM python:3.7-slim-buster AS python

FROM python AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends gdebi pandoc wget make xsltproc poppler-utils && \
    rm -rf /var/lib/apt/*
RUN wget --quiet https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb && \
  apt-get install -y -f --no-install-recommends ./wkhtmltox_0.12.5-1.buster_amd64.deb && \
  rm ./wkhtmltox_0.12.5-1.buster_amd64.deb && rm -rf /var/lib/apt/*

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM builder AS base

COPY samm2yaml2md/ /build/

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
