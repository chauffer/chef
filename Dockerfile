FROM python:3-alpine

WORKDIR /app
COPY requirements.txt /app/
RUN apk add --no-cache --virtual=.build-deps build-base && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps
COPY . /app
CMD ["python3", "chef/core.py"]

LABEL name=chef version=dev \
      maintainer="Simone Esposito <simone@kiwi.com>"

