FROM python:3.7-slim-buster AS python

FROM python AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils pandoc wget make xsltproc poppler-utils
RUN wget --quiet https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb && \
  apt install -y ./wkhtmltox_0.12.5-1.buster_amd64.deb && \
  rm ./wkhtmltox_0.12.5-1.buster_amd64.deb && rm -rf /var/lib/apt/*

RUN groupadd appgroup && useradd --home-dir /app -m -g appgroup appuser

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM builder AS base

COPY samm2yaml2md/ /build/

COPY entrypoint.sh /entrypoint.sh

USER appuser

ENTRYPOINT ["/entrypoint.sh"]