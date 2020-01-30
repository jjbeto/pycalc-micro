FROM python:alpine

MAINTAINER Beto Fonseca <jjbeto@gmail.com>

# If MICROSERVICE is not passed as a build arg, go with evaluate
ARG MICROSERVICE=evaluate2

WORKDIR /service

COPY ./microservices/${MICROSERVICE} ./app

COPY requirements ./requirements
RUN set -e && \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	&& \
    pip install --upgrade pip && \
    pip install -r ./requirements/requirements-main.txt && \
    pip install -r ./requirements/requirements-dev.txt && \
	apk del .build-deps

# Flask Port
EXPOSE 5000

COPY docker-entrypoint.sh .
RUN  chmod +x docker-entrypoint.sh
CMD  ["/service/docker-entrypoint.sh"]
