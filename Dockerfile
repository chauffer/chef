FROM python:3-alpine

MAINTAINER Ladislav Radon <lada@kiwi.com>

COPY *requirements.txt /app/

RUN pip install -r /app/requirements.txt --exists-action s

COPY . /app

RUN echo "* * * * * python /app/run.py" >> /etc/crontabs/root
WORKDIR /app

CMD ["crond", "-f"]
