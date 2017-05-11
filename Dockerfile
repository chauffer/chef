FROM python:3-alpine

MAINTAINER Ladislav Radon <lada@kiwi.com>
RUN mkdir -p /var/log/automation/autobooking/requests/

COPY *requirements.txt srv/app/

ARG PIP_INDEX_URL

RUN \
  pip install --upgrade pip && \
  pip install -r /srv/api/requirements.txt --exists-action s && \
  rm -rf /root/.smation/' > /usr/local/lib/python2.7/site-packages/kw.pth

COPY . /app
WORKDIR /app
