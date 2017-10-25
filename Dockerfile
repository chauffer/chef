FROM python:3-alpine3.6

WORKDIR /app
COPY requirements.txt /app/
RUN sed -i -e 's/v3\.6/edge/g' /etc/apk/repositories && \
    apk add --no-cache --virtual=.build-deps build-base zlib-dev jpeg-dev && \
    apk add --no-cache --virtual=.run-deps tesseract-ocr && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps
COPY . /app
CMD ["python3", "chef/core.py"]

LABEL name=chef version=dev \
      maintainer="Simone Esposito <simone@kiwi.com>"

